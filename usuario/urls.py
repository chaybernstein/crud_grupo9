from django.urls import path
from . import views

app_name = 'usuario'

urlpatterns = [
    path('', views.Criar.as_view(), name='criar'),
    path('editar/', views.Editar.as_view(), name='editar'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
]