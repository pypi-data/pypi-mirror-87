import {Container} from "./styled-components";
import React from "react";

function TaskSelect(props){
    return (
        <Container className="card-value grid-card is-light-text text-small center">
            <div className="" id={"task-"+props.formId}>
                <select value={props.selectedTask}
                            onChange={(event) => props.onTaskChange(props.formId, event.target.value)}>
                        {props.tasks.map((task) =>
                            <option key={task.value} value={task.value}>{task.display}</option>)}
                </select>
            </div>
        </Container>
    )
}

export default TaskSelect;