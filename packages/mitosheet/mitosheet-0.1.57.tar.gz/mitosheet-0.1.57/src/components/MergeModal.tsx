// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { Fragment } from 'react';
import { ModalEnum, ModalInfo } from './Mito';
import DefaultModal from './DefaultModal';

import { SheetJSON } from '../widget';

// import css
import "../../css/merge-modal.css"


type MergeModalProps = {
    setModal: (modalInfo: ModalInfo) => void;
    sheetJSONArray: SheetJSON[];
    dfNames: string[];
    send: (msg: Record<string, unknown>) => void,
};

type MergeModalState = {
    sheetOneIndex: number;
    sheetTwoIndex: number;
    sheetOneMergeKey: number | string,
    sheetTwoMergeKey: number | string,
    sheetOneSelectedColumns: boolean[],
    sheetTwoSelectedColumns: boolean[],
    sheetOneToggleAll: boolean;
    sheetTwoToggleAll: boolean;
};


type SuggestedKeys = {
    sheetOneMergeKey: string | number,
    sheetTwoMergeKey: string | number
}


const getSharedKeys = (sheetOneIndex: number, sheetTwoIndex: number, sheetJSONArray: SheetJSON[]): string[] => {
    // Given two sheets indexes, returns all the columns that are shared between both sheets

    const sheetOneColumnNames = sheetJSONArray[sheetOneIndex].columns;
    const sheetTwoColumnNames = sheetJSONArray[sheetTwoIndex].columns;

    const sharedKeys = sheetOneColumnNames.filter(columnName => sheetTwoColumnNames.includes(columnName)).map(columnHeader => columnHeader.toString())

    return sharedKeys;
}


const getSuggestedKeys = (sheetOneIndex: number, sheetTwoIndex: number, sheetJSONArray: SheetJSON[]): SuggestedKeys => {
    // Given two sheet indexes, reccomends a key to merge on. If there are x shared keys, then:
    // - If x.length == 1, it returns this key as reccomended.
    // - Else, it does not reccomend a key!
    
    const sharedKeys = getSharedKeys(sheetOneIndex, sheetTwoIndex, sheetJSONArray);
    const sheetOneMergeKey = sharedKeys.length === 1 ? sharedKeys[0] : sheetJSONArray[sheetOneIndex].columns[0];
    const sheetTwoMergeKey = sharedKeys.length === 1 ? sharedKeys[0] : sheetJSONArray[sheetTwoIndex].columns[0];
    return {
        sheetOneMergeKey: sheetOneMergeKey,
        sheetTwoMergeKey: sheetTwoMergeKey
    }
}

class MergeModal extends React.Component<MergeModalProps, MergeModalState> {

    constructor(props: MergeModalProps) {
        super(props);

        const sheetOneIndex = 0;
        const sheetTwoIndex = Math.min(1, props.sheetJSONArray.length - 1);
        const suggestedKeys = getSuggestedKeys(sheetOneIndex, sheetTwoIndex, props.sheetJSONArray);

        // We default to selecting _all_ columns
        const sheetOneSelectedColumns = this.props.sheetJSONArray[sheetOneIndex].columns.map(() => true)
        const sheetTwoSelectedColumns = this.props.sheetJSONArray[sheetTwoIndex].columns.map(() => true)
        
        this.state = {
            sheetOneIndex: sheetOneIndex,
            sheetTwoIndex: sheetTwoIndex,
            sheetOneMergeKey: suggestedKeys.sheetOneMergeKey,
            sheetTwoMergeKey: suggestedKeys.sheetTwoMergeKey,
            sheetOneSelectedColumns: sheetOneSelectedColumns,
            sheetTwoSelectedColumns: sheetTwoSelectedColumns,
            sheetOneToggleAll: true,
            sheetTwoToggleAll: true
        };

        this.updateSheetOneSelection = this.updateSheetOneSelection.bind(this);
        this.updateSheetOneKeySelection = this.updateSheetOneKeySelection.bind(this);
        this.updateSheetTwoSelection = this.updateSheetTwoSelection.bind(this);
        this.updateSheetTwoKeySelection = this.updateSheetTwoKeySelection.bind(this);
        this.completeMerge = this.completeMerge.bind(this);
    }

    updateSheetOneSelection = (e: React.ChangeEvent<HTMLSelectElement>): void => {
        const newSheetIndex = parseInt(e.target.value);
        const suggestedKeys = getSuggestedKeys(newSheetIndex, this.state.sheetTwoIndex, this.props.sheetJSONArray); 

        // default to selecting all of the columns of a newly selected sheet   
        const newSheetOneSelectedColumn = this.props.sheetJSONArray[newSheetIndex].columns.map(() => true);

        this.setState({
            sheetOneIndex: newSheetIndex,
            sheetOneSelectedColumns: newSheetOneSelectedColumn,
            sheetOneMergeKey: suggestedKeys.sheetOneMergeKey,
            sheetTwoMergeKey: suggestedKeys.sheetTwoMergeKey,
        });    
    }

