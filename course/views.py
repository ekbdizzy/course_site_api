from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Course


# Create your views here.
class CoursesListView(APIView):

    def get(self, request):
        # courses = Course.objects.values_list(flat=True)
        courses = Course.objects.all()
        return Response({courses})
