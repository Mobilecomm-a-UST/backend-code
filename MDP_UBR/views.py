from django.shortcuts import render
from rest_framework.decorators import api_view
import pandas as pd
from .models import UBR_MDP_Table
from rest_framework.response import Response

from django.db.models.functions import Cast,Round,Rank
from django.db.models import OuterRef,Window
from django.db.models import ExpressionWrapper, Case, Value, When, IntegerField,Sum, F, FloatField
# Create your views here.

Year = 2022

@api_view(["GET"])
def unique_coloumn_values(request):
    # circle=UBR_MDP_Table.objects.all().values("circle")
    Circle = list(UBR_MDP_Table.objects.values_list('Circle', flat=True).distinct())
    # circle.extend(["ALL"])              
    Project = list(UBR_MDP_Table.objects.values_list("Project", flat = True).distinct())
    # project.extend(["ALL"])
    Partner = list(UBR_MDP_Table.objects.values_list("Partner", flat = True).distinct())
    # Partner.extend(["ALL"])
    Month= list(UBR_MDP_Table.objects.values_list("Month", flat = True).distinct())
    # month.extend(["ALL"])
    return Response({"status":True,"circle":Circle,"project":Project,"partner":Partner,"month":Month,})

@api_view(["GET", "POST"])
def upload_report(request):

    print("Uploading Data", request.user)
    monthly_report_file = (
        request.FILES["monthly_report_file"]
        if "monthly_report_file" in request.FILES
        else None
    )
    monthly_report_df = pd.read_csv(monthly_report_file)
    
    for i, raw in monthly_report_df.iterrows():
        pk = (
            str(raw["Year"])
            + str(raw["Month"])
            + str(raw["Circle"])
            + str(raw["Project"])
            + str(raw["Partner"])
        )
        Done_Count = int(raw["Done Count"]) if not pd.isna(raw["Done Count"]) else 0
        Projected_Count = (
            int(raw["Projected Count"]) if not pd.isna(raw["Projected Count"]) else 0
        )
        # try:
        obj, created = UBR_MDP_Table.objects.update_or_create(
            id=pk,
            defaults={
                "Year": (raw["Year"]),
                "Month": str(raw["Month"]),
                "Circle": str(raw["Circle"]),
                "Project": str(raw["Project"]),
                "Partner": str(raw["Partner"]),
                "Done_Count": Done_Count,
                "Projected_Count": Projected_Count,
            },
        )

        # except Exception as e:
        #     print(e)
        #     error=str(e)

    return Response({"status": True})


@api_view(["GET"])
def graph_data(request):
    month_mapping = {
        "JAN": 1,
        "FEB": 2,
        "MAR": 3,
        "APR": 4,
        "MAY": 5,
        "JUN": 6,
        "JUL": 7,
        "AUG": 8,
        "SEP": 9,
        "OCT": 10,
        "NOV": 11,
        "DEC": 12,
    }

    total_projected_counts = (
        UBR_MDP_Table.objects
        .values("Month")
        .annotate(total_projected_count=Sum(Cast("Done_Count", IntegerField())))
    )

    query_set = (
        UBR_MDP_Table.objects.filter(Year=2023)
        .values("Month", "Partner","Year")
        .annotate(
            sum_projected_count=Sum(Cast("Done_Count", IntegerField())),
            month_numeric=ExpressionWrapper(
                Case(
                    *[
                        When(Month=month, then=Value(month_num))
                        for month, month_num in month_mapping.items()
                    ],
                    output_field=IntegerField(),
                ),
                output_field=IntegerField(),
            ),
        )
        .annotate(
            total_projected_count=total_projected_counts.filter(Month=OuterRef("Month"))
            .values("Month")
            .annotate(total_projected_count=Sum(Cast("Done_Count", IntegerField())))
            .values("total_projected_count"),
            percentage=ExpressionWrapper(
                F("sum_projected_count") * 100.0 / F("total_projected_count"),
                output_field=FloatField(),
            ),
        )
        .order_by("month_numeric")
    )

    return Response({"status": True, "data": query_set})




