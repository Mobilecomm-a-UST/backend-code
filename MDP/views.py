from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd
from MDP.models import upload_report_table
from MDP.serializers import *
from django.db.models.functions import Cast,Round,Rank
from django.db.models import OuterRef,Window
from django.db.models import ExpressionWrapper, Case, Value, When, IntegerField,Sum, F, FloatField



Year = 2023

@api_view(["GET"])
def unique_coloumn_values(request):
    # circle=upload_report_table.objects.all().values("circle")
    circle = list(upload_report_table.objects.values_list('circle', flat=True).distinct())
    # circle.extend(["ALL"])              
    project = list(upload_report_table.objects.values_list("project", flat = True).distinct())
    # project.extend(["ALL"])
    compatitor = list(upload_report_table.objects.values_list("COMPATITOR", flat = True).distinct())
    # compatitor.extend(["ALL"])
    month = list(upload_report_table.objects.values_list("MONTH", flat = True).distinct())
    # month.extend(["ALL"])
    return Response({"status":True,"circle":circle,"project":project,"compatitor":compatitor,"month":month,})
    

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
            str(raw["YEAR"])
            + str(raw["MONTH"])
            + str(raw["CIRCLE"])
            + str(raw["PROJECT"])
            + str(raw["COMPATITOR"])
        )
        DONE_COUNT = int(raw["DONE COUNT"]) if not pd.isna(raw["DONE COUNT"]) else 0
        PROJECTED_COUNT = (
            int(raw["PROJECTED_COUNT"]) if not pd.isna(raw["PROJECTED_COUNT"]) else 0
        )
        # try:
        obj, created = upload_report_table.objects.update_or_create(
            id=pk,
            defaults={
                "YEAR": (raw["YEAR"]),
                "MONTH": str(raw["MONTH"]),
                "circle": str(raw["CIRCLE"]),
                "project": str(raw["PROJECT"]),
                "COMPATITOR": str(raw["COMPATITOR"]),
                "DONE_COUNT": DONE_COUNT,
                "PROJECTED_COUNT": PROJECTED_COUNT,
            },
        )

        # except Exception as e:
        #     print(e)
        #     error=str(e)

    return Response({"status": True})


