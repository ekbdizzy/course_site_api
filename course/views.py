from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from user.models import User
from .models import Course, StudentOnCourse
from .serializers import CourseSerializer
from lesson.serializers import LessonSerializer
from user.serializers import StudentSerializer


# Create your views here.
@permission_classes((AllowAny,))
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


@permission_classes((AllowAny,))
class CourseDetailView(APIView):

    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        course_serializer = CourseSerializer(course)
        data = course_serializer.data

        lessons = course.lessons.all()
        lesson_serializer = LessonSerializer(lessons, many=True)
        data['lessons'] = lesson_serializer.data

        students = course.students.all()
        user_serializer = StudentSerializer(students, many=True)
        data['students'] = user_serializer.data
        return Response(data)

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


class StudentsOnCourseView(APIView):

    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        students = course.students.all()
        user_serializer = StudentSerializer(students, many=True)
        return Response(user_serializer.data)

    def post(self, request, pk):
        serializer = StudentSerializer(data=request.data)

        if serializer.is_valid():
            course = Course.objects.get(pk=pk)
            email = serializer.validated_data['email']

            try:
                student = User.objects.get(email=email)
                if StudentOnCourse.objects.filter(student=student, course=course):
                    return Response(
                        {"message": f"Student {student.email} is already on course"},
                        status.HTTP_100_CONTINUE
                    )

                StudentOnCourse.objects.create(
                    student=student,
                    course=course,
                    course_is_paid=True,
                )

                students = course.students.all()
                user_serializer = StudentSerializer(students, many=True)
                return Response(user_serializer.data, status.HTTP_201_CREATED)

            except User.DoesNotExist as e:
                return Response({"error": "Student does not exists"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
