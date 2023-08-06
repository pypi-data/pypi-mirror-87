// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { MouseEvent } from 'react';

// Import types
import { CellFocusedEvent, ColumnMovedEvent } from 'ag-grid-community';
import { SheetJSON, ErrorJSON, SheetShape } from '../widget';
import { MITO_INDEX } from '../utils/gridData';


// Import sheet and code components
import MitoSheet from './MitoSheet';
import SheetTab from './SheetTab';
import FormulaBar from './FormulaBar';
import MitoToolbar from './MitoToolbar';
import DocumentationSidebarContainer from './documentation/DocumentationSidebarContainer';
import LoadingIndicator from './LoadingIndicator';

// Import modals
import ErrorModal from './ErrorModal';
import DownloadModal from './DownloadModal';
import ColumnHeaderModal from './modals/ColumnHeaderModal';
import MergeModal from './MergeModal';
import FilterModal, {FiltersTypes} from './modals/FilterModal';
import DeleteColumnModal from './modals/DeleteColumnModal';
import SaveAnalysisModal from './modals/SaveAnalysisModal';
import SaveAnalysisOverwriteModal from './modals/SaveAnalysisOverwriteModal';
import ReplayAnalysisModal from './modals/ReplayAnalysisModal';
import GroupModal from './modals/GroupModal';

// Import css
import "../../css/mito.css"

export interface ColumnSpreadsheetCodeJSON {
    [Key: string]: string;
}

export type SheetColumnFiltersArray = SheetColumnFilterMap[]; 

export type ColumnType =
    | 'string'
    | 'number'
    | 'datetime'


export interface SheetColumnFilterMap {
    [column: string] : {
        operator: 'Or' | 'And',
        filters: FiltersTypes
    }
}

export interface ColumnTypeJSON {
    [Key: string]: ColumnType;
}
export type ColumnTypeJSONArray = ColumnTypeJSON[]; 


export enum ModalEnum {
    None = 'None',
    Error = 'Error',
    RepeatAnalysis = 'RepeatAnalysis',
    Download = 'Download',
    ColumnHeader = 'ColumnHeader',
    Merge = 'Merge',
    DeleteColumn = 'DeleteColumn',
    SaveAnalysis = 'SaveAnalysis',
    SaveAnalysisOverwrite = 'SaveAnalysisOverwrite',
    ReplayAnalysis = 'ReplayAnalysis',
    Filter = "Filter",
    Group = "Group"
}

/* 
    Each modal comes with modal info, and we enforce (through types) that if you set
    the current modal, you must also pass it the data that it requires. 

    To see what information a modal requires, see it's <>ModalInfo type definition
    below!

    NOTE: Currently, the column header modal is the only modal that needs any data...
    but this is a good investment for the future :)
*/
interface NoneModalInfo {type: ModalEnum.None}
interface ErrorModalInfo {type: ModalEnum.Error}
interface DownloadModalInfo {type: ModalEnum.Download}
interface MergeModalInfo {type: ModalEnum.Merge}
interface GroupModalInfo {type: ModalEnum.Group}
interface ColumnHeaderModalInfo {
    type: ModalEnum.ColumnHeader;
    columnHeader: string;
}
interface DeleteColumnModalInfo {
    type: ModalEnum.DeleteColumn;
    columnHeader: string;
}
interface SaveAnalysisModalInfo {
    type: ModalEnum.SaveAnalysis;
    saveAnalysisName?: string;
}
interface SaveAnalysisOverwriteModalInfo {
    type: ModalEnum.SaveAnalysisOverwrite;
    saveAnalysisName: string;
}
interface ReplayAnalysisModalInfo {
    type: ModalEnum.ReplayAnalysis;
}

interface FilterModalInfo {
    type: ModalEnum.Filter;
    columnHeader: string;
}

export type ModalInfo = 
    | NoneModalInfo 
    | ErrorModalInfo
    | DownloadModalInfo
    | MergeModalInfo
    | ColumnHeaderModalInfo
    | DeleteColumnModalInfo
    | SaveAnalysisModalInfo
    | SaveAnalysisOverwriteModalInfo
    | ReplayAnalysisModalInfo
    | FilterModalInfo
    | GroupModalInfo