@api_view(["GET","POST"])
def circle_wise_vendor_comparision(request):
    # objs = upload_report_table.objects.all()
    # ser = ser_upload_report_table(objs, many=True)
     # return Response({"status": True, "data": ser.data})
    objects=upload_report_table.objects.filter(YEAR=Year)
    done_or_projected="DONE_COUNT"
    circle = request.POST.get("circle")
    project = request.POST.get("project")
    if circle != "ALL" and project != "ALL":
        #CODE FOR ALLOCATED COUNT DISTRIBUTION PARTNER WISE
        custom_ordering = Case(
        When(MONTH='JAN', then=Value(1)),
        When(MONTH='FEB', then=Value(2)),
        When(MONTH='MAR', then=Value(3)),
        When(MONTH='APR', then=Value(4)),
        When(MONTH='MAY', then=Value(5)),
        When(MONTH='JUN', then=Value(6)),
        When(MONTH='JUL', then=Value(7)),
        When(MONTH='AUG', then=Value(8)),
        When(MONTH='SEP', then=Value(9)),
        When(MONTH='OCT', then=Value(10)),
        When(MONTH='NOV', then=Value(11)),
        When(MONTH='DEC', then=Value(12)),
        default=Value(999),  # Handle unexpected values
        output_field=IntegerField(),
        )

        # Query to retrieve the filtered data with custom ordering
        queryset = objects.exclude(COMPATITOR ='TOTAL').annotate(
            custom_order=custom_ordering
        ).filter(
            circle=circle, project=project
        ).values(
            'MONTH', 'circle', 'project', 'COMPATITOR', 'DONE_COUNT', 'PROJECTED_COUNT'
        ).order_by('custom_order')



        #CODE FOR OVERALL COUNTS
        
        result = (
        objects.filter(project=project,circle=circle)
        .exclude(COMPATITOR='TOTAL')
        .values('MONTH')
        .annotate(
            sum_projected_count=Sum(done_or_projected),
            month_order=Case(
                When(MONTH='JAN', then=Value(1)),
                When(MONTH='FEB', then=Value(2)),
                When(MONTH='MAR', then=Value(3)),
                When(MONTH='APR', then=Value(4)),
                When(MONTH='MAY', then=Value(5)),
                When(MONTH='JUN', then=Value(6)),
                When(MONTH='JUL', then=Value(7)),
                When(MONTH='AUG', then=Value(8)),
                When(MONTH='SEP', then=Value(9)),
                When(MONTH='OCT', then=Value(10)),
                When(MONTH='NOV', then=Value(11)),
                When(MONTH='DEC', then=Value(12)),
                default=Value(999),
                output_field=IntegerField(),
            )
        )
        .order_by('month_order')
    )


        

    if circle == "ALL" and project != "ALL":
        #CODE FOR ALLOCATED COUNT DISTRIBUTION PARTNER WISE
        custom_ordering = Case(
        When(MONTH='JAN', then=Value(1)),
        When(MONTH='FEB', then=Value(2)),
        When(MONTH='MAR', then=Value(3)),
        When(MONTH='APR', then=Value(4)),
        When(MONTH='MAY', then=Value(5)),
        When(MONTH='JUN', then=Value(6)),
        When(MONTH='JUL', then=Value(7)),
        When(MONTH='AUG', then=Value(8)),
        When(MONTH='SEP', then=Value(9)),
        When(MONTH='OCT', then=Value(10)),
        When(MONTH='NOV', then=Value(11)),
        When(MONTH='DEC', then=Value(12)),
        default=Value(999),  # Handle unexpected values
        output_field=IntegerField(),
         )

        # Query to retrieve the filtered data with custom ordering
        queryset = objects.annotate(
            custom_order=custom_ordering
        ).filter(
            project=project,
        ).exclude( COMPATITOR ='TOTAL').values(
            'MONTH', 'project', 'COMPATITOR'
        ).annotate(
            DONE_COUNT=Sum('DONE_COUNT'),
            PROJECTED_COUNT=Sum('PROJECTED_COUNT')
        ).order_by('custom_order')

        #CODE FOR OVERALL COUNT
        result = (
         objects.filter(project=project)
        .exclude(COMPATITOR='TOTAL')
        .values('MONTH')
        .annotate(
            sum_projected_count=Sum(done_or_projected),
            month_order=Case(
                When(MONTH='JAN', then=Value(1)),
                When(MONTH='FEB', then=Value(2)),
                When(MONTH='MAR', then=Value(3)),
                When(MONTH='APR', then=Value(4)),
                When(MONTH='MAY', then=Value(5)),
                When(MONTH='JUN', then=Value(6)),
                When(MONTH='JUL', then=Value(7)),
                When(MONTH='AUG', then=Value(8)),
                When(MONTH='SEP', then=Value(9)),
                When(MONTH='OCT', then=Value(10)),
                When(MONTH='NOV', then=Value(11)),
                When(MONTH='DEC', then=Value(12)),
                default=Value(999),
                output_field=IntegerField(),
            )
        )
        .order_by('month_order')
    )


    if circle != "ALL" and project == "ALL":
        #CODE FOR ALLOCATED COUNT DISTRIBUTION PARTNER WISE
        custom_ordering = Case(
        When(MONTH='JAN', then=Value(1)),
        When(MONTH='FEB', then=Value(2)),
        When(MONTH='MAR', then=Value(3)),
        When(MONTH='APR', then=Value(4)),
        When(MONTH='MAY', then=Value(5)),
        When(MONTH='JUN', then=Value(6)),
        When(MONTH='JUL', then=Value(7)),
        When(MONTH='AUG', then=Value(8)),
        When(MONTH='SEP', then=Value(9)),
        When(MONTH='OCT', then=Value(10)),
        When(MONTH='NOV', then=Value(11)),
        When(MONTH='DEC', then=Value(12)),
        default=Value(999),  # Handle unexpected values
        output_field=IntegerField(),
        )

        # Query to retrieve the filtered data with custom ordering
        queryset = objects.annotate(
            custom_order=custom_ordering
        ).filter(
            circle = circle,
        ).exclude( COMPATITOR ='TOTAL').values(
            'MONTH', 'circle', 'COMPATITOR'
        ).annotate(
            DONE_COUNT=Sum('DONE_COUNT'),
            PROJECTED_COUNT=Sum('PROJECTED_COUNT')
        ).order_by('custom_order')

        #CODE FOR OVERALL COUNTS
        result = (
        objects
        .values("MONTH")
        .filter( circle=circle).exclude(COMPATITOR='TOTAL',)
        .annotate(
            sum_projected_count=Sum(done_or_projected),
            month_order=Case(
                When(MONTH='JAN', then=Value(1)),
                When(MONTH='FEB', then=Value(2)),
                When(MONTH='MAR', then=Value(3)),
                When(MONTH='APR', then=Value(4)),
                When(MONTH='MAY', then=Value(5)),
                When(MONTH='JUN', then=Value(6)),
                When(MONTH='JUL', then=Value(7)),
                When(MONTH='AUG', then=Value(8)),
                When(MONTH='SEP', then=Value(9)),
                When(MONTH='OCT', then=Value(10)),
                When(MONTH='NOV', then=Value(11)),
                When(MONTH='DEC', then=Value(12)),
                default=Value(999),
                output_field=IntegerField(),
            )
        )
        .order_by("month_order")
    )

    if circle == "ALL" and project == "ALL":
        ##CODE FOR ALLOCATED COUNT DISTRIBUTION PARTNER WISE
        custom_ordering = Case(
        When(MONTH='JAN', then=Value(1)),
        When(MONTH='FEB', then=Value(2)),
        When(MONTH='MAR', then=Value(3)),
        When(MONTH='APR', then=Value(4)),
        When(MONTH='MAY', then=Value(5)),
        When(MONTH='JUN', then=Value(6)),
        When(MONTH='JUL', then=Value(7)),
        When(MONTH='AUG', then=Value(8)),
        When(MONTH='SEP', then=Value(9)),
        When(MONTH='OCT', then=Value(10)),
        When(MONTH='NOV', then=Value(11)),
        When(MONTH='DEC', then=Value(12)),
        default=Value(999),  # Handle unexpected values
        output_field=IntegerField(),
        )

        # Query to retrieve the filtered data with custom ordering
        queryset = objects.annotate(
            custom_order=custom_ordering
        ).exclude( COMPATITOR ='TOTAL').values(
            'MONTH','COMPATITOR'
        ).annotate(
            DONE_COUNT=Sum('DONE_COUNT'),
            PROJECTED_COUNT=Sum('PROJECTED_COUNT')
        ).order_by('custom_order')

        #CODE FOR OVERALL COUNT
        result = (
        objects
        .exclude(COMPATITOR='TOTAL')
        .values('MONTH')
        .annotate(
            sum_projected_count=Sum(done_or_projected),
            month_order=Case(
                When(MONTH='JAN', then=Value(1)),
                When(MONTH='FEB', then=Value(2)),
                When(MONTH='MAR', then=Value(3)),
                When(MONTH='APR', then=Value(4)),
                When(MONTH='MAY', then=Value(5)),
                When(MONTH='JUN', then=Value(6)),
                When(MONTH='JUL', then=Value(7)),
                When(MONTH='AUG', then=Value(8)),
                When(MONTH='SEP', then=Value(9)),
                When(MONTH='OCT', then=Value(10)),
                When(MONTH='NOV', then=Value(11)),
                When(MONTH='DEC', then=Value(12)),
                default=Value(999),
                output_field=IntegerField(),
            )
        )
        .order_by('month_order')
    )

            
        
    return Response({"status": True, "data":queryset ,"airtel_bucket":result })


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
        upload_report_table.objects.exclude(COMPATITOR="TOTAL")
        .values("MONTH")
        .annotate(total_projected_count=Sum(Cast("DONE_COUNT", IntegerField())))
    )

    query_set = (
        upload_report_table.objects.filter(YEAR=Year).exclude(COMPATITOR="TOTAL")
        .values("MONTH", "COMPATITOR","YEAR")
        .annotate(
            sum_projected_count=Sum(Cast("DONE_COUNT", IntegerField())),
            month_numeric=ExpressionWrapper(
                Case(
                    *[
                        When(MONTH=month, then=Value(month_num))
                        for month, month_num in month_mapping.items()
                    ],
                    output_field=IntegerField(),
                ),
                output_field=IntegerField(),
            ),
        )
        .annotate(
            total_projected_count=total_projected_counts.filter(MONTH=OuterRef("MONTH"))
            .values("MONTH")
            .annotate(total_projected_count=Sum(Cast("DONE_COUNT", IntegerField())))
            .values("total_projected_count"),
            percentage=ExpressionWrapper(
                F("sum_projected_count") * 100.0 / F("total_projected_count"),
                output_field=FloatField(),
            ),
        )
        .order_by("month_numeric")
    )

    return Response({"status": True, "data": query_set})


