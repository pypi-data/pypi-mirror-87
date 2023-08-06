// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { Fragment } from 'react';
import { ModalEnum, ModalInfo, ColumnType } from '../Mito';
import DefaultModal from '../DefaultModal';

// import css
import "../../../css/margins.css";
import "../../../css/filter_modal.css"

export enum SharedFilterCondition {
    EMPTY = 'empty',
    NOT_EMPTY = 'not_empty'
}

export enum StringFilterCondition {
    CONTAINS = 'contains',
    DOES_NOT_CONTAIN = 'string_does_not_contain',
    STRING_EXACTLY = 'string_exactly'
}

export enum NumberFilterCondition {
    NUMBER_EXACTLY = 'number_exactly',
    GREATER = 'greater',
    GREATER_THAN_OR_EQUAL = 'greater_than_or_equal',
    LESS = 'less',
    LESS_THAN_OR_EQUAL = 'less_than_or_equal',
}

export enum DateFilterCondition {
    DATETIME_EXTACTLY = 'datetime_exactly',
    DATETIME_GREATER_THAN = 'datetime_greater',
    DATETIME_GREATER_THAN_OR_EQUAL = 'datetime_greater_than_or_equal',
    DATETIME_LESS = 'datetime_less',
    DATETIME_LESS_THAN_OR_EQUAL = 'datetime_less_than_or_equal',
}

export enum SortDirection {
    ASCENDING = 'ascending',
    DESCENDING = 'descending',
    NONE = 'none'
}

export type FilterCondition = 
    | SharedFilterCondition
    | StringFilterCondition
    | NumberFilterCondition
    | DateFilterCondition

interface StringFilterType {
    type: 'string',
    condition: FilterCondition,
    value?: string
}

interface NumberFilterType {
    type: 'number',
    condition: FilterCondition,
    value?: number
}

interface DateFilterType {
    type: 'datetime',
    condition: FilterCondition,
    value?: string
}

export type FiltersTypes = (StringFilterType | NumberFilterType | DateFilterType)[];

type FilterModalProps = {
    selectedSheetIndex: number,
    columnHeader: string,
    filters: FiltersTypes,
    columnType: ColumnType;
    operator: 'And' | 'Or',
    setModal: (modalInfo: ModalInfo) => void,
    send: (msg: Record<string, unknown>) => void,
}

interface FilterModalState {
    filters: FiltersTypes,
    operator: 'And' | 'Or',
    sortDirection: SortDirection
}


// if one of these filters are selected, don't display the value input
const noInputFilters: FilterCondition[] = [SharedFilterCondition.EMPTY, SharedFilterCondition.NOT_EMPTY]

const getNumberDropdownOptions = () => {
    return (
        <React.Fragment>
            <option value={NumberFilterCondition.NUMBER_EXACTLY}>=</option>
            <option value={NumberFilterCondition.GREATER}>&gt;</option>
            <option value={NumberFilterCondition.GREATER_THAN_OR_EQUAL}>&ge;</option>
            <option value={NumberFilterCondition.LESS}>&lt;</option>
            <option value={NumberFilterCondition.LESS_THAN_OR_EQUAL}>&le;</option>
        </React.Fragment>
    )
}

const getStringDropdownOptions = () => {
    return (
        <React.Fragment>
            <option value={StringFilterCondition.CONTAINS}>contains</option>
            <option value={StringFilterCondition.DOES_NOT_CONTAIN}>does not contain</option>
            <option value={StringFilterCondition.STRING_EXACTLY}>is exactly</option>
        </React.Fragment>
    )
}

const getDatetimeDropdownOptions = () => {
    return (
        <React.Fragment>
            <option value={DateFilterCondition.DATETIME_EXTACTLY}>=</option>
            <option value={DateFilterCondition.DATETIME_GREATER_THAN}>&gt;</option>
            <option value={DateFilterCondition.DATETIME_GREATER_THAN_OR_EQUAL}>&ge;</option>
            <option value={DateFilterCondition.DATETIME_LESS}>&lt;</option>
            <option value={DateFilterCondition.DATETIME_LESS_THAN_OR_EQUAL}>&le;</option>
        </React.Fragment>
    )
}

const getSharedDropdownOptions = () => {
    return (
        <React.Fragment>
            <option value={SharedFilterCondition.EMPTY}>is empty</option>
            <option value={SharedFilterCondition.NOT_EMPTY}>is not empty</option>
        </React.Fragment>
    )
}

