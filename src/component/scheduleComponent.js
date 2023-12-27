import React from 'react'
import TaskCss from "./scheduleComponent.module.css"

export default function scheduleComponent(props) {
  return (
    <div className={TaskCss.main}>
      <h3>{props.name}</h3>
      <div>Remaining Time : {props.remaining}</div>
      <div>Interval : {props.interval}</div>
      <div>Passed Time : {props.passed}</div>
      <button className={TaskCss.btn}>
        <p>Edit</p>
        <img src='' alt="" />
      </button>
    </div>
  )
}
