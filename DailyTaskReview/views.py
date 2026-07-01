from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from django.contrib.auth.models import User
from mailapp.tasks import send_email
from datetime import datetime
from django.utils import timezone
from collections import Counter
from django.db.models import Count


def SplitFirstNameFromEmail(email_list):
    names = []
    for email in email_list:
        if isinstance(email, list):
            email = email[0]

        names.append(str(email).split('@')[0].split('.')[0])

    return ",".join(names)

def format_datetime(dt_string):

    if not dt_string:
        return ""

    dt = datetime.fromisoformat(dt_string)
    return dt.strftime("%d-%m-%Y (%H:%M)")

def send_email_assignTask(task_Data):

    body = f"""
            <html>
            <body style="font-family:Arial, sans-serif;background-color:#f5f5f5;">

            <div style="max-width:750px;margin:auto;background:white;padding:30px;border-radius:10px;">

                <h2 style="color:#1f4e79;">
                    📌 New Task Assigned
                </h2>

                <p>Hi {SplitFirstNameFromEmail(task_Data['owner'])},</p>

                <p>
                
                    You have been assigned a new task by
                    <b>{task_Data['assigned_by']}</b>.
                    Please review the task details below.
                </p>

                <table style="width:100%;border-collapse:collapse;">

                    <tr>
                        <td style="padding:10px;border:1px solid #ddd;"><b>Ticket No.</b></td>
                        <td style="padding:10px;border:1px solid #ddd;">{task_Data['task_id']}</td>
                    </tr>

                    <tr>
                        <td style="padding:10px;border:1px solid #ddd;"><b>OEM</b></td>
                        <td style="padding:10px;border:1px solid #ddd;">{task_Data['oem']}</td>
                    </tr>

                    <tr>
                        <td style="padding:10px;border:1px solid #ddd;"><b>Task</b></td>
                        <td style="padding:10px;border:1px solid #ddd;">{task_Data['task']}</td>
                    </tr>

                    <tr>
                        <td style="padding:10px;border:1px solid #ddd;"><b>Priority</b></td>
                        <td style="padding:10px;border:1px solid #ddd;color:red;">
                            <b>{task_Data['priority']}</b>
                        </td>
                    </tr>

                    <tr>
                        <td style="padding:10px;border:1px solid #ddd;"><b>Status</b></td>
                        <td style="padding:10px;border:1px solid #ddd;">
                            {task_Data['status']}
                        </td>
                    </tr>

                    <tr>
                        <td style="padding:10px;border:1px solid #ddd;"><b>Slot</b></td>
                        <td style="padding:10px;border:1px solid #ddd;">
                            {task_Data['slot']}
                        </td>
                    </tr>

                    <tr>
                        <td style="padding:10px;border:1px solid #ddd;"><b>Frequency</b></td>
                        <td style="padding:10px;border:1px solid #ddd;">
                            {task_Data['frequency']}
                        </td>
                    </tr>

                    <tr>
                        <td style="padding:10px;border:1px solid #ddd;"><b>Assigned At</b></td>
                        <td style="padding:10px;border:1px solid #ddd;">
                            {format_datetime(task_Data['assigned_at'])}
                        </td>
                    </tr>

                    <tr>
                        <td style="padding:10px;border:1px solid #ddd;"><b>Deadline</b></td>
                        <td style="padding:10px;border:1px solid #ddd; color:red;">
                            <b>
                            {format_datetime(task_Data['deadline'])}
                            </b>
                        </td>
                    </tr>

                    <tr>
                        <td style="padding:10px;border:1px solid #ddd;"><b>Remarks</b></td>
                        <td style="padding:10px;border:1px solid #ddd;">
                            {task_Data['remarks']}
                        </td>
                    </tr>

                </table>

                <br>
                <div style="text-align:center; margin-top:20px;">

                    <a
                        href="mailto:noreply@mcpspmis.com?subject=Task%20Update%20%7C%20{task_Data['task_id']}%20%7C%20Completed&body=Completed"
                        style="
                            display:inline-block;
                            background:#28a745;
                            color:white;
                            padding:12px 22px;
                            text-decoration:none;
                            border-radius:6px;
                            font-weight:bold;
                            margin-right:10px;">
                        ✅ Completed
                    </a>

                    <a
                        href="mailto:noreply@mcpspmis.com?subject=Task%20Update%20%7C%20{task_Data['task_id']}%20%7C%20In%20Progress&body=In%20Progress"
                        style="
                            display:inline-block;
                            background:#ffc107;
                            color:#000;
                            padding:12px 22px;
                            text-decoration:none;
                            border-radius:6px;
                            font-weight:bold;
                            margin-right:10px;">
                        🔄 In Progress
                    </a>

                    <a
                        href="mailto:noreply@mcpspmis.com?subject=Task%20Update%20%7C%20{task_Data['task_id']}%20%7C%20Pending&body=Pending"
                        style="
                            display:inline-block;
                            background:#dc3545;
                            color:white;
                            padding:12px 22px;
                            text-decoration:none;
                            border-radius:6px;
                            font-weight:bold;">
                        ⏳ Pending
                    </a>

                </div>

                <br>

                <p>
                    Please update the task status accordingly.
                </p>

                <hr>

                <p style="font-size:12px;color:gray;">
                    This is an automated email generated by Daily Task Review System.
                </p>

            </div>

            </body>
            </html>
            """

    subject = f"NTA | {task_Data['task_id']}"

    to_mail = task_Data["owner"]
    to_mail = ";".join(to_mail)


    # cc_mail = task_Data["assigned_by"]
    cc_mail = ""


    send_email(
        to_mail,
        cc_mail,
        subject,
        body,
        None,
        True
    )

