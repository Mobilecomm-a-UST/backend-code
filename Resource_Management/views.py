from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import MonthlyReport
from .serializers import MonthlyReportSerializer
from rest_framework.decorators import api_view
import os
from django.conf import settings
from mcom_website.settings import MEDIA_ROOT, MEDIA_URL

class MonthlyReportUpsertView(APIView):

    def get(self, request):
        month    = request.query_params.get('month')
        costCenter = request.query_params.get('costCenter')

        if not all([month, costCenter]):
            return Response({'error': 'Month And Cost Center Required'},status=status.HTTP_400_BAD_REQUEST)

        try:
            report = MonthlyReport.objects.get(month=month,costCenter = costCenter)
        except MonthlyReport.DoesNotExist:
            return Response({'error': 'Record Not found'},status=status.HTTP_404_NOT_FOUND)

        return Response({
            'id':              report.id,
            'circle':          report.circle,
            'category':        report.category,
            'customer':        report.customer,
            'month':           report.month,
            'year':            report.year,
            "costCenter":      report.costCenter,
            'costs':           report.costs,
            'resources':       report.resources,
            'other_resources': report.other_resources,
            'created_at':      report.created_at,
            'updated_at':      report.updated_at,
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MonthlyReportSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'error': serializer.errors},status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        report, created = MonthlyReport.objects.update_or_create(
            
            month    = data['month'],
            costCenter = data['costCenter'],
            defaults = {
                "circle" :data['circle'],
                "category" :data['category'],
                "customer" :data['customer'],
                'year':            data['year'],
                'costs':           data.get['costs',{}],
                'resources':       data.get['resources',{}],
                'other_resources': data.get('other_resources', {}),
            }
        )

        return Response({
            'message':  'Created' if created else 'Updated',
            'id':       report.id,
            'month':    report.month,
            'costCenter':report.costCenter,
            'created_at':      report.created_at,
            'updated_at':      report.updated_at,
        }, status=status.HTTP_200_OK)


class MonthlyReportBulkUpsertView(APIView):

    def post(self, request):
        # Array expect karta hai
        if not isinstance(request.data, list):
            return Response(
                {'error': 'Array bhejo — [ {...}, {...} ]'},
                status=status.HTTP_400_BAD_REQUEST
            )

        results = []
        errors  = []

        for index, item in enumerate(request.data):
            serializer = MonthlyReportSerializer(data=item)

            if not serializer.is_valid():
                errors.append({ 'index': index, 'error': serializer.errors })
                continue

            data = serializer.validated_data

            report, created = MonthlyReport.objects.update_or_create(
                circle     = data['circle'],
                category   = data['category'],
                customer   = data['customer'],
                month      = data['month'],
                costCenter = data['costCenter'],
                defaults   = {
                    'year':            data['year'],
                    'costs':           data['costs'],
                    'resources':       data['resources'],
                    'other_resources': data.get('other_resources', {}),
                    'month_wise_data': data.get('month_wise_data', {}),
                }
            )

            results.append({
                'index':      index,
                'message':    'Created' if created else 'Updated',
                'id':         report.id,
                'month':      report.month,
                'costCenter': report.costCenter,
                'created_at': report.created_at,
                'updated_at': report.updated_at,
            })

        return Response({
            'total':    len(request.data),
            'success':  len(results),
            'failed':   len(errors),
            'results':  results,
            'errors':   errors,
        }, status=status.HTTP_200_OK)




@api_view(['GET'])
def get_excel_temp_link(request):
    fileName = request.query_params.get("fileName", "")
    file_path = os.path.join(settings.MEDIA_ROOT, 'ResourceManagement',fileName)
    if os.path.exists(file_path):
        file_url = os.path.join(settings.MEDIA_URL ,'ResourceManagement',fileName)              
        return Response({'file_url': file_url,'template_version':'v1'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Excel file not found'}, status=status.HTTP_404_NOT_FOUND)