type MitoProps = {
    dfNames: string[];
    sheetShapeArray: SheetShape[];
    columnSpreadsheetCodeJSONArray: ColumnSpreadsheetCodeJSON[];
    sheetJSONArray: SheetJSON[];
    savedAnalysisNames: string[];
    columnFiltersArray: SheetColumnFiltersArray;
    columnTypeJSONArray: ColumnTypeJSONArray;
    send: (msg: Record<string, unknown>) => void
    model_id: string;
};

type MitoState = {
    dfNames: string[];
    sheetShapeArray: SheetShape[];
    columnSpreadsheetCodeJSONArray: ColumnSpreadsheetCodeJSON[];
    sheetJSONArray: SheetJSON[];
    columnFiltersArray: SheetColumnFiltersArray;
    columnTypeJSONArray: ColumnTypeJSONArray;
    selectedSheetIndex: number;
    formulaBarValue: string;
    selectedColumn: string;
    selectedRowIndex: number;
    errorJSON: ErrorJSON;
    documentationOpen: boolean;
    editingModeState: EditingModeState;
    movingColumnParams: MovingColumnParams;
    savedAnalysisNames: string[];
    modalInfo: ModalInfo;
    loading: boolean;
};

type EditingModeState = {
    editingModeOn: boolean;
    editingSheetIndex: number;
    editingCellColumn: string;
    editingCellRowIndex: number;
    lastFormula: string; // This is the last formula there is, and it notably might be invalid
    formulaCursorIndex: number;
}

type MovingColumnParams = ColumnMovedState | undefined

type ColumnMovedState = {
    column: string;
    newIndex: number
}

class Mito extends React.Component<MitoProps, MitoState> {

    constructor(props: MitoProps) {
        super(props);

        const formulaBarValue = this.props.sheetJSONArray[0].data[0] === undefined
            ? '' : this.props.sheetJSONArray[0].data[0][0];
        const selectedColumn = this.props.sheetJSONArray[0].columns[0] === undefined
            ? '' : this.props.sheetJSONArray[0].columns[0].toString();

        this.state = {
            dfNames: this.props.dfNames,
            sheetShapeArray: this.props.sheetShapeArray,
            columnSpreadsheetCodeJSONArray: this.props.columnSpreadsheetCodeJSONArray,
            sheetJSONArray: this.props.sheetJSONArray,
            columnFiltersArray: this.props.columnFiltersArray,
            columnTypeJSONArray: this.props.columnTypeJSONArray,
            selectedSheetIndex: 0,
            formulaBarValue: formulaBarValue,
            selectedColumn: selectedColumn,
            selectedRowIndex: 0,
            /*
                we tell if we're in cell editing mode through the editingModeOn state variable

                the editingCellColumn and editingCellRowIndex are used to update the formula of the correct
                cell editor. They get set to the new values when we turn cell editing mode back on, but are unchanged
                when we turn cell editing mode off so that we can handle formulas that error by letting the user 
                edit the formula that they submitted. 
            */
            editingModeState: {
                editingModeOn: false,
                editingSheetIndex: 0,
                editingCellColumn: "",
                editingCellRowIndex: -1,
                lastFormula: formulaBarValue,
                formulaCursorIndex: 2, // set to an arbitrary value -- it gets set correctly in gridData.tsx
            },
            movingColumnParams: undefined,
            documentationOpen: false,
            errorJSON: {
                event: '',
                type: '',
                header: '',
                to_fix: ''
            },
            modalInfo: {type: ModalEnum.None},
            savedAnalysisNames: this.props.savedAnalysisNames,
            loading: false
        };

        this.cellFocused = this.cellFocused.bind(this);
        this.handleFormulaBarDoubleClick = this.handleFormulaBarDoubleClick.bind(this);
        this.sendCellValueUpdate = this.sendCellValueUpdate.bind(this);
        this.setEditingMode = this.setEditingMode.bind(this);
        this.setEditingFormula = this.setEditingFormula.bind(this);
        this.setDocumentation = this.setDocumentation.bind(this);
        this.setModal = this.setModal.bind(this);
        this.getCurrentModalComponent = this.getCurrentModalComponent.bind(this);
        this.setSelectedSheetIndex = this.setSelectedSheetIndex.bind(this);
        this.turnOnCellEditor = this.turnOnCellEditor.bind(this);
        this.setCursorIndex = this.setCursorIndex.bind(this);
        this.columnMoved = this.columnMoved.bind(this);
        this.columnDragStopped = this.columnDragStopped.bind(this);
    }

