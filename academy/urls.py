from django.urls import path
from .views import IndexView, CadastroView, AcademyListView, AcademyDeleteView, AcademyUsuariosPendentesView
urlpatterns = [
    path("", IndexView.as_view(), name="index_view"),
    path("cadastro/", CadastroView.as_view(), name="cadastro_view"),
    path("listar/", AcademyListView.as_view(), name="academy_list"),
    path("deletar/<int:pk>", AcademyDeleteView.as_view(), name="delete_view"),
    path("usuarios_pendentes/", AcademyUsuariosPendentesView.as_view(), name="usuarios_pendentes_view"),
]