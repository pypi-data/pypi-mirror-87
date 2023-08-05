
import React from 'react';


type TooltipProps = {
    tooltip: string;
};

export default function Tooltip(props : TooltipProps) : JSX.Element {

    return (
        <div className="tooltip">
            {props.tooltip}
        </div>  
    );
}