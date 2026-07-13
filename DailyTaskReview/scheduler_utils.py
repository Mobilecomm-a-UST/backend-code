from datetime import datetime, timedelta
from django.utils import timezone
from .models import Dailytaskreviewmodel
from .models import TaskGenerationLog

# ========== # Recurrence Validation # ==========
# def should_generate_template(template,today,current_time):
#     """
#     Returns True if the template should generate task now.
#     """

#     print("\nChecking Template :", template.task)

#     # ----------------------------------------
#     # Template Active Date Validation
#     # ----------------------------------------

#     if today < template.start_date:
#         print("Template not started yet.")
#         return False

#     if template.end_date and today > template.end_date:
#         print("Template expired.")
#         return False

#     # ----------------------------------------
#     # Read Recurrence Rule
#     # ----------------------------------------

#     rule = template.recurrence_rule or {}

#     recurrence_type = rule.get(
#         "type",
#         ""
#     ).lower()

#     if recurrence_type == "":
#         print("Recurrence Type Missing")
#         return False

#     interval = rule.get(
#         "interval",
#         1
#     )

#     times = rule.get(
#         "times",
#         []
#     )

#     current_time = current_time.strftime("%H:%M")

#     # ----------------------------------------
#     # Time Validation
#     # ----------------------------------------

#     if current_time not in times:

#         print(
#             f"Current Time {current_time} not in {times}"
#         )

#         return False

#     # ==========================================================
#     # DAILY
#     # ==========================================================

#     if recurrence_type == "daily":

#         days_difference = (
#             today -
#             template.start_date
#         ).days

#         if days_difference % interval == 0:

#             print("Daily Rule Matched")

#             return True

#         return False

#     # ==========================================================
#     # WEEKLY
#     # ==========================================================

#     elif recurrence_type == "weekly":

#         weekdays = rule.get(
#             "days",
#             []
#         )

#         weeks_difference = (
#             (today - template.start_date).days // 7
#         )

#         if weeks_difference % interval != 0:
#             return False

#         if today.isoweekday() not in weekdays:
#             return False

#         print("Weekly Rule Matched")

#         return True

#     # ==========================================================
#     # MONTHLY
#     # ==========================================================

#     elif recurrence_type == "monthly":

#         dates = rule.get(
#             "dates",
#             []
#         )

#         months_difference = (
#             (today.year - template.start_date.year) * 12
#             + (today.month - template.start_date.month)
#         )

#         if months_difference % interval != 0:
#             return False

#         if today.day not in dates:
#             return False

#         print("Monthly Rule Matched")

#         return True

#     # ==========================================================
#     # UNKNOWN
#     # ==========================================================

#     print("Unknown recurrence type :", recurrence_type)

#     return False

# def should_generate_template(template, today, current_time):
#     """
#     Returns True if the template should generate task now.
#     """

#     print("\nChecking Template :", template.task)

#     # ----------------------------------------
#     # Template Active Date Validation
#     # ----------------------------------------

#     if today < template.start_date:
#         print("Template not started yet.")
#         return False

#     if template.end_date and today > template.end_date:
#         print("Template expired.")
#         return False

#     # ----------------------------------------
#     # Read Recurrence Rule
#     # ----------------------------------------

#     rule = template.recurrence_rule or {}

#     recurrence_type = rule.get(
#         "type",
#         ""
#     ).lower()

#     if recurrence_type == "":
#         print("Recurrence Type Missing")
#         return False

#     interval = rule.get(
#         "interval",
#         1
#     )

#     times = rule.get(
#         "times",
#         []
#     )

#     # ----------------------------------------
#     # Time Validation (with 60 sec tolerance)
#     # ----------------------------------------

#     current = datetime.strptime(
#         current_time.strftime("%H:%M"),
#         "%H:%M"
#     )

#     matched = False

#     for t in times:

#         schedule = datetime.strptime(
#             t,
#             "%H:%M"
#         )

#         diff = abs(
#             (current - schedule).total_seconds()
#         )

#         # Accept if within 60 seconds
#         if diff <= 60:
#             matched = True
#             break

#     if not matched:

#         print(
#             f"Current Time {current.strftime('%H:%M')} not in {times}"
#         )

#         return False

#     # ==========================================================
#     # DAILY
#     # ==========================================================

#     if recurrence_type == "daily":

#         days_difference = (
#             today -
#             template.start_date
#         ).days

#         if days_difference % interval == 0:

#             print("Daily Rule Matched")

#             return True

#         return False

#     # ==========================================================
#     # WEEKLY
#     # ==========================================================

#     elif recurrence_type == "weekly":

#         weekdays = rule.get(
#             "days",
#             []
#         )

#         weeks_difference = (
#             (today - template.start_date).days // 7
#         )

#         if weeks_difference % interval != 0:
#             return False