@api_view(["GET", "POST"])
def project_comparision(request):
    circle = request.POST.get("CIRCLE")
    print(circle)
    compatitor = request.POST.get("COMPATITOR")
    print(compatitor)
    DONE_COUNT = request.POST.get("DONE_COUNT")
    print(DONE_COUNT)
    month_mapping = {
    'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4,
    'MAY': 5, 'JUN': 6, 'JUL': 7, 'AUG': 8,
    'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12
    }
    
    if DONE_COUNT=="True":
        if circle != "ALL"  and compatitor !="ALL":
            result_queryset = (
                        upload_report_table.objects
                        .filter(COMPATITOR=compatitor,circle=circle)
                        .values('MONTH', 'project')
                        .annotate(Counting=Sum('DONE_COUNT'))
                        .annotate(month_order=Case(
                            When(MONTH='JAN', then=Value(1)),
                            When(MONTH='FEB', then=Value(2)),
                            When(MONTH='MAR', then=Value(3)),
                            When(MONTH='APR', then=Value(4)),
                            When(MONTH='MAY', then=Value(5)),
                            When(MONTH='JUN', then=Value(6)),
                            When(MONTH='JUL', then=Value(7)),
                            When(MONTH='AUG', then=Value(8)),
                            When(MONTH='SEP', then=Value(9)),
                            When(MONTH='OCT', then=Value(10)),
                            When(MONTH='NOV', then=Value(11)),
                            When(MONTH='DEC', then=Value(12)),
                            default=Value(999),  # Handle unexpected values
                            output_field=IntegerField()
                        ))
                        .order_by('month_order')
                    )
            overall_result = upload_report_table.objects.filter(circle=circle , COMPATITOR = compatitor).values('MONTH').annotate(
                                    sum_projected_count=Sum('DONE_COUNT')
                                ).annotate(
                                    month_numeric=Case(
                                        When(MONTH='JAN', then=Value(1)),
                                        When(MONTH='FEB', then=Value(2)),
                                        When(MONTH='MAR', then=Value(3)),
                                        When(MONTH='APR', then=Value(4)),
                                        When(MONTH='MAY', then=Value(5)),
                                        When(MONTH='JUN', then=Value(6)),
                                        When(MONTH='JUL', then=Value(7)),
                                        When(MONTH='AUG', then=Value(8)),
                                        When(MONTH='SEP', then=Value(9)),
                                        When(MONTH='OCT', then=Value(10)),
                                        When(MONTH='NOV', then=Value(11)),
                                        When(MONTH='DEC', then=Value(12)),
                                        default=Value(999),  # Handle unexpected values
                                        output_field=IntegerField(),
                                    )
                                ).order_by('month_numeric')

        if  circle == "ALL"  and compatitor !="ALL":
            result_queryset = (
                        upload_report_table.objects
                        .filter(COMPATITOR=compatitor)
                        .values('MONTH', 'project')
                        .annotate(Counting=Sum('DONE_COUNT'))
                        .annotate(month_order=Case(
                            When(MONTH='JAN', then=Value(1)),
                            When(MONTH='FEB', then=Value(2)),
                            When(MONTH='MAR', then=Value(3)),
                            When(MONTH='APR', then=Value(4)),
                            When(MONTH='MAY', then=Value(5)),
                            When(MONTH='JUN', then=Value(6)),
                            When(MONTH='JUL', then=Value(7)),
                            When(MONTH='AUG', then=Value(8)),
                            When(MONTH='SEP', then=Value(9)),
                            When(MONTH='OCT', then=Value(10)),
                            When(MONTH='NOV', then=Value(11)),
                            When(MONTH='DEC', then=Value(12)),
                            default=Value(999),  # Handle unexpected values
                            output_field=IntegerField()
                        ))
                        .order_by('month_order')
                    )
            overall_result = upload_report_table.objects.filter( COMPATITOR = compatitor).values('MONTH').annotate(
                                        sum_projected_count=Sum('DONE_COUNT')
                                    ).annotate(
                                        month_numeric=Case(
                                            When(MONTH='JAN', then=Value(1)),
                                            When(MONTH='FEB', then=Value(2)),
                                            When(MONTH='MAR', then=Value(3)),
                                            When(MONTH='APR', then=Value(4)),
                                            When(MONTH='MAY', then=Value(5)),
                                            When(MONTH='JUN', then=Value(6)),
                                            When(MONTH='JUL', then=Value(7)),
                                            When(MONTH='AUG', then=Value(8)),
                                            When(MONTH='SEP', then=Value(9)),
                                            When(MONTH='OCT', then=Value(10)),
                                            When(MONTH='NOV', then=Value(11)),
                                            When(MONTH='DEC', then=Value(12)),
                                            default=Value(999),  # Handle unexpected values
                                            output_field=IntegerField(),
                                        )
                                    ).order_by('month_numeric')

        if  circle !="ALL"  and compatitor =="ALL":
           result_queryset = (
                        upload_report_table.objects
                        .filter(circle=circle)
                        .exclude(COMPATITOR='TOTAL')
                        .values('MONTH', 'project')
                        .annotate(Counting=Sum('DONE_COUNT'))
                        .annotate(month_order=Case(
                            When(MONTH='JAN', then=Value(1)),
                            When(MONTH='FEB', then=Value(2)),
                            When(MONTH='MAR', then=Value(3)),
                            When(MONTH='APR', then=Value(4)),
                            When(MONTH='MAY', then=Value(5)),
                            When(MONTH='JUN', then=Value(6)),
                            When(MONTH='JUL', then=Value(7)),
                            When(MONTH='AUG', then=Value(8)),
                            When(MONTH='SEP', then=Value(9)),
                            When(MONTH='OCT', then=Value(10)),
                            When(MONTH='NOV', then=Value(11)),
                            When(MONTH='DEC', then=Value(12)),
                            default=Value(999),  # Handle unexpected values
                            output_field=IntegerField()
                        ))
                        .order_by('month_order')
                    )
           overall_result = upload_report_table.objects.filter(circle=circle).exclude(COMPATITOR='TOTAL').values('MONTH').annotate(
                                    sum_projected_count=Sum('DONE_COUNT')
                                ).annotate(
                                    month_numeric=Case(
                                        When(MONTH='JAN', then=Value(1)),
                                        When(MONTH='FEB', then=Value(2)),
                                        When(MONTH='MAR', then=Value(3)),
                                        When(MONTH='APR', then=Value(4)),
                                        When(MONTH='MAY', then=Value(5)),
                                        When(MONTH='JUN', then=Value(6)),
                                        When(MONTH='JUL', then=Value(7)),
                                        When(MONTH='AUG', then=Value(8)),
                                        When(MONTH='SEP', then=Value(9)),
                                        When(MONTH='OCT', then=Value(10)),
                                        When(MONTH='NOV', then=Value(11)),
                                        When(MONTH='DEC', then=Value(12)),
                                        default=Value(999),  # Handle unexpected values
                                        output_field=IntegerField(),
                                    )
                                ).order_by('month_numeric')
           
        if  circle =="ALL"  and compatitor =="ALL":
           result_queryset = (
                        upload_report_table.objects
                        .exclude(COMPATITOR='TOTAL')
                        .values('MONTH', 'project')
                        .annotate(Counting=Sum('DONE_COUNT'))
                        .annotate(month_order=Case(
                            When(MONTH='JAN', then=Value(1)),
                            When(MONTH='FEB', then=Value(2)),
                            When(MONTH='MAR', then=Value(3)),
                            When(MONTH='APR', then=Value(4)),
                            When(MONTH='MAY', then=Value(5)),
                            When(MONTH='JUN', then=Value(6)),
                            When(MONTH='JUL', then=Value(7)),
                            When(MONTH='AUG', then=Value(8)),
                            When(MONTH='SEP', then=Value(9)),
                            When(MONTH='OCT', then=Value(10)),
                            When(MONTH='NOV', then=Value(11)),
                            When(MONTH='DEC', then=Value(12)),
                            default=Value(999),  # Handle unexpected values
                            output_field=IntegerField()
                        ))
                        .order_by('month_order')
                    )
           overall_result = upload_report_table.objects.exclude(COMPATITOR='TOTAL').values('MONTH').annotate(
                                    sum_projected_count=Sum('DONE_COUNT')
                                ).annotate(
                                    month_numeric=Case(
                                        When(MONTH='JAN', then=Value(1)),
                                        When(MONTH='FEB', then=Value(2)),
                                        When(MONTH='MAR', then=Value(3)),
                                        When(MONTH='APR', then=Value(4)),
                                        When(MONTH='MAY', then=Value(5)),
                                        When(MONTH='JUN', then=Value(6)),
                                        When(MONTH='JUL', then=Value(7)),
                                        When(MONTH='AUG', then=Value(8)),
                                        When(MONTH='SEP', then=Value(9)),
                                        When(MONTH='OCT', then=Value(10)),
                                        When(MONTH='NOV', then=Value(11)),
                                        When(MONTH='DEC', then=Value(12)),
                                        default=Value(999),  # Handle unexpected values
                                        output_field=IntegerField(),
                                    )
                                ).order_by('month_numeric')

        # Select the desired columns
        result_queryset = result_queryset.values("MONTH", "project", "Counting")

        # Execute the queryset to get the result
        results = result_queryset.all()



   

        return Response({
            "status":True,
            "message":"Successfully fetched ...",
            "data":results,
            "overall_data":overall_result
        })

    else :
        if circle != "ALL"  and compatitor !="ALL":
            result_queryset = (
                        upload_report_table.objects
                        .filter(COMPATITOR=compatitor,circle=circle)
                        .values('MONTH', 'project')
                        .annotate(Counting=Sum('PROJECTED_COUNT'))
                        .annotate(month_order=Case(
                            When(MONTH='JAN', then=Value(1)),
                            When(MONTH='FEB', then=Value(2)),
                            When(MONTH='MAR', then=Value(3)),
                            When(MONTH='APR', then=Value(4)),
                            When(MONTH='MAY', then=Value(5)),
                            When(MONTH='JUN', then=Value(6)),
                            When(MONTH='JUL', then=Value(7)),
                            When(MONTH='AUG', then=Value(8)),
                            When(MONTH='SEP', then=Value(9)),
                            When(MONTH='OCT', then=Value(10)),
                            When(MONTH='NOV', then=Value(11)),
                            When(MONTH='DEC', then=Value(12)),
                            default=Value(999),  # Handle unexpected values
                            output_field=IntegerField()
                        ))
                        .order_by('month_order')
                    )
            overall_result = upload_report_table.objects.filter(circle=circle , COMPATITOR = compatitor).values('MONTH').annotate(
                                    sum_projected_count=Sum('PROJECTED_COUNT')
                                ).annotate(
                                    month_numeric=Case(
                                        When(MONTH='JAN', then=Value(1)),
                                        When(MONTH='FEB', then=Value(2)),
                                        When(MONTH='MAR', then=Value(3)),
                                        When(MONTH='APR', then=Value(4)),
                                        When(MONTH='MAY', then=Value(5)),
                                        When(MONTH='JUN', then=Value(6)),
                                        When(MONTH='JUL', then=Value(7)),
                                        When(MONTH='AUG', then=Value(8)),
                                        When(MONTH='SEP', then=Value(9)),
                                        When(MONTH='OCT', then=Value(10)),
                                        When(MONTH='NOV', then=Value(11)),
                                        When(MONTH='DEC', then=Value(12)),
                                        default=Value(999),  # Handle unexpected values
                                        output_field=IntegerField(),
                                    )
                                ).order_by('month_numeric')

        if  circle == "ALL"  and compatitor !="ALL":
           result_queryset = (
                        upload_report_table.objects
                        .filter(COMPATITOR=compatitor)
                        .values('MONTH', 'project')
                        .annotate(Counting=Sum('PROJECTED_COUNT'))
                        .annotate(month_order=Case(
                            When(MONTH='JAN', then=Value(1)),
                            When(MONTH='FEB', then=Value(2)),
                            When(MONTH='MAR', then=Value(3)),
                            When(MONTH='APR', then=Value(4)),
                            When(MONTH='MAY', then=Value(5)),
                            When(MONTH='JUN', then=Value(6)),
                            When(MONTH='JUL', then=Value(7)),
                            When(MONTH='AUG', then=Value(8)),
                            When(MONTH='SEP', then=Value(9)),
                            When(MONTH='OCT', then=Value(10)),
                            When(MONTH='NOV', then=Value(11)),
                            When(MONTH='DEC', then=Value(12)),
                            default=Value(999),  # Handle unexpected values
                            output_field=IntegerField()
                        ))
                        .order_by('month_order')
                    )
           overall_result = upload_report_table.objects.filter( COMPATITOR = compatitor).values('MONTH').annotate(
                                    sum_projected_count=Sum('PROJECTED_COUNT')
                                ).annotate(
                                    month_numeric=Case(
                                        When(MONTH='JAN', then=Value(1)),
                                        When(MONTH='FEB', then=Value(2)),
                                        When(MONTH='MAR', then=Value(3)),
                                        When(MONTH='APR', then=Value(4)),
                                        When(MONTH='MAY', then=Value(5)),
                                        When(MONTH='JUN', then=Value(6)),
                                        When(MONTH='JUL', then=Value(7)),
                                        When(MONTH='AUG', then=Value(8)),
                                        When(MONTH='SEP', then=Value(9)),
                                        When(MONTH='OCT', then=Value(10)),
                                        When(MONTH='NOV', then=Value(11)),
                                        When(MONTH='DEC', then=Value(12)),
                                        default=Value(999),  # Handle unexpected values
                                        output_field=IntegerField(),
                                    )
                                ).order_by('month_numeric')

        if  circle !="ALL"  and compatitor =="ALL":
           result_queryset = (
                        upload_report_table.objects
                        .filter(circle=circle)
                        .exclude(COMPATITOR='TOTAL')
                        .values('MONTH', 'project')
                        .annotate(Counting=Sum('PROJECTED_COUNT'))
                        .annotate(month_order=Case(
                            When(MONTH='JAN', then=Value(1)),
                            When(MONTH='FEB', then=Value(2)),
                            When(MONTH='MAR', then=Value(3)),
                            When(MONTH='APR', then=Value(4)),
                            When(MONTH='MAY', then=Value(5)),
                            When(MONTH='JUN', then=Value(6)),
                            When(MONTH='JUL', then=Value(7)),
                            When(MONTH='AUG', then=Value(8)),
                            When(MONTH='SEP', then=Value(9)),
                            When(MONTH='OCT', then=Value(10)),
                            When(MONTH='NOV', then=Value(11)),
                            When(MONTH='DEC', then=Value(12)),
                            default=Value(999),  # Handle unexpected values
                            output_field=IntegerField()
                        ))
                        .order_by('month_order')
                    )
           overall_result = upload_report_table.objects.filter(circle=circle).exclude(COMPATITOR='TOTAL').values('MONTH').annotate(
                                    sum_projected_count=Sum('PROJECTED_COUNT')
                                ).annotate(
                                    month_numeric=Case(
                                        When(MONTH='JAN', then=Value(1)),
                                        When(MONTH='FEB', then=Value(2)),
                                        When(MONTH='MAR', then=Value(3)),
                                        When(MONTH='APR', then=Value(4)),
                                        When(MONTH='MAY', then=Value(5)),
                                        When(MONTH='JUN', then=Value(6)),
                                        When(MONTH='JUL', then=Value(7)),
                                        When(MONTH='AUG', then=Value(8)),
                                        When(MONTH='SEP', then=Value(9)),
                                        When(MONTH='OCT', then=Value(10)),
                                        When(MONTH='NOV', then=Value(11)),
                                        When(MONTH='DEC', then=Value(12)),
                                        default=Value(999),  # Handle unexpected values
                                        output_field=IntegerField(),
                                    )
                                ).order_by('month_numeric')
           
        if  circle =="ALL"  and compatitor =="ALL":
           result_queryset = (
                        upload_report_table.objects
                        .exclude(COMPATITOR='TOTAL')
                        .values('MONTH', 'project')
                        .annotate(Counting=Sum('PROJECTED_COUNT'))
                        .annotate(month_order=Case(
                            When(MONTH='JAN', then=Value(1)),
                            When(MONTH='FEB', then=Value(2)),
                            When(MONTH='MAR', then=Value(3)),
                            When(MONTH='APR', then=Value(4)),
                            When(MONTH='MAY', then=Value(5)),
                            When(MONTH='JUN', then=Value(6)),
                            When(MONTH='JUL', then=Value(7)),
                            When(MONTH='AUG', then=Value(8)),
                            When(MONTH='SEP', then=Value(9)),
                            When(MONTH='OCT', then=Value(10)),
                            When(MONTH='NOV', then=Value(11)),
                            When(MONTH='DEC', then=Value(12)),
                            default=Value(999),  # Handle unexpected values
                            output_field=IntegerField()
                        ))
                        .order_by('month_order')
                    )
           overall_result = upload_report_table.objects.exclude(COMPATITOR='TOTAL').values('MONTH').annotate(
                                    sum_projected_count=Sum('PROJECTED_COUNT')
                                ).annotate(
                                    month_numeric=Case(
                                        When(MONTH='JAN', then=Value(1)),
                                        When(MONTH='FEB', then=Value(2)),
                                        When(MONTH='MAR', then=Value(3)),
                                        When(MONTH='APR', then=Value(4)),
                                        When(MONTH='MAY', then=Value(5)),
                                        When(MONTH='JUN', then=Value(6)),
                                        When(MONTH='JUL', then=Value(7)),
                                        When(MONTH='AUG', then=Value(8)),
                                        When(MONTH='SEP', then=Value(9)),
                                        When(MONTH='OCT', then=Value(10)),
                                        When(MONTH='NOV', then=Value(11)),
                                        When(MONTH='DEC', then=Value(12)),
                                        default=Value(999),  # Handle unexpected values
                                        output_field=IntegerField(),
                                    )
                                ).order_by('month_numeric')

    # Select the desired columns
    result_queryset = result_queryset.values("MONTH", "project", "Counting")

    # Execute the queryset to get the result
    results = result_queryset.all()



   

    return Response({
        "status":True,
        "message":"Successfully fetched ...",
        "data":results,
        "overall_data":overall_result
    })