    /* 
        called by the cell editor so that the column the user clicks on can be appended
        to the correct location in the formula
    */
    setCursorIndex(index: number) : void {
        this.setState(prevState => {
            return {
                editingModeState: {                   
                    ...prevState.editingModeState,    
                    formulaCursorIndex: index                          
                }
            };
        });
    }

    /* 
        This function is responsible for turning cell editing mode on and off
        by setting the state of editingCellColumn, and editingCellRowIndex.

        If you call this function with on===true, then the passed column and rowIndex
        should be the cell you want to start editing.

        If you call this function with on===false, then editing will be stopped, and the 
        passed column and rowIndex will be focused on.
    */
   
    setEditingMode(on: boolean, column: string, rowIndex: number) : void {
        if (on && !this.state.editingModeState.editingModeOn) {
            /* 
                This runs (and turns on editing mode) when we're not in editing mode and:
                1. The user double clicks on a cell
                2. The user presses enter on a cell. 
                3. The user types any character on a cell. 
            */

           this.setState(prevState => {
                return {
                    editingModeState: {                   
                        ...prevState.editingModeState,  
                        editingSheetIndex: this.state.selectedSheetIndex,  
                        editingModeOn: true,
                        editingCellColumn: column,
                        editingCellRowIndex: rowIndex             
                    }
                };
            });
            
        } else if (!on) {
            /* 
                We turn off cell-editing mode and select the given cell.

                This handles some of the many ways cell editing can be stopped
                explicitly (e.g. ENTER), as we want only sometimes want ENTER to stop 
                editing (in other cases, we want it to select a suggestion!).

                To see a list of events that stop editing, see:
                https://www.ag-grid.com/javascript-grid-cell-editing/#stop-end-editing
            */

            this.setState(prevState => {
                return {
                    editingModeState: {                   
                        ...prevState.editingModeState,
                        editingModeOn: false,          
                    }
                };
            });
            

            // We actually stop the grid from editing in this case, and set cell focus
            // as stopping editing focuses on nothing by default.
            window.gridApiMap?.get(this.props.model_id)?.stopEditing();
            window.gridApiMap?.get(this.props.model_id)?.setFocusedCell(
                rowIndex, 
                column
            );
        }
    }

    /*
        This function is called by the cell editor to update the formula of the editing cell
        in the mito state, so that when cellFocused starts editing mode again, it can 
        pass in the starting formula.  

        We save the formula in the state because:
            1) when the user clicks on another cell, it closes the cell editor.
            We need to store the formula in state so when we put the editor 
            back in cell editing mode in the CellFocussedEvent, 
            we're able to start the cell editor with the correct formula. 
            
            Note: we don't want to send the intermediate formula to the parser

            2) we need to display the formula that is in the editor in the formula bar as well.  
    */
    setEditingFormula(formula : string) : void {
        this.setState(prevState => {
            return {
                editingModeState: {                   
                    ...prevState.editingModeState, 
                    lastFormula: formula
                },
                formulaBarValue: formula,
            };
        });                 
    }

    turnOnCellEditor() : void {
        const editingModeParams = {
            rowIndex: this.state.editingModeState.editingCellRowIndex,
            colKey: this.state.editingModeState.editingCellColumn,
        }

        // turn the editing cell's cell editor back on!
        window.gridApiMap?.get(this.props.model_id)?.startEditingCell(editingModeParams);
    }

