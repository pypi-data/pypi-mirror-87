import React, {Component} from "react";
import {Container} from "./styled-components";
import $ from "jquery";
import ColHeadings from './ColHeadings.js';
import FileUpload from "./FileUpload";
import TaskSelect from "./TaskSelect";
import ModelSelect from "./ModelSelect";
import Preview from "./Preview";
import Buttons from "./Buttons";
import ConfigButtons from "./ConfigButtons";
import {TaskData} from "./TaskData";
import {ModelData} from "./ModelData";

const host = process.env.REACT_APP_BASE_URL;

class Home extends Component {
    constructor(props) {
        super(props);
        this.state = {
            file: {},   //current file selected
            task: {},   //current task selected
            model: {},  //current model selected
            backendTaskId: {},  // for file download
            availableModels: {}, // depends on the current selected task
            //{
            //  model-0:
            //      [
            //          {display:"pubMedBERT (BC5CDR chemical)", selected: "pubMedBERT_BC5CDR_chem"}
            //          , {display:"pubMedBERT (BC5CDR chemical)", selected: "pubMedBERT_BC5CDR_chem"}
            //          ]
            // , model-1:[]
            // , ...}
            availableTasks: []  //[task1, task2]
        };
        this.update_run = this.update_run.bind(this);
        this.runModel = this.runModel.bind(this);
        this.downloadFile = this.downloadFile.bind(this);
        this.update_preview = this.update_preview.bind(this);
        this.runAll = this.runAll.bind(this);
        this.saveConfig = this.saveConfig.bind(this);
        this.isValid = this.isValid.bind(this);
        this.disableButtons = this.disableButtons.bind(this);
        this.enableButtons = this.enableButtons.bind(this);
        this.onModelChange = this.onModelChange.bind(this);
        this.onTaskChange = this.onTaskChange.bind(this);
        this.fetchConfig = this.fetchConfig.bind(this);
    }

    componentDidMount() {
        const that = this;

        $(document).ready(function () {
            $('input').change(function () {
                let id = $(this).attr("id").valueOf();
                let file = $(this)[0].files[0];
                that.setState(prevState => ({
                    file: {                   // object that we want to update
                        ...that.state.file,    // keep all other key-value pairs
                        [id]: file,       // update the value of specific key
                    }
                }));
            });
        });

        fetch(host + "/config/tasks")
            .then((response) => {
                return response.json();
            })
            .then(data => {
                let modelsFromApi = $.parseJSON(data).map(task => {
                    return {value: task.value, display: task.label}
                });
                this.setState({
                    availableTasks: [{value: '', display: '(Select a Task)'}].concat(modelsFromApi)
                });
            }).catch(error => {
            let modelsFromApi = TaskData.map(task => {
                    return {value: task.value, display: task.label}
                });
            this.setState({
                availableTasks: [{value: '', display: '(Select a Task)'}].concat(modelsFromApi)
            });
        });
    }

    onModelChange(numForm, value) {
        this.setState(prevState => ({
            model: {                   // object that we want to update
                ...this.state.model,    // keep all other key-value pairs
                ["model-" + numForm]: value    // update the value of specific key
            }
        }));
    }

    onTaskChange(numForm, value) {
        this.setState(prevState => ({
            task: {                   // object that we want to update
                ...this.state.task,    // keep all other key-value pairs
                ["task-" + numForm]: value    // update the value of specific key
            }
        }));
        fetch(host + "/config/models/" + value)
            .then((response) => {
                return response.json();
            })
            .then(data => {
                let modelsFromApi = $.parseJSON(data).models.map(model => {
                    return {value: model.value, display: model.label}
                });
                this.setState(prevState => ({
                    availableModels: {                   // object that we want to update
                        ...this.state.availableModels,    // keep all other key-value pairs
                        ["model-" + numForm]: [{value: '', display: '(Select a Model)'}].concat(modelsFromApi)    // update the value of specific key
                    }
                }));
                // this.setState({
                //     availableModels: [{value: '', display: '(Select a Model)'}].concat(modelsFromApi)
                // });
            }).catch(error => {
            if (value !== 'ner')
                return;
            let modelsFromApi = ModelData.map(model => {
                    return {value: model.value, display: model.label}
                });
            this.setState(prevState => ({
                availableModels: {                   // object that we want to update
                    ...this.state.availableModels,    // keep all other key-value pairs
                    ["model-" + numForm]: [{value: '', display: '(Select a Model)'}].concat(modelsFromApi)    // update the value of specific key
                }
            }));
        });
    }

