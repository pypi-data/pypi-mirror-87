import React, {Component} from 'react';
import {DataGrid} from '@material-ui/data-grid';
import Grid from "@material-ui/core/Grid";
import $ from "jquery";

const columns = [
    {field: 'id', headerName: 'ID', width: 325},
    {field: 'task', headerName: 'TASK', width: 125},
    {field: 'model', headerName: 'MODEL', width: 300},
    {field: 'status', headerName: 'STATUS', width: 125},
    {field: 'date_done', headerName: 'COMPLETION TIME', type: 'date', width: 225}
];

const host = process.env.REACT_APP_BASE_URL;

export default class History extends Component {
    state = {
        setSelection: "",
        rows: []
    };

    componentDidMount() {
        fetch(host + "/celery/history")
            .then((response) => {
                return response.json();
            })
            .then(data => {
                this.setState({
                    rows: data
                });
            }).catch(error => {
            console.log(error);
        });
    }

    downloadFile() {
        if (this.state.setSelection === "") {
            alert("Please select a record !!!");
            return;
        }
        fetch(host + `/celery/fileDownload/${this.state.setSelection}`, {
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

    render() {
        return (
            <Grid>
                <Grid style={{height: 500, backgroundColor: "white"}}>
                    <DataGrid rows={this.state.rows} columns={columns} pageSize={7} checkboxSelection
                              onSelectionChange={(newSelection) => {
                                  this.setState({
                                      setSelection: newSelection.rowIds
                                  });
                              }}/>

                </Grid>
                <Grid className="saveBox-grid">
                    <button className="saveButton-grid" title="download"
                            onClick={() => this.downloadFile()}>
                        <i className="fas fa-download"/>
                    </button>
                </Grid>
            </Grid>

        );
    }

}
