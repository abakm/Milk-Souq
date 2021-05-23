from django.shortcuts import render
from .form import *
from tables.models import *
from  tables.views import *
def farmer(request):
    return render(request, 'farmer/index.html')

def AddItem(request):

    if request.method=="POST":
        name=request.POST.get('name')
        pic = request.FILES.get('photo')
        print(pic)
        min=request.POST.get('min')
        quantity=request.POST.get('quantity')
        date = request.POST.get('date')
        stime=request.POST.get('stime')
        etime = request.POST.get('etime')
        st=storeitems(name=name,quantity=quantity,min=min,bid_date=date,bid_start_time=stime,bid_end_time=etime,photo=pic,sid_id=request.session['id'])
        st.save()
        text="Item Inserted"
        alertaudio(text)

    context = {}
    context['form'] = additem()
    return render(request, 'farmer/AddItem.html',context)



