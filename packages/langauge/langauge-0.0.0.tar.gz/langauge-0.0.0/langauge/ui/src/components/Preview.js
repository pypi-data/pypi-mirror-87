import {Container} from "./styled-components";
import React from "react";

function Preview(props) {
    return (
        <Container className="card grid-card is-card-dark custom-preview">
            <Container className="card-value text-small">
                <div className="previewDescription is-light-text" id={"preview-"+props.formId}>
                    {/*<span>Preview the model output format for each selected file</span>*/}
                </div>
            </Container>
        </Container>
    )
}

export default Preview;