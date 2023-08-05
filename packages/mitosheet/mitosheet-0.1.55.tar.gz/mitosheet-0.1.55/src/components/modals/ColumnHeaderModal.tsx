// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { Fragment, useState } from 'react';
import { ModalEnum, ModalInfo } from '../Mito';
import DefaultModal from '../DefaultModal';

// import css
import "../../../css/margins.css";
import "../../../css/column-header-modal.css";


const isFullyNumeric = (s: string) : boolean => {
    // Returns true if the given string is a number
    for (let i = 0; i < s.length; i++) {
        const c = s.charAt(i);
        if (c < '0' || c > '9') {
            return false;
        }
    }
    return true;
}

export const isValidHeader = (columnHeader: string) : boolean => {
    // To be a valid header:
    // 1. Matches the regex [A-z0-9_]+ (just once, the entire string)
    // 2. Is not all digits (aka cannot be mistake for a number)

    // Check (1)
    const re = /[A-z0-9_]+/;
    const matches = re.exec(columnHeader);
    if (matches === null || matches.length != 1 || matches[0] !== columnHeader) {
        return false;
    }

    // Check (2) (all digits)
    return !isFullyNumeric(columnHeader);
}  

const getHeaderErrorMessage = (columnHeader: string): string => {
    /* 
        Given a column header, returns a message about _how_ that columnHeader is invalid, 
        where it can detect three cases currently:
        1. The column header includes whitespace.
        2. The column header includes _only_ numbers.
        3. The column header includes a "-". 
        4. A catch-all: the column header is invalid in other ways.

        Note: We can expand these as we see users make more invalid column headers
        and see what types of errors are common!

        If the columnHeader is valid returns the empty string. 
    
    */
    if (isValidHeader(columnHeader) || columnHeader.length === 0) {
        return '';
    }

    // Check for whitespace
    if (columnHeader.indexOf(' ') >= 0) {
        return `Invalid column name. Please remove all spaces.`
    }

    // Check if it's got a -
    if (columnHeader.indexOf('-') >= 0) {
        return `Invalid column name. Try switching "-" for "_".`
    }

    // Check if it's only numbers
    if (isFullyNumeric(columnHeader)) {
        return `Invalid column name. Add at least one non-digit.`
    }

    // Catch the rest... :( )
    return 'Invalid column name. All characters must be letters, digits, and "_".';
}


/*
    A modal that allows a user to enter a new name for a given
    column.
*/
const ColumnHeaderModal = (
    props : {
        setModal: (modalInfo: ModalInfo) => void,
        columnHeader: string,
        send: (msg: Record<string, unknown>) => void,
        selectedSheetIndex: number
    }): JSX.Element => {
    const [columnHeader, setColumnHeader] = useState('');
    const [invalidInputError, setInvalidInputError] = useState('');

    const onChange = (e: React.ChangeEvent<HTMLInputElement>) : void => {
        const newColumnHeader = e.target.value;
        // Update the saved columnHeader
        setColumnHeader(newColumnHeader);
        // Display an error message, if it has one
        setInvalidInputError(getHeaderErrorMessage(newColumnHeader));
    }

    const changeColumnHeader = () : void => {
        if (!isValidHeader(columnHeader)) {
            // We make sure the new column header is a valid mito column,
            // and we don't allow the user to submit if it's not! 
            // We also update the error to tell them to fix the issue.
            setInvalidInputError(
                `Please fix issues before submitting: ${getHeaderErrorMessage(columnHeader)}`
            );

            return;
        }

        props.send({
            'event': 'edit_event',
            'type': 'rename_column_edit',
            'sheet_index': props.selectedSheetIndex,
            'old_column_header': props.columnHeader,
            'new_column_header': columnHeader
        })

        props.setModal({type: ModalEnum.None});
    }

    return (
        <DefaultModal
            header={`Change Column Name: ${props.columnHeader}`}
            modalType={ModalEnum.RepeatAnalysis}
            viewComponent= {
                <Fragment>
                    <div className="mt-2">
                        <input 
                            className="modal-input column-header-input"
                            type="text" 
                            placeholder='column_header' 
                            value={columnHeader} 
                            onChange={onChange} 
                            autoFocus
                        />
                        {invalidInputError !== '' && 
                            <p className='column-header-error'>
                                {invalidInputError}
                            </p>
                        }
                    </div>
                </Fragment>
            }
            buttons = {
                <Fragment>
                    <div className='modal-close-button modal-dual-button-left' onClick={() => {props.setModal({type: ModalEnum.None})}}> Close </div>
                    <div className='modal-action-button modal-dual-button-right' onClick={changeColumnHeader}> {"Change Column Name"}</div>
                </Fragment>
            }
        />
    );
};

export default ColumnHeaderModal;