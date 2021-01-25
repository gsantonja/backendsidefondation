from django.db import models

import datetime
from django.utils.timezone import now

from django_cryptography.fields import encrypt

#https://blog.pboehm.org/blog/2013/02/05/extracting-field-names-from-django-model-instance/


# Create your models here.
def getDefaultCurrency():
    # send the default currency
    try:
        # try to see if a default currency exist
        fiatCurrency = FiatCurrency.objects.all().filter(default=True)[0]
    except :
        try:
            # try to see if the constant default currency exist
            fiatCurrency = FiatCurrency.objects.all().filter(symbol=FiatCurrency.DEFAULT_SYMBOL)[0]
        except :
            # create it if not
            fiatCurrency = FiatCurrency()
            fiatCurrency.symbol = FiatCurrency.DEFAULT_SYMBOL
            fiatCurrency.nameShort  = FiatCurrency.DEFAULT_NAMESHORT
            fiatCurrency.nameLong = FiatCurrency.DEFAULT_NAMELONG
            fiatCurrency.default = True
            fiatCurrency.save()
    return fiatCurrency

class FiatCurrency(models.Model):
    DEFAULT_SYMBOL='€'
    DEFAULT_NAMESHORT='EUR'
    DEFAULT_NAMELONG= 'Euro'
    symbol =  models.CharField(max_length=5,default=DEFAULT_SYMBOL,unique=True)
    nameShort =  models.CharField(max_length=5,default=DEFAULT_NAMESHORT,unique=True)
    nameLong =  models.CharField(max_length=20,default=DEFAULT_NAMELONG,null=True,blank=True)
    comment =  models.CharField(max_length=200,default='',null=True,blank=True)
    default = models.BooleanField(default=False) # if this currency is the default fiat for the application
    active=models.BooleanField(default=True)
    update = models.DateTimeField(default = now,null=False)
    create = models.DateTimeField(default = now,null=False)
    order_view = models.IntegerField(default=0) # used for the list view to sort the list
    def __str__(self):
        if self.active == False :
            return "INACTIVE - {}".format(self.nameLong)
        else:
            return "{}".format(self.nameLong)

class M_o_d_e_l_C_o_m_p_o_n_e_n_t(models.Model):
    # class test for testing the skeleton template
    # those fields are needed to test the functionnality
    name =  models.CharField(max_length=100,default='',null=True,blank=True)
    comment =  models.CharField(max_length=200,default='',null=True,blank=True)
    value = models.FloatField(default=0.0) # value
    sensitive_information =  encrypt(models.CharField(max_length=200,default='',null=True,blank=True))
    currentCurrency = models.ForeignKey("FiatCurrency",related_name="M_o_d_e_l_s_k_e_l_e_t_o_n_fiatcurrency",on_delete=models.CASCADE,default=getDefaultCurrency,null=True,blank=True)
    active=models.BooleanField(default=True)
    order_view = models.IntegerField(default=0)
    update = models.DateTimeField(default = now,null=False)
    create = models.DateTimeField(default = now,null=False)

    def __str__(self):
        if self.active == False :
            return "INACTIVE - {} - {} - {}".format(self.name,self.value,self.update.isoformat())
        else:
            return "{} - {} - {}".format(self.name,self.value,self.update.isoformat())


