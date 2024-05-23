from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import *
from rest_framework.response import Response
from .models import *
from .permissions import IsClient
from .serializers import *

@api_view(['POST'])
def login_views(request):
    serializers = LoginSerializers(data=request.data)
    if serializers.is_valid():
        try:
            user = User.objects.get(login=serializers.validated_data['login'])
        except:
            return Response({'error': {'code': 401, 'message': 'Authentication failed'}})
        token,_= Token.objects.get_or_create(user=user)
        if user.is_staff:
            isAdmin = True
        else:
            isAdmin = False
            return Response({"data": {'user_token': token.key, "isAdmin": isAdmin}})
        return Response({'error': {'code': 422, 'message': "Validation error", "errors": serializers.errors}})

@api_view(['POST'])
def register_views(request):
    serializers = RegistrationSerializers(data=request.data)
    if serializers.is_valid():
        user = serializers.save()
        token = Token.objects.create(user=user)
        if user.is_staff:
            isAdmin = True
        else:
            isAdmin = False
            return Response({"data": {'user_token': token.key, "isAdmin": isAdmin}})
    return Response({'error': {'code': 422, 'message': "Validation error", "errors": serializers.errors}})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    request.user.auth_token.delete()
    return Response({'message': 'logout'})

@api_view(['GET'])
def getApps(request):
    if request.user.is_staff:
        return Response(
            {'error': {'code': 403, 'message': "Forbidden for you"}})
    elif request.user.is_authenticated:
        apps = Application.objects.filter(user=request.user)
    else:
        apps = Application.objects.all()
    serializers = ApplicationSerializers(apps, many=True)
    data = []
    for app in serializers.data:
        newApp = {
            "id": app['id'],
            "name": app['name'],
            "auto_num": app['auto_num'],
            "desc": app['desc'],
            "status": app['status']['name'],
        }
        data.append(newApp)
    return Response({'data': data})

@api_view(['POST'])
@permission_classes([IsClient])
def creatApp(request):
    serializers = ApplicationSerializersUser(data=request.data)
    if serializers.is_valid():
        Application.odjects.create(name=serializers.validated_data['data'],
                                   auto_num=serializers.validated_data['auto_num'],
                                   desc=serializers.validated_data['desc'],
                                   user=request.user,
                                   status=Status.objects.get(pk=1))
        return Response({'data': {'message': "Your claim added"}})
    return Response({'error': {'code': 422, 'message': "Validation error", "errors": serializers.errors}})


@api_view(['DELETE'])
@permission_classes([IsClient])
def delete_app_view(request, pk):
    try:
        app = Application.objects.get(pk=pk)
    except:
        return Response({"error": {'code': 404, "message": "Not Found"}})
    app.delete()
    return Response({'data': {'message': "Claim was removed"}})


@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAdminUser])
def redact_or_delete_app(request, pk):
    try:
        app = Application.objects.get(pk=pk)
    except:
        return Response({"error": {'code': 404, "message": "Not Found"}})
    if request.method == 'DELETE':
        app.delete()
        return Response({'data': {'message': "Claim was removed"}})
    elif request.method == 'PATCH':
        serializers = ApplicationSerializersAdmin(data=request.data, instance=app, partial=True)

        if serializers.is_valid():
            serializers.save()
            app = serializers.data
            status = Status.objects.get(pk=int(app['status']))
            newApp = {
                'id': app['id'],
                'name': app['name'],
                'auto_num': app['auto_num'],
                'desc': app['desc'],
                'status': status.name
            }

            return Response({"data": newApp})
        return Response({'error': {'code': 422, 'message': "Validation error", "errors": serializers.errors}})