def send_email_updateTask(task_Data):

    status_color = "#28a745" if task_Data["status"] == "Completed" else "#ffc107"

    body = f"""
    <html>
    <body style="font-family:Arial, sans-serif;background-color:#f5f5f5;">

    <div style="max-width:750px;margin:auto;background:white;padding:30px;border-radius:10px;">

        <h2 style="color:#1f4e79;">
            🔔 Task Status Updated
        </h2>

        <p>Hello,</p>

        <p>
            The assigned user has updated the status of the following task.
        </p>

        <table style="width:100%;border-collapse:collapse;">

            <tr>
                <td style="padding:10px;border:1px solid #ddd;"><b>Ticket No.</b></td>
                <td style="padding:10px;border:1px solid #ddd;">{task_Data['task_id']}</td>
            </tr>

            <tr>
                <td style="padding:10px;border:1px solid #ddd;"><b>OEM</b></td>
                <td style="padding:10px;border:1px solid #ddd;">{task_Data['oem']}</td>
            </tr>

            <tr>
                <td style="padding:10px;border:1px solid #ddd;"><b>Task</b></td>
                <td style="padding:10px;border:1px solid #ddd;">{task_Data['task']}</td>
            </tr>

            <tr>
                <td style="padding:10px;border:1px solid #ddd;"><b>Updated By</b></td>
                <td style="padding:10px;border:1px solid #ddd;">
                    {task_Data.get('updated_by', 'N/A')}
                </td>
            </tr>

            <tr>
                <td style="padding:10px;border:1px solid #ddd;"><b>Current Status</b></td>
                <td style="padding:10px;border:1px solid #ddd;color:{status_color};">
                    <b>{task_Data['status']}</b>
                </td>
            </tr>

            <tr>
                <td style="padding:10px;border:1px solid #ddd;"><b>Priority</b></td>
                <td style="padding:10px;border:1px solid #ddd;">
                    {task_Data['priority']}
                </td>
            </tr>

            <tr>
                <td style="padding:10px;border:1px solid #ddd;"><b>Frequency</b></td>
                <td style="padding:10px;border:1px solid #ddd;">
                    {task_Data['frequency']}
                </td>
            </tr>

            <tr>
                <td style="padding:10px;border:1px solid #ddd;"><b>Deadline</b></td>
                <td style="padding:10px;border:1px solid #ddd;">
                    {format_datetime(task_Data['deadline'])}
                </td>
            </tr>

            <tr>
                <td style="padding:10px;border:1px solid #ddd;"><b>Remarks</b></td>
                <td style="padding:10px;border:1px solid #ddd;">
                    {task_Data['remarks']}
                </td>
            </tr>

        </table>

        <br>

        <div style="
            background-color:#f8f9fa;
            padding:15px;
            border-left:5px solid {status_color};
        ">

            <b>Status Update:</b><br><br>

            User <b>{task_Data.get('updated_by', 'N/A')}</b>
            has marked the task
            <b>{task_Data['task']}</b>
            as
            <b>{task_Data['status']}</b>.

        </div>

        <br>

        <hr>

        <p style="font-size:12px;color:gray;">
            This is an automated notification generated by Daily Task Review System.
        </p>

    </div>

    </body>
    </html>
    """

    if task_Data["status"] == "Completed":
        subject = f"✅ Task Completed | {task_Data['task_id']}"
    else:
        subject = f"🔔 Task Updated | {task_Data['task_id']}"

    # Mail goes to the assigner
    to_mail = task_Data["assigned_by"]

    # CC all owners
    cc_mail = ";".join(task_Data["owner"])

    send_email(
        to_mail,
        cc_mail,
        subject,
        body,
        None,
        True
    )