    update_run(status_url, numForm, status_div) {
        // send GET request to status URL
        const that = this;
        $.getJSON(status_url, function (data) {
            // update UI
            if (data['state'] !== 'PENDING' && data['state'] !== 'PROGRESS') {
                if ('id' in data) {
                    // show result
                    $(status_div.childNodes[0]).text('Done');
                    that.setState(prevState => ({
                        backendTaskId: {                   // object that we want to update
                            ...that.state.backendTaskId,    // keep all other key-value pairs
                            [numForm]: data['id']
                        }
                    }));
                    that.props.onTimeTakenChange(numForm, Number(data['time']));
                } else {
                    // something unexpected happenedss
                    $(status_div.childNodes[0]).text('Failed');
                    $(status_div).toggleClass("custom-progress-failure");
                }
                that.enableButtons(numForm);
            } else {
                // rerun in 2 seconds
                setTimeout(function () {
                    that.update_run(status_url, numForm, status_div);
                }, 10000);
            }
        });
    }

    update_preview(status_url, numForm, status_div) {
        // send GET request to status URL
        const that = this;
        const previewholder = "#preview-" + numForm;
        $.getJSON(status_url, function (data) {
            if (data['state'] !== 'PENDING' && data['state'] !== 'PROGRESS') {
                if ('preview' in data) {
                    // show result
                    $(status_div.childNodes[0]).text('Done');
                    $(previewholder).append(JSON.stringify(data['preview']));
                } else {
                    // something unexpected happened
                    $(status_div.childNodes[0]).text('Failed');
                    $(status_div).toggleClass("custom-progress-failure");
                }
                that.enableButtons(numForm);
            } else {
                // rerun in 2 seconds
                setTimeout(function () {
                    that.update_preview(status_url, numForm, status_div);
                }, 10000);
            }
        });
    }

    runModel(ev, type, numForm) {
        ev.preventDefault();
        const progressholder = "#progress-" + numForm;
        const fileholder = "file-" + numForm;
        const taskholder = "task-" + numForm;
        const modelholder = "model-" + numForm;
        let endPoint = '';
        if (type === 'preview') {
            endPoint = `/${this.state.task[taskholder]}/preview/${this.state.model[modelholder]}/5/${numForm}`;
        } else {
            endPoint = `/${this.state.task[taskholder]}/${this.state.model[modelholder]}/${numForm}`;
        }
        if (!this.isValid(numForm)) {
            alert('Please select all the options !!')
        } else {
            this.disableButtons(numForm);
            const div = $('<div class="custom-progress-success">' +
                '<div style="color:white;text-align:center;">' +
                'Started' +
                '</div>' +
                '</div><hr>');
            const data = new FormData();
            data.append('file', this.state.file[fileholder]);
            $(progressholder).html(div);
            fetch(host + endPoint, {
                method: 'POST',
                body: data,
            }).then(response => response.json())
                .then(data => {
                        if (type === 'preview') {
                            this.update_preview(host + data, numForm, div[0]);
                        } else {
                            this.update_run(host + data, numForm, div[0]);
                        }
                    }
                ).catch(error => {
                $(div[0].childNodes[0]).text('Failed');
                $(div[0]).toggleClass("custom-progress-failure");
                $(progressholder).html(div);
            });
        }
    }

    isValid(numForm) {
        let fileholder = "file-" + numForm;
        let taskholder = "task-" + numForm;
        let modelholder = "model-" + numForm;
        if (typeof this.state.file[fileholder] === 'undefined'
            || typeof this.state.task[taskholder] === 'undefined'
            || typeof this.state.model[modelholder] === 'undefined') {
            return false;
        } else {
            return true;
        }
    }

    disableButtons(numForm) {
        $("#channel-" + numForm + " *").attr("disabled", "disabled").off('click');
        $('#preview-button-' + numForm).css('pointer-events', "none");
        $('#run-button-' + numForm).css('pointer-events', "none");
        $('#download-button-' + numForm).css('pointer-events', "none");
    }

    enableButtons(numForm) {
        $("#channel-" + numForm + " *").removeAttr("disabled");
        $('#preview-button-' + numForm).removeAttr('style');
        $('#run-button-' + numForm).removeAttr('style');
        $('#download-button-' + numForm).removeAttr('style');
    }

