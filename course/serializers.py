from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "description",
            "start_date",
            "price",
            "duration",
            "icon"
        )

    duration = serializers.CharField(required=False)
