from django.shortcuts import redirect
from functools import wraps
from django.http import HttpResponseForbidden

def recruiter_required(view_func):
    @wraps(view_func)
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated and request.user.user_type == 'recruiter' and not request.user.is_superuser:
            return view_func(request,*args, **kwargs)
        return HttpResponseForbidden("You do not access this page Only Recruiter can access this page")
        
    return wrapper 

def jobseeker_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == 'jobseeker':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')
    return wrapper