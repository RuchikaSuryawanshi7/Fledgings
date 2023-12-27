import { Routes, Route } from 'react-router-dom';
import './App.css';
import Home from "./pages/home.js"
import Calendar from "./pages/calendar.js"
import Search from "./pages/search.js"
import Todo from "./pages/todo.js"

function App() {
  return (
    <Routes>
      <Route path='/' element={<Home />} />
      <Route path='/calendar' element={<Calendar />} />
      <Route path='/search' element={<Search />} />
      <Route path='/todo' element={<Todo />} />
    </Routes>
  );
}

export default App;