    updateSheetOneKeySelection = (e: React.ChangeEvent<HTMLSelectElement>): void => {
        const newSheetMergeKey = e.target.value;
        this.setState({sheetOneMergeKey: newSheetMergeKey});    
    }

    updateSheetTwoSelection = (e: React.ChangeEvent<HTMLSelectElement>): void => {
        const newSheetIndex = parseInt(e.target.value);
        const suggestedKeys = getSuggestedKeys(this.state.sheetOneIndex, newSheetIndex, this.props.sheetJSONArray);

        // default to selecting all of the columns of a newly selected sheet   
        const newSheetTwoSelectedColumn = this.props.sheetJSONArray[newSheetIndex].columns.map(() => true);

        this.setState({
            sheetTwoIndex: newSheetIndex,
            sheetTwoSelectedColumns: newSheetTwoSelectedColumn,
            sheetOneMergeKey: suggestedKeys.sheetOneMergeKey,
            sheetTwoMergeKey: suggestedKeys.sheetTwoMergeKey
        });
    }

    updateSheetTwoKeySelection = (e: React.ChangeEvent<HTMLSelectElement>): void => {
        const newSheetMergeKey = e.target.value;
        this.setState({sheetTwoMergeKey: newSheetMergeKey});    
    }
    
    completeMerge = (): void => {

        const selectedColumnsOne = this.props.sheetJSONArray[this.state.sheetOneIndex].columns.filter((columnHeader, index) => {
            if (columnHeader == this.state.sheetOneMergeKey) {
                return true;
            }
            return this.state.sheetOneSelectedColumns[index];
        })
        const selectedColumnsTwo = this.props.sheetJSONArray[this.state.sheetTwoIndex].columns.filter((columnHeader, index) => {
            if (columnHeader == this.state.sheetTwoMergeKey) {
                return true;
            }
            return this.state.sheetTwoSelectedColumns[index];
        })

        window.logger?.track({
            userId: window.user_id,
            event: 'button_merge_log_event',
            properties: {
                stage: 'merged',
                sheet_index_one: this.state.sheetOneIndex,
                merge_key_one: this.state.sheetOneMergeKey,
                selected_columns_one: selectedColumnsOne,
                sheet_index_two: this.state.sheetTwoIndex,
                merge_key_two: this.state.sheetTwoMergeKey,
                selected_columns_two: selectedColumnsTwo,
            }
        })

        this.props.send({
            'event': 'edit_event',
            'type': 'merge_edit',
            'sheet_index_one': this.state.sheetOneIndex,
            'merge_key_one': this.state.sheetOneMergeKey,
            'selected_columns_one': selectedColumnsOne,
            'sheet_index_two': this.state.sheetTwoIndex,
            'merge_key_two': this.state.sheetTwoMergeKey,
            'selected_columns_two': selectedColumnsTwo
        })
        this.props.setModal({type: ModalEnum.None});
    }

