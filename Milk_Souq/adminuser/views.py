from django.shortcuts import render,redirect
from tables.models import *
from tables.views import *
from django.db.models import Q
from Milk_Souq.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.contrib import messages
import datetime
from tables.views import *
from tables.views import *
# Create your views here.
def adminuser(request):
    #return render(request,'adminuser/index.html')

    if not valid_user(request):
        return redirect('http://127.0.0.1:8000/home/')

    if request.method=="POST":
        if request.POST.get('edit'):
            e=request.POST.get('edit')
            print(e)
            t=item.objects.get(id=e)
            b = brand.objects.get(id=t.bid_id)
            return render(request, 'adminuser/item.html',{'item':t,'brand':b})

        elif request.POST.get('dedit'):
                e = request.POST.get('dedit')
                print(e)
                dt = dailyitem.objects.get(id=e)
                b = brand.objects.get(id=dt.bid_id)
                return render(request, 'adminuser/ditem.html', {'ditem': dt, 'brand': b})

        elif request.POST.get('dupdate'):
            u = request.POST.get('dupdate')
            p = request.POST.get('price')
            req = int(request.POST.get('req'))
            dailyitem.objects.filter(id=u).update(price=p,required=req)
            text="Dailyitem updated"
            alertaudio(text)


        else:
            u=request.POST.get('update')
            t=item.objects.get(id=u)
            p=request.POST.get('price')
            q=int(request.POST.get('qty'))
            qt=t.quantity+q
            item.objects.filter(id=u).update(quantity=qt,price=p)





    t=item.objects.all()
    dt=dailyitem.objects.all()
    if t.count()>0 or dt.count()>0:
        return render(request, 'adminuser/itemlist.html',{'item':t,'ditem':dt})
    else:
        return render(request, 'adminuser/index.html')

def itemadd(request):
    if not valid_user(request):
        return redirect('http://127.0.0.1:8000/home/')

    if request.method=='POST' and request.FILES['item']:
    #if request.method == 'POST' and request.FILES['item']:
        pic=request.FILES.get('item')
        name = request.POST.get('name')
        bid = request.POST.get('brand')
        qty = request.POST.get('qty')
        price = request.POST.get('price')
        type = request.POST.get('type')
        t=item(photo=pic,type=type,name=name.title(),quantity=qty,price=price,bid_id=bid)
        t.save()
        alertaudio()

    b=brand.objects.all()
    if b.count():
        return render(request, 'adminuser/itemadd.html',{'brand':b})
    else:
        return render(request, 'adminuser/index.html')



def brandadd(request):
    if not valid_user(request):
        return redirect('http://127.0.0.1:8000/home/')

    if request.method=='POST':
    #if request.method == 'POST' and request.FILES['item']:

        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        b=brand(name=name.title(),email=email,phone=phone)
        b.save()
        #t.photo=item
        #t.save()

    #return render(request,'adminuser/itemadd.html')
    return render(request, 'adminuser/brandadd.html')

def deliveryadd(request):
    if not valid_user(request):
        return redirect('http://127.0.0.1:8000/home/')

    if request.method=='POST':
        fname = request.POST.get('fname')
        mname = request.POST.get('mname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        d=deliveryboy(fname=fname,mname=mname,lname=lname,email=email,phone=phone)
        d.save()
        uname='deliver'+str(d.id)
        pwd='deliver'+str(d.id)
        l = login(userid=d.id, username=uname, password=pwd, usertype=2)
        l.save()
        subject = 'Milk-Souq:Delivery Boy Registration'
        message = 'Hello,\nYour login credentials for http://127.0.0.1:800/home are as follows,\nUsername: ' + uname + '\nPassword: ' + pwd
        message += '\nNote: Please use forgot password option to change your password!'
        recepient = str(d.email)
        send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently=False)
        messages.success(request,"Inserted successfully")
    return render(request, 'adminuser/deliveryboyadd.html')


def dailyitemadd(request):
    if not valid_user(request):
        return redirect('http://127.0.0.1:8000/home/')

    if request.method=="POST":
        pic = request.FILES.get('photo')
        print(pic)
        name = request.POST.get('name')
        price = request.POST.get('price')
        br= request.POST.get('brand')
        required = request.POST.get('req')
        d=dailyitem(photo=pic,name=name.title(),price=price,bid_id=br,required=required)
        d.save()



    b=brand.objects.all()
    return render(request, 'adminuser/DailyItemReg.html',{'b':b})

def dailyitemcollection(request):
    if not valid_user(request):
        return redirect('http://127.0.0.1:8000/home/')


    if request.method=="POST":
        got = int(request.POST.get('got'))
        b = request.POST.get('sub')
        d=dailyrequired(did_id=b,got=got,date=datetime.date.today())
        d.save()
        print(b)
        s=Subscription.objects.filter(did_id=b)
        print(s.count())
        if s.count()>0:
            print("inside")

            for a in s:
                if  not a.sdate <= datetime.date.today() or not a.edate>=datetime.date.today():
                    print('End')
                    break

                if got==0:
                    print('Hallo')
                    break

                if int(a.qty)<=got:
                    pr = dailyitem.objects.get(id=b).price
                    tot=int(a.qty)*got
                    ad=address.objects.get(sub_id_id=a.id).id
                    p=purchase(amt=tot,paid=1,status=1,cid_id=a.cid_id,date=datetime.date.today(),ad_id_id=ad)
                    p.save()
                    DeliveryBoyAlloc(p.id)
                    got=got-a.qty




    dc=dailyrequired.objects.filter(date=datetime.date.today())
    d=dailyitem.objects.filter(~Q(id__in=dc.values('did_id')))

    if d.count()>0:
        b=brand.objects.get(id=d[0].bid_id)
        print(d[0].name)
        print(b.name)
        return render(request, 'adminuser/DailyItemCollection.html', {'d':d[0],'b':b})
        #return render(request, 'adminuser/DailyItemCollection.html')

    return redirect('http://127.0.0.1:8000/home/adminuser/')

def DiscountAdd(request):
    if not valid_user(request):
        return redirect('http://127.0.0.1:8000/home/')

    if request.method=='POST':
        name = request.POST.get('name')
        percent = request.POST.get('percent')
        amt=request.POST.get('amt')
        sdate = request.POST.get('sdate')
        edate = request.POST.get('edate')
        if name=='':
            dc=discount(min_amt=amt,percent=percent,sdate=sdate,edate=edate)
        else:
            dc = discount(name=name,min_amt=amt, percent=percent, sdate=sdate, edate=edate)

        dc.save()
        text='Offer Inserted'
        alertaudio(text)

    return render(request, 'adminuser/DiscountAdd.html')




