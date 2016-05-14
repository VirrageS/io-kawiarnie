from django.shortcuts import render


def statistics_navigate(request):
    return render(request, 'home/statistics.html')
