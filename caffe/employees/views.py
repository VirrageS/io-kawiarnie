from django.shortcuts import render

def employees_login_employee(request):
    return render(request, 'employees/login.html')

# TODO: create middleware to check if employee is logged in
def employees_logout_employee(request):
    return render(request, 'employees/logout.html')
