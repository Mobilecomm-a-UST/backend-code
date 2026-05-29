from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from django.contrib.auth.models import User


@api_view(['GET'])
def get_users(request):
    users = User.objects.all().values()
    return Response(list(users))




   

@api_view(['POST'])
def fatch_username(request):
    username = request.data.get("username")
    try:
        queryset = User.objects.all()

        if username:
            queryset = queryset.filter(username__icontains=username)

        users = queryset.values_list("username", flat=True).distinct()[:15]

        return Response({
            "status": True,
            "users": list(users),
            "message": "user name found"
        }, status=200)

    except Exception as e:
        return Response({
            "message": False,
            "error": str(e)
        }, status=500)
    




# ================= TASK CRUD =================

@api_view(['POST'])
def create_task(request):
    serializer = DailyreviewTaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
def get_tasks(request):
    tasks = DailyreviewTask.objects.all()
    serializer = DailyreviewTaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_task(request, pk):
    try:
        task = DailyreviewTask.objects.get(pk=pk)
    except DailyreviewTask.DoesNotExist:
        return Response({"error": "Task not found"}, status=404)

    serializer = DailyreviewTaskSerializer(task)
    return Response(serializer.data)


@api_view(['PUT'])
def update_task(request, pk):
    try:
        task = DailyreviewTask.objects.get(pk=pk)
    except DailyreviewTask.DoesNotExist:
        return Response({"error": "Task not found"}, status=404)

    serializer = DailyreviewTaskSerializer(task, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
def delete_task(request, pk):
    try:
        task = DailyreviewTask.objects.get(pk=pk)
    except DailyreviewTask.DoesNotExist:
        return Response({"error": "Task not found"}, status=404)

    task.delete()
    return Response({"message": "Task deleted successfully"})


# ================= DAILY TASK REVIEW =================

@api_view(['POST'])
def create_daily_task_review(request):
    
    serializer = DailytaskreviewmodelSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
def get_daily_task_reviews(request):
    reviews = Dailytaskreviewmodel.objects.all()
    serializer = DailytaskreviewmodelSerializer(reviews, many=True)
    return Response(serializer.data)


# ================= OVERALL DATA =================

@api_view(['GET'])
def get_all_data(request):
    reviews = Dailytaskreviewmodel.objects.all()
    # owners = DailytaskreviewOwner.objects.all()
    tasks = DailyreviewTask.objects.all()

    return Response({
        "daily_task_reviews": DailytaskreviewmodelSerializer(reviews, many=True).data,
        # "owners": DailytaskreviewOwnerSerializer(owners, many=True).data,
        "tasks": DailyreviewTaskSerializer(tasks, many=True).data
    })