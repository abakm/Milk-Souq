from django.shortcuts import render,redirect
import pyttsx3
from django.db.models import Q
from .models import *
# Create your views here.

def DeletePurchase(user_id):
    p=purchase.objects.filter(Q(cid_id=user_id) & Q(status=0))
    if p.count()>0:
        s=shoppingcart.objects.filter(Q(pid_id__in=p.values('id')))
        if s.count():
            for a in s:
                t=item.objects.get(id=a.itid_id)
                m=int(t.quantity)
                n=int(a.quantity)
                t.quantity=m+n
                t.save()
        p.delete()


def alertaudio(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def valid_user(request):
    keys = request.session.keys()
    if 'id' in keys:
        return 1
    else:
        return 0

def EndUser(request):
    for key in list(request.session.keys()):
        if not key.startswith("_"):  # skip keys set by the django system
            del request.session[key]

def Logout(request):
    if valid_user(request):
       EndUser(request)
    return redirect('http://127.0.0.1:8000/home/')




def DeliveryBoyAlloc(pid):
    d = deliveryboy.objects.all()
    print(d)
    p=purchase.objects.filter(Q(status=1) & ~Q(did_id=None))
    if p.count()>0:
        d=d.filter(~Q(id__in=p.values('did_id')))

    print(d)
    if d.count()>0:
        pt=purchase.objects.get(id=pid)
        pt.did_id=d[0].id
        pt.save()
        print(pt.did_id)


def EndSession(request):
    DeletePurchase(request.session['id'])
    return Logout(request)










