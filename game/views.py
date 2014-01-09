from django.shortcuts import render, redirect
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.http import HttpResponse
import json
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from govt.models import State
from collections import defaultdict
from industry.models import ProductIndustry
from energy.models import EnergyIndustry
import decimal
from django.contrib.auth import authenticate,login as auth_login
from transport.models import Transport
from django.db import connection
from django.core.cache import cache
from Crypto.Cipher import AES
from player.models import Player
from django.contrib.auth import logout

#Complicated code ahead. Beware!
def index(request):
    queries = connection.queries
    if request.method == "POST":
        data = request.POST.get("data")
        if data == None:
            return redirect("login")
        
        try:
            username = decrypt(data.decode("hex"))
        except Exception:
            return redirect("login")
        
        authent = authenticate(username = username, password = "heyheyhai")
        if authent is None:
            user = User.objects.create_user(username = username, password = "heyheyhai")
            player = Player(user = user)
            player.save()
            authent = authenticate(username = username, password = "heyheyhai")
            auth_login(request, authent)
        else:
            auth_login(request,authent)
    if not request.user.is_authenticated():
        return redirect("login")
    request.session['user_id'] = request.user.id
    states = cache.get('states')
    productIndustries = cache.get('productIndustries')
    energyIndustries = cache.get('energyIndustries')
    transports = cache.get('transports')
    
    if any(n is None for n in [states,productIndustries,energyIndustries,transports]):
        states = json.dumps(list(State.objects.values()),default=decimal_default)
        cache.set('states',states)
        transportList = list(Transport.objects.values())
        transportStates = Transport.states.through.objects.values('transport__id','state__id')  # @UndefinedVariable
        tList = defaultdict(lambda:[])
        for tr in transportStates:
            tList[tr['transport__id']].append(tr['state__id'])
        for transport in transportList:
            transport['states'] = tList[transport['id']]
        transports = json.dumps(transportList,default=decimal_default)
        cache.set('transports',transports)
        
        energyList = list(EnergyIndustry.objects.values())
        energyStates = EnergyIndustry.states.through.objects.values('energyindustry__id','state__id')  # @UndefinedVariable
        eList = defaultdict(lambda:[])
        for en in energyStates:
            eList[en['energyindustry__id']].append(en['state__id'])
        for energy in energyList:
            energy['states'] = eList[energy['id']]
        energyIndustries = json.dumps(energyList,default=decimal_default)
        cache.set('energyIndustries',energyIndustries)
        
        productsList = list(ProductIndustry.objects.values())
        productStates = ProductIndustry.states.through.objects.values('productindustry__id','state__id')  # @UndefinedVariable
        pList = defaultdict(lambda:[])
        for pro in productStates:
            pList[pro['productindustry__id']].append(pro['state__id'])
        for product in productsList:
            product['states'] = pList[product['id']]
        productIndustries = json.dumps(productsList,default=decimal_default)
        cache.set('productIndustries',productIndustries)
    print len(queries)
    return render(request,'index.html',{'states':states,'productIndustries':productIndustries,'energyIndustries':energyIndustries,'transports':transports})

def leave(request):
    logout(request)
    return redirect('login')

#Phew complicated shit over. :)

class JsonMixin(object):
    '''
    Mixin to generate Json responses.
    '''
    
    def render(self,context,**kwargs):
        return HttpResponse(self.json(context), content_type="application/json", **kwargs)
    
    def json(self,context):
        #Can be modified later to be better
        return json.dumps(context,default=decimal_default)

class OnlyPostMixin(object):
    '''
    Mixin to allow only post requests by default.
    '''
    def get(self,request):
        raise PermissionDenied

def check_ajax(function):
    '''
    Only allow authenticated ajax requests. Else 404 error.
    '''
    def wrapper(request, *args, **kwargs):
        if request.is_ajax() and request.session.get('user_id') != None:
            return function(request,*args,**kwargs)
        else:
            raise PermissionDenied
    return wrapper

class ApiTemplate(OnlyPostMixin,JsonMixin,View):
    '''
    Template for json response view
    '''
    #@method_decorator(check_ajax)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

#Other boring functions here
def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

def decrypt(text):
    key = 'ktjsawesomekeyss'
    IV = 16*'\x42'
    mode = AES.MODE_CBC
    decryptor = AES.new(key,mode, IV=IV)
    username = decryptor.decrypt(text)
    username = username.rstrip('[').encode('utf-8')
    return username