import React, { useState, useEffect } from 'react';
import { obtenerProductosPrueba } from 'C:/Users/romer/feed-back/src/Controllers/ProductoController';

function Comparador() {
  const [productos, setProductos] = useState([]);

  useEffect(() => {
    setProductos(obtenerProductosPrueba());
  }, []);

  return (
    <div className="min-h-screen p-8 bg-gray-100">
      <h1 className="text-3xl font-bold mb-6">Comparador de Precios 🛒</h1>
      <table className="w-full bg-white shadow-md rounded-lg overflow-hidden">
        <thead className="bg-blue-500 text-white">
          <tr>
            <th className="p-4">Producto</th>
            <th className="p-4">Supermercado</th>
            <th className="p-4">Productor Local</th>
          </tr>
        </thead>
        <tbody>
          {productos.map((producto, index) => (
            <tr key={index} className="border-b text-center">
              <td className="p-4">{producto.nombre}</td>
              <td className="p-4 text-red-500 font-semibold">${producto.precioSupermercado}</td>
              <td className="p-4 text-green-500 font-semibold">${producto.precioProductor}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Comparador;