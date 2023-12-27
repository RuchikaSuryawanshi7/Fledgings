import homec from "./home.module.css";
import mic from "../graphics/mic.png";
import submit from "../graphics/submit.png";
import calendar from "../graphics/calendar.png";
import search from "../graphics/search.png";
import music from "../graphics/music.png";
import todo from "../graphics/todo.png";
import React, { useState } from "react";
import { Link } from "react-router-dom";
import TodoCard from "../component/todoComponent.js";

export default function Home() {
  const todoList = [
    {
      name: "Practice",
      remaining: "0hrs",
      timepassed: "2hrs",
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
    <div className={homec.main}>
      <div className={homec.blank}></div>
      <div className={homec.body}>
        <div className={homec.features}>
          <Link className={homec.feature} to="/calendar">
            <h3>Google Calendar</h3>
            <img src={calendar} alt="" />
          </Link>
          <Link className={homec.feature} to="/todo">
            <h3>Schedule Tasks</h3>
            <img src={todo} alt="" />
          </Link>
          <Link className={homec.feature} to="/search">
            <h3>Ask me anything!</h3>
            <img src={search} alt="" />
          </Link>
          <Link className={homec.feature}>
            <h3>User Analysis</h3>
            <img src={music} alt="" />
          </Link>
        </div>

        <div className={homec.audio}>
          <h1>TimeTrove</h1>
          <img id={homec.mic} src={mic} alt="mic" />
          <div>
            <input type="text" />
            <button>
              <img src={submit} id={homec.submit} alt="" />
            </button>
          </div>
        </div>

        <div className={homec.overview}>
          <h2>Upcoming : </h2>
          <div className={homec.list}>
            {todoList.map((task) => (
              <TodoCard
                name={task.name}
                remaining={task.remaining}
                passed={task.timepassed}
                interval={task.cycle}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
