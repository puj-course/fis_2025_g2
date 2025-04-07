import { Producto } from 'C:/Users/romer/feed-back/src/Models/modelo';

export function obtenerProductosPrueba() {
  return [
    new Producto('Arroz', 3000, 2500),
    new Producto('Papa', 4000, 3200),
    new Producto('Tomate', 3500, 2800),
  ];
}