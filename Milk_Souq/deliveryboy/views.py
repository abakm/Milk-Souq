from django.shortcuts import render,redirect
from tables.models import *
from django.db.models import Q
from tables.views import *
import datetime
# Create your views here.
def deliveryhome(request):

    if not valid_user(request):
        text='Session Expired'
        alertaudio(text)
        return redirect('http://127.0.0.1:8000/home/')


    if request.method=="POST":
        pid=request.POST.get('deliver')
        purchase.objects.filter(id=pid).update(status=2)
        text="product delivered"
        alertaudio(text)
        return render(request, 'deliveryboy/index.html')


    ad=None
    user_id = request.session['id']
    tp = purchase.objects.filter(Q(did_id=user_id) & Q(status=1))
    #tp=tp.filter(date=datetime.date.today())
    if tp.count() > 0:
        print(tp[0].date)


        ad=address.objects.filter(id=tp[0].ad_id_id)

        #for products
        s=None
        t=None
        b=None
        p=None
        if ad[0].sub_id_id==None:
            p=tp[0]

        if p:
            s = shoppingcart.objects.filter(pid_id=p.id)
            t = item.objects.filter(id__in=s.values('itid_id'))
            b = brand.objects.filter(id__in=t.values('bid_id'))

        #for daily products
        sub=None
        dt=None
        db=None
        dtp=None
        adt=ad.filter(~Q(sub_id_id=None))
        if adt.count()>0:
            dtp=tp.filter(ad_id_id=adt[0].id)[0]
            sub=Subscription.objects.filter(id=adt[0].sub_id_id)[0]
            dt=dailyitem.objects.filter(id=sub.did_id)[0]
            db=brand.objects.filter(id=dt.bid_id)[0]



        #address objects
        ad=ad[0]





    if tp.count():
        return render(request, 'deliveryboy/home.html',{'p':p,'s':s,'t':t,'b':b,'ad':ad,'sub':sub,'dtp':dtp,'dt':dt,'db':db})
    else:
        text = 'No product to deliver'
        alertaudio(text)
        return render(request, 'deliveryboy/index.html')
