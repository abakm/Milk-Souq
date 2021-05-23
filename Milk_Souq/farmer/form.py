from django import forms


class additem(forms.Form):
    name=forms.CharField(max_length=10)
    photo=forms.ImageField()
    min=forms.FloatField()
    quantity=forms.IntegerField()
    #bid_date=forms.DateField(widget=forms.SelectDateWidget())
    #bid_start_time=forms.TimeField(widget=forms.TimeInput())
    #bid_end_time=forms.TimeField(widget=forms.TimeInput())


