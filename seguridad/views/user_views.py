from django.core import signing
from urllib.parse import quote_plus
from backend.settings.base import FRONTEND_URL
from django.urls import reverse
from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from seguridad.models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from django.contrib.sites.shortcuts import get_current_site
from seguridad.utils import Util
from rest_framework import status
from seguridad.serializers.user_serializers import RecuperarUsuarioSerializer, SetNewPasswordSerializer, UserSerializer, UserSerializerWithToken, UserRolesSerializer, RegisterSerializer  ,LoginSerializer, DesbloquearUserSerializer, SetNewPasswordUnblockUserSerializer, HistoricoActivacionSerializers, UsuarioBasicoSerializer, UsuarioFullSerializer, UsuarioInternoAExternoSerializers
from rest_framework import status
from seguridad.serializers.user_serializers import UserSerializer, UserSerializerWithToken, UserRolesSerializer, RegisterExternoSerializer,LoginErroneoSerializers,LoginSerializers
from datetime import datetime
from django.contrib.sessions.models import Session
from rest_framework.exceptions import NotFound,ValidationError, PermissionDenied

from geojson.models.personas_models import Personas


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def roles(request):
    roles = UsuariosRol.objects.all()
    serializers = UserRolesSerializer(roles, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)

class GetUserRoles(generics.ListAPIView):
    queryset = UsuariosRol.objects.all()
    serializer_class = UserRolesSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request, pk):
    try:
        user = User.objects.get(id_usuario=pk)
        pass
    except:
        raise NotFound('No existe ningún usuario con este ID')
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

"""@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserAdmin(request, pk):
    user = User.objects.get(id_usuario=pk)

    data = request.data

    user.nombre_de_usuario= data['email']
    user.email = data['email']
    user.is_blocked = data['is_blocked']


    user.save()

    serializer = UserSerializer(user, many=False)

    return Response(serializer.data)"""

class UnBlockUserPassword(generics.GenericAPIView):
    serializer_class = SetNewPasswordUnblockUserSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success':True, 'detail':'Usuario Desbloqueado'}, status=status.HTTP_200_OK)

class LoginConsultarApiViews(generics.RetrieveAPIView):
    serializer_class=LoginSerializers
    queryset = Login.objects.all()

class LoginListApiViews(generics.ListAPIView):
    serializer_class=LoginSerializers
    queryset = Login.objects.all()

class DeactivateUsers(generics.ListAPIView):
    serializer_class=LoginSerializers
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def post(self, request, id_persona):
        usuario = self.queryset.all().filter(persona__id_persona = id_persona).first()
        sesiones = Session.objects.all()
        
        if usuario:
            for sesion in sesiones:
                if sesion.get_decoded().get('_auth_user_id') == usuario.id_usuario:
                    sesion.delete()
            usuario.is_active = False
            usuario.save()
            
            return Response({'success':True, 'detail':'Se eliminó la sesión del usuario elegido'}, status=status.HTTP_200_OK)
        else:
            raise ValidationError('No se encontró el usuario para la persona ingresada')

#__________________LoginErroneo

class LoginErroneoConsultarApiViews(generics.RetrieveAPIView):
    serializer_class=LoginErroneoSerializers
    queryset = LoginErroneo.objects.all()

class LoginErroneoListApiViews(generics.ListAPIView):
    serializer_class=LoginErroneoSerializers
    queryset = LoginErroneo.objects.all()

# class LoginApiView(generics.CreateAPIView):
#     serializer_class=LoginSerializer

#     def post(self, request):
#         data = request.data
#         user = User.objects.filter(nombre_de_usuario=str(data['nombre_de_usuario']).lower()).first()
        
#         ip = Util.get_client_ip(request)
#         device = Util.get_client_device(request)
#         if user:
#             if user.is_active:
#                 roles = UsuariosRol.objects.filter(id_usuario=user.id_usuario).values()
#                 rol_id_list = [rol['id_rol_id'] for rol in roles]
#                 permisos_list = []
#                 for rol in rol_id_list:
#                     permisos = PermisosModuloRol.objects.filter(id_rol=rol).values()
#                     permisos_list.append(permisos)
               
#                 try:
#                     login_error = LoginErroneo.objects.filter(id_usuario=user.id_usuario).last()
                    
#                     serializer = self.serializer_class(data=data)
#                     serializer.is_valid(raise_exception=True)

#                     login = Login.objects.create(
#                         id_usuario = user,
#                         dirip = str(ip),
#                         dispositivo_conexion = device
#                     )

