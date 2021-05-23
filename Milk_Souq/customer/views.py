from django.shortcuts import render,redirect
from tables.models import *
import datetime
from datetime import datetime as dte
from django.db.models import Max
from django.db.models import Q
from tables.views import *
from django.contrib import messages
# Create your views here.
def customerhome(request):

    if not valid_user(request):
        return redirect('http://127.0.0.1:8000/home/')

    if request.method=="POST":
        word = request.POST.get('word')
        t = item.objects.filter(Q(name__contains=word) | Q(name__contains=word.title()) | Q(name__contains=word.lower()) | Q(name__contains=word.upper()))
        dt = dailyitem.objects.filter(Q(name__contains=word) | Q(name__contains=word.title()) | Q(name__contains=word.lower()) | Q(name__contains=word.upper()))
        msg=str(word)
    else:
        t=item.objects.all()
        dt=dailyitem.objects.all()
        msg=None

    dc=discount.objects.all()
    if dc.count()>0:
        dc=dc[0]

    st = storeitems.objects.filter(bid_date__gte=datetime.date.today())
    stn=None
    print(request.session['id'])
    bd=bid.objects.filter(cid_id=request.session['id'])

    if bd.count()>0:
        stn=st.filter(~Q(id__in=bd.values('stid_id')))
        print(stn.count())
    else:
        stn=st

    st=st.filter(id__in=bd.values('stid_id'))


    if t.count()>0 or dt.count()>0:
        return render(request, 'customer/products.html',{'item':t,'ditem':dt,'dc':dc,'msg':msg,'st':st,'stn':stn})
    else:
        return render(request, 'customer/index.html')

def Purchase(request,item_id):
    if not valid_user(request):
        return redirect('http://127.0.0.1:8000/home/')

    t = item.objects.get(id=item_id)
    if request.method=="POST":
        qty=request.POST.get('qty')
        c=customer.objects.get(id=request.session['id'])
        item_id=request.POST.get('add')
        p=purchase.objects.filter(Q(cid=request.session['id']) & Q(status=0))
        if p.count()==0:
            p=purchase(cid_id=c.id)
            p.save()
            p = purchase.objects.filter(Q(cid=request.session['id']) & Q(status=0))
       

        s=shoppingcart(pid_id=p[0].id,itid_id=item_id,quantity=qty)
        s.save()
        t.quantity=int(t.quantity)-int(qty)
        t.save()
        return redirect('http://127.0.0.1:8000/home/customer/')




    return render(request, 'customer/purchase.html',{'t':t})

def cart(request):

    if not valid_user(request):
        return redirect('http://127.0.0.1:8000/home/')

    if request.method=="POST":
        street=request.POST.get('street')
        print(street)
        city=request.POST.get('city')
        dis=request.POST.get('district')
        pin=request.POST.get('pin')
        pid=request.POST.get('book')
        print('hallo')
        print(pid)

        sum = 0
        s = shoppingcart.objects.filter(pid_id=pid)
        for a in s:
            t=item.objects.get(id=a.itid_id)
            sum=sum+(a.quantity*t.price)
            #t.quantity = t.quantity - a.quantity
            #t.save()

        ad = address(street=street, city=city, district=dis, pin=pin)
        ad.save()
        dt=datetime.date.today()
        print(dt)
        purchase.objects.filter(id=pid).update(amt=sum, paid=1, status=1,date=dt,ad_id_id=ad.id)
        text = "Successfully inserted"
        alertaudio(text)
        DeliveryBoyAlloc(pid)
        return redirect('http://127.0.0.1:8000/home/customer/')

    p = purchase.objects.filter(Q(cid=request.session['id']) & Q(status=0))
    if p.count()>0:
        s=shoppingcart.objects.filter(pid_id=p[0].id)
        if s.count()>0:
            t=item.objects.all()
            b=brand.objects.all()
            c=s.count()
            sum = 0
            for a in s:
                ot = item.objects.get(id=a.itid_id)
                sum = sum + (a.quantity * ot.price)
                # t.quantity = t.quantity - a.quantity
                # t.save()

            return render(request,'customer/cart.html',{'s':s,'p':p[0],'t':t,'b':b,'c':c,'sum':sum})

    else:
        return redirect('http://127.0.0.1:8000/home/customer/')


def subscribe(request,ditem_id):

    if request.method=="POST":
        add=request.POST.get('add')
        qty = request.POST.get('qty')
        sdate = request.POST.get('sdate')
        edate =request.POST.get('edate')
        street = request.POST.get('street')
        city = request.POST.get('city')
        dis = request.POST.get('dis')
        pin = request.POST.get('pin')

        df="%Y-%m-%d"
        d1=dte.strptime(sdate,df)
        d2=dte.strptime(edate,df)
        d=d2-d1
        d=d.days
        dt=dailyitem.objects.get(id=add).price

        sub = Subscription(amt=dt*d,sdate=sdate, edate=edate, did_id=add, cid_id=request.session['id'], qty=qty)
        sub.save()

        ad = address(street=street, city=city, district=dis, pin=pin,sub_id_id=sub.id)
        ad.save()

        text="Successfully inserted"
        alertaudio(text)
        return redirect('http://127.0.0.1:8000/home/customer/')


    d=dailyitem.objects.get(id=ditem_id)
    return render(request, 'customer/subscribe.html', {'dt': d})


def RegisterBid(request,item_id):
    if not valid_user(request):
        return redirect('http://127.0.0.1:8000/home/')

    b=bid(cid_id=request.session['id'],stid_id=item_id)
    b.save()
    text='Registered for Auction'
    alertaudio(text)
    return redirect('http://127.0.0.1:8000/home/customer/')

def AuctionList(request):
    if not valid_user(request):
        return redirect('http://127.0.0.1:8000/home/')

    s = storeitems.objects.filter(id__in=bid.objects.filter(cid_id=request.session['id']).values('stid_id'))

    pv=s.filter(bid_date__lt=datetime.date.today()) #Previous
    td=s.filter(bid_date=datetime.date.today()) #Today
    nt=s.filter(bid_date__gt=datetime.date.today())#Next
    print(nt.count())
    if s.count():

        return render(request,'customer/AuctionList.html',{'td':td,'pv':pv,'nt':nt})
    else:
        return redirect('http://127.0.0.1:8000/home/customer/')


def Auction(request,auction_id):
    if not valid_user(request):
        return redirect('http://127.0.0.1:8000/home/')

    if request.method=='POST':
        amt = request.POST.get('amt')
        print(amt)
        bid.objects.filter(stid_id=auction_id).filter(cid_id=request.session['id']).update(amt=amt)
        text='Amount Added'
        alertaudio(text)

    c=None
    max=None
    b=bid.objects.filter(Q(stid_id=auction_id))
    b=b.filter(~Q(amt=None))
    if b.count()>0:
        max=b.aggregate(Max('amt'))
        max=max['amt__max']
        c=customer.objects.get(id=bid.objects.get(amt=max).cid_id)






    st=storeitems.objects.get(id=auction_id)
    print(st.bid_date)

    if st.bid_date==datetime.date.today():
        return render(request, 'customer/Auction.html', {'st': st,'c':c,'max':max,'u':request.session['id']})
    else:
        return redirect('http://127.0.0.1:8000/home/customer/')






