from decimal import Decimal

from django.test import TestCase

from gestion_productos.DAO.productoDAO import ProductoDAO
from gestion_productos.exceptions.productoExceptions import (
    ProductoNoEncontrado_404,
)


class ProductoDAOTest(TestCase):
    def _crear(self, name="Lapiz", product_key="LPZ00001"):
        return ProductoDAO.crear_producto(
            type="util",
            name=name,
            price=Decimal("12.50"),
            status=True,
            product_key=product_key,
            image_link="https://example.test/lapiz.png",
            description="Lapiz de grafito",
        )

    def test_crear_y_obtener(self):
        producto = self._crear()
        encontrado = ProductoDAO.obtener_producto_por_id(producto.id)
        self.assertEqual(encontrado.name, "Lapiz")

    def test_borrado_logico_y_restaurar(self):
        producto = self._crear()
        ProductoDAO.eliminar_producto(producto.id)
        with self.assertRaises(ProductoNoEncontrado_404):
            ProductoDAO.obtener_producto_por_id(producto.id)
        restaurado = ProductoDAO.restaurar_producto(producto.id)
        self.assertFalse(restaurado.is_deleted)

    def test_buscar_y_filtrar_precio(self):
        self._crear()
        self.assertEqual(ProductoDAO.buscar_productos("Lapi").count(), 1)
        self.assertEqual(
            ProductoDAO.filtrar_por_rango_precio(10, 20).count(),
            1,
        )

    def test_activar_desactivar(self):
        producto = self._crear()
        ProductoDAO.desactivar_producto(producto.id)
        producto.refresh_from_db()
        self.assertFalse(producto.status)
        ProductoDAO.activar_producto(producto.id)
        producto.refresh_from_db()
        self.assertTrue(producto.status)