#                     LoginPostSerializers(login, many=False)

#                     if login_error:
#                         login_error.contador = 0
#                         login_error.save()
                    
#                     # REPRESENTANTE LEGAL
#                     representante_legal=Personas.objects.filter(representante_legal=user.persona.id_persona)
#                     representante_legal_list=RepresentanteLegalGetSerializer(representante_legal, many=True)
#                     representante_legal_list=representante_legal_list.data
                    
#                     # APODERADOS
#                     apoderados=ApoderadoPersona.objects.filter(persona_apoderada=user.persona.id_persona)
#                     apoderados_list=ApoderadoPersonaGetSerializer(apoderados, many=True)
#                     apoderados_list=apoderados_list.data
                    
#                     # DEFINIR SI UN USUARIO SI O SI DEBE TENER UN PERMISO O NO
#                     permisos_list = permisos_list[0] if permisos_list else []
                    
#                     serializer_data = serializer.data

#                     #TAMAÑO MAXIMO DE ARCHIVOS
#                     #FormatosTiposMedioGetSerializer
#                     maximo_archivo = FormatosTiposMedio.objects.filter(control_tamagno_max__isnull=False)
                    
#                     data_archivos = FormatosTiposMedioGetSerializer(maximo_archivo, many=True)
                    
#                     user_info={'userinfo':serializer_data,'permisos':permisos_list,'representante_legal':representante_legal_list, 'apoderados':apoderados_list,'tamagno_archivos':data_archivos.data}
#                     sms = "Bia Cormacarena te informa que se ha registrado una conexion con el usuario " + user.nombre_de_usuario + " en la fecha " + str(datetime.now(pytz.timezone('America/Bogota')))
                    
#                     if user.persona.telefono_celular:
#                         Util.send_sms(user.persona.telefono_celular, sms)
#                     else:
#                         subject = "Login exitoso"
#                         template = "notificacion-login.html"
#                         Util.notificacion(user.persona,subject,template,nombre_de_usuario=user.nombre_de_usuario)
                    
#                     return Response({'userinfo':user_info}, status=status.HTTP_200_OK)
#                 except:
#                     login_error = LoginErroneo.objects.filter(id_usuario=user.id_usuario).first()
#                     if login_error:
#                         if login_error.contador < 3:
#                             hour_difference = datetime.utcnow().replace(tzinfo=None) - login_error.fecha_login_error.replace(tzinfo=None)
#                             hour_difference = (hour_difference.days * 24) + (hour_difference.seconds//3600)
#                             if hour_difference < 24:
#                                 login_error.contador += 1
#                                 login_error.restantes = 3 - login_error.contador
#                                 login_error.save()
#                             else :
#                                 login_error.contador = 1
#                                 login_error.save()
#                             if login_error.contador == 3:
#                                 user.is_blocked = True
#                                 user.save()
                                
#                                 cod_operacion_instance = OperacionesSobreUsuario.objects.filter(cod_operacion='B').first()
                        
#                                 HistoricoActivacion.objects.create(
#                                     id_usuario_afectado = user,
#                                     cod_operacion = cod_operacion_instance,
#                                     fecha_operacion = datetime.now(),
#                                     justificacion = 'Usuario bloqueado por exceder los intentos incorrectos en el login',
#                                     usuario_operador = user,
#                                 )
                                

