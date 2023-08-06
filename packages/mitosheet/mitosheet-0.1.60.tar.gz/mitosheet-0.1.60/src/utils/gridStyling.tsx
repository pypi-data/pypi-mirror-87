// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

const SHEET_HEIGHT_PIXELS = 250; // this should be the same as the height defined in widget.css

export const headerHeightParams = {
    defaultHeaderHeight: 40,
    charactersPerRow: 9, // our estimate of the number of characters that fit in each row 
    pixelsPerRow: 35 // number of pixels per row
}

export function calculateAndSetHeaderHeight(model_id: string) : void {

    // we now do some work to find the best height to give the header row
    // first find the largest header
    let maxHeaderLength = 0
    const gridApi = window.gridApiMap?.get(model_id);

    // if the gridApi does not exist, stop
    if (gridApi === undefined) {
        return
    }

    const rowNodeData = gridApi.getRowNode('0')?.data;
    if (rowNodeData === undefined) {
        // This is undefined when the sheet is empty, and thus there aren't
        // any column headers to resize. Thus, we don't need to do anything.
        return;
    }

    Object.keys(rowNodeData).forEach(key => {
        /* 
            because each row can only hold 9 characters on average, 
            if any words are greater than 9 characters, it will be split into two rows. 

            To make sure that we accommodate these special situations, we assume the worst case
            scenario, and add an extra entire line. 
        */

        let paddingCharacters = 0
        getHeaderWords(key).forEach(word => {
            if (word.length > headerHeightParams.charactersPerRow) {
                paddingCharacters += headerHeightParams.charactersPerRow
            }
        });

        maxHeaderLength = key.length + paddingCharacters > maxHeaderLength ? key.length + paddingCharacters : maxHeaderLength
    });

    /* 
        then set the correct header height... 
        we fit on average 10 letters per row with a starting width of 40 pixels
        and we give each row 30 px of space
    */ 

    gridApi.setHeaderHeight(
        Math.min(
            Math.max(
                (maxHeaderLength / headerHeightParams.charactersPerRow - 1) * headerHeightParams.pixelsPerRow, 
                headerHeightParams.defaultHeaderHeight
            ), SHEET_HEIGHT_PIXELS / 3)
    );

    gridApi.refreshHeader();
}
       

export function getHeaderWords(header: string) : string[] {
    /*
    we split each word of the header (separated by _), adding the _ to 
    the latter half of the split. ie: first_name -> [first, _name]

    This split is taken from: https://stackoverflow.com/a/45323715
    */

    return header.split(/(?=_)/g)
} 
