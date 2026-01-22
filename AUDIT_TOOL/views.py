from django.shortcuts import render
from django.http import HttpResponse
from .tasks import add_numbers, monitor_task_status,find_2G_audit_HRY,find_2G_audit_KOL,find_2G_audit_PNB
from .models import Task
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os
import uuid
import datetime

class TaskList(APIView):
    def get(self, request):
        print(request.user)
        date=datetime.datetime.now().date()
        print(date) 
        tasks = Task.objects.filter(created_at__date=date,user=request.user)
        # tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


def dashboard(request):
    # Retrieve all tasks from the database
    tasks = Task.objects.all()
    return render(request, 'dashboard.html', {'tasks': tasks})



@api_view(['POST'])
def audit_2g(request):
    print(request.data)
    print(request.user)
    DUMP_2G = request.FILES.get("2G_Dump") 
    BSC_SITE = request.FILES.get("BSC_SITE") 
    GPL_2G = request.FILES.get("2G_GPL") 
    circle = request.data.get("circle")
    output_file_save_name= str(DUMP_2G.name) + "_" + str(uuid.uuid1())
    
    dump_2g_path = default_storage.save('tmp/' + DUMP_2G.name, ContentFile(DUMP_2G.read()))
    bsc_site_path = default_storage.save('tmp/' + BSC_SITE.name, ContentFile(BSC_SITE.read()))
    gpl_2g_path = default_storage.save('tmp/' + GPL_2G.name, ContentFile(GPL_2G.read()))

    dump_2g_abs_path = os.path.join(settings.MEDIA_ROOT, dump_2g_path)
    bsc_site_abs_path = os.path.join(settings.MEDIA_ROOT, bsc_site_path)
    gpl_2g_abs_path = os.path.join(settings.MEDIA_ROOT, gpl_2g_path)
    
    if circle == "HRY":
        q = find_2G_audit_HRY.delay(dump_2g_abs_path, bsc_site_abs_path, gpl_2g_abs_path,output_file_save_name)
    if circle == "KOL":
        q = find_2G_audit_KOL.delay(dump_2g_abs_path, bsc_site_abs_path, gpl_2g_abs_path,output_file_save_name)
    if circle == "PNB":
        q = find_2G_audit_PNB.delay(dump_2g_abs_path, bsc_site_abs_path, gpl_2g_abs_path,output_file_save_name)
    # q=find_2G_audit.delay(DUMP_2G,BSC_SITE,GPL_2G)
    task_id=q.id
    print(request.user)
    user=request.user
    task = Task.objects.create(task_id=task_id,app_name="2G_AUDIT" ,status='pending', user=user, file_link="",circle = circle)
    user_name=request.user.username
    monitor_task_status.delay(user_name,task_id, task.pk,output_file_save_name, circle)
    return Response({'status': True,"message":f"you will get a mail shortly including the output link Note yor task id:{task_id}","task_id":task_id}, status=status.HTTP_200_OK)