const getNewEmptyFilter = (columnType: ColumnType): StringFilterType | NumberFilterType | DateFilterType => {
    switch (columnType) {
        case 'string':
            return {
                type: 'string',
                condition: StringFilterCondition.CONTAINS,
                value: ''
            }
        case 'number':
            return {
                type: 'number',
                condition: NumberFilterCondition.NUMBER_EXACTLY,
                value: 0
            }
        case 'datetime':
            return {
                type: 'datetime',
                condition: DateFilterCondition.DATETIME_EXTACTLY,
                value: ''
            }
            
    }
}


/*
    A modal that allows a user to filter a column
*/
class FilterModal extends React.Component<FilterModalProps, FilterModalState> {

    constructor(props: FilterModalProps) {
        super(props);

        this.state = {
            filters: this.props.filters,
            operator: this.props.operator,
            sortDirection: SortDirection.NONE
        }

        this.filterAndSortColumn = this.filterAndSortColumn.bind(this);
        this.buildFilters = this.buildFilters.bind(this);
        this.setSortDirection = this.setSortDirection.bind(this);
    }

    setSortDirection = (sortDirection : SortDirection) : void => {
        // if the user toggled the button that was already selected, turn off the sort
        if (sortDirection == this.state.sortDirection) {
            this.setState({
                sortDirection: SortDirection.NONE
            });
            return;
        } 

        // otherwise the user selected a new direction, so set that as the sortDirection
        this.setState({
            sortDirection: sortDirection
        });
    }

    filterAndSortColumn = () : void => {

        // We make sure all the filter values are defined, as serialized
        // JSON messages loose the undefined values
        const filters = this.state.filters.map(filter => {
            return {
                'type': filter.type,
                'condition': filter.condition,
                'value': filter.value === undefined ? 0 : filter.value
            }
        })
        
        window.logger?.track({
            userId: window.user_id,
            event: 'button_filter_and_sort_log_event',
            properties: {
                'sheet_index': this.props.selectedSheetIndex,
                'column_header': this.props.columnHeader,
                'filters': filters,
                'sort': this.state.sortDirection
            }
        });

        this.props.send({
            'event': 'edit_event',
            'type': 'filter_column_edit',
            'sheet_index': this.props.selectedSheetIndex,
            'column_header': this.props.columnHeader,
            'operator': this.state.operator,
            'filters': filters,
        });

        // sort the columns if the sortDirection is not None
        if (this.state.sortDirection != SortDirection.NONE) {
            this.props.send({
                'event': 'edit_event',
                'type': 'sort_edit',
                'sheet_index': this.props.selectedSheetIndex,
                'column_header': this.props.columnHeader,
                'sort_direction': this.state.sortDirection
            });
        }
        this.props.setModal({type: ModalEnum.None});
    }

