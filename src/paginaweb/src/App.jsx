import { Routes, Route } from 'react-router-dom';
import Home from './views/Home';
import Comparador from './views/Comparador';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/comparador" element={<Comparador />} />
    </Routes>
  );
}

export default App;