from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication

from .serializers import UserSerializer, CreateProfileSerializer, SalarySerializer, ProfileSerializer
from .utils import token_validator
from .models import Profile, Salary


class AddEmployeeAPI(APIView):
    authentication_classes = [TokenAuthentication, ]

    def post(self, request):
        if "Human Resources" in request.user.groups.values_list('name', flat=True):
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Employee added successfully"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)


class ProfileAPI(APIView):
    authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        profile = ProfileSerializer(request.user.profile)
        return Response(profile.data, status=status.HTTP_200_OK)

    def put(self, request):
        if "Human Resources" in request.user.groups.values_list('name', flat=True):
            profile = Profile.objects.get(id=request.data.get("id"))
            profile_serializer = ProfileSerializer(data=request.data)
            if profile_serializer.is_valid():
                profile_serializer.update(profile, profile_serializer.validated_data)
                return Response(profile_serializer.validated_data, status=status.HTTP_200_OK)
            else:
                return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)


class ListOfProfilesAPI(APIView):
    authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        if "Human Resources" in request.user.groups.values_list('name', flat=True) or \
                "Payroll Manager" in request.user.groups.values_list('name', flat=True):
            profiles = ProfileSerializer(Profile.objects.all(), many=True)
            return Response(profiles.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)


class CreateProfileAPI(APIView):

    def post(self, request, token):
        try:
            user = token_validator(token)
            profile_serializer = CreateProfileSerializer(data=request.data, context={"user": user})
            if profile_serializer.is_valid():
                profile_serializer.save()
                return Response(profile_serializer.validated_data, status=status.HTTP_200_OK)
            else:
                return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Invalid Token"}, status=status.HTTP_400_BAD_REQUEST)


class ListOfPayrollsAPI(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        groups = request.user.groups.values_list('name', flat=True)
        if "Payroll Manager" in groups or "Human Resources" in groups:
            list_of_payrolls = SalarySerializer(data=Salary.objects.all(), many=True)
            return Response(list_of_payrolls.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)


class PayrollsAPI(APIView):
    authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        history = SalarySerializer(request.user.salaries.all(), many=True)
        return Response(history.data, status=status.HTTP_200_OK)

    def post(self, request):
        if "Payroll Manager" in request.user.groups.values_list('name', flat=True):
            salary_serializer = SalarySerializer(data=request.data)
            if salary_serializer.is_valid():
                salary_serializer.save()
                return Response(salary_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": salary_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request):
        if "Payroll Manager" in request.user.groups.values_list('name', flat=True):
            salary = Salary.objects.get(id=request.data.get("id"))
            salary_serializer = SalarySerializer(data=request.data)
            if salary_serializer.is_valid():
                salary_serializer.update(salary, salary_serializer.validated_data)
                return Response(salary_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": salary_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)


class Logout(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