    buildFilters(): JSX.Element {
        /*
            Builds all the JSX for the filter selections, for all of the filters in
            this.state.filters
        */

        const handleToggleOperator = (e: React.ChangeEvent<HTMLSelectElement>): void => {
            // Occurs when the user switches which operator is being used

            const newOperator = e.target.value as 'And' | 'Or';
            this.setState({
                operator: newOperator
            })
        }

        const handleConditionChange = (filterIndex: number, e: React.ChangeEvent<HTMLSelectElement>): void => {
            // Occurs when a user changes the condition on a specific filter
            
            // This case is safe, as users can only select from a list of the enum
            const newCondition = e.target.value as FilterCondition;

            this.setState(prevState => {
                const newFilters = [...prevState.filters] as FiltersTypes;
                // Note: we save the new condition outside the setState, as react does
                // not keep events around! 
                newFilters[filterIndex].condition = newCondition
                if (noInputFilters.includes(newCondition)) {
                    // Clear the value, if this condition has no value
                    newFilters[filterIndex].value = undefined;
                }

                return {
                    filters: newFilters,
                }
            })
        }

        const handleValueChange = (filterIndex: number, e: React.ChangeEvent<HTMLInputElement>): void => {
            // Occurs when the user changes a value on a specific filter, which is then
            // saved to the state for this filter

            const filter = this.state.filters[filterIndex];
            let newValue: string | number = e.target.value;
            // Cast it to the correct type
            if (filter.type === 'number') {
                const float = parseFloat(newValue);
                if (!Number.isNaN(float)) {
                    newValue = float;
                }
            }

            this.setState(prevState => {
                const newFilters = [...prevState.filters] as FiltersTypes;
                // Note: we save the new condition outside the setState, as react does
                // not keep events around! 
                newFilters[filterIndex].value = newValue;

                return {
                    filters: newFilters,
                }
            })
        }

        const removeFilter = (filterIndex: number) : void => {
            // Removes the filter at the given filterIndex 

            this.setState(prevState => {
                const newFilters = [...prevState.filters];
                newFilters.splice(filterIndex, 1);
                return {
                    filters: newFilters
                }
            })
        }

        const getFilter = (filter: NumberFilterType | StringFilterType | DateFilterType, filterIndex: number): JSX.Element => {
            // Builds the table row element for a given filter at a given index

            // We use styles to hide divs we don't want, to keep the spacing the same
            const operatorStyle: {visibility: 'hidden' | 'visible'} = filterIndex === 0 ? {visibility: 'hidden'} : {visibility: 'visible'};
            const inputStyle: {visibility: 'hidden' | 'visible'} = noInputFilters.includes(filter.condition) ? {visibility: 'hidden'} : {visibility: 'visible'};

            return (
                <React.Fragment>
                    <tr>
                        <td>
                            <select className='select filter-modal-input' style={operatorStyle} value={this.state.operator} onChange={handleToggleOperator} >
                                <option value={'And'}>And</option>
                                <option value={'Or'}>Or</option>
                            </select>
                        </td>
                        <td>
                            <select className="select filter-modal-condition-select" value={filter.condition} onChange={e => handleConditionChange(filterIndex, e)} >
                                {filter.type === 'number' && getNumberDropdownOptions()}
                                {filter.type === 'string' && getStringDropdownOptions()}
                                {filter.type === 'datetime' && getDatetimeDropdownOptions()}
                                {getSharedDropdownOptions()}
                            </select>
                        </td>
                        <td>
                            <input className="input filter-modal-value-input" style={inputStyle} value={filter.value?.toString()} onChange={e => handleValueChange(filterIndex, e)}/>
                        </td>
                        <td>
                            <div className='ml-1 mr-1' onClick={() => removeFilter(filterIndex)}>
                                <svg width="13" height="3" viewBox="0 0 13 3" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <rect width="13" height="3" rx="1" fill="#B1B1B1"/>
                                </svg>
                            </div>    
                        </td>
                    </tr>
                </React.Fragment>
            )
        }

        return (
            <table>
                {this.state.filters.length > 0 &&
                    <tr>
                        <td/>
                        <td>Filter Condition</td>
                        <td>Value</td>
                    </tr>
                }   
                {this.state.filters.map((filter, filterIndex) => {
                    return getFilter(filter, filterIndex);
                })}
            </table>
        )
    }


    render() : JSX.Element {

        const addFilter = () => {
            this.setState(prevState => {
                const newFilters = [...prevState.filters]
                newFilters.push(getNewEmptyFilter(this.props.columnType));
                return {
                    filters: newFilters
                }
            })
        }

        // determine css styling of sort buttons
        const ascendingButtonClass = this.state.sortDirection == SortDirection.ASCENDING ? 'sort-button sort-button-selected' : 'sort-button sort-button-unselected';
        const descendingButtonClass = this.state.sortDirection == SortDirection.DESCENDING ? 'sort-button sort-button-selected' : 'sort-button sort-button-unselected';

        return (
            <DefaultModal
                header={`${this.props.columnHeader} Control Panel`}
                modalType={ModalEnum.Filter}
                viewComponent= {
                    <Fragment>
                        <div>
                            <div className='filter-modal-section-title'>
                                <p> Sort </p>
                            </div>
                            <div className="filter-modal-centering-container">
                                <div className='sort-buttons-div'>
                                    <button 
                                        className={ascendingButtonClass}
                                        onClick={() => this.setSortDirection(SortDirection.ASCENDING)}> 
                                            Ascending 
                                    </button>
                                    <button 
                                        className={descendingButtonClass}
                                        onClick={() => this.setSortDirection(SortDirection.DESCENDING)}>
                                             Descending 
                                    </button>
                                </div>
                            </div>
                            <div className='filter-modal-section-title filter-modal-section-spacer'>
                                <p> Filter </p>
                            </div>
                            <div className="filter-modal-centering-container">
                                {this.state.filters.length === 0 &&
                                <p className='mb-1'>
                                    Hit the Add Filter button below to begin filtering
                                    this column.
                                </p>
                                }
                                {this.buildFilters()}
                                <div className='filter-modal-add-value' onClick={addFilter}>
                                    + Add Filter
                                </div>
                            </div>
                        </div>
                    </Fragment>
                }
                buttons = {
                    <Fragment>
                        <div className='modal-close-button modal-dual-button-left' onClick={() => {this.props.setModal({type: ModalEnum.None})}}> Close </div>
                        <div className='modal-action-button modal-dual-button-right' onClick={this.filterAndSortColumn}> {"Apply"}</div>
                    </Fragment>
                }
            />
        );
    }
}

export default FilterModal;