#                                 # raise PermissionDenied('Su usuario ha sido bloqueado')
#                                 return Response({'success':False, 'detail':'Su usuario ha sido bloqueado'}, status=status.HTTP_403_FORBIDDEN)
#                             serializer = LoginErroneoPostSerializers(login_error, many=False)
#                             # try:
#                             #     raise ValidationError('La contraseña es invalida')
#                             # except ValidationError as e:
#                             return Response({'success':False, 'detail':'La contraseña es invalida', 'login_erroneo': serializer.data}, status=status.HTTP_400_BAD_REQUEST)
#                         else:
#                             if user.is_blocked:
#                                 raise PermissionDenied('Su usuario está bloqueado, debe comunicarse con el administrador')
#                             else:
#                                 login_error.contador = 1
#                                 login_error.save()
#                                 serializer = LoginErroneoPostSerializers(login_error, many=False)
#                                 # try:
#                                 #     raise ValidationError('La contraseña es invalida')
#                                 # except ValidationError as e:
#                                 return Response({'success':False, 'detail':'La contraseña es invalida', 'login_erroneo': serializer.data}, status=status.HTTP_400_BAD_REQUEST)
#                     else:
#                         if user.is_blocked:
#                             raise PermissionDenied('Su usuario está bloqueado, debe comunicarse con el administrador')
#                         else:
#                             login_error = LoginErroneo.objects.create(
#                                 id_usuario = user,
#                                 dirip = str(ip),
#                                 dispositivo_conexion = device,
#                                 contador = 1
#                             )
#                         login_error.restantes = 3 - login_error.contador
#                         serializer = LoginErroneoPostSerializers(login_error, many=False)
#                         # try:
#                         #     raise ValidationError('La contraseña es invalida')
#                         # except ValidationError as e:
#                         return Response({'success':False, 'detail':'La contraseña es invalida', 'login_erroneo': serializer.data}, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 try:
#                     raise PermissionDenied('Usuario no activado')
#                 except PermissionDenied as e:
#                     return Response({'success':False, 'detail':'Usuario no activado', 'data':{'modal':True, 'id_usuario':user.id_usuario, 'tipo_usuario':user.tipo_usuario}}, status=status.HTTP_403_FORBIDDEN)
#         else:
#             UsuarioErroneo.objects.create(
#                 campo_usuario = str(data['nombre_de_usuario']).lower(),
#                 dirip = str(ip),
#                 dispositivo_conexion = device
#             )
#             return Response({'success':False, 'detail':'No existe el nombre de usuario ingresado'}, status=status.HTTP_400_BAD_REQUEST)

