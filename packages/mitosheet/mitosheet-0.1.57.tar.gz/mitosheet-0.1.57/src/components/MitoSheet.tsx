// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';
import {AgGridReact} from 'ag-grid-react';
import { 
    CellValueChangedEvent, 
    CellFocusedEvent, 
    GridReadyEvent, 
    SuppressKeyboardEventParams,
    GridColumnsChangedEvent,
    ColumnMovedEvent
} from 'ag-grid-community';
import 'ag-grid-community/dist/styles/ag-grid.css';
import 'ag-grid-community/dist/styles/ag-theme-alpine.css';
import '../../css/mitosheet.css';
import MitoCellEditor from './MitoCellEditor';

import { TAKE_SUGGESTION_KEYS, ARROW_UP_KEYS, ARROW_DOWN_KEYS } from './MitoCellEditor';

// And functions for building components
import { buildGridData, buildGridColumns } from '../utils/gridData';

// Import types
import { SheetJSON } from '../widget';
import { ModalInfo, ColumnSpreadsheetCodeJSON, SheetColumnFilterMap } from './Mito';
import { calculateAndSetHeaderHeight, headerHeightParams } from '../utils/gridStyling';
    
const MitoSheet = (props: {
    sheetJSON: SheetJSON; 
    formulaBarValue: string;
    editingColumn: string;
    columnSpreadsheetCodeJSON: ColumnSpreadsheetCodeJSON;
    columnFiltersJSON: SheetColumnFilterMap;
    sendCellValueUpdate: (column : string, newValue : string) => void; 
    setEditingMode: (on: boolean, column: string, rowIndex: number) => void;
    setModal: (modal: ModalInfo) => void;
    setEditingFormula: (formula: string) => void;
    setCursorIndex: (index: number) => void;
    cursorIndex: number;
    cellFocused: (event: CellFocusedEvent) => void;
    columnMoved: (event: ColumnMovedEvent) => void;
    columnDragStopped: () => void;
    model_id: string;
}): JSX.Element => {
    
    function onGridReady(params: GridReadyEvent) {
        if (window.gridApiMap === undefined) {
            window.gridApiMap = new Map();
        }
        window.gridApiMap.set(props.model_id, params.api);

        calculateAndSetHeaderHeight(props.model_id);
    }

    function onGridColumnsChanged(params: GridColumnsChangedEvent) {
        /* 
            Ag-grid does some sort of caching that means if we rename a column
            it will treat this as a new column that got added to the _end_.

            This function runs whenever the columns change. 
            
            It makes sure that the columns are in the correct order. If they aren't,
            it then places them in the correct order.
        */

        const columnState = params.columnApi.getColumnState();
        const correctColumnOrder = props.sheetJSON.columns;

        for (let i = 0; i < correctColumnOrder.length; i++) {
            const columnName = correctColumnOrder[i].toString();

            // If, ignoring the index column, this column is not in the right place, then
            // we have some reordering to do!
            const correctIndex = i + 1;
            const currentDisplayIndex = columnState.findIndex((columnState) => {
                return columnState.colId === columnName;
            })

            if (correctIndex !== currentDisplayIndex) {
                params.columnApi.moveColumn(columnName, correctIndex);
            }
        }
    }

    const cellValueChanged = (e : CellValueChangedEvent) => {
        const column = e.colDef.field ? e.colDef.field : "";
        const newValue = e.newValue;
        
        props.sendCellValueUpdate(column, newValue);
    };

    const columns = buildGridColumns(
        props.sheetJSON.columns, 
        props.columnSpreadsheetCodeJSON, 
        props.columnFiltersJSON,
        props.formulaBarValue,
        props.editingColumn,
        props.cursorIndex,
        props.setEditingMode, 
        props.setEditingFormula,
        props.setCursorIndex,
        props.setModal
    );
    const rowData = buildGridData(props.sheetJSON);

    const frameworkComponents = {
        simpleEditor: MitoCellEditor,
    }

    return (
        <div>
            <div className="ag-theme-alpine ag-grid"> 
                <AgGridReact
                    onGridReady={onGridReady}
                    onGridColumnsChanged={onGridColumnsChanged}
                    onCellFocused={(e : CellFocusedEvent) => props.cellFocused(e)}
                    onColumnMoved={(e: ColumnMovedEvent) => props.columnMoved(e)}
                    onDragStopped={() => props.columnDragStopped()}
                    rowData={rowData}
                    headerHeight={headerHeightParams.defaultHeaderHeight}
                    frameworkComponents={frameworkComponents}
                    suppressKeyboardEvent={(params: SuppressKeyboardEventParams) => {
                        /* 
                            While we're editing a cell, we suppress events that we use
                            to do things within the editor.

                            NOTE: this function should suppress the events matched in onKeyDown
                            in MitoCellEditor!
                        */

                        if (!params.editing) {
                            return false;
                        }
                        return TAKE_SUGGESTION_KEYS.includes(params.event.key) ||
                               ARROW_UP_KEYS.includes(params.event.key) ||
                              ARROW_DOWN_KEYS.includes(params.event.key);
                    }}
                    onCellValueChanged={cellValueChanged}
                    suppressDragLeaveHidesColumns={true}
                    suppressColumnMoveAnimation={true} >
                    {columns}
                </AgGridReact>
            </div>
        </div>
    );
};

export default MitoSheet;