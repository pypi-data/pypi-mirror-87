// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { Fragment } from 'react';
import { ModalEnum, ModalInfo } from '../Mito';
import DefaultModal from '../DefaultModal';

import { SheetJSON } from '../../widget';

import "../../../css/group-modal.css"

// The aggregation functions we're supporting, out of the box
const AGGREGATION_OPTIONS = [
    'sum', 'mean', 'min', 'max', 'count'
]

export enum KeyType {
    Row = 'Row',
    Col = 'Col',
}


type GroupModalProps = {
    setModal: (modalInfo: ModalInfo) => void;
    sheetJSONArray: SheetJSON[];
    dfNames: string[];
    send: (msg: Record<string, unknown>) => void,
    selectedSheetIndex: number
};

type GroupModalState = {
    selectedGroupByRows: boolean[],
    selectedGroupByCols: boolean[],
    values: [string | number, string][], // tuple of column header, aggregation option
    keyError: string
};


class GroupModal extends React.Component<GroupModalProps, GroupModalState> {

    constructor(props: GroupModalProps) {
        super(props);

        const columns = this.props.sheetJSONArray[props.selectedSheetIndex].columns;

        // We default to selecting _no_ columns to group by
        const selectedGroupByRows = columns.map(() => false)
        const selectedGroupByCols = columns.map(() => false)
    
        // If there are any columns, we select the first one as the value, and just sum it
        // NOTE: this is because users don't notice they can do this when we don't show them
        const values: [string | number, string][]= [];
        if (columns.length > 0) {
            values.push([columns[0], AGGREGATION_OPTIONS[0]]);
        }
        
        this.state = {
            selectedGroupByRows: selectedGroupByRows,
            selectedGroupByCols: selectedGroupByCols,
            values: values,
            keyError: ''
        };

        this.getGroupByKeys = this.getGroupByKeys.bind(this);
        this.getValues = this.getValues.bind(this);
        this.addValue = this.addValue.bind(this);
        this.completeGroup = this.completeGroup.bind(this);
    }
    
    completeGroup = (): void => {
        /*
            Completes the group operation by sending information for the group
            to the backend.

            Errors if no group-by keys are selected.
        */
        const groupByRows = this.props.sheetJSONArray[this.props.selectedSheetIndex].columns.filter((columnHeader, index) => {
            return this.state.selectedGroupByRows[index];
        })

        const groupByCols = this.props.sheetJSONArray[this.props.selectedSheetIndex].columns.filter((columnHeader, index) => {
            return this.state.selectedGroupByCols[index];
        })

        // If there are no keys grouped by, we insert an error, and do not let the user submit
        if (groupByRows.length == 0 && groupByCols.length == 0) {
            this.setState({
                keyError: 'Please select a at least one row or column before submitting'
            })
            return;
        }

        // Build the values mapping
        const values: Record<string, unknown> = {};
        this.state.values.forEach((value) => {
            values[value[0]] = value[1];
        })

        // Log
        window.logger?.track({
            userId: window.user_id,
            event: 'button_group_log_event',
            properties: {
                sheet_index: this.props.selectedSheetIndex,
                group_by_rows: groupByRows,
                group_by_cols: groupByCols,
                values: values
            }
        })

        this.props.send({
            'event': 'edit_event',
            'type': 'group_edit',
            sheet_index: this.props.selectedSheetIndex,
            group_rows: groupByRows,
            group_columns: groupByCols,
            values: values
        })
        this.props.setModal({type: ModalEnum.None});
    }

    getGroupByKeys(keyType: KeyType) : JSX.Element {
        /* 
            Returns the group key selection boxes in a container that 
            allow them to scroll and easily be selected.
        */ 
        return (
            // add a top margin to the column selection div
            <div className={keyType === KeyType.Col ? 'group-modal-column-selection-container' : ''}>
                <div className='group-modal-label'>
                    {keyType === KeyType.Row ? 'Rows' : 'Columns'}
                </div>
                <div className='group-modal-column-selection'>
                    {this.props.sheetJSONArray[this.props.selectedSheetIndex].columns.map((columnHeader, index) => {

                        // determine if the key is selected
                        const isSelected =  keyType === KeyType.Row ? this.state.selectedGroupByRows[index] : this.state.selectedGroupByCols[index];
                        return (
                        <div key={columnHeader}>
                            <input
                                key={columnHeader}
                                type="checkbox"
                                name={columnHeader.toString()}
                                checked={isSelected}
                                onChange={() => {
                                    if (keyType === KeyType.Row) {
                                        this.setState(prevState => {
                                            const newSelectedGroupByRows = [...prevState.selectedGroupByRows];
                                            newSelectedGroupByRows[index] = !newSelectedGroupByRows[index];
                                            return {
                                                selectedGroupByRows: newSelectedGroupByRows,
                                                keyError: '' // Clear the key error
                                            }                                    
                                        })
                                    } else {
                                        this.setState(prevState => {
                                            const newSelectedGroupByCols = [...prevState.selectedGroupByCols];
                                            newSelectedGroupByCols[index] = !newSelectedGroupByCols[index];
                                            return {
                                                selectedGroupByCols: newSelectedGroupByCols,
                                                keyError: '' // Clear the key error
                                            }                                    
                                        })
                                    }
                                    
                                }}
                                className="form-check-input"
                            />
                            {columnHeader}
                        </div>
                        )
                    })}
                </div>
            </div>
        )
    }