class SetNewPasswordApiView(generics.GenericAPIView):
    serializer_class=SetNewPasswordSerializer
    
    def patch(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        password = request.data.get('password')
        uidb64 = request.data.get('uidb64')
        id = int(signing.loads(uidb64)['user'])
        user = User.objects.filter(id_usuario=id).first()
        
        if user.password and user.password != "":
            message = 'Contraseña actualizada'
        else:
            user.is_active = True
            user.activated_at = datetime.now()
            
            cod_operacion_instance = OperacionesSobreUsuario.objects.filter(cod_operacion='A').first()
            
            HistoricoActivacion.objects.create(
                id_usuario_afectado=user,
                justificacion='Activación Inicial del Usuario',
                usuario_operador=user,
                cod_operacion=cod_operacion_instance
            )
            
            subject = "Verificación exitosa"
            template = "verificacion-cuenta.html"
            absurl = FRONTEND_URL+"#/auth/login"
            Util.notificacion(user.persona,subject,template,absurl=absurl)
            
            message = 'Usuario activado correctamente'
        
        user.set_password(password)
        user.save()
        
        return Response({'success':True, 'detail':message},status=status.HTTP_200_OK)

@api_view(['POST'])
def uploadImage(request):
    data = request.data
    user_id = data['id_usuario']
    user = User.objects.get(id_usuario=user_id)

    user.profile_img = request.FILES.get('image') # EDITAR
    user.save()

    return Response('Image was uploaded')
        
class ReenviarCorreoVerificacionDeUsuario(generics.UpdateAPIView):
    serializer_class = RegisterExternoSerializer
    
    def put(self,request,id_usuario):
        
        user = User.objects.filter(id_usuario=id_usuario).first()
        
        if user.is_active == False and user.tipo_usuario == "E":
            
            redirect_url=request.data.get('redirect_url','')
            redirect_url=quote_plus(redirect_url)

            token = RefreshToken.for_user(user)

            current_site=get_current_site(request).domain

            persona = Personas.objects.filter(id_persona = user.persona.id_persona).first()

            relativeLink= reverse('verify')
            absurl= 'http://'+ current_site + relativeLink + "?token="+ str(token) + '&redirect-url=' + redirect_url

            subject = "Verifica tu usuario"
            template = "activación-de-usuario.html"

            Util.notificacion(persona,subject,template,absurl=absurl,email=persona.email)
            
            return Response({"success":True, 'detail':"Se ha enviado un correo a "+persona.email+" con la información para la activación del usuario en el sistema"})
            
        else: 
            raise PermissionDenied('El usuario ya se encuentra activado o es un usuario interno')

class BusquedaHistoricoActivacion(generics.ListAPIView):
    serializer_class = HistoricoActivacionSerializers
    queryset = HistoricoActivacion.objects.all()

    def get_queryset(self):
        id_usuario = self.kwargs['id_usuario_afectado']
        queryset = HistoricoActivacion.objects.filter(id_usuario_afectado=id_usuario)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
            return Response({'success':True, 'detail':'Se encontró el siguiente historico de activación para ese usuario', 'data': data}, status=status.HTTP_200_OK)
        else:
            raise NotFound('No se encontro historico de activación para ese usuario')

class UsuarioInternoAExterno(generics.UpdateAPIView):
    serializer_class = UsuarioInternoAExternoSerializers
    queryset = User.objects.all()

    def put(self, request, id_usuario):
        user_loggedin = request.user
        serializador = self.serializer_class(user_loggedin)
        usuario = User.objects.filter(id_usuario=id_usuario, tipo_usuario='I', is_active=False).first()
        if usuario:
            usuario.tipo_usuario = 'E'
            usuario.is_active = True
            usuario.save()
            
            cod_operacion_instance = OperacionesSobreUsuario.objects.filter(cod_operacion='A').first()
            
            HistoricoActivacion.objects.create(
                id_usuario_afectado=usuario,
                justificacion='Usuario activado desde el portal, con cambio de INTERNO a EXTERNO',
                usuario_operador=user_loggedin,
                cod_operacion=cod_operacion_instance
            )

            subject = "Cambio a usuario externo"
            template = "cambio-tipo-de-usuario.html"
            Util.notificacion(usuario.persona,subject,template,nombre_de_usuario=usuario.nombre_de_usuario)

            return Response({'success':True, 'detail':'Se activo como usuario externo', 'data': serializador.data}, status=status.HTTP_200_OK)
        else:
            raise ValidationError('El usuario no existe o no cumple con los requisitos para ser convertido en usuario externo')
        
#BUSQUEDA DE USUARIOS ENTREGA 18 UD.11

class BusquedaByNombreUsuario(generics.ListAPIView):
    serializer_class = UsuarioBasicoSerializer
    queryset = User.objects.all()
        
    def get(self,request):
        
        nombre_de_usuario = str(request.query_params.get('nombre_de_usuario', '')).lower()
        
        busqueda_usuario = self.queryset.all().filter(nombre_de_usuario__icontains=nombre_de_usuario)
        
        serializador = self.serializer_class(busqueda_usuario,many=True, context = {'request':request})
        
        return Response({'succes':True, 'detail':'Se encontraron los siguientes usuarios.','data':serializador.data},status=status.HTTP_200_OK)

#BUSQUEDA ID PERSONA Y RETORNE LOS DATOS DE LA TABLA USUARIOS

class BuscarByIdPersona(generics.RetrieveAPIView):
    serializer_class = UsuarioBasicoSerializer
    queryset = User.objects.all()
    
    def get(self,request,id_persona):
        usuarios = self.queryset.all().filter(persona=id_persona)
            
        serializador = self.serializer_class(usuarios,many=True, context = {'request':request})
        return Response({'succes':True, 'detail':'Se encontraron los siguientes usuarios.','data':serializador.data},status=status.HTTP_200_OK)
    
class GetByIdUsuario(generics.RetrieveAPIView):
    serializer_class = UsuarioFullSerializer
    queryset = User.objects.all()
    
    def get(self,request,id_usuario):
        usuario = self.queryset.all().filter(id_usuario=id_usuario).first()
        
        if not usuario:
            raise NotFound('No se encontró el usuario ingresado')
        
        serializador = self.serializer_class(usuario, context = {'request':request})
        return Response({'succes':True, 'detail':'Se encontró la información del usuario', 'data':serializador.data},status=status.HTTP_200_OK)
    

class RecuperarNombreDeUsuario(generics.UpdateAPIView):
    serializer_class = RecuperarUsuarioSerializer
    queryset = User.objects.all()
    
    def put(self,request):
        data = request.data
        
        if not data.get('tipo_documento') or not data.get('numero_documento') or not data.get('email'):
            raise ValidationError('Debe ingresar los parámetros respectivos: tipo de documento, número de documento, email')
        
        persona = Personas.objects.filter(tipo_documento=data['tipo_documento'], numero_documento=data['numero_documento'], email=data['email']).first()
        
        if persona:
            usuario = self.queryset.all().filter(persona = persona.id_persona).exclude(id_usuario=1).first()
            
            if usuario:
                
                subject = "Verifica tu usuario"
                template = "recuperar-usuario.html"

                Util.notificacion(persona,subject,template,nombre_de_usuario=usuario.nombre_de_usuario)

                return Response({'success':True, 'detail':'Se ha enviado el correo'},status=status.HTTP_200_OK)
            
            else:
                raise NotFound('No existe usuario') 
        raise NotFound('No existe usuario')