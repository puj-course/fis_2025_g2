import { Link } from "react-router-dom";
import NavBar from "../Components/NavBar";
import './Home.css'; // Asegúrate de importar el archivo CSS

function Home() {
  return (
    <div className="home-container">
      <NavBar />
      <div className="home-content">
        <h1 className="home-title">Bienvenido a FEED-Back 🏡</h1>
        <p className="home-description">
          Tu plataforma de transparencia de precios, conectando productores locales con consumidores conscientes.
        </p>
        <Link to="/comparador">
          <button className="home-button">
            Ir al Comparador de Precios
          </button>
        </Link>
      </div>
    </div>
  );
}

export default Home;
