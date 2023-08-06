// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { useState } from 'react';

// Import the content this displays
import FunctionDocumentationContent from './FunctionDocumentationContent';
import DocumentationListContent from './DocumentationListContent';
import BasicExampleContainer from './BasicExampleContainer';

// Import css
import "../../../css/default-modal.css"
import "../../../css/margins.css"



type BasicDocumentation = {
    kind: 'basic';
    basicExampleName: string;
}

type FunctionDocumentation = {
    kind: 'function';
    function: string;
}

export type SelectedDocumentation = BasicDocumentation | FunctionDocumentation | undefined;

/*
    This object holds the documentation sidebar, as well as the
    state currently displayed by the documentation. 

    This can either be:
    1. A list of all content (when selectedDocumentation is undefined)
    2. Documentation for a specific function (when typeof selectedDocumentation is FunctionDocumentation)
    3. Documentation for some basic example (when typeof selectedDocumentation is BasicDocumentation)
*/
const DocumentationSidebarContainer = (
    props : {
        setDocumentation: (documentationOpen: boolean) => void;
    }): JSX.Element => {
    const [selectedDocumentation, setSelectedDocumentation] = useState<SelectedDocumentation>(undefined);

    const getSelectedDocumentationContent = () => {
        // Returns the selected documentation, which is either nothing (the list of all documentation), 
        // a basic example, or a specific function.

        if (selectedDocumentation === undefined) {
            return (<DocumentationListContent setSelectedDocumentation={setSelectedDocumentation}/>)
        } else if (selectedDocumentation.kind === 'basic') {
            return <BasicExampleContainer basicExampleName={selectedDocumentation.basicExampleName}/>
        } else if (selectedDocumentation.kind === 'function') {
            return (<FunctionDocumentationContent function={selectedDocumentation.function}/>)
        }
    }

    return (
        <div className='documentation-sidebar-container'>
            <div className='documentation-sidebar-header'>
                {
                    selectedDocumentation === undefined &&
                    <div className='documentation-sidebar-header-title'>
                        Documentation
                    </div>
                }
                {
                    selectedDocumentation !== undefined &&
                    <div className='documentation-sidebar-header-back-and-title'>
                        <div className='documentation-sidebar-header-back' onClick={() => {setSelectedDocumentation(undefined)}}>
                            <svg width="12" height="16" viewBox="0 0 12 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M0.292893 7.29289C-0.0976311 7.68342 -0.0976311 8.31658 0.292893 8.70711L6.65685 15.0711C7.04738 15.4616 7.68054 15.4616 8.07107 15.0711C8.46159 14.6805 8.46159 14.0474 8.07107 13.6569L2.41421 8L8.07107 2.34315C8.46159 1.95262 8.46159 1.31946 8.07107 0.928932C7.68054 0.538408 7.04738 0.538408 6.65685 0.928932L0.292893 7.29289ZM12 7L1 7V9L12 9V7Z" fill="#343434"/>
                            </svg>
                        </div>
                        <div className='documentation-sidebar-header-title'>
                            Documentation
                        </div>
                    </div>
                }
                <div className='documentation-sidebar-header-close' onClick={() => {props.setDocumentation(false)}}>
                    <svg width="22" height="23" viewBox="0 0 22 23" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <line x1="5.91849" y1="6.1967" x2="16.5251" y2="16.8033" stroke="#343434" strokeWidth="2"/>
                        <line x1="5.91852" y1="16.8033" x2="16.5251" y2="6.19671" stroke="#343434" strokeWidth="2"/>
                    </svg>
                </div>
            </div>
            <div className='documentation-sidebar-content'>
                {getSelectedDocumentationContent()}
            </div>
        </div>
    )
};

export default DocumentationSidebarContainer;