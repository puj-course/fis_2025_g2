// src/views/Home.jsx
import { Link } from "react-router-dom";
import NavBar from "../Components/NavBar";
import { motion } from "framer-motion";
import './Home.css';

export default function Home() {
  const container = { hidden: {}, show: { transition: { staggerChildren: 0.15 } } };
  const item = { hidden: { opacity: 0, y: 20 }, show: { opacity: 1, y: 0 } };

  return (
    <div className="home-bg full-screen">
      {/* Barra de navegación fija arriba, gestionada por NavBar */}
      <NavBar />

      {/* Contenido centrado debajo de la barra */}
      <div className="content-wrapper">
        <motion.div
          className="home-content"
          variants={container}
          initial="hidden"
          animate="show"
        >
          <motion.h1 variants={item} className="home-title">
            Bienvenido a FEED-Back 🏡
          </motion.h1>
          <motion.p variants={item} className="home-description">
            Tu plataforma de transparencia de precios, conectando productores locales con consumidores conscientes.
          </motion.p>
          <motion.div variants={item}>
            <Link to="/comparador">
              <button className="home-button">
                Ir al Comparador de Precios
              </button>
            </Link>
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
}