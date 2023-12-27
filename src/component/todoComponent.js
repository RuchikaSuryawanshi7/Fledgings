import React from "react";
import todoC from "./todo.module.css";
import edit from "../graphics/edit.png"

export default function todoComponent(props) {
  return (
    <div className={todoC.main}>
      <h3>{props.name}</h3>
      <div>Remaining Time : {props.remaining}</div>
      <div>Interval : {props.interval}</div>
      <div>Passed Time : {props.passed}</div>
      <button className={todoC.btn}>
        <p>Edit</p>
        <img src={edit} alt="" />
      </button>
    </div>
  );
}