#         if today.isoweekday() not in weekdays:
#             return False

#         print("Weekly Rule Matched")

#         return True

#     # ==========================================================
#     # MONTHLY
#     # ==========================================================

#     elif recurrence_type == "monthly":

#         dates = rule.get(
#             "dates",
#             []
#         )

#         months_difference = (
#             (today.year - template.start_date.year) * 12
#             + (today.month - template.start_date.month)
#         )

#         if months_difference % interval != 0:
#             return False

#         if today.day not in dates:
#             return False

#         print("Monthly Rule Matched")

#         return True

#     # ==========================================================
#     # UNKNOWN
#     # ==========================================================

#     print("Unknown recurrence type :", recurrence_type)

#     return False

def should_generate_template(template, today):
    """
    Check only recurrence.
    Time checking will be done in auto_task_generation().
    """

    print(f"\nChecking Template : {template.task}")

    if today < template.start_date:
        return False

    if template.end_date and today > template.end_date:
        return False

    rule = template.recurrence_rule or {}

    recurrence_type = rule.get("type", "").lower()

    interval = int(rule.get("interval", 1))

    if recurrence_type == "daily":

        days = (today - template.start_date).days

        return days % interval == 0


    elif recurrence_type == "weekly":

        weeks = (today - template.start_date).days // 7

        if weeks % interval != 0:
            return False

        return today.isoweekday() in rule.get("days", [])


    elif recurrence_type == "monthly":

        months = (
            (today.year - template.start_date.year) * 12
            + (today.month - template.start_date.month)
        )

        if months % interval != 0:
            return False

        return today.day in rule.get("dates", [])

    return False

# =========== # Deadline Calculation # ===========

def calculate_deadline(template, assigned_at):
    """
    Calculate deadline from assigned_at.

    Input:
        assigned_at -> timezone aware datetime

    Returns:
        deadline -> timezone aware datetime
    """

    # ----------------------------------------
    # Default Deadline
    # ----------------------------------------

    deadline = assigned_at

    rule = template.deadline_rule or {}

    rule_type = rule.get(
        "type",
        "same_day"
    )

    # ==================================================
    # Same Day
    # ==================================================

    if rule_type == "same_day":

        deadline_time = datetime.strptime(
            rule.get("time", "18:00"),
            "%H:%M"
        ).time()

        deadline = timezone.make_aware(

            datetime.combine(

                assigned_at.date(),

                deadline_time

            )

        )

    # ==================================================
    # After Hours
    # ==================================================

    elif rule_type == "after_hours":

        hours = int(
            rule.get("hours", 8)
        )

        deadline = assigned_at + timedelta(
            hours=hours
        )

    # ==================================================
    # After Days
    # ==================================================

    elif rule_type == "after_days":

        days = int(
            rule.get("days", 1)
        )

        deadline_time = datetime.strptime(
            rule.get("time", "18:00"),
            "%H:%M"
        ).time()

        deadline = timezone.make_aware(

            datetime.combine(

                assigned_at.date() + timedelta(days=days),

                deadline_time

            )

        )

    # ==================================================
    # Fixed Datetime
    # ==================================================

    elif rule_type == "fixed_datetime":

        deadline = timezone.make_aware(

            datetime.strptime(

                rule["datetime"],

                "%Y-%m-%d %H:%M"

            )

        )

    # ==================================================
    # End Of Day
    # ==================================================

    elif rule_type == "end_of_day":

        deadline = timezone.make_aware(

            datetime.combine(

                assigned_at.date(),

                datetime.strptime(
                    "23:59",
                    "%H:%M"
                ).time()

            )

        )

    return deadline

# ========= Task Create Validation =========
def create_task_from_template(
    template,
    owner,
    assigned_at,
    deadline
 ):
    """
    Create a new task from template.

    Returns:
        Dailytaskreviewmodel object
    """

    task = Dailytaskreviewmodel.objects.create(

        # -------------------------
        # Basic Information
        # -------------------------

        oem=template.oem,

        task=template.task,

        slot='',

        owner=[owner],

        # -------------------------
        # Assignment
        # -------------------------

        assigned_by=template.assigned_by,

        assigned_at=assigned_at,

        deadline=deadline,

        # -------------------------
        # Task Properties
        # -------------------------

        priority=template.priority,

        remarks=template.remarks,

        status=template.status,

        task_type="assign",

        # Optional
        frequency="None",

        updated_by=template.assigned_by

    )

    return task

# ======== Log Save ========
def create_generation_log(template,owner,task,scheduled_datetime):
    """
    Save task generation history.

    This prevents duplicate task creation
    for the same template + owner + date.
    """

    log = TaskGenerationLog.objects.create(

        template=template,

        owner=owner,

        task_id=task.task_id,

        scheduled_datetime=scheduled_datetime


    )

    return log
