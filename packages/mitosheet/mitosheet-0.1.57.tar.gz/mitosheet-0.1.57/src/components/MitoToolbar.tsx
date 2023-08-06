// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';

// Import CSS
import "../../css/mito-toolbar.css"
import "../../css/margins.css"


// Import Types
import { SheetJSON } from '../widget';
import { ModalInfo, ModalEnum } from './Mito';

// Import Components 
import Tooltip from './Tooltip';

const MitoToolbar = (
    props: {
        sheetJSON: SheetJSON, 
        selectedSheetIndex: number,
        send: (msg: Record<string, unknown>) => void,
        setEditingMode: (on: boolean, column: string, rowIndex: number) => void,
        setDocumentation: (documentationOpen: boolean) => void,
        setModal: (modal: ModalInfo) => void,
        model_id: string,
        selectedColumn: string
    }): JSX.Element => {

    /* Adds a new column onto the end of a sheet, with A, B, C... as the name */
    const addColumn = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        const newColumn = String.fromCharCode(65 + props.sheetJSON.columns.length);
        // Log the new column creation
        window.logger?.track({
            userId: window.user_id,
            event: 'button_column_added_log_event',
            properties: {
                column_header: newColumn
            }
        })
        // TODO: have to update these timestamps, etc to be legit
        props.send({
            'event': 'edit_event',
            'type': 'add_column_edit',
            'sheet_index': props.selectedSheetIndex,
            'column_header': newColumn
        })
    }


    /* Undoes the last step that was created */
    const undo = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        // Log the new column creation
        window.logger?.track({
            userId: window.user_id,
            event: 'undo_log_event',
            properties: {}
        })
        // TODO: have to update these timestamps, etc to be legit
        props.send({
            'event': 'update_event',
            'type': 'undo'
        })
    }

    /* Saves the current file as as an exported analysis */
    const downloadAnalysis = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        // Send a log message to the backend
        props.send({
            'event': 'log_event',
            'type': 'button_download_log_event'
        })
        // And log with segment
        window.logger?.track({
            userId: window.user_id,
            event: 'button_download_log_event',
            properties: {}
        })
        // We export using the gridApi.
        window.gridApiMap?.get(props.model_id)?.exportDataAsCsv({
            fileName: 'mito-export'
        });
        props.setModal({type: ModalEnum.Download});
    }

    const openDocumentation = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        // Send a log message to the backend
        props.send({
            'event': 'log_event',
            'type': 'button_documentation_log_event'
        })

        // We log the opening of the repeat documentation sidebar
        window.logger?.track({
            userId: window.user_id,
            event: 'button_documentation_log_event',
            properties: {
                stage: 'opened'
            }
        });
        props.setDocumentation(true);
    }

    const openMerge = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        props.setModal({type: ModalEnum.Merge});
    }

    const openGroup = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        props.setModal({type: ModalEnum.Group});
    }

    const openDeleteColumn = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        props.setModal({type: ModalEnum.DeleteColumn, columnHeader: props.selectedColumn});
    }

    const openSave = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        props.setModal({type: ModalEnum.SaveAnalysis});
    }

    const openReplay = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);
        
        props.setModal({type: ModalEnum.ReplayAnalysis});
    }

    return (
        <div className='mito-toolbar-container'>
            <div className='mito-toolbar-container-left'>
                    <button className='mito-toolbar-item vertical-align-content' onClick={undo}>
                        <svg width="24" height="10" viewBox="0 0 12 5" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M0.802595 2.66537C0.719857 2.77576 0.741164 2.93409 0.850186 3.01899C0.959208 3.10389 1.11466 3.08322 1.1974 2.97283L0.802595 2.66537ZM2.54776 0.753934L2.67568 0.538802C2.56722 0.47157 2.42691 0.498052 2.35035 0.600204L2.54776 0.753934ZM4.73383 2.4034C4.85105 2.47605 5.00334 2.43863 5.074 2.31982C5.14465 2.20101 5.1069 2.04579 4.98968 1.97313L4.73383 2.4034ZM1.1974 2.97283L2.74516 0.907664L2.35035 0.600204L0.802595 2.66537L1.1974 2.97283ZM2.41983 0.969067L4.73383 2.4034L4.98968 1.97313L2.67568 0.538802L2.41983 0.969067Z" fill="#343434"/>
                            <path d="M11.5 0C11.5 2.41714 9.03395 4.37659 6.60866 4.37659C4.64237 4.37659 3.05958 2.77564 2.5 1" stroke="#343434" strokeWidth="0.6"/>
                        </svg>
                        {/* Extra styling to make sure the tooltip doesn't float off the screen*/}
                        <Tooltip tooltip={"Undo"} style={{'marginLeft': '-15px'}}/>
                    </button>
                    <div className="vertical-line mt-1"></div>
                    <button className='mito-toolbar-item vertical-align-content' onClick={addColumn}>
                        <svg width="22" height="30" viewBox="0 0 8 12" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M6.45456 1V2.81818" stroke="#343434" strokeWidth="0.6" strokeLinecap="round"/>
                            <path d="M7.36365 1.90909L5.54547 1.90909" stroke="#343434" strokeWidth="0.6" strokeLinecap="round"/>
                            <path d="M6.45455 4.18182V6.90909V10.5455C6.45455 10.7965 6.25104 11 6 11H1.45455C1.20351 11 1 10.7965 1 10.5455V1.45455C1 1.20351 1.20351 1 1.45455 1H4.8961" stroke="#343434" strokeWidth="0.6"/>
                            <rect x="1" y="4.63635" width="5.45455" height="3.63636" fill="#343434" fillOpacity="0.19"/>
                        </svg>
                        <Tooltip tooltip={"Add Column"}/>
                    </button>
                    <button className='mito-toolbar-item vertical-align-content' onClick={openDeleteColumn}>
                        <svg width="20" height="28" viewBox="0 0 7 11" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M5.99142 10.75H1.0641C0.956936 10.75 0.867939 10.6673 0.860102 10.5604L0.285102 2.7195C0.276409 2.60096 0.370239 2.5 0.489099 2.5H6.51414C6.63246 2.5 6.72611 2.60009 6.71823 2.71815L6.19551 10.5591C6.18834 10.6665 6.0991 10.75 5.99142 10.75Z" stroke="#343434" strokeWidth="0.6"/>
                            <path d="M1.60416 2.41164V1.375V0.733332H5.45416V2.41165" stroke="#343434" strokeWidth="0.6" strokeLinecap="round" strokeLinejoin="round"/>
                            <path d="M2.56668 4.58334L2.5666 8.43335" stroke="#343434" strokeWidth="0.6" strokeLinecap="round" strokeLinejoin="round"/>
                            <path d="M4.49167 4.58334L4.49158 8.43335" stroke="#343434" strokeWidth="0.6" strokeLinecap="round" strokeLinejoin="round"/>
                        </svg>
                        <Tooltip tooltip={"Delete Column"}/>
                    </button>
                    <div className="vertical-line mt-1"></div>
                    <button className='mito-toolbar-item' onClick={openGroup}>
                    <svg width="30" height="30" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <rect x="1.25" y="8.25" width="5.5" height="5.5" rx="0.75" stroke="#343434" strokeWidth="0.6"/>
                        <rect x="1.25" y="1.25" width="5.5" height="5.5" rx="0.75" stroke="#343434" strokeWidth="0.6"/>
                        <rect x="8.25" y="8.25" width="5.5" height="5.5" rx="0.75" stroke="#343434" strokeWidth="0.6"/>
                        <rect x="8.25" y="1.25" width="5.5" height="5.5" rx="0.75" stroke="#343434" strokeWidth="0.6"/>
                        <circle cx="3" cy="3" r="1" fill="#343434"/>
                        <circle cx="5" cy="5" r="1" fill="#343434"/>
                        <path d="M9.49994 2.49992L9.49992 5.5M12.5 2.5L12.4999 5.50008M10.9999 2.50014L10.9999 5.50022" stroke="#343434" strokeWidth="0.6"/>
                        <path d="M5.63898 9.5L2.32331 9.5M5.63901 12.3181L3.97868 12.3182L2.31834 12.3183M5.63898 10.8809L2.31834 10.8809" stroke="#343434" strokeWidth="0.6"/>
                    </svg>
                        <Tooltip tooltip={"Group"}/>
                    </button>
                    <button className='mito-toolbar-item' onClick={openMerge}>
                        <svg width="40" height="30" viewBox="0 0 17 11" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M11.6467 5.12789C11.6467 7.78833 9.13157 10.0058 5.94835 10.0058C2.76513 10.0058 0.25 7.78833 0.25 5.12789C0.25 2.46744 2.76513 0.25 5.94835 0.25C9.13157 0.25 11.6467 2.46744 11.6467 5.12789Z" fill="#C8C8C8" stroke="#343434" strokeWidth="0.6"/>
                            <path d="M16.4784 5.12789C16.4784 7.78833 13.9632 10.0058 10.78 10.0058C7.59679 10.0058 5.08167 7.78833 5.08167 5.12789C5.08167 2.46744 7.59679 0.25 10.78 0.25C13.9632 0.25 16.4784 2.46744 16.4784 5.12789Z" stroke="#343434" strokeWidth="0.6"/>
                        </svg>
                        <Tooltip tooltip={"Merge"}/>
                    </button>
                    <div className="vertical-line mt-1"></div>
                    <button className='mito-toolbar-item' onClick={openSave}>
                        <svg width="25" height="25" viewBox="0 0 10 11" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M8 10.75H2C1.0335 10.75 0.25 9.9665 0.25 9V2C0.25 1.0335 1.0335 0.25 2 0.25H5.40054C5.81012 0.25 6.20673 0.393662 6.52129 0.655968L9.12075 2.82358C9.51948 3.15607 9.75 3.64844 9.75 4.16761V9C9.75 9.9665 8.9665 10.75 8 10.75Z" stroke="#343434" strokeWidth="0.6"/>
                            <rect x="2.12503" y="6.05005" width="5.875" height="0.75" fill="#343434"/>
                            <rect x="4.375" y="2.88745" width="2.8875" height="0.75" transform="rotate(-90 4.375 2.88745)" fill="#343434"/>
                            <rect x="2.12503" y="8.11255" width="5.875" height="0.75" fill="#343434"/>
                        </svg>
                        <Tooltip tooltip={"Save"}/>
                    </button>
                    <button className='mito-toolbar-item' onClick={openReplay}>
                        <svg width="30" height="30" viewBox="0 0 14 11" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M0.799219 8.65346C0.713311 8.76181 0.733559 8.91606 0.844444 8.99798C0.955329 9.07989 1.11486 9.05846 1.20077 8.95011L0.799219 8.65346ZM2.65464 6.71478L2.788 6.50394C2.6775 6.4392 2.53338 6.46616 2.45387 6.56645L2.65464 6.71478ZM4.9951 8.37511C5.11448 8.44506 5.27096 8.40737 5.34461 8.29093C5.41825 8.17449 5.38118 8.02339 5.2618 7.95344L4.9951 8.37511ZM1.20077 8.95011L2.85542 6.8631L2.45387 6.56645L0.799219 8.65346L1.20077 8.95011ZM2.52129 6.92561L4.9951 8.37511L5.2618 7.95344L2.788 6.50394L2.52129 6.92561Z" fill="#343434"/>
                            <path d="M11.6906 5.95284C11.6906 8.39554 9.58876 10.3757 6.99598 10.3757C4.89389 10.3757 3.09822 8.79442 2.5 7" stroke="#343434" strokeWidth="0.6"/>
                            <path d="M13.2008 2.80751C13.2867 2.69916 13.2664 2.54491 13.1556 2.46299C13.0447 2.38107 12.8851 2.40251 12.7992 2.51086L13.2008 2.80751ZM11.3454 4.74619L11.212 4.95702C11.3225 5.02177 11.4666 4.99481 11.5461 4.89451L11.3454 4.74619ZM9.0049 3.08586C8.88552 3.01591 8.72904 3.0536 8.65539 3.17004C8.58175 3.28648 8.61882 3.43758 8.7382 3.50753L9.0049 3.08586ZM12.7992 2.51086L11.1446 4.59786L11.5461 4.89451L13.2008 2.80751L12.7992 2.51086ZM11.4787 4.53535L9.0049 3.08586L8.7382 3.50753L11.212 4.95702L11.4787 4.53535Z" fill="#343434"/>
                            <path d="M2.30938 5.5081C2.30938 3.0654 4.41124 1.08521 7.00402 1.08521C9.10611 1.08521 10.9018 2.70558 11.5 4.5" stroke="#343434" strokeWidth="0.6"/>
                        </svg>
                        <Tooltip tooltip={"Repeat Saved Analysis"}/>
                    </button>
                    <button className='mito-toolbar-item vertical-align-content' onClick={downloadAnalysis}>
                        <svg width="23.5" height="27" viewBox="0 0 11 12" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M1 8V9.5V11H10V8" stroke="#343434" strokeWidth="0.6" strokeLinecap="round" strokeLinejoin="round"/>
                            <path d="M5.51321 7.75887V0.999992" stroke="#343434" strokeWidth="0.6" strokeLinecap="round"/>
                            <path d="M8.83495 4.94249C8.93049 4.84281 8.92714 4.68456 8.82747 4.58901C8.72779 4.49347 8.56953 4.49682 8.47399 4.5965L8.83495 4.94249ZM5.55788 8.00002L5.37987 8.17556C5.42729 8.22364 5.49213 8.25049 5.55965 8.25001C5.62717 8.24953 5.69163 8.22176 5.73836 8.17301L5.55788 8.00002ZM2.54999 4.59395C2.45304 4.49564 2.29475 4.49454 2.19644 4.59149C2.09814 4.68844 2.09704 4.84673 2.19399 4.94503L2.54999 4.59395ZM8.47399 4.5965L5.3774 7.82702L5.73836 8.17301L8.83495 4.94249L8.47399 4.5965ZM5.73588 7.82447L2.54999 4.59395L2.19399 4.94503L5.37987 8.17556L5.73588 7.82447Z" fill="#343434"/>
                        </svg>
                        <Tooltip tooltip={"Download Sheet"}/>
                    </button>
                    {/* add className mito-toolbar-item to a div below to add another toolbar item! */}
            </div>
            <div className='mito-toolbar-container-right mr-1'>
                <button className='mito-toolbar-item' onClick={openDocumentation}>
                    <svg width="25" height="25" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="7" cy="7" r="6.75" stroke="#404040" strokeWidth="0.6"/>
                        <path d="M7.27173 8.43865C7.2624 8.34531 7.2624 8.30798 7.2624 8.26131C7.2624 7.89731 7.38373 7.56131 7.67307 7.36531L8.1024 7.07598C8.64373 6.71198 9.0544 6.19865 9.0544 5.45198C9.0544 4.49998 8.31707 3.57598 7.0104 3.57598C5.57307 3.57598 4.94773 4.63065 4.94773 5.48931C4.94773 5.65731 4.9664 5.80665 5.00373 5.93731L5.90907 6.04931C5.87173 5.94665 5.84373 5.75065 5.84373 5.59198C5.84373 5.00398 6.1984 4.39731 7.0104 4.39731C7.75707 4.39731 8.12107 4.91065 8.12107 5.46131C8.12107 5.82531 7.94373 6.16131 7.6264 6.37598L7.21573 6.65598C6.66507 7.02931 6.44107 7.49598 6.44107 8.11198C6.44107 8.23331 6.44107 8.32665 6.4504 8.43865H7.27173ZM6.24507 9.77331C6.24507 10.1093 6.51573 10.38 6.85173 10.38C7.18773 10.38 7.46773 10.1093 7.46773 9.77331C7.46773 9.43731 7.18773 9.15731 6.85173 9.15731C6.51573 9.15731 6.24507 9.43731 6.24507 9.77331Z" fill="#343434"/>
                    </svg>
                    {/* Extra styling to make sure the documentation tooltip doesn't float off the screen*/}
                    <Tooltip tooltip={"Documentation"} style={{'marginLeft': '-80.5px'}}/>
                </button>
            </div>
        </div>
    );
};

export default MitoToolbar;