    /* 
        Occurs when a cell is clicked. If we are currently editing a cell, we append the clicked
        column to the currently-edited cell. Otherwise, we select the clicked cell.
    */
    cellFocused(event : CellFocusedEvent) : void {
        /* 
            We avoid cell focused throwing an error when switching sheets by making sure the 
            event is defined, and just returning. Not sure why this occurs!

            Additionally, turn of cell editing mode & reset the formulaBarValue. when the user switches
            sheets we reset the editing cell to clear the formula bar
        */
        const column = event.column?.getColId();
        const rowIndex = event.rowIndex;
        if (!column) {
            this.setEditingMode(false, "", -1);
            this.setState(prevState => {
                return {
                    editingModeState: {                   
                        ...prevState.editingModeState, 
                        editingCellColumn: '',
                        editingCellRowIndex: -1
                    },
                    formulaBarValue: '',
                };
            }); 
            return;
        } 

        // if we're in cell editing mode, turn cell editor back on
        if (this.state.editingModeState.editingModeOn) {

            /* 
                if the column we focussed on is the editing column or the index column, don't append to the formula
            */ 
            if (column === this.state.editingModeState.editingCellColumn || column === MITO_INDEX) {
                this.turnOnCellEditor();
                return;
            }

            /*
                If we're in editing mode & the cell focused on is not in the column we're editing
                or the index column, append the clicked column to the editing formula;
            */ 

            // add the column reference to the formula where the user's cursor is in the input field
            const formulaCursorIndex = this.state.editingModeState.formulaCursorIndex
            
            // If you click on the same row, we just insert that column name. If you click on a different
            // row than the one you are editing, we insert an offset formula.
            const columnReference = this.state.editingModeState.editingCellRowIndex === rowIndex 
                                    ? column 
                                    : `OFFSET(${column}, ${rowIndex - this.state.editingModeState.editingCellRowIndex})`;

            const newFormula = this.state.formulaBarValue.slice(0, formulaCursorIndex) + columnReference + this.state.formulaBarValue.slice(formulaCursorIndex);

            this.setState(prevState => {
                return {
                    editingModeState: {                   
                        ...prevState.editingModeState, 
                        lastFormula: newFormula,
                        formulaCursorIndex: formulaCursorIndex + columnReference.length // update the formula cursor index to include appended characters
                    },
                    formulaBarValue: newFormula,
                };
            }, () => {
                this.turnOnCellEditor()
            });
        } else {
            // If we're not in editing mode, then we update the formula bar only

            // if the column is the index column, then we reset the selected cell state
            if (column === MITO_INDEX) {
                this.setState({
                    selectedColumn: '',
                    selectedRowIndex: 0,
                    formulaBarValue: ''
                });
                return;
            }

            // otherwise, get the cell's formula to display
            const columnIndex = this.state.sheetJSONArray[this.state.selectedSheetIndex].columns.indexOf(column);
            const rowIndex = event.rowIndex;

            const columnFormula = this.state.columnSpreadsheetCodeJSONArray[this.state.selectedSheetIndex][column];

            let formulaBarValue = this.state.formulaBarValue;

            if (columnFormula === '') {
                // If there no formula, we just display the value
                formulaBarValue = this.state.sheetJSONArray[this.state.selectedSheetIndex].data[rowIndex][columnIndex];
            } else {
                // Otherwise, we display the formula that is in the column
                formulaBarValue = columnFormula;
                if (this.state.selectedSheetIndex === this.state.editingModeState.editingSheetIndex && column === this.state.editingModeState.editingCellColumn) {
                    // The last formula is always equal to the _last_ edit made to a formula
                    // and so we take it so we keep an error formula
                    formulaBarValue = this.state.editingModeState.lastFormula;
                }
            }

            this.setState({
                selectedColumn: column,
                selectedRowIndex: rowIndex,
                formulaBarValue: formulaBarValue
            });
        }
    }

    handleFormulaBarDoubleClick(e : MouseEvent<HTMLButtonElement>) : void {
        e.preventDefault();

        /*
            when the formula bar is double clicked, turns on cell editing mode and opens the 
            selected cell's cell editor 

            TODO: make sure it works with multiple sheets. fix: when we switch sheets, 
            reset this.state.selectedColumn & this.state.selectedRowIndex
        */

        // do nothing if the selected cell is a data column
        if (this.state.columnSpreadsheetCodeJSONArray[this.state.selectedSheetIndex][this.state.selectedColumn] === '') {
            return
        }

        // turn cell editing mode on
        this.setEditingMode(true, this.state.selectedColumn, this.state.selectedRowIndex)

        /* 
            turns on the correct cell editor. If the selected cell is not in view, 
            the spreadsheet will be scrolled automatically until it is. 
        */
        const editingModeParams = {
            rowIndex: this.state.selectedRowIndex,
            colKey: this.state.selectedColumn,
        }
        window.gridApiMap?.get(this.props.model_id)?.startEditingCell(editingModeParams);
    }

    // TODO: this event should be broken out into a formula edit and a value edit
    sendCellValueUpdate(column : string, newValue : string) : void {
        /*
            We don't send the formula to the evaluator while in cell editing mode
            because this function gets called after the CellValueChangedEvent fires 
            each time the cell editor is closed. 
            
            However, the cell editor closes each time the user uses their mouse 
            to reference another column - which isn't a finished update yet!
        */
        if (!this.state.editingModeState.editingModeOn) {
            this.props.send({
                'event': 'edit_event',
                'type': 'set_column_formula_edit',
                'sheet_index': this.state.selectedSheetIndex,
                'column_header': column,
                'new_formula': newValue
            });
        }
    }

