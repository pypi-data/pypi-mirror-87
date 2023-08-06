// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';

import '../../../css/documentation-sidebar.css';

const listIcon = (
    <svg width="16" height="18" viewBox="0 0 16 18" fill="none" xmlns="http://www.w3.org/2000/svg">
        <mask id="path-1-inside-1" fill="white">
        <rect width="16" height="18" rx="1"/>
        </mask>
        <rect width="16" height="18" rx="1" stroke="#0081DE" strokeWidth="2.4" mask="url(#path-1-inside-1)"/>
        <line x1="2" y1="3.2" x2="14" y2="3.2" stroke="#0081DE" strokeWidth="1.2"/>
        <line x1="2" y1="7" x2="14" y2="7" stroke="#0081DE" strokeWidth="1.2"/>
        <line x1="2" y1="10.8" x2="14" y2="10.8" stroke="#0081DE" strokeWidth="1.2"/>
        <line x1="2" y1="14.6" x2="14" y2="14.6" stroke="#0081DE" strokeWidth="1.2"/>
    </svg>
)

import { SelectedDocumentation } from './DocumentationSidebarContainer';
import { functionDocumentationObjects } from '../../data/function_documentation';
import { basicExamples } from './BasicExampleContainer';


/*
    This documentation sidebar content displays a list of all 
    documentation entries users can select. 

    These are either:
    1. Basic examples (e.g. how to write a formula)
    2. Function documentations
*/
const DocumentationListContent = (
    props: {
        setSelectedDocumentation: React.Dispatch<React.SetStateAction<SelectedDocumentation>>
    }): JSX.Element => {

    const basicExamplesList = basicExamples.map((basicExample) => {
        return (
            <li 
                className='documentation-sidebar-content-function-list-element'
                key={basicExample.basicExampleName} 
                onClick={() => {props.setSelectedDocumentation({
                    kind: 'basic',
                    basicExampleName: basicExample.basicExampleName
                })}}>
                <div className='documentation-sidebar-content-function-list-icon'>
                    {listIcon}
                </div>
                {basicExample.basicExampleName}
            </li>
        )
    })

    const functionNameList = functionDocumentationObjects.map((funcDocObject) => {
        return (
            <li 
                className='documentation-sidebar-content-function-list-element'
                key={funcDocObject.function} 
                onClick={() => {props.setSelectedDocumentation({
                    kind: 'function',
                    function: funcDocObject.function
                })}}>
                <div className='documentation-sidebar-content-function-list-icon'>
                    {listIcon}
                </div>
                {funcDocObject.function}
            </li>
        )
    })

    return (
        <React.Fragment>
            <div className='documentation-sidebar-content-function-list-title'>
                Basic Examples
            </div>
            <ul className='documentation-sidebar-content-function-list'>
                {basicExamplesList}
            </ul>
            <div className='documentation-sidebar-content-function-list-section-title'>
                Functions
            </div>
            <ul className='documentation-sidebar-content-function-list'>
                {functionNameList}
            </ul>
        </React.Fragment>
    ) 
};

export default DocumentationListContent;