@api_view(["GET","POST"])
def circle_wise_vendor_comparision(request):
    # objs = UBR_MDP_Table.objects.all()
    # ser = ser_UBR_MDP_Table(objs, many=True)
     # return Response({"status": True, "data": ser.data})
    objects=UBR_MDP_Table.objects.filter(Year=2023)
    done_or_projected="Done_Count"
    circle = request.POST.get("circle")
    project = request.POST.get("project")
    if circle != "ALL" and project != "ALL":
        #CODE FOR ALLOCATED COUNT DISTRIBUTION PARTNER WISE
        custom_ordering = Case(
        When(Month='JAN', then=Value(1)),
        When(Month='FEB', then=Value(2)),
        When(Month='MAR', then=Value(3)),
        When(Month='APR', then=Value(4)),
        When(Month='MAY', then=Value(5)),
        When(Month='JUN', then=Value(6)),
        When(Month='JUL', then=Value(7)),
        When(Month='AUG', then=Value(8)),
        When(Month='SEP', then=Value(9)),
        When(Month='OCT', then=Value(10)),
        When(Month='NOV', then=Value(11)),
        When(Month='DEC', then=Value(12)),
        default=Value(999),  # Handle unexpected values
        output_field=IntegerField(),
        )

        # Query to retrieve the filtered data with custom ordering
        queryset = objects.annotate(
            custom_order=custom_ordering
        ).filter(
            Circle=circle, Project=project
        ).values(
            'Month', 'Circle', 'Project', 'Partner', 'Done_Count', 'Projected_Count'
        ).order_by('custom_order')



        #CODE FOR OVERALL COUNTS
        
        result = (
        objects.filter(Project=project,Circle=circle)
        
        .values('Month')
        .annotate(
            sum_projected_count=Sum(done_or_projected),
            month_order=Case(
                When(Month ='JAN', then=Value(1)),
                When(Month='FEB', then=Value(2)),
                When(Month='MAR', then=Value(3)),
                When(Month='APR', then=Value(4)),
                When(Month='MAY', then=Value(5)),
                When(Month='JUN', then=Value(6)),
                When(Month='JUL', then=Value(7)),
                When(Month='AUG', then=Value(8)),
                When(Month='SEP', then=Value(9)),
                When(Month='OCT', then=Value(10)),
                When(Month='NOV', then=Value(11)),
                When(Month='DEC', then=Value(12)),
                default=Value(999),
                output_field=IntegerField(),
            )
        )
        .order_by('month_order')
    )


        

    if circle == "ALL" and project != "ALL":
        #CODE FOR ALLOCATED COUNT DISTRIBUTION PARTNER WISE
        custom_ordering = Case(
        When(Month='JAN', then=Value(1)),
        When(Month='FEB', then=Value(2)),
        When(Month='MAR', then=Value(3)),
        When(Month='APR', then=Value(4)),
        When(Month='MAY', then=Value(5)),
        When(Month='JUN', then=Value(6)),
        When(Month='JUL', then=Value(7)),
        When(Month='AUG', then=Value(8)),
        When(Month='SEP', then=Value(9)),
        When(Month='OCT', then=Value(10)),
        When(Month='NOV', then=Value(11)),
        When(Month='DEC', then=Value(12)),
        default=Value(999),  # Handle unexpected values
        output_field=IntegerField(),
         )

        # Query to retrieve the filtered data with custom ordering
        queryset = objects.annotate(
            custom_order=custom_ordering
        ).filter(
            Project=project,
        ).values(
            'Month', 'Project', 'Partner'
        ).annotate(
            DONE_COUNT=Sum('Done_Count'),
            PROJECTED_COUNT=Sum('Projected_Count')
        ).order_by('custom_order')

        #CODE FOR OVERALL COUNT
        result = (
         objects.filter(Project=project)
        .values('Month')
        .annotate(
            sum_projected_count=Sum(done_or_projected),
            month_order=Case(
                When(Month='JAN', then=Value(1)),
                When(Month='FEB', then=Value(2)),
                When(Month='MAR', then=Value(3)),
                When(Month='APR', then=Value(4)),
                When(Month='MAY', then=Value(5)),
                When(Month='JUN', then=Value(6)),
                When(Month='JUL', then=Value(7)),
                When(Month='AUG', then=Value(8)),
                When(Month='SEP', then=Value(9)),
                When(Month='OCT', then=Value(10)),
                When(Month='NOV', then=Value(11)),
                When(Month='DEC', then=Value(12)),
                default=Value(999),
                output_field=IntegerField(),
            )
        )
        .order_by('month_order')
    )


    if circle != "ALL" and project == "ALL":
        #CODE FOR ALLOCATED COUNT DISTRIBUTION PARTNER WISE
        custom_ordering = Case(
        When(Month='JAN', then=Value(1)),
        When(Month='FEB', then=Value(2)),
        When(Month='MAR', then=Value(3)),
        When(Month='APR', then=Value(4)),
        When(Month='MAY', then=Value(5)),
        When(Month='JUN', then=Value(6)),
        When(Month='JUL', then=Value(7)),
        When(Month='AUG', then=Value(8)),
        When(Month='SEP', then=Value(9)),
        When(Month='OCT', then=Value(10)),
        When(Month='NOV', then=Value(11)),
        When(Month='DEC', then=Value(12)),
        default=Value(999),  # Handle unexpected values
        output_field=IntegerField(),
        )

        # Query to retrieve the filtered data with custom ordering
        queryset = objects.annotate(
            custom_order=custom_ordering
        ).filter(
            Circle = circle,
        ).values(
            'Month', 'Circle', 'Partner'
        ).annotate(
            DONE_COUNT=Sum('Done_Count'),
            PROJECTED_COUNT=Sum('Projected_Count')
        ).order_by('custom_order')

        #CODE FOR OVERALL COUNTS
        result = (
        objects
        .values("Month")
        .filter( Circle=circle)
        .annotate(
            sum_projected_count=Sum(done_or_projected),
            month_order=Case(
                When(Month='JAN', then=Value(1)),
                When(Month='FEB', then=Value(2)),
                When(Month='MAR', then=Value(3)),
                When(Month='APR', then=Value(4)),
                When(Month='MAY', then=Value(5)),
                When(Month='JUN', then=Value(6)),
                When(Month='JUL', then=Value(7)),
                When(Month='AUG', then=Value(8)),
                When(Month='SEP', then=Value(9)),
                When(Month='OCT', then=Value(10)),
                When(Month='NOV', then=Value(11)),
                When(Month='DEC', then=Value(12)),
                default=Value(999),
                output_field=IntegerField(),
            )
        )
        .order_by("month_order")
    )

    if circle == "ALL" and project == "ALL":
        ##CODE FOR ALLOCATED COUNT DISTRIBUTION PARTNER WISE
        custom_ordering = Case(
        When(Month='JAN', then=Value(1)),
        When(Month='FEB', then=Value(2)),
        When(Month='MAR', then=Value(3)),
        When(Month='APR', then=Value(4)),
        When(Month='MAY', then=Value(5)),
        When(Month='JUN', then=Value(6)),
        When(Month='JUL', then=Value(7)),
        When(Month='AUG', then=Value(8)),
        When(Month='SEP', then=Value(9)),
        When(Month='OCT', then=Value(10)),
        When(Month='NOV', then=Value(11)),
        When(Month='DEC', then=Value(12)),
        default=Value(999),  # Handle unexpected values
        output_field=IntegerField(),
        )

        # Query to retrieve the filtered data with custom ordering
        queryset = objects.annotate(
            custom_order=custom_ordering
        ).values(
            'Month','Partner'
        ).annotate(
            DONE_COUNT=Sum('Done_Count'),
            PROJECTED_COUNT=Sum('Projected_Count')
        ).order_by('custom_order')

        #CODE FOR OVERALL COUNT
        result = (
        objects
        .values('Month')
        .annotate(
            sum_projected_count=Sum(done_or_projected),
            month_order=Case(
                When(Month='JAN', then=Value(1)),
                When(Month='FEB', then=Value(2)),
                When(Month='MAR', then=Value(3)),
                When(Month='APR', then=Value(4)),
                When(Month='MAY', then=Value(5)),
                When(Month='JUN', then=Value(6)),
                When(Month='JUL', then=Value(7)),
                When(Month='AUG', then=Value(8)),
                When(Month='SEP', then=Value(9)),
                When(Month='OCT', then=Value(10)),
                When(Month='NOV', then=Value(11)),
                When(Month='DEC', then=Value(12)),
                default=Value(999),
                output_field=IntegerField(),
            )
        )
        .order_by('month_order')
    )

            
        
    return Response({"status": True, "data":queryset ,"airtel_bucket":result })





