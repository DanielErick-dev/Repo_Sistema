from django.urls import path
from .views import IndexView, AcademyListView, AcademyDeleteView, AcademyAdministrativeView, CriandoUsuario, Atualizando_pagamento_usuario, Academy_search, Listando_usuarios_pendentes
urlpatterns = [
    path("", IndexView.as_view(), name="index_view"),
    path("cadastro/", CriandoUsuario, name="cadastro"),
    path("listar/", AcademyListView.as_view(), name="academy_list"),
    path("deletar/<int:pk>", AcademyDeleteView.as_view(), name="delete_view"),
    path("usuarios_pendentes/", Listando_usuarios_pendentes, name="academy_usuarios_pendentes"),
    path("area_administrativa/", AcademyAdministrativeView.as_view(), name="administrative_view"),
    path("atualizacao_de_pagamento/", Atualizando_pagamento_usuario, name="academy_atualizacao"),
    path("procurando_usuario/", Academy_search, name='academy_search'),
]