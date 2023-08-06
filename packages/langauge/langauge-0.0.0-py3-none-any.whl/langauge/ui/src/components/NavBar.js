import {Container, Nav} from "./styled-components";
import UserImg from "../assets/images/flapmax.png";
import React from "react";
import Tabs from "./Tabs";

function NavBar(props) {
    return (
        <Nav className="navbar navbar-expand-lg fixed-top is-white is-dark-text">
            <Container className="navbar-brand h1 text-large font-medium">
                Lan<i>G</i>auge
            </Container>
            <Container>
                <Tabs/>
            </Container>
            <Container className="navbar-nav ml-auto">
                <Container className="user-detail-section">
                    <span className="pr-2"></span>
                    <span className="img-container">
                        <img src={UserImg} className="rounded-circle" alt="user"/>
                    </span>
                </Container>
            </Container>
        </Nav>
    );
}

export default NavBar;