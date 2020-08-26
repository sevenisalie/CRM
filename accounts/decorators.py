#yep you guessed it, we're makin custom decorators
from django.http import HttpResponse
from django.shortcuts import redirect


def authenticated_usercheck(view_func):                 #this is how you start a custom decorator.  straight from docs.  function name is whatever you want it to be.  view_func is what you put into it to make it work with django. magic
    def wrapper_func(request, *args, **kwargs):         #this is the second line of a custom decorator.  must take those three arguments and be called wrapper_func. i dont fuckin know, its greek. straight from docs

        if request.user.is_authenticated:
            return redirect('/')
        else:
            return view_func(request, *args, **kwargs)      #MUST ALWAYS INCLUDE. returning this as the wrapper function means just go on with the regular view as its written in views.py

    return wrapper_func                             #always return wrapper_func to the def wrapper_func



def allowed_users(allowed_roles=[]):                #custom decorator that takes a custom argument
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

                group = None
                if request.user.groups.exists():           #query for if groups for users exist
                    group = request.user.groups.all()[0].name     #query for the users group name. idfk. its on google
                if group in allowed_roles:
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponse('You are not authorized to view this page')     #message to display if group of user not in allowed_roles

        return wrapper_func
    return decorator
