import React from "react";
import {Container} from "./styled-components";

function ColHeadings(props) {
    return (
        <Container className="container-fluid-side row">
            <Container className="card-heading grid-card is-light-text ">
                <Container className="is-dark-text-light letter-spacing text-medium">
                    Data
                </Container>

            </Container>
            <Container className="card-heading grid-card is-light-text ">
                <Container className="is-dark-text-light letter-spacing text-medium">
                    Task
                </Container>

            </Container>
            <Container className="card-heading grid-card is-light-text ">
                <Container className="is-dark-text-light letter-spacing text-medium">
                    Model
                </Container>

            </Container>
            <Container className="card-heading grid-card is-light-text ">
                <Container className="is-dark-text-light letter-spacing text-medium">
                    Preview
                </Container>

            </Container>
        </Container>
    );
}

export default ColHeadings;