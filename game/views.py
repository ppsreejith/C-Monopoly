from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
import json
from django.http.response import Http404

def index(request):
    return render(request,'index.html',{})

class JsonMixin(object):
    '''
    Mixin to generate Json responses.
    '''
    
    def render(self,context,**kwargs):
        return HttpResponse(self.json(context), content_type="application/json", **kwargs)
    
    def json(self,context):
        #Can be modified later to be better
        return json.dumps(context)

class OnlyPostMixin(object):
    '''
    Mixin to allow only post requests by default.
    '''
    def get(self,request):
        return Http404()

def check_ajax(function):
    '''
    Only allow ajax requests. Else 404 error.
    '''
    def wrapper(request, *args, **kwargs):
        if request.is_ajax():
            return login_required(function)
        else:
            return Http404()
    return wrapper

class ApiTemplate(OnlyPostMixin,JsonMixin,View):
    '''
    Template for json response view
    '''
    @method_decorator(check_ajax)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)