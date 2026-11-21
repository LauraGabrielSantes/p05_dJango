from django.test import TestCase

from gestion_usuarios.DAO.usuarioDAO import UsuarioDAO
from gestion_usuarios.exceptions.usuarioExeptions import (
    ConflictoUsuario_409,
    DatosInvalidos_400,
    UsuarioNoEncontrado_404,
)
from gestion_usuarios.models import Usuario


class UsuarioDAOTest(TestCase):
    def _crear(self, username="laura", email="laura" + "@" + "example.test"):
        return UsuarioDAO.crear_usuario(
            username=username,
            password="secreto123",
            date_of_birth="1990-01-01",
            email=email,
            first_name="Laura",
            last_name="Pruebas",
        )

    def test_crear_y_obtener_por_id(self):
        usuario = self._crear()
        encontrado = UsuarioDAO.obtener_usuario_por_id(usuario.id)
        self.assertEqual(encontrado.username, "laura")
        self.assertTrue(encontrado.password.startswith("pbkdf2_"))

    def test_username_largo_rechazado(self):
        with self.assertRaises(Exception):
            self._crear(username="usuario_demasiado_largo")

    def test_email_duplicado_conflicto(self):
        self._crear()
        with self.assertRaises(ConflictoUsuario_409):
            self._crear(username="otro", email="laura" + "@" + "example.test")

    def test_obtener_inexistente(self):
        with self.assertRaises(UsuarioNoEncontrado_404):
            UsuarioDAO.obtener_usuario_por_id("00000000-0000-0000-0000-000000000000")

    def test_activar_desactivar(self):
        usuario = self._crear()
        UsuarioDAO.desactivar_usuario(usuario.id)
        usuario.refresh_from_db()
        self.assertFalse(usuario.is_active)
        UsuarioDAO.activar_usuario(usuario.id)
        usuario.refresh_from_db()
        self.assertTrue(usuario.is_active)
        with self.assertRaises(DatosInvalidos_400):
            UsuarioDAO.activar_usuario(usuario.id)

    def test_borrado_logico_y_restaurar(self):
        usuario = self._crear()
        UsuarioDAO.eliminar_usuario(usuario.id)
        with self.assertRaises(UsuarioNoEncontrado_404):
            UsuarioDAO.obtener_usuario_por_id(usuario.id)
        restaurado = UsuarioDAO.restaurar_usuario(usuario.id)
        self.assertFalse(restaurado.is_deleted)
        self.assertIsNone(restaurado.deleted_at)

    def test_verificar_email(self):
        usuario = self._crear()
        UsuarioDAO.verificar_email(usuario.id)
        usuario.refresh_from_db()
        self.assertTrue(usuario.email_verified)
        self.assertIsNotNone(usuario.email_verified_at)
        with self.assertRaises(DatosInvalidos_400):
            UsuarioDAO.verificar_email(usuario.id)

    def test_reset_password_request(self):
        usuario = self._crear()
        resultado = UsuarioDAO.reset_password_request(usuario.email)
        self.assertIn("token", resultado)
        usuario.refresh_from_db()
        self.assertIsNotNone(usuario.reset_password_expires_at)

    def test_listado(self):
        self._crear()
        self.assertEqual(Usuario.objects.count(), 1)
        self.assertEqual(UsuarioDAO.obtener_todos().count(), 1)
