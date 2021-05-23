from django.shortcuts import render,redirect
from tables.models import *
from tables.views import *
from django.db.models import Q
# Create your views here.
def home(request):
    if valid_user(request):
        EndUser(request)
    return render(request,'home/index.html')

def log(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        pwd = request.POST['pwd']

        u = login.objects.filter(Q(username=uname) & Q(password=pwd))
        if u.count()>0:
            request.session['id']=u[0].userid
            if u[0].usertype==0:
                return redirect('http://127.0.0.1:8000/home/adminuser/')
            if u[0].usertype==1:
                DeletePurchase(request.session['id'])
                return redirect('http://127.0.0.1:8000/home/customer/')
            if u[0].usertype==2:
                return redirect('http://127.0.0.1:8000/home/deliveryboy/')
            if u[0].usertype == 3:
                return redirect('http://127.0.0.1:8000/home/farmer/')




    return render(request,'home/login.html')

def custom_reg(request):
    if request.method=='POST':
        fname=request.POST.get('fname')
        mname = request.POST.get('mname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')
        c=customer(fname=fname,mname=mname,lname=lname,email=email,phone=phone)
        c.save()
        l=login(userid=c.id,username=uname,password=pwd,usertype=1)
        l.save()

    return render(request, 'home/customer_reg.html')


def store_reg(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')
        s = store(name=name, email=email, phone=phone)
        s.save()
        l = login(userid=s.id, username=uname, password=pwd, usertype=3)
        l.save()

    return render(request, 'home/store_reg.html')
