from django.utils.decorators import decorator_from_middleware
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from todo_drf.middleware import JWTDecodeMiddleware
from .serializers import TaskSerializer
from .models import Task

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
# creating middleware decorator from class to use on views
@decorator_from_middleware(JWTDecodeMiddleware)
def taskList(request):

    print(request.user)

    # Getting all tasks from DB
    tasks = Task.objects.filter(user=request.user)

    # Serializing the database data as API response
    # many=True should be kept when we expect multiple data from model
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@decorator_from_middleware(JWTDecodeMiddleware)
def taskDetail(request, pk):

    task = Task.objects.filter(id=pk, user=request.user).first()

    serializer = TaskSerializer(task, many=False)

    return Response(serializer.data)


@api_view(['POST'])
@decorator_from_middleware(JWTDecodeMiddleware)
def taskCreate(request):

    request.data['user'] = request.user.id

    serializer = TaskSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['PATCH'])
@decorator_from_middleware(JWTDecodeMiddleware)
def taskUpdate(request, pk):

    task = Task.objects.filter(id=pk, user=request.user).first()

    if not task:
        raise NotFound('Task not found')

    request.data['user'] = request.user.id

    serializer = TaskSerializer(instance=task, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
@decorator_from_middleware(JWTDecodeMiddleware)
def taskDelete(request, pk):

    task = Task.objects.filter(id=pk, user=request.user).first()

    if not task:
        raise NotFound('Task not found!')

    task.delete()

    return Response({'success': True})
