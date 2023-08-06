import React from 'react';
import {Bar} from 'react-chartjs-2';
import {Container} from "./styled-components";

function dynamicColors() {
    let r = Math.floor(Math.random() * 255);
    let g = Math.floor(Math.random() * 255);
    let b = Math.floor(Math.random() * 255);
    return "rgba(" + r + "," + g + "," + b + ", 0.5)";
}

function poolColors(a) {
    let pool = [];
    for (let i = 0; i < a; i++) {
        pool.push(dynamicColors());
    }
    return pool;
}

function BarChart(props) {

    const options = {
        legend: {
                labels: {
                    fontColor: "white",
                    fontSize: 14
                }
            },
        scales: {
            yAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: 'Time',
                    fontColor: 'white'
                },
                ticks: {
                    fontColor: 'white'
                    }
            }],
            xAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: 'Channel',
                    fontColor: 'white'
                },
                ticks: {
                    fontColor: 'white'
                    }
            }],
        },
        tooltips: {
            callbacks: {
                label: function (t, d) {
                    let xLabel = d.datasets[t.datasetIndex].label;
                    let yLabel = d.datasets[t.datasetIndex].data[t.index];
                    return xLabel + ': $' + yLabel;
                }
            }
        }
    }

    const time_state = {
        labels: props.channel,
        datasets: [
            {
                label: 'Execution Time',
                borderWidth: 1,
                backgroundColor: poolColors(Object.keys(props.data).length),
                borderColor: poolColors(Object.keys(props.data).length),
                data: Object.values(props.data)
            }
        ]
    }

    return (
        <Container className="container-fluid-side row is-card-dark">
            <Container className="container-fluid-side row">
            </Container>
            <Container className="container-fluid-side row" style={{height: '500px'}}>
                <div>
                    <Bar data={time_state} options={options} height={450} width={800}/>
                </div>
            </Container>
            {/*<Container className="container-fluid-side row custom-row">*/}
            {/*    <Bar data={acc_state} options={options}/>*/}
            {/*</Container>*/}
        </Container>
    );
}

export default BarChart;