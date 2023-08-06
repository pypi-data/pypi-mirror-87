import React from "react";
import {Container} from "./styled-components";

function FileUpload(props) {

    return (
        <Container clasName="card-value text-small center">
            <input className="custom-file-upload is-light-text"
                   type="file" id={"file-"+props.formId} name="myfile" accept=".txt"/>
        </Container>
    );
}

export default FileUpload;