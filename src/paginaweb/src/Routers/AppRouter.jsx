import { Routes, Route } from "react-router-dom";
import Home from "../views/Home";
import Comparador from "../views/Comparador";
import Login from "../views/Login";
import Register from "../views/Register";
import Prediccion from "../views/Prediccion";
const AppRouter = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/comparador" element={<Comparador />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/prediccion" element={<Prediccion />} />
    </Routes>
  );
};

export default AppRouter;
