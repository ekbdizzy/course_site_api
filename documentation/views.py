from django.shortcuts import render


# Create your views here.
def documentation_view(request):
    return render(request, 'documentation/documentation.html', {})