@api_view(["POST","GET"])
def projectWise_circle_comparision_pichart(request):
    compatitor = request.POST.get("COMPATITOR")
    print(compatitor)
    # circle = request.POST.get("circle")
    project = request.POST.get("project")
    print(project)
    month = request.POST.get("MONTH")
    print(month)
    done_count = request.POST.get("DONE_COUNT")
    print(done_count)

  
    

    if done_count == "False":
        # Calculate the total sum of PROJECTED_COUNT for the specified conditions
        total_sum = upload_report_table.objects.filter(
            COMPATITOR=compatitor, project=project, MONTH=month
        ).aggregate(total_sum=Sum('PROJECTED_COUNT'))['total_sum']

        # Query to calculate the sum_projected_count without the percentage
        queryset = (
            upload_report_table.objects
            .filter(COMPATITOR='MobileComm', project='ULS', MONTH='JAN')
            .values('COMPATITOR', 'MONTH', 'project', 'circle')
            .annotate(sum_projected_count=Sum('PROJECTED_COUNT'))
            .order_by('project')
        )

        # Calculate the projected_count_percentage in Python
        result = [
            {
                'COMPATITOR': item['COMPATITOR'],
                'MONTH': item['MONTH'],
                'project': item['project'],
                'circle': item['circle'],
                'sum_projected_count': item['sum_projected_count'],
                'projected_count_percentage': round(item['sum_projected_count'] * 100.0 / total_sum, 2),
            }
            for item in queryset
        ]
    else:
        total_sum = upload_report_table.objects.filter(
            COMPATITOR=compatitor, project=project, MONTH=month
        ).aggregate(total_sum=Sum('DONE_COUNT'))['total_sum']

        # Query to calculate the sum_projected_count without the percentage
        queryset = (
            upload_report_table.objects
            .filter(COMPATITOR=compatitor, project=project, MONTH=month)
            .values('COMPATITOR', 'MONTH', 'project', 'circle')
            .annotate(sum_projected_count=Sum('DONE_COUNT'))
            .order_by('project')
        )

        # Calculate the projected_count_percentage in Python
        result = [
            {
                'COMPATITOR': item['COMPATITOR'],
                'MONTH': item['MONTH'],
                'project': item['project'],
                'circle': item['circle'],
                'sum_projected_count': item['sum_projected_count'],
                'projected_count_percentage': round(item['sum_projected_count'] * 100.0 / total_sum, 2),
            }
            for item in queryset
        ]

    # result_queryset = result.values("MONTH", "COMPATITOR", "circle", "project","sum_projected_count","total_projected_count","projected_count_percentage")

    # results = result_queryset.all()
    print(result)

    unique_circle = upload_report_table.objects.values('circle').distinct()
  
    print(unique_circle)
    return Response({
        'status':True,
        'message':"Done Sucessfully......",
        'data':result,
        "unique_circle":unique_circle
    })

