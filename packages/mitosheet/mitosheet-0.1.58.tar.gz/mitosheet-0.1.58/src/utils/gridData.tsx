// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';
import { AgGridColumn } from 'ag-grid-react';
import { SheetJSON } from '../widget';
import ColumnHeader from '../components/ColumnHeader';
import { ModalInfo, ColumnSpreadsheetCodeJSON, SheetColumnFilterMap } from '../components/Mito';

interface RowDict<T> {
    [Key: string]: T;
}

export const MITO_INDEX = 'mito_index';

// convert json formatted data frame into Ag-Grid data structure 
export function buildGridData(sheet_json : SheetJSON) : RowDict<string>[] {
    const gridData = [];
    const columns = sheet_json.columns;

    // iterate through the data frame to get each row
    for (let i = 0; i < sheet_json.data.length; i++) {
        const rowDict : RowDict<string> = {};
        // set the index column of the Ag-Grid
        rowDict[MITO_INDEX] = `${i + 1}`;
        // iterate through the column to get each element
        for (let j = 0; j < sheet_json.data[i].length; j++) {
            // create dict entry for row
            const rowDictKey = columns[j];
            rowDict[rowDictKey] = sheet_json.data[i][j];
        }
        gridData.push(rowDict);
    }
    return gridData;
}


// create columns from data frame columns
export function buildGridColumns(
        df_columns : (string|number)[], 
        columnSpreadsheetCodeJSON : ColumnSpreadsheetCodeJSON, 
        columnFiltersJSON : SheetColumnFilterMap,
        formulaBarValue: string,
        editingColumn: string,
        editingColumnCursorIndex: number,
        setEditingMode : (on: boolean, column: string, rowIndex: number) => void,
        setEditingFormula: (formula: string) => void,
        setCursorIndex: (index: number) => void,
        setModal: (modalInfo: ModalInfo) => void
    ) : JSX.Element[] {
    const gridColumns = [];
    
    // create index column
    gridColumns.push(
        <AgGridColumn 
            key={MITO_INDEX} 
            headerName={''} 
            resizable={true} 
            field={MITO_INDEX} 
            width={10} 
            lockPosition={true}
        />
    );

    // iterate through columns of df_columns to create Ag-Grid columns
    df_columns.forEach((columnHeader : string|number)  => {
        const headerName = columnHeader.toString();
        
        // only allow formula columns to be editable 
        const isEditable = columnSpreadsheetCodeJSON[headerName] !== '';

        /*
            if the column is the selected column:
                1. set the formula to the formula bar value to make sure that if the user has been editing the formula before ending 
                cell editing mode, the most recent formula is used. 
                2. set the cursor index to the last index the user was editing at
        */
        let columnFormula = columnSpreadsheetCodeJSON[headerName]
        let cursorIndex = columnFormula.length
        if (headerName === editingColumn) {
            columnFormula = formulaBarValue
            cursorIndex = editingColumnCursorIndex
        }

        gridColumns.push(
            <AgGridColumn 
                key={headerName} 
                field={headerName} 
                headerName={headerName}
                headerComponentFramework={ColumnHeader}
                resizable={true}
                headerComponentParams={{ 
                    setModal: setModal,
                    displayName: headerName,
                    filters: columnFiltersJSON[headerName].filters
                }}
                cellEditor='simpleEditor'
                cellEditorParams={{
                    formula: columnFormula,
                    setEditingMode: setEditingMode,
                    setEditingFormula: setEditingFormula,
                    setCursorIndex: setCursorIndex,
                    cursorIndex: cursorIndex,
                    columns: df_columns
                }}
                editable={isEditable} 
                width={125}
            />
        );
    });

    return gridColumns;
}