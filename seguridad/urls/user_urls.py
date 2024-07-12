from django.urls import path
from seguridad.views import user_views as views
from rest_framework_simplejwt.views import (TokenRefreshView)

urlpatterns = [
    
    # path('login/', views.LoginApiView.as_view(), name='token_obtain_pair'),
    path('upload/', views.uploadImage, name="image-upload"),
    path('recuperar-nombre-usuario/',views.RecuperarNombreDeUsuario.as_view(),name='recuperar-nombre-de-usuario'),
    
    path('profile/', views.getUserProfile, name="users-profile"),
   
    path('roles/', views.roles, name='roles'),
    path("get/", views.getUsers, name="get-users"),
    path("get/<str:pk>/", views.getUserById, name="get-users"), 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('pasword-reset-complete', views.SetNewPasswordApiView.as_view(),name='pasword-reset-complete'), 
    path('get-user-by-nombre-de-usuario/',views.BusquedaByNombreUsuario.as_view(),name='get-user-by-nombre-de-usuario'),
    path('get-buscar-by-id-persona/<str:id_persona>/',views.BuscarByIdPersona.as_view(),name='get-buscar-id-persona'),
    path('get-by-pk/<str:id_usuario>/',views.GetByIdUsuario.as_view(),name='get-by-pk'),
    path('password-unblock-complete/', views.UnBlockUserPassword.as_view(), name='password-unblock-complete'),
    path('reenviar-correo-verificacion-usuario/<str:id_usuario>/', views.ReenviarCorreoVerificacionDeUsuario.as_view(), name='reenviar-correo-verificacion-usuario'),

    #Login
    path('login/get-list/', views.LoginListApiViews.as_view(),name='login-get'),
    path('login/get-by-id/<str:pk>/', views.LoginConsultarApiViews.as_view(),name='login-id-get'),
    #LoginErroneo
    path('login-erroneo/get-list/', views.LoginErroneoListApiViews.as_view(),name='login-erroneo-get'),
    path('login-erroneo/get-by-id/<str:pk>/', views.LoginErroneoConsultarApiViews.as_view(),name='login-erroneo-id-get'),
    path('deactivate/<str:id_persona>/', views.DeactivateUsers.as_view(),name='deactivate-user'),
    path('historico-activacion/<str:id_usuario_afectado>/', views.BusquedaHistoricoActivacion.as_view(),name='historico-activacion'),
    path('usuario/interno-a-externo/<str:id_usuario>/', views.UsuarioInternoAExterno.as_view(), name='usuario-interno-a-externo'),

    
]