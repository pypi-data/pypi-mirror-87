import React, { Fragment } from 'react';
import { ModalEnum, ModalInfo } from './Mito';
import DefaultModal from './DefaultModal';

/*
    A modal that pops up to alert users their file has
    been downloaded to their downloads folder!
*/
const DownloadModal = (props : {setModal: (modalInfo: ModalInfo) => void}): JSX.Element => {

    return (
        <DefaultModal
            header='Download'
            modalType={ModalEnum.Download}
            viewComponent= {
                <Fragment>
                    <p>
                        Your download has completed. Check your downloads folder!
                    </p>
                </Fragment>
            }
            buttons={
                <Fragment>
                    <div className='modal-close-button' onClick={() => {props.setModal({type: ModalEnum.None})}}> Close </div>
                </Fragment> 
            }
        />
    )
};

export default DownloadModal;