from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
from Profile.models import ProfileModel, userCircle
from Profile.serializers import ProfileModelSer
from rest_framework import status

@api_view(["GET"])
def get_profile_data(request, employee_name):
    try:
        profiles = ProfileModel.objects.filter(Employee_Name=employee_name)
        print(profiles)
    except ProfileModel.DoesNotExist:
        return Response(
            {
                "status": False,
                "message": "Profile not found.",
            },
        )

    if profiles.exists():
        serializer = ProfileModelSer(profiles, many=True)
        return Response(
            {
                "status": "200",
                "message": f"Successfully retrieved profiles for {employee_name}",
                "data": serializer.data,
            }
        )
    else:
        return Response(
            {
                "status": "404",
                "message": f"No profiles found for {employee_name}",
                "data": [],
            }
        )


@api_view(["PATCH", "POST", "GET"])
def update_profile_data(request, employee_name):
    try:
        item = ProfileModel.objects.get(Employee_Name=employee_name)
    except ProfileModel.DoesNotExist:
        return Response(
            {
                "status": False,
                "message": "Profile not found.",
            },
        )

    data = ProfileModelSer(instance=item, data=request.data, partial=True)

    if data.is_valid():
        data.save()
        return Response(
            {
                "status": True,
                "message": "Updated successfully.",
                "data": data.data,
            }
        )
    else:
        return Response(
            {
                "status": False,
                "message": "Validation error.",
                "errors": data.errors,
            }
        )


@api_view(['GET'])
def get_user_circle(request):
    print("user...")
    user = request.user
    print("user:",request.user)
    try:
        user_circle = user.usercircle.Circle
        user_catagory = user.usercircle.user_catagory
        return Response({'circle': user_circle,"user_catagory":user_catagory}, status=status.HTTP_200_OK)
    except userCircle.DoesNotExist:
        return Response({'error': 'Circle not found for the user'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(["GET"])
def data(request):
    return Response({"sata":"hihi"})