    downloadFile(ev, numForm) {
        ev.preventDefault();
        if (this.state.backendTaskId[numForm] === undefined) {
            alert("No file available for download !!!");
            return;
        }
        fetch(host + `/celery/fileDownload/${this.state.backendTaskId[numForm]}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'text/csv'
            },
            responseType: 'blob'
        }).then(response => response.blob())
            .then(blob => {
                let url = window.URL.createObjectURL(blob);
                let a = document.createElement('a');
                a.href = url;
                a.download = "results.txt";
                document.body.appendChild(a); // we need to append the element to the dom -> otherwise it will not work in firefox
                a.click();
                a.remove();  //afterwards we remove the element again
            });
    }

    saveConfig(ev) {
        ev.preventDefault();
        if (Object.keys(this.state.task).length !== Object.keys(this.state.model).length) {
            alert("Partial options cannot be saved !!")
        } else {
            // console.log(this.state.file['file-0'].value);
            let data = JSON.stringify({
                // 'file': window.URL.createObjectURL(this.state.file['file-0']),
                'task': this.state.task,
                'model': this.state.model
            });
            let bb = new Blob([data], {type: 'application/json'});
            let a = document.createElement('a');
            a.download = 'selection.json';
            a.href = window.URL.createObjectURL(bb);
            a.click();
        }
    }

    fetchConfig(ev) {
        ev.preventDefault();
        const reader = new FileReader();
        let selection_data = {};
        reader.onload = async (e) => {
            let text = (e.target.result);
            if (typeof text !== 'string') {
                return;
            }
            try {
                selection_data = JSON.parse(text);
            } catch (e) {
                return;
            }
            if (Object.keys(selection_data.model).length !== 0) {
                let jsonModel = selection_data.model;
                let jsonTask = selection_data.task;
                this.setState({task: jsonTask});
                let that = this;
                $.each(jsonTask, function (key, val) {
                    fetch(host + "/config/models/" + val)
                        .then((response) => {
                            return response.json();
                        })
                        .then(data => {
                            let modelsFromApi = $.parseJSON(data).models.map(model => {
                                return {value: model.value, display: model.label}
                            });
                            that.setState(prevState => ({
                                availableModels: {                   // object that we want to update
                                    ...that.state.availableModels,    // keep all other key-value pairs
                                    ["model-" + key.split("-")[1]]: [{
                                        value: '',
                                        display: '(Select a Model)'
                                    }].concat(modelsFromApi)    // update the value of specific key
                                }
                            }));
                        }).catch(error => {
                            if(val!=='ner')
                                return;
                            let modelsFromApi = ModelData.map(model => {
                                    return {value: model.value, display: model.label}
                                });
                                that.setState(prevState => ({
                                    availableModels: {                   // object that we want to update
                                        ...that.state.availableModels,    // keep all other key-value pairs
                                        ["model-" + key.split("-")[1]]: [{
                                            value: '',
                                            display: '(Select a Model)'
                                        }].concat(modelsFromApi)    // update the value of specific key
                                    }
                                }));
                    });
                });
                this.setState({model: jsonModel});
            }
        };
        reader.readAsText(ev.target.files[0]);

    }

    runAll(ev) {
        ev.preventDefault();
        Object.keys(this.props.channel).map((key, i) => {
                this.runModel(ev, 'run', i);
            }
        );
    }


    render() {
        const channel = this.props.channel;
        return (
            <Container>
                <Container className="custom-fixed-top nav-secondary is-dark is-light-text">
                    <ConfigButtons saveConfig={this.saveConfig} fetchConfig={this.fetchConfig} runAll={this.runAll}/>
                </Container>
                <Container className="container-fluid-side row is-card-dark">
                    <ColHeadings/>
                    {Object.keys(channel).map((key, i) => (
                        <Container id={"channel-" + i} className="container-fluid-side row custom-row">
                            <Container className='is-light-text' style={{'paddingLeft': '5px'}}>
                                <a>{channel[key]}:</a>
                            </Container>
                            <FileUpload formId={i}/>
                            <TaskSelect formId={i} selectedTask={this.state.task["task-" + i]}
                                        tasks={this.state.availableTasks} onTaskChange={this.onTaskChange}/>
                            <ModelSelect formId={i} selectedModel={this.state.model["model-" + i]}
                                         models={this.state.availableModels["model-" + i]}
                                         onModelChange={this.onModelChange}/>
                            <Preview formId={i}/>
                            <Buttons formId={i} runModel={this.runModel}
                                     downloadFile={this.downloadFile}/>
                        </Container>
                    ))}
                </Container>
            </Container>
        );
    }
}


export default Home;
