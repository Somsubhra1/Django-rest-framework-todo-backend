from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated, NotFound
from .serializers import TaskSerializer
from .models import Task
import jwt
import os

JWT_SECRET = os.environ.get('JWT_SECRET')

# Create your views here.

# Specify which request types to listen to in @api_view()


@api_view(['GET'])
def apiOverView(request):

    api_urls = {
        'List': '/task-list/',
        'Detail View': '/task-detail/<int:pk>/',
        'Create': '/task-create/',
        'Update': '/task-update/<int:pk>/',
        'Delete': '/task-delete/<int:pk>/',
    }
    # Response() handles the API View response
    return Response(api_urls)


@api_view(['GET'])
def taskList(request):

    token = request.COOKIES.get('jwt')

    if not token:
        raise NotAuthenticated('Unauthenticated')

    try:
        payload = jwt.decode(token, JWT_SECRET, ['HS256'])
    except jwt.ExpiredSignatureError:
        raise NotAuthenticated('Unauthenticated')

    # Getting all tasks from DB
    tasks = Task.objects.filter(user=payload['id'])

    # Serializing the database data as API response
    # many=True should be kept when we expect multiple data from model
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def taskDetail(request, pk):

    token = request.COOKIES.get('jwt')

    if not token:
        raise NotAuthenticated('Unauthenticated')

    try:
        payload = jwt.decode(token, JWT_SECRET, ['HS256'])
    except jwt.ExpiredSignatureError:
        raise NotAuthenticated('Unauthenticated')

    task = Task.objects.filter(id=pk, user=payload['id']).first()

    serializer = TaskSerializer(task, many=False)

    return Response(serializer.data)


@api_view(['POST'])
def taskCreate(request):

    token = request.COOKIES.get('jwt')

    if not token:
        raise NotAuthenticated('Unauthenticated')

    try:
        payload = jwt.decode(token, JWT_SECRET, ['HS256'])
    except jwt.ExpiredSignatureError:
        raise NotAuthenticated('Unauthenticated')

    request.data['user'] = payload['id']

    serializer = TaskSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['PATCH'])
def taskUpdate(request, pk):

    token = request.COOKIES.get('jwt')

    if not token:
        raise NotAuthenticated('Unauthenticated')

    try:
        payload = jwt.decode(token, JWT_SECRET, ['HS256'])
    except jwt.ExpiredSignatureError:
        raise NotAuthenticated('Unauthenticated')

    task = Task.objects.filter(id=pk, user=payload['id']).first()

    if not task:
        raise NotFound('Task not found')

    request.data['user'] = payload['id']

    serializer = TaskSerializer(instance=task, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def taskDelete(request, pk):

    token = request.COOKIES.get('jwt')

    if not token:
        raise NotAuthenticated('Unauthenticated')

    try:
        payload = jwt.decode(token, JWT_SECRET, ['HS256'])
    except jwt.ExpiredSignatureError:
        raise NotAuthenticated('Unauthenticated')

    task = Task.objects.filter(id=pk, user=payload['id']).first()

    if not task:
        raise NotFound('Task not found!')

    task.delete()

    return Response({'success': True})