    getValues(): JSX.Element {
        /*
            Returns the values JSX element, which are tuples of columnHeader, aggregation
            function selection boxes. 
        */
        return (
            <div className='mt-1'>
                <div className='group-modal-value-mapping'>
                    <div className='group-modal-label group-modal-value-mapping-key'>
                        Value
                    </div>
                    <div className='group-modal-label'>
                        Aggregation Method
                    </div>
                </div>
                <div className='group-modal-value-mapping-container'>
                    {this.state.values.map((value, index) => {
                        const columnHeader = value[0];
                        const aggregationOption = value[1];

                        const changeColumnSelect = (e: React.ChangeEvent<HTMLSelectElement>) => {
                            // Save outside the set state, because react cleans up events, 
                            // so it may be undefined inside setState callback
                            const columnHeader_ = e.target.value;
                            this.setState(prevState => {
                                const newValues = [...prevState.values];
                                newValues[index][0] = columnHeader_;
                                return {
                                    values: newValues
                                }
                            })
                        }

                        const changeAggSelect = (e: React.ChangeEvent<HTMLSelectElement>) => {
                            // Save outside the set state, because react cleans up events, 
                            // so it may be undefined inside setState callback
                            const aggFunction = e.target.value;
                            this.setState(prevState => {
                                const newValues = [...prevState.values];
                                newValues[index][1] = aggFunction;
                                return {
                                    values: newValues
                                }
                            })
                        }

                        const removeValueMapping = () => {
                            this.setState(prevState => {
                                const newValues = [...prevState.values];
                                newValues.splice(index, 1);
                                return {
                                    values: newValues
                                }
                            })
                        }

                        const columnSelect = (
                            <select className='group-modal-dropdown group-modal-value-mapping-key' onChange={changeColumnSelect}>
                                {this.props.sheetJSONArray[this.props.selectedSheetIndex].columns.map((columnHeader_) => {
                                    return (<option key={columnHeader_} value={columnHeader_} selected={columnHeader === columnHeader_}>{columnHeader_}</option>);
                                })}
                            </select>
                        )
                        
                        
                        const aggregationSelect = (
                            <select className='group-modal-dropdown group-modal-value-mapping-value' onChange={changeAggSelect}>
                                {AGGREGATION_OPTIONS.map(aggregationOption_ => {
                                    return (<option key={aggregationOption_} value={aggregationOption_} selected={aggregationOption_ === aggregationOption}>{aggregationOption_}</option>);
                                })}
                            </select>
                        )
                        return (
                            <div key={index} className='group-modal-value-mapping mb-1'>
                                {columnSelect}
                                {aggregationSelect}
                                <div className='ml-1 mr-1' onClick={removeValueMapping}>
                                    <svg width="13" height="3" viewBox="0 0 13 3" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <rect width="13" height="3" rx="1" fill="#B1B1B1"/>
                                    </svg>
                                </div>
                            </div>
                        )
                    })}
                </div>
            </div>
        )
    }

    addValue(): void {
        /*
            Adds a new value (columnHeader, aggregationFunction) mapping to this.state.values.

            Has some heuristics to guess which columnHeader you want!
        */
        this.setState(prevState => {
            const newValues = [...prevState.values];
            // We get the first column header in the array that 
            const columns = this.props.sheetJSONArray[this.props.selectedSheetIndex].columns;
            // If there is no columns in this, then we have nothing to group!
            if (columns.length === 0) {
                newValues.push(['none', AGGREGATION_OPTIONS[0]])
                return {
                    values: newValues
                }
            }
            // Find the first column that has not been selected as a key, and
            // also has not been grouped too, as a heuristic for what the user
            // wants to aggregate
            const unaggregatedColumns = columns.filter((columnHeader, index) => {
                return !prevState.selectedGroupByRows[index] && prevState.values.findIndex((value) => {
                    return value[0] == columnHeader;
                }) < 0;
            })
            // Take the first unaggregated column if it exists, otherwise just take the 
            // first column
            const newColumn = unaggregatedColumns.length > 0 ? unaggregatedColumns[0] : columns[0];
            newValues.push([newColumn, AGGREGATION_OPTIONS[0]])
            return {
                values: newValues
            }
        })
    }


    render() : JSX.Element  {
        const groupByRows = this.getGroupByKeys(KeyType.Row);
        const groupByCols = this.getGroupByKeys(KeyType.Col);
        const values = this.getValues()
        
        // if there are no sheets to group, don't try to display modal
        if (this.props.dfNames.length === 0) {
            return (
                <DefaultModal
                    header={'Group ' + this.props.dfNames[this.props.selectedSheetIndex]}
                    modalType={ModalEnum.Merge}
                    viewComponent= {
                        <Fragment>
                            There are no sheets to group
                        </Fragment>
                    }
                    buttons = {
                        <Fragment>
                            <div className='modal-close-button' onClick={() => {this.props.setModal({type: ModalEnum.None})}}> Close </div>
                        </Fragment>
                    }
                />
            )
        }

        return (
            <DefaultModal
                header={'Group ' + this.props.dfNames[this.props.selectedSheetIndex]}
                modalType={ModalEnum.Merge}
                viewComponent= {
                    <Fragment>
                        <div>
                            {groupByRows}
                            {groupByCols}
                            <div className='group-modal-key-error'>
                                {this.state.keyError}
                            </div>
                            {values}
                            <div className='group-modal-add-value' onClick={this.addValue}>
                                + Add Value
                            </div>
                        </div>
                    </Fragment>
                }
                buttons = {
                    <Fragment>
                        <div className='modal-close-button modal-dual-button-left' onClick={() => {this.props.setModal({type: ModalEnum.None})}}> Close </div>
                        <div className='modal-action-button modal-dual-button-right' onClick={this.completeGroup}> {"Group"}</div>
                    </Fragment>
                }
            />
        ); 
    }
}

export default GroupModal;