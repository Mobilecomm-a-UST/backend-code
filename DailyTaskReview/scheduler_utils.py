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


# def should_generate_template(template, today):
#     """
#     Check only recurrence.
#     Time checking will be done in auto_task_generation().
#     """

#     print(f"\nChecking Template : {template.task}")

#     if today < template.start_date:
#         return False

#     if template.end_date and today > template.end_date:
#         return False

#     rule = template.recurrence_rule or {}

#     recurrence_type = rule.get("type", "").lower()

#     interval = int(rule.get("interval", 1))

#     if recurrence_type == "daily":

#         days = (today - template.start_date).days

#         return days % interval == 0


#     elif recurrence_type == "weekly":

#         weeks = (today - template.start_date).days // 7

#         if weeks % interval != 0:
#             return False

#         return today.isoweekday() in rule.get("days", [])


#     elif recurrence_type == "monthly":

#         months = (
#             (today.year - template.start_date.year) * 12
#             + (today.month - template.start_date.month)
#         )

#         if months % interval != 0:
#             return False

#         return today.day in rule.get("dates", [])

#     return False

def should_generate_template(template, today):
    """
    Check recurrence only.
    Time validation is handled in auto_task_generation().
    """

    print(f"\nChecking Template : {template.task}")

    # --------------------------------------------------
    # Template Validity
    # --------------------------------------------------

    if today < template.start_date:
        return False

    if template.end_date and today > template.end_date:
        return False

    rule = template.recurrence_rule or {}

    recurrence_type = rule.get(
        "type",
        ""
    ).lower()

    interval = int(
        rule.get(
            "interval",
            1
        )
    )

    # ==========================================================
    # DAILY
    # ==========================================================

    if recurrence_type == "daily":

        days = (
            today -
            template.start_date
        ).days

        return days % interval == 0

    # ==========================================================
    # WEEKLY
    # ==========================================================

    elif recurrence_type == "weekly":

        weeks = (
            today -
            template.start_date
        ).days // 7

        if weeks % interval != 0:
            return False

        weekday_map = {
            "MON":1,
            "TUE":2,
            "WED":3,
            "THU":4,
            "FRI":5,
            "SAT":6,
            "SUN":7,
        }

        days = rule.get("days", [])

        current_day = today.isoweekday()

        return current_day in [
            weekday_map.get(d, d)
            for d in days
        ]

    # ==========================================================
    # MONTHLY (DATES)
    # ==========================================================

    elif recurrence_type == "monthly" and "dates" in rule:

        months = (

            (today.year - template.start_date.year) * 12

            +

            (today.month - template.start_date.month)

        )

        if months % interval != 0:
            return False

        return today.day in rule.get("dates", [])

    # ==========================================================
    # MONTHLY (FIRST / SECOND / THIRD / FOURTH / LAST)
    # ==========================================================

    elif recurrence_type == "monthly" and "week" in rule:

        months = (

            (today.year - template.start_date.year) * 12

            +

            (today.month - template.start_date.month)

        )

        if months % interval != 0:
            return False

        weekday_map = {
            "MON":0,
            "TUE":1,
            "WED":2,
            "THU":3,
            "FRI":4,
            "SAT":5,
            "SUN":6
        }

        week_map = {
            "FIRST":1,
            "SECOND":2,
            "THIRD":3,
            "FOURTH":4,
            "LAST":-1
        }

        target_weekday = weekday_map[
            rule["day"]
        ]

        target_week = week_map[
            rule["week"]
        ]

        if today.weekday() != target_weekday:
            return False

        if target_week == -1:

            last_day = monthrange(
                today.year,
                today.month
            )[1]

            remaining_days = last_day - today.day

            return remaining_days < 7

        else:

            week_number = (
                (today.day - 1) // 7
            ) + 1

            return week_number == target_week

    # ==========================================================
    # CUSTOM
    # ==========================================================

    elif recurrence_type == "custom":

        weekday_map = {
            "MON":1,
            "TUE":2,
            "WED":3,
            "THU":4,
            "FRI":5,
            "SAT":6,
            "SUN":7,
        }

        current_day = today.isoweekday()

        allowed_days = [

            weekday_map[d]

            for d in rule.get(
                "days",
                []
            )

        ]

        return current_day in allowed_days

    # ==========================================================

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
