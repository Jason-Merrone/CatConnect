import { Outlet } from "react-router-dom";
import './App.css';
import Banner from "./Banner.jsx";

function App() {
  return (
    <div>
      <Banner />
      <Outlet />
    </div>
  )
}

export default App;