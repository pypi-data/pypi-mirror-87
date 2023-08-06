// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { Fragment } from 'react';
import { ModalEnum, ModalInfo } from '../Mito';
import DefaultModal from '../DefaultModal';


// import css
import "../../../css/save-analysis-modal.css"

type SaveAnalysisOverwriteProps = {
    setModal: (modalInfo: ModalInfo) => void;
    send: (msg: Record<string, unknown>) => void,
    savedAnalysisNames: string[];
    saveAnalysisName: string;
};


/* 
  A modal that appears if a user tries to overwrite a saved analysis,
  prompting them they want to overwrite it. 
*/
const SaveAnalysisOverwriteModal = (props: SaveAnalysisOverwriteProps): JSX.Element => {

    const clickBack = () => {
        props.setModal({
            type: ModalEnum.SaveAnalysis, 
            saveAnalysisName: props.saveAnalysisName
        })
    }

    const clickOverwrite = () => {
        window.logger?.track({
            userId: window.user_id,
            event: 'button_save_analysis_log_event',
            properties: {
                analysis_name: props.saveAnalysisName
            }
        })

        props.send({
            'event': 'update_event',
            'type': 'save_analysis',
            'analysis_name': props.saveAnalysisName
        });

        props.setModal({type: ModalEnum.None});
    }

    return (
        <DefaultModal
        header={`There is already an analysis called ${props.saveAnalysisName}`}
        modalType={ModalEnum.ReplayAnalysis}
        viewComponent= {
            <Fragment>
                <p>
                    Saving this analysis will overwrite your existing analysis. Are you sure you want to continue?
                </p>
            </Fragment>
        }
        buttons = {
            <Fragment>
                <div className='modal-close-button modal-dual-button-left' onClick={clickBack}> Back </div>
                <div className='modal-action-button modal-dual-button-right' onClick={clickOverwrite}> Overwrite</div>
            </Fragment>
        }
    />
    )
} 

export default SaveAnalysisOverwriteModal;