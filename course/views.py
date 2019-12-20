from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .models import Course
from .serializers import CourseSerializer
from lesson.models import Lesson


# Create your views here.
class CoursesListView(APIView):

    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        data = request.data
        if serializer.is_valid():
            if not data or data['start_date']:
                return Response(
                    {'message': "start_date is cannot be empty"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailView(APIView):

    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        lessons = Lesson.objects.filter(course=course)
        serializer = CourseSerializer(course, lessons)
        return Response(serializer.data)

    def patch(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        serializer = CourseSerializer(instance=course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(request.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        serializer = CourseSerializer(course)
        data = serializer.data
        course.delete()
        return Response(data, status=status.HTTP_204_NO_CONTENT)
