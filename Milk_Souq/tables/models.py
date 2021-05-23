from django.db import models
from distutils.command.upload import upload
# Create your models here.
class login(models.Model):
    id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    userid=models.IntegerField()
    usertype=models.IntegerField()

class brand(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone=models.CharField(max_length=10)

class item(models.Model):
    id=models.AutoField(primary_key=True)
    photo = models.ImageField(null=True, upload_to='items/')
    name=models.CharField(max_length=50)
    type=models.CharField(default=None,max_length=50)
    bid=models.ForeignKey(brand,on_delete=models.CASCADE)
    price = models.FloatField()
    quantity=models.IntegerField()

class dailyitem(models.Model):
    id=models.AutoField(primary_key=True)
    photo = models.ImageField(null=True, upload_to='items/')
    name=models.CharField(max_length=50)
    required=models.IntegerField(default=0)
    price = models.FloatField(default=None)
    bid = models.ForeignKey(brand, on_delete=models.CASCADE)


class dailyrequired(models.Model):
    id=models.AutoField(primary_key=True)
    did = models.ForeignKey(dailyitem, on_delete=models.CASCADE)
    got=models.IntegerField()
    date=models.DateField()

class customer(models.Model):
    id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=50)
    mname = models.CharField(max_length=50,null=True)
    lname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=10)

class deliveryboy(models.Model):
    id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=50)
    mname = models.CharField(max_length=50,null=True)
    lname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=10)


class Subscription(models.Model):
    id=models.AutoField(primary_key=True)
    cid=models.ForeignKey(customer, on_delete=models.CASCADE)
    qty=models.IntegerField(default=0)
    amt = models.FloatField(default=0)
    did = models.ForeignKey(dailyitem, on_delete=models.CASCADE)
    paid=models.BooleanField(default=False)
    sdate=models.DateField()
    edate=models.DateField()

class address(models.Model):
    id = models.AutoField(primary_key=True)
    #pid=models.ForeignKey(purchase,on_delete=models.CASCADE,null=True)
    street = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    district = models.CharField(max_length=50, null=True)
    pin = models.IntegerField(null=True)
    sub_id=models.ForeignKey(Subscription, on_delete=models.CASCADE,null=True)




class purchase(models.Model):
    id = models.AutoField(primary_key=True)
    amt=models.FloatField(default=0)
    cid=models.ForeignKey(customer,on_delete=models.DO_NOTHING,null=True)
    paid=models.BooleanField(default=False)
    date=models.DateField(null=True)
    status=models.IntegerField(default=0)
    did = models.ForeignKey(deliveryboy, on_delete=models.DO_NOTHING,null=True)
    ad_id=models.ForeignKey(address, on_delete=models.DO_NOTHING,null=True)


class shoppingcart(models.Model):
    id = models.AutoField(primary_key=True)
    pid=models.ForeignKey(purchase,on_delete=models.CASCADE)
    itid=models.ForeignKey(item, on_delete=models.DO_NOTHING,null=True)
    item_type=models.IntegerField(default=0)
    quantity=models.IntegerField()

class discount(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=50,null=True)
    percent=models.FloatField()
    min_amt=models.FloatField(default=1.0)
    sdate=models.DateField()
    edate=models.DateField()




class store(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone=models.CharField(max_length=10)
    status=models.BooleanField(default=False)

class storeitems(models.Model):
    id=models.AutoField(primary_key=True)
    photo=models.ImageField(null=True,upload_to='store/')
    name=models.CharField(max_length=50)
    sid=models.ForeignKey(store,on_delete=models.CASCADE)
    min = models.FloatField(null=True)
    quantity=models.IntegerField()
    bid_date=models.DateField()
    bid_start_time=models.TimeField()
    bid_end_time = models.TimeField()
    cid = models.ForeignKey(customer, on_delete=models.CASCADE,null=True)
    adid = models.ForeignKey(address, on_delete=models.CASCADE,null=True)

class bid(models.Model):
    id = models.AutoField(primary_key=True)
    stid = models.ForeignKey(storeitems, on_delete=models.CASCADE)
    cid = models.ForeignKey(customer, on_delete=models.CASCADE)
    amt=models.FloatField(null=True)




