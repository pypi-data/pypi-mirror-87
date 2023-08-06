import {Container} from "./styled-components";
import React, {Component} from "react";

class ModelSelect extends Component {

    render() {
        return (
            <Container className="card-value grid-card is-light-text text-small center">
                <div className="" id={"model-" + this.props.formId}>
                    <select value={this.props.selectedModel}
                            onChange={(event) => this.props.onModelChange(this.props.formId, event.target.value)}>
                        {this.props.models && this.props.models.map((model) =>
                            <option key={model.value} value={model.value}>{model.display}</option>)}
                    </select>
                </div>
            </Container>
        )
    }
}

export default ModelSelect;