# ======= Add Task Table CRUD =======


@api_view(['POST'])
def add_task_to_table(request):
    serializer = AddTaskTableSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "message": "Task added successfully",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def get_tasks_from_table(request):
    tasks = AddTaskTable.objects.filter(userID=request.data.get('userID'))
    serializer = AddTaskTableSerializer(tasks, many=True)

    return Response(
        {
            "message": "Tasks fetched successfully",
            "data": serializer.data
        },
        status=status.HTTP_200_OK
    )

@api_view(['PUT'])
def update_task_in_table(request, pk):
    try:
        task = AddTaskTable.objects.get(id=pk)
    except AddTaskTable.DoesNotExist:
        return Response(
            {"error": "Task not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = AddTaskTableSerializer(task, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "message": "Task updated successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_task_from_table(request, pk):
    try:
        task = AddTaskTable.objects.get(id=pk)
    except AddTaskTable.DoesNotExist:
        return Response(
            {"error": "Task not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    task.delete()

    return Response(
        {
            "message": "Task deleted successfully"
        },
        status=status.HTTP_200_OK
    )


#  ====== =====API  Add Email Hierarchy  =================
@api_view(['POST'])
def add_email_hierarchy(request):
    serializer = ReportingEmailHierarchySerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "message": "Email hierarchy added successfully",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def get_email_hierarchy(request):
    email_hierarchy = ReportingEmailHierarchy.objects.filter(userID=request.data.get('userID'))
    serializer = ReportingEmailHierarchySerializer(email_hierarchy, many=True)

    return Response(
        {
            "message": "Email hierarchy fetched successfully",
            "data": serializer.data
            # "data": email_hierarchy
        },
        status=status.HTTP_200_OK
    )

@api_view(['PUT'])
def update_email_hierarchy(request, pk):
    try:
        email_hierarchy = ReportingEmailHierarchy.objects.get(id=pk)
    except ReportingEmailHierarchy.DoesNotExist:
        return Response(
            {"error": "Email hierarchy not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = ReportingEmailHierarchySerializer(email_hierarchy, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "message": "Email hierarchy updated successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_email_hierarchy(request, pk):
    try:
        email_hierarchy = ReportingEmailHierarchy.objects.get(id=pk)
    except ReportingEmailHierarchy.DoesNotExist:
        return Response(
            {"error": "Email hierarchy not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    email_hierarchy.delete()

    return Response(
        {
            "message": "Email hierarchy deleted successfully"
        },
        status=status.HTTP_200_OK
    )





# ================= Assign Task API function  =================



@api_view(['POST'])
def create_task(request):
    data = request.data.copy()
    data['task_type'] = 'assign'
    serializer = DailytaskreviewmodelSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        send_email_assignTask(serializer.data)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
def get_all_tasks(request):

    assigned_by = request.data.get('assigned_by')
    assigned_at = request.data.get('assigned_at')

    queryset = Dailytaskreviewmodel.objects.filter(
        task_type='assign',
        assigned_by=assigned_by,
        assigned_at__date=assigned_at
    )

    serializer = DailytaskreviewmodelSerializer(queryset, many=True)

    return Response(serializer.data)


@api_view(['PUT','POST'])
def update_task(request, pk):
    try:
        task = Dailytaskreviewmodel.objects.get(id=pk)
    except Dailytaskreviewmodel.DoesNotExist:
        return Response({"error": "Task not found"}, status=404)

    serializer = DailytaskreviewmodelSerializer(
        task,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)

    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
def delete_task(request, pk):
    try:
        task = Dailytaskreviewmodel.objects.get(id=pk)
    except Dailytaskreviewmodel.DoesNotExist:
        return Response({"error": "Task not found"}, status=404)

    task.delete()

    return Response(
        {"message": "Task deleted successfully"},
        status=200
    )



#  ==== ================= My Task API function  =================

# @api_view(['POST'])
# def get_my_tasks(request):
#     owner = request.data.get('owner')
#     assigned_at = request.data.get('assigned_at')
#     queryset = Dailytaskreviewmodel.objects.filter(
#         # task_type='received',
#         assigned_at__date=assigned_at,
#     )

#     if owner:
#         queryset = queryset.filter(owner__contains=[owner])

#     serializer = DailytaskreviewmodelSerializer(queryset, many=True)
#     return Response(serializer.data, status=200)


@api_view(['POST'])
def get_my_tasks(request):
    owner = request.data.get("owner")
    assigned_at = request.data.get("assigned_at")

    queryset = Dailytaskreviewmodel.objects.filter(
        assigned_at__date=assigned_at
    )

    if owner:
        owner = owner.strip().lower()

        queryset = [
            task for task in queryset
            if any(email.lower() == owner for email in (task.owner or []))
        ]

    serializer = DailytaskreviewmodelSerializer(queryset, many=True)
    return Response(serializer.data, status=200)


@api_view(['PUT', 'POST'])
def update_my_task(request, pk):
    try:
        task = Dailytaskreviewmodel.objects.get(
            id=pk,
            # task_type='received'
        )
    except Dailytaskreviewmodel.DoesNotExist:
        return Response(
            {"error": "Task not found"},
            status=404
        )
    if task.status == "Completed":
        return Response(
            {
                "error": "Task is already completed and cannot be modified."
            },
            status=400
        )
    serializer = DailytaskreviewmodelSerializer(
        task,
        data=request.data,
        partial=True
    )
    if serializer.is_valid():
        serializer.save()
        send_email_updateTask(serializer.data)
        return Response(
            serializer.data,
            status=200
        )
    return Response(
        serializer.errors,
        status=400
    )


# =================  Assign Task Dashboard API function  =================


@api_view(['POST'])
def get_user_wise_analytics(request):
    """
    POST body:
    {
        "assigned_by": "Girraj.Singh@ust.com",
        "date_from": "2026-06-01",
        "date_to":   "2026-06-19"
    }
    """

    assigned_by = request.data.get('assigned_by')
    date_from   = request.data.get('date_from')
    date_to     = request.data.get('date_to') or date_from

    # ── Validation ────────────────────────────────────────────
    if not assigned_by or not date_from:
        return Response(
            {"error": "assigned_by and date_from are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        datetime.strptime(date_from, "%Y-%m-%d")
        datetime.strptime(date_to,   "%Y-%m-%d")
    except ValueError:
        return Response(
            {"error": "Invalid date format. Use YYYY-MM-DD."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        qs = Dailytaskreviewmodel.objects.filter(
            assigned_by=assigned_by,
            assigned_at__date__gte=date_from,
            assigned_at__date__lte=date_to,
        )

        tasks = list(qs.values(
            'id', 'owner', 'status', 'priority',
            'deadline', 'oem', 'slot'
        ))

        now = timezone.now()

        # ── Global counters ────────────────────────────────────
        by_status   = {"Active": 0, "In Progress": 0, "Completed": 0, "Cancelled": 0}
        by_priority = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
        by_oem      = {}
        by_slot     = {"Morning": 0, "Afternoon": 0, "Evening": 0, "Night": 0}

        # ── Per-user counters ──────────────────────────────────
        user_stats  = {}

        for task in tasks:
            status_val = task.get('status', '')
            priority   = task.get('priority', '')
            oem        = task.get('oem', '') or 'Unknown'
            slot       = (task.get('slot', '') or '').capitalize()
            deadline   = task.get('deadline')

            # ── Global aggregations ────────────────────────────
            if status_val in by_status:
                by_status[status_val] += 1

            if priority in by_priority:
                by_priority[priority] += 1

            by_oem[oem] = by_oem.get(oem, 0) + 1

            if slot in by_slot:
                by_slot[slot] += 1

            # ── Per-user aggregations ──────────────────────────
            owner_list = task['owner']
            if not isinstance(owner_list, list):
                owner_list = [owner_list] if owner_list else []

            for user in owner_list:
                if user not in user_stats:
                    user_stats[user] = {
                        "user":        user,
                        "total":       0,
                        "completed":   0,
                        "in_progress": 0,
                        "active":      0,
                        "cancelled":   0,
                        "overdue":     0,
                        "completion_rate": 0,
                    }

                s = user_stats[user]
                s["total"] += 1

                if status_val == "Completed":   s["completed"]   += 1
                if status_val == "In Progress": s["in_progress"] += 1
                if status_val == "Active":      s["active"]      += 1
                if status_val == "Cancelled":   s["cancelled"]   += 1

                if (deadline and deadline < now
                        and status_val not in ["Completed", "Cancelled"]):
                    s["overdue"] += 1

        # ── Compute completion_rate per user ───────────────────
        result = []
        for user, s in user_stats.items():
            s["completion_rate"] = (
                round((s["completed"] / s["total"]) * 100)
                if s["total"] > 0 else 0
            )
            result.append(s)

        result.sort(key=lambda x: x["total"], reverse=True)

        return Response({
            "meta": {
                "assigned_by": assigned_by,
                "date_from":   date_from,
                "date_to":     date_to,
                "total_users": len(result),
            },
            "user_performance": result,
            "by_status":   by_status,
            "by_priority": by_priority,
            "by_oem":      by_oem,
            "by_slot":     by_slot,
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": "Something went wrong.", "detail": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# @api_view(['POST'])
# def get_user_wise_analytics(request):

#     assigned_by = request.data.get('assigned_by')
#     date_from   = request.data.get('date_from')
#     date_to     = request.data.get('date_to') or date_from

#     if not assigned_by or not date_from:
#         return Response(
#             {"error": "assigned_by and date_from are required."},
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     try:
#         datetime.strptime(date_from, "%Y-%m-%d")
#         datetime.strptime(date_to,   "%Y-%m-%d")
#     except ValueError:
#         return Response(
#             {"error": "Invalid date format. Use YYYY-MM-DD."},
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     try:
#         qs = Dailytaskreviewmodel.objects.filter(
#             assigned_by=assigned_by,
#             assigned_at__date__gte=date_from,
#             assigned_at__date__lte=date_to,
#         )

#         # ── Flatten owner arrays with full task detail ─────────
#         user_stats = {}  # { email: { total, by_status, by_priority } }

#         # Only fetch needed columns — not full serialized rows
#         tasks = qs.values('id', 'owner', 'status', 'priority', 'deadline', 'oem')

#         now = timezone.now()

#         for task in tasks:
#             owner_list = task['owner']
#             if not isinstance(owner_list, list):
#                 owner_list = [owner_list] if owner_list else []

#             for user in owner_list:
#                 if user not in user_stats:
#                     user_stats[user] = {
#                         "user":        user,
#                         "total":       0,
#                         "completed":   0,
#                         "in_progress": 0,
#                         "active":      0,
#                         "cancelled":   0,
#                         "overdue":     0,
#                         "completion_rate": 0,
#                     }

#                 s = user_stats[user]
#                 s["total"] += 1

#                 status_val = task['status']
#                 if status_val == "Completed":   s["completed"]   += 1
#                 if status_val == "In Progress": s["in_progress"] += 1
#                 if status_val == "Active":      s["active"]      += 1
#                 if status_val == "Cancelled":   s["cancelled"]   += 1

#                 # overdue check
#                 deadline = task['deadline']
#                 if (deadline and deadline < now
#                         and status_val not in ["Completed", "Cancelled"]):
#                     s["overdue"] += 1

#         # ── Compute completion_rate per user ───────────────────
#         result = []
#         for user, s in user_stats.items():
#             s["completion_rate"] = (
#                 round((s["completed"] / s["total"]) * 100)
#                 if s["total"] > 0 else 0
#             )
#             result.append(s)

#         # Sort by total tasks desc
#         result.sort(key=lambda x: x["total"], reverse=True)

#         return Response({
#             "meta": {
#                 "assigned_by": assigned_by,
#                 "date_from":   date_from,
#                 "date_to":     date_to,
#                 "total_users": len(result),
#             },
#             "user_performance": result,
#         }, status=status.HTTP_200_OK)

#     except Exception as e:
#         return Response(
#             {"error": "Something went wrong.", "detail": str(e)},
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR
#         )



@api_view(['POST'])
def get_my_tasks_analytics(request):


    owner     = request.data.get('owner')
    date_from = request.data.get('date_from') or request.data.get('assigned_at')
    date_to   = request.data.get('date_to') or date_from  # fallback = same day

    # ── Validation ────────────────────────────────────────────
    if not date_from:
        return Response(
            {"error": "date_from is required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        datetime.strptime(date_from, "%Y-%m-%d")
        datetime.strptime(date_to,   "%Y-%m-%d")
    except ValueError:
        return Response(
            {"error": "Invalid date format. Use YYYY-MM-DD."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # ── Base queryset ─────────────────────────────────────────
    try:
        qs = Dailytaskreviewmodel.objects.filter(
            assigned_at__date__gte=date_from,
            assigned_at__date__lte=date_to,
        )

        if owner:
            qs = qs.filter(owner__contains=[owner])  # ArrayField
            # JSONField use kar raha hai to:
            # qs = qs.filter(owner__icontains=owner)

        # ── Analytics (DB level) ──────────────────────────────
        total = qs.count()
        now   = timezone.now()

        by_status = dict(
            qs.values('status')
              .annotate(c=Count('id'))
              .values_list('status', 'c')
        )

        by_priority = dict(
            qs.values('priority')
              .annotate(c=Count('id'))
              .values_list('priority', 'c')
        )

        by_oem = dict(
            qs.exclude(oem='')
              .values('oem')
              .annotate(c=Count('id'))
              .values_list('oem', 'c')
        )

        by_slot = dict(
            qs.values('slot')
              .annotate(c=Count('id'))
              .values_list('slot', 'c')
        )

        overdue = qs.filter(
            deadline__lt=now
        ).exclude(
            status__in=['Completed', 'Cancelled']
        ).count()

        # owner is array field — flatten in Python
        # only fetch owner column, not full rows
        user_workload = _calc_user_workload(qs)

        completed       = by_status.get('Completed', 0)
        completion_rate = round((completed / total * 100)) if total else 0

        return Response({
            "meta": {
                "owner":     owner,
                "date_from": date_from,
                "date_to":   date_to,
            },
            "summary": {
                "total":           total,
                "completion_rate": completion_rate,
                "overdue":         overdue,
            },
            "by_status":     _fill_defaults(by_status,   ["Active", "In Progress", "Completed", "Cancelled"]),
            "by_priority":   _fill_defaults(by_priority, ["Critical", "High", "Medium", "Low"]),
            "by_oem":        by_oem,
            "by_slot":       _fill_defaults(by_slot,     ["Morning", "Afternoon", "Evening", "Night"]),
            "user_workload": user_workload,
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": "Something went wrong.", "detail": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ── Helpers ────────────────────────────────────────────────────────────────

def _calc_user_workload(qs):
    """Flatten owner arrays and count per user."""
    counter = Counter()
    for owner_list in qs.values_list('owner', flat=True):
        if isinstance(owner_list, list):
            counter.update(owner_list)
        elif isinstance(owner_list, str) and owner_list:
            counter[owner_list] += 1

    return [
        {"user": u, "task_count": c}
        for u, c in counter.most_common(10)
    ]


def _fill_defaults(data: dict, keys: list) -> dict:
    """Ensure all expected keys exist with 0 as default."""
    return {k: data.get(k, 0) for k in keys}

# ====== get user email and name ======
@api_view(['POST'])
def get_user_email_and_name(request):
    user_id = request.data.get('user_id')

    try:
        user = User.objects.get(id=user_id)
        return Response({
            "email": user.email,
            "name": user.get_full_name() or user.username
        }, status=200)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
