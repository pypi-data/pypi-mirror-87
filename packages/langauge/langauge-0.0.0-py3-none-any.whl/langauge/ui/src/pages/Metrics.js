import React from 'react';
import BarChart from "../components/BarChart";

function Metrics(props) {
  return (
    <BarChart channel={props.channel} data={props.time_taken}/>
  );
}

export default Metrics;