#generate kpi trend in desired format


@api_view(["GET","POST"])
def project_wise_partners_ranking_of_perticular_circle_and_month(request):
    month = request.POST.get("MONTH")
    circle = request.POST.get("circle")


    if circle != "ALL":
        query_set = (
            upload_report_table.objects
            .exclude(COMPATITOR='TOTAL')
            .filter(MONTH=month, circle=circle,YEAR=Year)
            .values('project', 'COMPATITOR', 'DONE_COUNT')
            .annotate(
                partners_rank=Window(
                    expression=Rank(),
                    partition_by=[F('project')],
                    order_by=F('DONE_COUNT').desc()
                )
            )
            .order_by('project', '-DONE_COUNT')
        )

    if circle=="ALL":
            query_set = upload_report_table.objects.filter(
            MONTH='JAN'
        ).exclude(COMPATITOR='TOTAL').annotate(
            partners_rank=Window(expression=Rank(),
                    partition_by=[F('project')],
                    order_by=F('PROJECTED_COUNT').desc()
            )
        ).values(
            'project',
            'COMPATITOR',
            'PROJECTED_COUNT',
            'partners_rank'
        ).order_by(
            'project',
            '-partners_rank'  # Descending order for rank
        )
        # pass
    
    ############################# dataframe operations ######################
    df=pd.DataFrame(query_set)
    print(df.fillna(0, inplace=True))
    df_piv = df.pivot_table(columns=["COMPATITOR"],index=["project"],values=["partners_rank"])
    df_piv1=df_piv["partners_rank"]
    # df_piv1.fillna(0,inplace=True)
    json_data = df_piv1.to_json(orient='index')
    print("Jsone_data----:",json_data)
    ######################****************************#########################
    return Response({
        'Status':True,
        'message':"Successfully Done.....",
        'data':json_data,
    })


    
