import {Container} from "./styled-components";
import React from "react";

function Buttons(props) {
    return (
        <Container className="ml-auto custom-button">
            <div id={"progress-"+props.formId}></div>
            <div className="previewBox">
                <button className="previewButton" id={"preview-button-"+props.formId} title="preview"
                        onClick={(event) => props.runModel(event,'preview',props.formId)}>
                    <i className="fas fa-border-style"/>
                </button>
            </div>
            <div className="runBox">
                <button className="runButton" id={"run-button-"+props.formId} title="submit"
                        onClick={(event) => props.runModel(event,'main',props.formId)}>
                    <i className="fas fa-play"/>
                </button>
            </div>

            <div className="saveBox">
                <button className="saveButton" id={"download-button-"+props.formId} title="download"
                        onClick={(event) => props.downloadFile(event,props.formId)}>
                    <i className="fas fa-download"/>
                </button>
            </div>
        </Container>
    );
}

export default Buttons;