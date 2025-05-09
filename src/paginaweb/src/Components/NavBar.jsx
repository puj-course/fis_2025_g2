import { Link } from "react-router-dom";
import './NavBar.css'; // Estilo separado

function NavBar() {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">FEED-Back</Link>
        <ul className="navbar-menu">
          <li className="navbar-item">
            <Link to="/" className="navbar-link">Inicio</Link>
          </li>
          <li className="navbar-item">
            <Link to="/quienes-somos" className="navbar-link">Quiénes Somos</Link>
          </li>
          <li className="navbar-item">
            <Link to="/login" className="navbar-link">Login</Link>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default NavBar;

