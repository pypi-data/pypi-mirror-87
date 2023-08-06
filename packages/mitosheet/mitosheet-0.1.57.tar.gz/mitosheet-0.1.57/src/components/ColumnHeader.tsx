// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';
import { ModalEnum, ModalInfo } from './Mito';
import { FiltersTypes } from './modals/FilterModal'

import '../../css/column-header.css';
import '../../css/margins.css';
import { getHeaderWords } from '../utils/gridStyling';

/* 
  A custom component that AG-Grid displays for the column
  header, that we extend to open the column header popup when clicked.
*/
const ColumnHeader = (props: {
    setModal: (modal: ModalInfo) => void;
    filters: FiltersTypes
    displayName: string;
  }): JSX.Element => {

    /*
      we split each word of the header (separated by _) into its own span element, adding the _ to 
      the latter half of the split. ie: first_name -> [first, _name]
      This lets us wrap the column headers without breaking words in half, which we would
      do if we just used a fix length cutoff for each row as the cutoff.

      Note: this behaves better when the header's words are <10 characters, but worse when
      the header's words are > 10 characters. The 10 number is decided by the default column width
    */
    const wordsSpans: JSX.Element[] = getHeaderWords(props.displayName).map(word => {
      // give the span a random key. we don't use the word because there may be duplicates
      return (<span key={Math.random()}>{word}</span>)
    });

    return (
      <div className='column-header-cell'>
        <div className='column-header-header-container'>
          <div 
            onClick={() => {props.setModal({type: ModalEnum.ColumnHeader, columnHeader: props.displayName})}} 
            className="column-header-column-header mr-1"
            >
              {wordsSpans}
          </div>
        </div>
        <div className='column-header-filter-container'>
          <div className='column-header-filter-button'
              onClick={() => {props.setModal({ 
                type: ModalEnum.Filter, 
                columnHeader: props.displayName
               })
          }}>
            {props.filters.length === 0 && 
              <svg width="13" height="10" viewBox="0 0 9 7" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M3.63486 6.75C3.49679 6.75 3.38486 6.63807 3.38486 6.5V4.18709C3.38486 4.00613 3.31943 3.83127 3.20064 3.69476L0.781003 0.91411C0.640219 0.75232 0.755131 0.5 0.969598 0.5L8.30011 0.5C8.51458 0.5 8.62949 0.75232 8.48871 0.91411L6.06907 3.69476C5.95028 3.83127 5.88486 4.00613 5.88486 4.18709L5.88486 6.5C5.88486 6.63807 5.77293 6.75 5.63486 6.75H3.63486Z" stroke="#343434" strokeWidth="0.5" />
              </svg> 
            }
            {props.filters.length !== 0 && 
              <svg width="13" height="10" viewBox="0 0 9 7" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M3.63481 6.75C3.49674 6.75 3.38481 6.63807 3.38481 6.5V4.18709C3.38481 4.00613 3.31939 3.83127 3.2006 3.69476L0.780957 0.91411C0.640173 0.75232 0.755085 0.5 0.969552 0.5L8.30007 0.5C8.51453 0.5 8.62945 0.75232 8.48866 0.91411L6.06903 3.69476C5.95024 3.83127 5.88481 4.00613 5.88481 4.18709L5.88481 6.5C5.88481 6.63807 5.77288 6.75 5.63481 6.75H3.63481Z" fill="#0081DE" stroke="#343434" strokeWidth="0.5"/>
              </svg>
            }
          </div>
        </div>
      </div>      
    )
} 

export default ColumnHeader