    getColumnSelection(mergeSheetIndex: 0 | 1) : JSX.Element {
        /* 
            Returns the columns selection box, that allows users
            to select which columns they want to keep.
        */
        const sheetIndexName = mergeSheetIndex == 0 ? 'sheetOneIndex' : 'sheetTwoIndex';
        const sheetIndex = mergeSheetIndex == 0 ? this.state.sheetOneIndex : this.state.sheetTwoIndex;
        const mergeKey = mergeSheetIndex == 0 ? this.state.sheetOneMergeKey : this.state.sheetTwoMergeKey;
        const sheetName = this.props.dfNames[sheetIndex];
 
        return (
            <div className='merge-modal-column-selection-container'>
                <div className='merge-modal-label'>
                    Columns to keep from {sheetName}
                </div>
                <div className='merge-modal-column-selection'>
                    <div>
                        {/* This is the toggle all check box, which is the first option */}
                        <input
                            type="checkbox"
                            checked={mergeSheetIndex == 0 ? this.state.sheetOneToggleAll : this.state.sheetTwoToggleAll}
                            onChange={() => {
                                if (mergeSheetIndex === 0) {
                                    this.setState(prevState => {
                                        const newValue = !prevState.sheetOneToggleAll;
                                        return {
                                            sheetOneToggleAll: newValue,
                                            sheetOneSelectedColumns: prevState.sheetOneSelectedColumns.map(() => newValue)
                                        };                                  
                                    })
                                } else {
                                    this.setState(prevState => {
                                        const newValue = !prevState.sheetTwoToggleAll;
                                        return {
                                            sheetTwoToggleAll: newValue,
                                            sheetTwoSelectedColumns: prevState.sheetTwoSelectedColumns.map(() => newValue)
                                        };                                  
                                    })   
                                }
                            }}
                            className="form-check-input"
                        />
                        Select all
                    </div>
                    {this.props.sheetJSONArray[this.state[sheetIndexName]].columns.map((columnHeader, index) => {
                        // We don't display the merge key!
                        if (mergeKey == columnHeader) {
                            return undefined;
                        }

                        const isSelected = mergeSheetIndex == 0 ? 
                            this.state.sheetOneSelectedColumns[index]: 
                            this.state.sheetTwoSelectedColumns[index];
                        return (
                        <div key={columnHeader}>
                            <input
                                key={columnHeader}
                                type="checkbox"
                                name={columnHeader.toString()}
                                checked={isSelected}
                                onChange={() => {
                                    if (mergeSheetIndex === 0) {
                                        this.setState(prevState => {
                                            const newSheetOneSelectedColumns = [...prevState.sheetOneSelectedColumns];
                                            newSheetOneSelectedColumns[index] = !newSheetOneSelectedColumns[index];
                                            return {
                                                sheetOneSelectedColumns: newSheetOneSelectedColumns
                                            }                                    
                                        })
                                    } else {
                                        this.setState(prevState => {
                                            const newSheetTwoSelectedColumns = [...prevState.sheetTwoSelectedColumns];
                                            newSheetTwoSelectedColumns[index] = !newSheetTwoSelectedColumns[index];
                                            return {
                                                sheetTwoSelectedColumns: newSheetTwoSelectedColumns
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


    render() : JSX.Element  {
        const sheetOneSelect = (
            <select className='merge-modal-sheet-dropdown' onChange={this.updateSheetOneSelection}>
                {this.props.dfNames.map((dfName, index) => {
                    return (<option key={dfName} value={index} selected={this.state.sheetOneIndex === index}>{dfName}</option>);
                })}
            </select>
        )

        const sheetOneMergeKeySelect = (
            <select className='merge-modal-key-dropdown' onChange={this.updateSheetOneKeySelection}>
                {this.props.sheetJSONArray[this.state.sheetOneIndex].columns.map((columnHeader) => {
                    return (<option key={columnHeader} value={columnHeader} selected={this.state.sheetOneMergeKey === columnHeader}>{columnHeader}</option>);
                })}
            </select>
        )

        const sheetOneColumnsToKeep = this.getColumnSelection(0);
    
        const sheetTwoSelect = (
            <select className='merge-modal-sheet-dropdown' onChange={this.updateSheetTwoSelection}>
                {this.props.dfNames.map((dfName, index) => {
                    return (<option key={dfName} value={index} selected={this.state.sheetTwoIndex === index}>{dfName}</option>);
                })}
            </select>
        )

        const sheetTwoMergeKeySelect = (
            <select className='merge-modal-key-dropdown' onChange={this.updateSheetTwoKeySelection}>
                {this.props.sheetJSONArray[this.state.sheetTwoIndex].columns.map((columnHeader) => {
                    return (<option key={columnHeader} value={columnHeader} selected={this.state.sheetTwoMergeKey === columnHeader}>{columnHeader}</option>);
                })}
            </select>
        )

        const sheetTwoColumnsToKeep = this.getColumnSelection(1)
        
        // if there are no sheets to merge, don't try to display modal
        if (this.props.dfNames.length === 0) {
            return (
                <DefaultModal
                    header='Merge two sheets'
                    modalType={ModalEnum.Merge}
                    viewComponent= {
                        <Fragment>
                            There are no sheets to merge
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
                header='Merge two sheets'
                modalType={ModalEnum.Merge}
                viewComponent= {
                    <Fragment>
                        <div>
                            <div className='merge-modal-sheet-and-key'>
                                <div className='merge-modal-sheet' >
                                    <p className='merge-modal-label'>
                                        First Sheet
                                    </p>
                                    {sheetOneSelect}
                                </div>
                                <div className='merge-modal-key' >
                                    <p className='merge-modal-label'>
                                        Merge Key
                                    </p>
                                    {sheetOneMergeKeySelect}
                                </div>
                            </div>
                            {sheetOneColumnsToKeep}
                            <div className='merge-modal-sheet-and-key'>
                                <div className='merge-modal-sheet' >
                                    <p className='merge-modal-label'>
                                        Second Sheet
                                    </p>
                                    {sheetTwoSelect}
                                </div>
                                <div className='merge-modal-key' >
                                    <p className='merge-modal-label'>
                                        Merge Key
                                    </p>
                                    {sheetTwoMergeKeySelect}
                                </div>
                            </div> 
                            {sheetTwoColumnsToKeep}
                        </div>
                    </Fragment>
                }
                buttons = {
                    <Fragment>
                        <div className='modal-close-button modal-dual-button-left' onClick={() => {this.props.setModal({type: ModalEnum.None})}}> Close </div>
                        <div className='modal-action-button modal-dual-button-right' onClick={this.completeMerge}> {"Merge"}</div>
                    </Fragment>
                }
            />
        ); 
    }
}

export default MergeModal;