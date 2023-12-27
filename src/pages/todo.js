import React from 'react'
import Schedule from './schedule.module.css'

import ScheduleComponent from '../component/scheduleComponent.js';

export default function todo() {

  const todoList = [
    {
      name: "Practice",
      remaining: "0hrs",
      timepassed: "2",
      cycle: "30mins",
    },
    {
      name: "Coding",
      remaining: "0.4hrs",
      timepassed: "0",
      cycle: "1hr",
    },
    {
      name: "Guitar",
      remaining: "1.3hrs",
      timepassed: "0",
      cycle: "1hrs",
    },
    {
      name: "Gym",
      remaining: "2hrs",
      timepassed: "0",
      cycle: "2hrs",
    },
    {
      name: "Reading",
      remaining: "8hrs",
      timepassed: "0",
      cycle: "2hrs",
    },
    {
      name: "Anime",
      remaining: "10hrs",
      timepassed: "0",
      cycle: "2hrs",
    },
  ];

  return (
    <div className={Schedule.main}>
      <div className={Schedule.blank}></div>
      <h1 className={Schedule.title}>Task Scheduler</h1>
      <div className={Schedule.list}>
      {todoList.map((task) => (
              <ScheduleComponent
                name={task.name}
                remaining={task.remaining}
                passed={task.timepassed}
                interval={task.cycle}
              />
            ))}
      </div>
    </div>
  )
}