    setDocumentation(documentationOpen: boolean) : void {
        this.setState({documentationOpen: documentationOpen});
    }

    getCurrentModalComponent(): JSX.Element {
        // Returns the JSX.element that is currently, open, and is used
        // in render to display this modal
        switch(this.state.modalInfo.type) {
            case ModalEnum.None: return <div></div>;
            case ModalEnum.Error: return (
                <ErrorModal
                    errorJSON={this.state.errorJSON}
                    setModal={this.setModal}
                    />
            )
            case ModalEnum.Download: return (
                <DownloadModal
                    setModal={this.setModal}
                    />
            )
            case ModalEnum.ColumnHeader: return (
                <ColumnHeaderModal
                    setModal={this.setModal}
                    send={this.props.send}
                    columnHeader={this.state.modalInfo.columnHeader}
                    selectedSheetIndex={this.state.selectedSheetIndex} />
            )
            case ModalEnum.Merge: return (
                <MergeModal
                    setModal={this.setModal}
                    sheetJSONArray={this.state.sheetJSONArray}
                    dfNames={this.state.dfNames}
                    send={this.props.send}
                    />
            ) 
            case ModalEnum.Group: return (
                <GroupModal
                    setModal={this.setModal}
                    sheetJSONArray={this.state.sheetJSONArray}
                    dfNames={this.state.dfNames}
                    send={this.props.send}
                    selectedSheetIndex={this.state.selectedSheetIndex}
                    />
            ) 
            case ModalEnum.Filter : return (
                <FilterModal
                    selectedSheetIndex={this.state.selectedSheetIndex}
                    setModal={this.setModal}
                    columnHeader={this.state.modalInfo.columnHeader}
                    columnType={this.state.columnTypeJSONArray[this.state.selectedSheetIndex][this.state.modalInfo.columnHeader]}
                    send={this.props.send}
                    operator={this.state.columnFiltersArray[this.state.selectedSheetIndex][this.state.modalInfo.columnHeader].operator}
                    filters={this.state.columnFiltersArray[this.state.selectedSheetIndex][this.state.modalInfo.columnHeader].filters}
                />
            )
            case ModalEnum.DeleteColumn: return (
                <DeleteColumnModal
                    setModal={this.setModal}
                    send={this.props.send}
                    columnHeader={this.state.modalInfo.columnHeader}
                    selectedSheetIndex={this.state.selectedSheetIndex}
                    />
            )
            case ModalEnum.SaveAnalysis: return (
                <SaveAnalysisModal
                    setModal={this.setModal}
                    send={this.props.send}
                    savedAnalysisNames={this.state.savedAnalysisNames}
                    saveAnalysisName={this.state.modalInfo.saveAnalysisName} />
            )
            case ModalEnum.SaveAnalysisOverwrite: return (
                <SaveAnalysisOverwriteModal
                    setModal={this.setModal}
                    send={this.props.send}
                    savedAnalysisNames={this.state.savedAnalysisNames}
                    saveAnalysisName={this.state.modalInfo.saveAnalysisName} />
            )
            case ModalEnum.ReplayAnalysis: return (
                <ReplayAnalysisModal
                setModal={this.setModal}
                send={this.props.send}
                savedAnalysisNames={this.state.savedAnalysisNames} />
            )
        }
    }

    setModal(modalInfo: ModalInfo) : void {
        // Sets the current modal. We _always_ turn off cell editing mode here, just
        // in case the user opens/closes a modal in cell editing mode.
        this.setEditingMode(false, "", -1);
        // And then we actually update the modalInfo
        this.setState({modalInfo: modalInfo});
    }

    setSelectedSheetIndex(newIndex: number): void {
        // We turn off editing mode, if it is on, because we moved to a new sheet
        this.setEditingMode(false, "", -1);
        // We use the backend to log that we switched sheets
        this.props.send({
            'event': 'log_event',
            'type': 'switch_sheet_log_event',
            'sheet_index': newIndex
        });
        // And then we update the selected index
        this.setState({selectedSheetIndex: newIndex});
    }

    /*
        the ColumnMovedEvent gets fired when a user drags a column to change its location. 
        While dragging the column from one position to another, this event gets fired multiple times. 
        Wh
        en a column is moving, we set the movingColumnParams so we can send a reorder event to the backend
    */ 
    columnMoved(event : ColumnMovedEvent) : void {
        this.setState({
            movingColumnParams: {
                column: event.column?.getColId() ? event.column?.getColId() : '', // make sure type checks
                newIndex: event.toIndex ? event.toIndex : -1 // make sure type checks
            }
        })
    }