@api_view(["GET", "POST"])
def project_comparision(request):
    circle = request.POST.get("CIRCLE")
    print(circle)
    Partner = request.POST.get("Partner")
    print(Partner)
    DONE_COUNT = request.POST.get("DONE_COUNT")
    print(DONE_COUNT)
    month_mapping = {
    'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4,
    'MAY': 5, 'JUN': 6, 'JUL': 7, 'AUG': 8,
    'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12
    }
    year = 2023
    if DONE_COUNT=="True":
        if circle != "ALL"  and Partner !="ALL":
            result_queryset = (
                        UBR_MDP_Table.objects
                        .filter(Partner=Partner,Circle=circle,Year=2023)
                        .values('Month', 'Project')
                        .annotate(Counting=Sum('Done_Count'))
                        .annotate(month_order=Case(
                            When(Month='JAN', then=Value(1)),
                            When(Month='FEB', then=Value(2)),
                            When(Month='MAR', then=Value(3)),
                            When(Month='APR', then=Value(4)),
                            When(Month='MAY', then=Value(5)),
                            When(Month='JUN', then=Value(6)),
                            When(Month='JUL', then=Value(7)),
                            When(Month='AUG', then=Value(8)),
                            When(Month='SEP', then=Value(9)),
                            When(Month='OCT', then=Value(10)),
                            When(Month='NOV', then=Value(11)),
                            When(Month='DEC', then=Value(12)),
                            default=Value(999),  # Handle unexpected values
                            output_field=IntegerField()
                        ))
                        .order_by('month_order')
                    )
            overall_result = UBR_MDP_Table.objects.filter(Circle=circle , Partner = Partner).values('Month').annotate(
                                    sum_projected_count=Sum('Done_Count')
                                ).annotate(
                                    month_numeric=Case(
                                        When(Month='JAN', then=Value(1)),
                                        When(Month='FEB', then=Value(2)),
                                        When(Month='MAR', then=Value(3)),
                                        When(Month='APR', then=Value(4)),
                                        When(Month='MAY', then=Value(5)),
                                        When(Month='JUN', then=Value(6)),
                                        When(Month='JUL', then=Value(7)),
                                        When(Month='AUG', then=Value(8)),
                                        When(Month='SEP', then=Value(9)),
                                        When(Month='OCT', then=Value(10)),
                                        When(Month='NOV', then=Value(11)),
                                        When(Month='DEC', then=Value(12)),
                                        default=Value(999),  # Handle unexpected values
                                        output_field=IntegerField(),
                                    )
                                ).order_by('month_numeric')

        if  circle == "ALL"  and Partner !="ALL":
            result_queryset = (
                        UBR_MDP_Table.objects
                        .filter(Partner=Partner,Year=2023)
                        .values('Month', 'Project')
                        .annotate(Counting=Sum('Done_Count'))
                        .annotate(month_order=Case(
                            When(Month='JAN', then=Value(1)),
                            When(Month='FEB', then=Value(2)),
                            When(Month='MAR', then=Value(3)),
                            When(Month='APR', then=Value(4)),
                            When(Month='MAY', then=Value(5)),
                            When(Month='JUN', then=Value(6)),
                            When(Month='JUL', then=Value(7)),
                            When(Month='AUG', then=Value(8)),
                            When(Month='SEP', then=Value(9)),
                            When(Month='OCT', then=Value(10)),
                            When(Month='NOV', then=Value(11)),
                            When(Month='DEC', then=Value(12)),
                            default=Value(999),  # Handle unexpected values
                            output_field=IntegerField()
                        ))
                        .order_by('month_order')
                    )
            overall_result = UBR_MDP_Table.objects.filter( Partner=Partner).values('Month').annotate(
                                        sum_projected_count=Sum('Done_Count')
                                    ).annotate(
                                        month_numeric=Case(
                                            When(Month='JAN', then=Value(1)),
                                            When(Month='FEB', then=Value(2)),
                                            When(Month='MAR', then=Value(3)),
                                            When(Month='APR', then=Value(4)),
                                            When(Month='MAY', then=Value(5)),
                                            When(Month='JUN', then=Value(6)),
                                            When(Month='JUL', then=Value(7)),
                                            When(Month='AUG', then=Value(8)),
                                            When(Month='SEP', then=Value(9)),
                                            When(Month='OCT', then=Value(10)),
                                            When(Month='NOV', then=Value(11)),
                                            When(Month='DEC', then=Value(12)),
                                            default=Value(999),  # Handle unexpected values
                                            output_field=IntegerField(),
                                        )
                                    ).order_by('month_numeric')

        if  circle !="ALL"  and Partner =="ALL":
           result_queryset = (
                        UBR_MDP_Table.objects
                        .filter(Circle=circle,Year=2023)
                       
                        .values('Month', 'Project')
                        .annotate(Counting=Sum('Done_Count'))
                        .annotate(month_order=Case(
                            When(Month='JAN', then=Value(1)),
                            When(Month='FEB', then=Value(2)),
                            When(Month='MAR', then=Value(3)),
                            When(Month='APR', then=Value(4)),
                            When(Month='MAY', then=Value(5)),
                            When(Month='JUN', then=Value(6)),
                            When(Month='JUL', then=Value(7)),
                            When(Month='AUG', then=Value(8)),
                            When(Month='SEP', then=Value(9)),
                            When(Month='OCT', then=Value(10)),
                            When(Month='NOV', then=Value(11)),
                            When(Month='DEC', then=Value(12)),
                            default=Value(999),  # Handle unexpected values
                            output_field=IntegerField()
                        ))
                        .order_by('month_order')
                    )
           overall_result = UBR_MDP_Table.objects.filter(Circle=circle).values('Month').annotate(
                                    sum_projected_count=Sum('Done_Count')
                                ).annotate(
                                    month_numeric=Case(
                                        When(Month='JAN', then=Value(1)),
                                        When(Month='FEB', then=Value(2)),
                                        When(Month='MAR', then=Value(3)),
                                        When(Month='APR', then=Value(4)),
                                        When(Month='MAY', then=Value(5)),
                                        When(Month='JUN', then=Value(6)),
                                        When(Month='JUL', then=Value(7)),
                                        When(Month='AUG', then=Value(8)),
                                        When(Month='SEP', then=Value(9)),
                                        When(Month='OCT', then=Value(10)),
                                        When(Month='NOV', then=Value(11)),
                                        When(Month='DEC', then=Value(12)),
                                        default=Value(999),  # Handle unexpected values
                                        output_field=IntegerField(),
                                    )
                                ).order_by('month_numeric')
           
        if  circle =="ALL"  and Partner =="ALL":
           result_queryset = (
                        UBR_MDP_Table.objects.filter(Year=2023)
                        
                        .values('Month', 'Project')
                        .annotate(Counting=Sum('Done_Count'))
                        .annotate(month_order=Case(
                            When(Month='JAN', then=Value(1)),
                            When(Month='FEB', then=Value(2)),
                            When(Month='MAR', then=Value(3)),
                            When(Month='APR', then=Value(4)),
                            When(Month='MAY', then=Value(5)),
                            When(Month='JUN', then=Value(6)),
                            When(Month='JUL', then=Value(7)),
                            When(Month='AUG', then=Value(8)),
                            When(Month='SEP', then=Value(9)),
                            When(Month='OCT', then=Value(10)),
                            When(Month='NOV', then=Value(11)),
                            When(Month='DEC', then=Value(12)),
                            default=Value(999),  # Handle unexpected values
                            output_field=IntegerField()
                        ))
                        .order_by('month_order')
                    )
           overall_result = UBR_MDP_Table.objects.values('Month').annotate(
                                    sum_projected_count=Sum('Done_Count')
                                ).annotate(
                                    month_numeric=Case(
                                        When(Month='JAN', then=Value(1)),
                                        When(Month='FEB', then=Value(2)),
                                        When(Month='MAR', then=Value(3)),
                                        When(Month='APR', then=Value(4)),
                                        When(Month='MAY', then=Value(5)),
                                        When(Month='JUN', then=Value(6)),
                                        When(Month='JUL', then=Value(7)),
                                        When(Month='AUG', then=Value(8)),
                                        When(Month='SEP', then=Value(9)),
                                        When(Month='OCT', then=Value(10)),
                                        When(Month='NOV', then=Value(11)),
                                        When(Month='DEC', then=Value(12)),
                                        default=Value(999),  # Handle unexpected values
                                        output_field=IntegerField(),
                                    )
                                ).order_by('month_numeric')

        # Select the desired columns
        result_queryset = result_queryset.values("Month", "Project", "Counting")

        # Execute the queryset to get the result
        results = result_queryset.all()



   

        return Response({
            "status":True,
            "message":"Successfully fetched ...",
            "data":results,
            "overall_data":overall_result
        })
    
    else :
        if circle != "ALL"  and Partner !="ALL":
            result_queryset = (
                        UBR_MDP_Table.objects
                        .filter(Partner=Partner,circle=circle, Year = year)
                        .values('Month', 'project')
                        .annotate(Counting=Sum('PROJECTED_COUNT'))
                        .annotate(month_order=Case(
                            When(Month='JAN', then=Value(1)),
                            When(Month='FEB', then=Value(2)),
                            When(Month='MAR', then=Value(3)),
                            When(Month='APR', then=Value(4)),
                            When(Month='MAY', then=Value(5)),
                            When(Month='JUN', then=Value(6)),
                            When(Month='JUL', then=Value(7)),
                            When(Month='AUG', then=Value(8)),
                            When(Month='SEP', then=Value(9)),
                            When(Month='OCT', then=Value(10)),
                            When(Month='NOV', then=Value(11)),
                            When(Month='DEC', then=Value(12)),
                            default=Value(999),  # Handle unexpected values
                            output_field=IntegerField()
                        ))
                        .order_by('month_order')
                    )
            overall_result = UBR_MDP_Table.objects.filter(circle=circle , Partner = Partner).values('Month').annotate(
                                    sum_projected_count=Sum('PROJECTED_COUNT')
                                ).annotate(
                                    month_numeric=Case(
                                        When(Month='JAN', then=Value(1)),
                                        When(Month='FEB', then=Value(2)),
                                        When(Month='MAR', then=Value(3)),
                                        When(Month='APR', then=Value(4)),
                                        When(Month='MAY', then=Value(5)),
                                        When(Month='JUN', then=Value(6)),
                                        When(Month='JUL', then=Value(7)),
                                        When(Month='AUG', then=Value(8)),
                                        When(Month='SEP', then=Value(9)),
                                        When(Month='OCT', then=Value(10)),
                                        When(Month='NOV', then=Value(11)),
                                        When(Month='DEC', then=Value(12)),
                                        default=Value(999),  # Handle unexpected values
                                        output_field=IntegerField(),
                                    )
                                ).order_by('month_numeric')

        if  circle == "ALL"  and Partner !="ALL":
           result_queryset = (
                        UBR_MDP_Table.objects
                        .filter(Partner=Partner)
                        .values('Month', 'project')
                        .annotate(Counting=Sum('PROJECTED_COUNT'))
                        .annotate(month_order=Case(
                            When(Month='JAN', then=Value(1)),
                            When(Month='FEB', then=Value(2)),
                            When(Month='MAR', then=Value(3)),
                            When(Month='APR', then=Value(4)),
                            When(Month='MAY', then=Value(5)),
                            When(Month='JUN', then=Value(6)),
                            When(Month='JUL', then=Value(7)),
                            When(Month='AUG', then=Value(8)),
                            When(Month='SEP', then=Value(9)),
                            When(Month='OCT', then=Value(10)),
                            When(Month='NOV', then=Value(11)),
                            When(Month='DEC', then=Value(12)),
                            default=Value(999),  # Handle unexpected values
                            output_field=IntegerField()
                        ))
                        .order_by('month_order')
                    )
           overall_result = UBR_MDP_Table.objects.filter( Partner = Partner).values('Month').annotate(
                                    sum_projected_count=Sum('PROJECTED_COUNT')
                                ).annotate(
                                    month_numeric=Case(
                                        When(Month='JAN', then=Value(1)),
                                        When(Month='FEB', then=Value(2)),
                                        When(Month='MAR', then=Value(3)),
                                        When(Month='APR', then=Value(4)),
                                        When(Month='MAY', then=Value(5)),
                                        When(Month='JUN', then=Value(6)),
                                        When(Month='JUL', then=Value(7)),
                                        When(Month='AUG', then=Value(8)),
                                        When(Month='SEP', then=Value(9)),
                                        When(Month='OCT', then=Value(10)),
                                        When(Month='NOV', then=Value(11)),
                                        When(Month='DEC', then=Value(12)),
                                        default=Value(999),  # Handle unexpected values
                                        output_field=IntegerField(),
                                    )
                                ).order_by('month_numeric')

        if  circle !="ALL"  and Partner =="ALL":
           result_queryset = (
                        UBR_MDP_Table.objects
                        .filter(circle=circle)
                        .exclude(Partner='TOTAL')
                        .values('Month', 'project')
                        .annotate(Counting=Sum('PROJECTED_COUNT'))
                        .annotate(month_order=Case(
                            When(Month='JAN', then=Value(1)),
                            When(Month='FEB', then=Value(2)),
                            When(Month='MAR', then=Value(3)),
                            When(Month='APR', then=Value(4)),
                            When(Month='MAY', then=Value(5)),
                            When(Month='JUN', then=Value(6)),
                            When(Month='JUL', then=Value(7)),
                            When(Month='AUG', then=Value(8)),
                            When(Month='SEP', then=Value(9)),
                            When(Month='OCT', then=Value(10)),
                            When(Month='NOV', then=Value(11)),
                            When(Month='DEC', then=Value(12)),
                            default=Value(999),  # Handle unexpected values
                            output_field=IntegerField()
                        ))
                        .order_by('month_order')
                    )
           overall_result = UBR_MDP_Table.objects.filter(circle=circle).exclude(Partner='TOTAL').values('Month').annotate(
                                    sum_projected_count=Sum('PROJECTED_COUNT')
                                ).annotate(
                                    month_numeric=Case(
                                        When(Month='JAN', then=Value(1)),
                                        When(Month='FEB', then=Value(2)),
                                        When(Month='MAR', then=Value(3)),
                                        When(Month='APR', then=Value(4)),
                                        When(Month='MAY', then=Value(5)),
                                        When(Month='JUN', then=Value(6)),
                                        When(Month='JUL', then=Value(7)),
                                        When(Month='AUG', then=Value(8)),
                                        When(Month='SEP', then=Value(9)),
                                        When(Month='OCT', then=Value(10)),
                                        When(Month='NOV', then=Value(11)),
                                        When(Month='DEC', then=Value(12)),
                                        default=Value(999),  # Handle unexpected values
                                        output_field=IntegerField(),
                                    )
                                ).order_by('month_numeric')
           
        if  circle =="ALL"  and Partner =="ALL":
           result_queryset = (
                        UBR_MDP_Table.objects
                        .exclude(Partner='TOTAL')
                        .values('Month', 'project')
                        .annotate(Counting=Sum('PROJECTED_COUNT'))
                        .annotate(month_order=Case(
                            When(Month='JAN', then=Value(1)),
                            When(Month='FEB', then=Value(2)),
                            When(Month='MAR', then=Value(3)),
                            When(Month='APR', then=Value(4)),
                            When(Month='MAY', then=Value(5)),
                            When(Month='JUN', then=Value(6)),
                            When(Month='JUL', then=Value(7)),
                            When(Month='AUG', then=Value(8)),
                            When(Month='SEP', then=Value(9)),
                            When(Month='OCT', then=Value(10)),
                            When(Month='NOV', then=Value(11)),
                            When(Month='DEC', then=Value(12)),
                            default=Value(999),  # Handle unexpected values
                            output_field=IntegerField()
                        ))
                        .order_by('month_order')
                    )
           overall_result = UBR_MDP_Table.objects.exclude(Partner='TOTAL').values('Month').annotate(
                                    sum_projected_count=Sum('PROJECTED_COUNT')
                                ).annotate(
                                    month_numeric=Case(
                                        When(Month='JAN', then=Value(1)),
                                        When(Month='FEB', then=Value(2)),
                                        When(Month='MAR', then=Value(3)),
                                        When(Month='APR', then=Value(4)),
                                        When(Month='MAY', then=Value(5)),
                                        When(Month='JUN', then=Value(6)),
                                        When(Month='JUL', then=Value(7)),
                                        When(Month='AUG', then=Value(8)),
                                        When(Month='SEP', then=Value(9)),
                                        When(Month='OCT', then=Value(10)),
                                        When(Month='NOV', then=Value(11)),
                                        When(Month='DEC', then=Value(12)),
                                        default=Value(999),  # Handle unexpected values
                                        output_field=IntegerField(),
                                    )
                                ).order_by('month_numeric')

        # Select the desired columns
        result_queryset = result_queryset.values("Month", "project", "Counting")

        # Execute the queryset to get the result
        results = result_queryset.all()



    

        return Response({
            "status":True,
            "message":"Successfully fetched ...",
            "data":results,
            "overall_data":overall_result
        })