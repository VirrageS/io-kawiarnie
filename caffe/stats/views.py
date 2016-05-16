from django.shortcuts import render


def statistics_navigate(request):
    """Show main statistics about cafe."""

    return render(request, 'home/statistics.html')
