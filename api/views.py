from rest_framework.decorators import api_view
from rest_framework.response import Response
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
def taskList(request):

    # Getting all tasks from DB
    tasks = Task.objects.all()

    # Serializing the database data as API response
    # many=True should be kept when we expect multiple data from model
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def taskDetail(request, pk):
    task = Task.objects.get(id=pk)

    serializer = TaskSerializer(task, many=False)

    return Response(serializer.data)


@api_view(['POST'])
def taskCreate(request):
    serializer = TaskSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['PATCH'])
def taskUpdate(request, pk):

    task = Task.objects.get(id=pk)
    serializer = TaskSerializer(instance=task, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def taskDelete(request, pk):
    task = Task.objects.get(id=pk)

    task.delete()

    return Response({'success': True})
