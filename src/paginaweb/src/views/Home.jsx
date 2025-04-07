import { Link } from 'react-router-dom';

function Home() {
  return (
    <div className="container">
      <h1>Bienvenido a FEED-Back 🏡</h1>
      <p>Tu plataforma de transparencia de precios.</p>
      <Link to="/comparador">
        <button className="boton">Ir al Comparador de Precios</button>
      </Link>
    </div>
  );
}

export default Home;

