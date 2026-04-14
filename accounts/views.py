from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import CustomUser
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            if user.user_role=='student':
                return redirect('student_dashboard')
            elif user.user_role=='guide':
                return redirect('guide_dashboard')
            else:
                return redirect('coordinator_dashboard')
            
        else:
            print("Authentication failed")
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')
def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('login')

