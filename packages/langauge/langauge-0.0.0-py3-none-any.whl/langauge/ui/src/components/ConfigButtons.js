import {Container} from "./styled-components";
import React from "react";

class ConfigButtons extends React.Component {

    render() {
        return (
            <Container className="ml-auto custom-button">
                <div className="nav-saveBox">
                    <button className="previewButton" id="save-config-button" title="save selection"
                            onClick={(event) => this.props.saveConfig(event)}>
                        <i className="fas fa-save"/>
                    </button>
                </div>
                <label className="nav-previewBox">
                    <input type="file" className="nav-previewButton" id="fetch-config-button" title="fetch selection"
                           accept="application/JSON" onChange={(event)=>this.props.fetchConfig(event)}>
                    </input>
                    <i className="fas fa-spinner"></i>
                </label>
                <div className="nav-runBox">
                    <button className="runButton" id="run-config-button" title="run all saved"
                            onClick={(event) => this.props.runAll(event)}>
                        <i className="fas fa-play"/>
                    </button>
                </div>
            </Container>
        );
    }


}

export default ConfigButtons;