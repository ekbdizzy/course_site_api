from django.urls import path
from .views import documentation_view

app_name = 'documentation'

urlpatterns = [
    path('', documentation_view, name="documentation")
]