###################################### MDP upload ###############################
    # views.py
import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ProjectedData

@api_view(['POST'])
def bulk_upload(request):
    print(request.data)
    circle = request.data.get('circle')
    month = request.data.get('month')
    aop = request.data.get('aop')
    actual_or_projected = request.data.get('actual_or_projected')

    if not circle or not month or not actual_or_projected:
        return Response({'error': 'Circle, month, and actual_or_projected are required'}, status=status.HTTP_400_BAD_REQUEST)

    if 'file' not in request.FILES:
        return Response({'error': 'No file found in request'}, status=status.HTTP_400_BAD_REQUEST)

    excel_file = request.FILES['file']
    if not excel_file.name.endswith(('.xls', '.xlsx')):
        return Response({'error': 'Please upload a valid Excel file'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        df = pd.read_excel(excel_file,skiprows=1)
        df.columns = [col.strip() for col in df.columns] # to remove the  leading and trailing spaces from the column name
        if actual_or_projected == "Projected":
            for index, row in df.iterrows():
                obj, created = ProjectedData.objects.update_or_create(
                    circle=circle,
                    month=month,
                    project=row['Project'],
                    aop=aop,
                    defaults={
                        # 'actual_or_projected': actual_or_projected,
                        'airtel_projection': row['Airtel Projection'],
                        'mobilecomm_projection': row['Mobilecomm Projection'],
                        'uploaded_by':request.user.username
                    }
                )
        elif actual_or_projected == "Actual":
            for index, row in df.iterrows():
                obj, created = ActualData.objects.update_or_create(
                    circle=circle,
                    month=month,
                    project=row['Project'],
                    aop=aop,
                    defaults={
                        # 'actual_or_projected': actual_or_projected,
                        'airtel_actual': row['Airtel Actual'],
                        'mobilecomm_actual': row['Mobilecomm Actual'],
                        'Ericsson_Actual': row['Ericsson Actual'],
                        'Nokia_Actual': row['Nokia Actual'],
                        'vedang_actual': row['Vedang Actual'],
                        'frog_cell_actual': row['Frog Cell Actual'],
                        'ariel_actual': row['Ariel Actual'],
                        'others_actual': row['Others'],
                        'uploaded_by':request.user.username
                    }
                )    
        return Response({'message': 'Bulk upload successful'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(str(e))
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


api_view(["GET"])
def data(request):
    print(ActualData.objects.all())

from django.conf import settings
import os
@api_view(['GET'])
def get_excel_temp_link_actual(request):
    user = request.user
    # user_circle = get_user_circle(request)
    print("usrname: ", user)
    # Path to the Excel file
    file_path = os.path.join(settings.MEDIA_ROOT, 'MDP',"template", 'Actual Template.xlsx')

    # Check if the file exists
    if os.path.exists(file_path):
        # Construct the URL to access the file
        file_url = os.path.join(settings.MEDIA_URL ,'MDP',"template" , 'Actual Template.xlsx')              
        return Response({'file_url': file_url}, status=status.HTTP_200_OK)
    else:
        # Return a 404 response if the file does not exist
        return Response({'error': 'Excel file not found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def get_excel_temp_link_projected(request):
    user = request.user
    # user_circle = get_user_circle(request)
    print("usrname: ", user)
    # Path to the Excel file
    file_path = os.path.join(settings.MEDIA_ROOT, 'MDP',"template", 'Projection Template.xlsx')

    # Check if the file exists
    if os.path.exists(file_path):
        # Construct the URL to access the file
        file_url = os.path.join(settings.MEDIA_URL ,'MDP',"template" , 'Projection Template.xlsx')              
        return Response({'file_url': file_url}, status=status.HTTP_200_OK)
    else:
        # Return a 404 response if the file does not exist
        return Response({'error': 'Excel file not found'}, status=status.HTTP_404_NOT_FOUND)
    


import requests

def fetch_data_from_api(request):
    print(request.headers)
    url = 'http://103.242.225.195:8000/get_user_circle'
    token=request.headers.get('Authorization')
    print(token)
    headers = {
        'Authorization': token  # Replace 'your_access_token' with the actual token
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        
        return response.json()  # return the JSON data
    else:
        return None


@api_view(['GET'])
def view_MDP_projection(request):
     data=fetch_data_from_api(request)
     circle=data.get('circle').split(',')
     if 'Admin' in circle:
         objects=ProjectedData.objects.all()
     else:
         objects=ProjectedData.objects.filter(circle__in=circle)
    #  objects=ProjectedData.objects.filter(circle__in=circle)
     data = ProjectedDataSerializer(objects, many=True).data
     return Response({'data' :data},status=status.HTTP_200_OK)


@api_view(['GET'])
def view_MDP_actual(request):
     data=fetch_data_from_api(request)
     circle=data.get('circle').split(',')
     if 'Admin' in circle:
         objects=ActualData.objects.all()
     else:
         objects=ActualData.objects.filter(circle__in=circle)
 
     data = ActualDataSerializer(objects, many=True).data
     return Response({'data' :data},status=status.HTTP_200_OK)