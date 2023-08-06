import React, {Component} from 'react';
import './App.css';
import {BrowserRouter as Router, Route, Switch} from 'react-router-dom';
import Metrics from "./pages/Metrics";
import History from "./pages/History";
import Home from "./components/Home.js";
import NavBar from "./components/NavBar";

const channel = {0:'A', 1:'B'};

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            time_taken: {}
        };
        this.handleTimeTakenChange = this.handleTimeTakenChange.bind(this);
    }

    handleTimeTakenChange(numForm, time_taken) {
        let that = this;
        that.setState(prevState => ({
            time_taken: {                   // object that we want to update
                ...that.state.time_taken,    // keep all other key-value pairs
                [numForm]: time_taken
            }
        }));
    }

    render() {
        return (
            <>
                <Router>
                    <NavBar/>
                    <Switch>
                        <Route exact path='/' render={(props) => (
                            <Home channel={channel}
                                  time_taken={this.state.time_taken}
                                  onTimeTakenChange={this.handleTimeTakenChange}/>
                        )}/>
                        <Route path='/metrics' render={(props) => (
                            <Metrics channel={Object.values(channel)}
                                  time_taken={this.state.time_taken}/>
                        )}/>
                        <Route path='/history' component={History}/>
                    </Switch>
                </Router>
            </>
        );
    }


}

export default App;