    // when the column stops moving, send the column reorder event 
    // to the backend 
    columnDragStopped() : void {

        /* 
            the DragStoppedEvent gets fired when the user changes the width of the column and when 
            the user reorders the column. We only want to send a column_reorder_event when the user is 
            reordering the column, so we check if the user is moving a column by checking this.state.columnMovedState.column
        */
        if (this.state.movingColumnParams != undefined && this.state.movingColumnParams.column !== '') {

            // if the column did not change locations, don't send a column_reorder_event
            if (this.state.sheetJSONArray[this.state.selectedSheetIndex].columns[this.state.movingColumnParams.newIndex - 1] === this.state.movingColumnParams.column) {
                return;
            }
                        
            this.props.send({
                'event': 'edit_event',
                'type': 'reorder_column_edit',
                'sheet_index': this.state.selectedSheetIndex,
                'column_header': this.state.movingColumnParams.column,
                'new_column_index': this.state.movingColumnParams.newIndex - 1 // - 1 to account for the index column
            });

            // log the column reorder event
            window.logger?.track({
                userId: window.user_id,
                event: 'column_reoder_event',
                properties: {
                    column_header: this.state.movingColumnParams.column,
                    new_column_index: this.state.movingColumnParams.newIndex - 1
                }
            });

            // reset the columnMovedState so a column resizing doesn't cause the column_reorder_event to get sent
            this.setState({
                movingColumnParams : undefined
            });
        }
    }


    // eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
    render() {
        return (
            <div className="mito-container">
                <div className="mitosheet">
                    <MitoToolbar 
                        sheetJSON={this.state.sheetJSONArray[this.state.selectedSheetIndex]} 
                        selectedSheetIndex={this.state.selectedSheetIndex}
                        send={this.props.send}
                        setEditingMode={this.setEditingMode}
                        setDocumentation={this.setDocumentation}
                        setModal={this.setModal}
                        model_id={this.props.model_id}
                        selectedColumn={this.state.selectedColumn}
                        />
                    <FormulaBar
                        formulaBarValue={this.state.formulaBarValue}
                        handleFormulaBarDoubleClick={this.handleFormulaBarDoubleClick} 
                    />
                    <MitoSheet 
                        formulaBarValue={this.state.formulaBarValue} 
                        editingColumn={this.state.editingModeState.editingCellColumn}
                        columnSpreadsheetCodeJSON={this.state.columnSpreadsheetCodeJSONArray[this.state.selectedSheetIndex]}
                        sheetJSON={this.state.sheetJSONArray[this.state.selectedSheetIndex]} 
                        columnFiltersJSON={this.state.columnFiltersArray[this.state.selectedSheetIndex]}
                        setEditingMode={this.setEditingMode}
                        setModal={this.setModal}
                        setEditingFormula={this.setEditingFormula}
                        setCursorIndex={this.setCursorIndex}
                        cursorIndex={this.state.editingModeState.formulaCursorIndex}
                        cellFocused={this.cellFocused}
                        columnMoved={this.columnMoved}
                        columnDragStopped={this.columnDragStopped}
                        model_id={this.props.model_id}
                        sendCellValueUpdate={this.sendCellValueUpdate} 
                        />
                    <div className="sheet-tab-bar">
                        {this.state.sheetJSONArray.map((sheetJSON, index) => {
                            // If we can't get the df name, we just call it df{index}!
                            const sheetName = this.state.dfNames[index] ? this.state.dfNames[index] : `df${index + 1}`
                            return (
                                <SheetTab 
                                    key={sheetName}
                                    sheetName={sheetName}
                                    sheetShape={this.state.sheetShapeArray[index]}
                                    sheetIndex={index}
                                    selectedSheetIndex={this.state.selectedSheetIndex}
                                    setSelectedSheetIndex={this.setSelectedSheetIndex} />
                            )
                        })}
                    </div>
                </div>
                {this.getCurrentModalComponent()}
                {this.state.documentationOpen && 
                    <div className="sidebar">
                        <DocumentationSidebarContainer setDocumentation={this.setDocumentation}/>
                    </div>
                }
                {this.state.loading && <LoadingIndicator/>}          
            </div>
        );
    }

}


export default Mito;