from django.db import models, backend

# Create your models here.



class Organisation(models.Model):
    """this is a concept of the organisation independant of address or heirarchy. The "essence" of the organisation although the most recent name and address are kept for convenience."""
    orgcode=models.CharField(max_length=8,primary_key=True)
    level=models.PositiveSmallIntegerField() #level 0 is special as it is the lowest level - practices. Others are just layers and not necessarily in the order specified.
    name=models.CharField(max_length=100) #this is denormalised for performance. Should contain the latest address
    addr=models.CharField(blank=True,max_length=200)
    postcode=models.CharField(blank=True,max_length=10)
    website=models.URLField(verify_exists=False,blank=True)

    def niceaddr(self):
         split=self.addr.split('#')
         return ', '.join(filter(bool,split))
         

class Address(models.Model):
    """The various address by year. The most recent is stored with the main organisation details"""
    orgcode=models.ForeignKey(Organisation)
    year=models.PositiveSmallIntegerField(db_index=True)
    name=models.CharField(max_length=100)
    address=models.CharField(blank=True,max_length=200)
    postcode=models.CharField(blank=True,max_length=10)
    website=models.URLField(verify_exists=False,blank=True)



    def address_parts(self):
        split_addr=self.address.split('#',4)
        return split_addr+[self.postcode]
    
class Indicator(models.Model):
    """An indicator. Include type and description"""
    flavour=models.PositiveSmallIntegerField()
    areaid=models.CharField(primary_key=True,max_length=15)
    description=models.CharField(max_length=1024)
    area=models.CharField(max_length=50,db_index=True)
    sort_order=models.PositiveSmallIntegerField()
    prevtext=models.CharField(blank=True,max_length=40) #if thhis is a prevalence indicator need some text for the prevalence screen
    base=models.CharField(blank=True,max_length=20)#where indicators have changed they often only change a little whilst having a new number. This should be the first instance of that inidcator.


class Achievement(models.Model):
    """The main data for a given indicator and organisation"""
    year=models.PositiveSmallIntegerField(db_index=True)
    numerator=models.IntegerField(null=True)#values can be suppressed at source 
    denominator=models.IntegerField(null=True)
    ratio=models.FloatField(null=True)
    centile=models.FloatField(null=True)
    orgcode=models.ForeignKey(Organisation,db_index=True)
    areaid=models.ForeignKey(Indicator,db_index=True)

    def percent(self):
         return str(round(self.ratio*100,1))+'%'

class Threshold(models.Model):
    """The thresholds and points for indicators. Not actually used currently"""
    lower=models.IntegerField()
    upper=models.IntegerField()
    points=models.DecimalField(decimal_places=1,max_digits=4)
    year=models.PositiveSmallIntegerField()
    areaid=models.ForeignKey(Indicator,db_index=True)

class OrgHeirarchy(models.Model):
    year=models.PositiveSmallIntegerField()
    orgcode=models.ForeignKey(Organisation,db_index=True)
    parent=models.ForeignKey(Organisation,db_index=True,related_name='children')

class Distance(models.Model):
    org1=models.ForeignKey(Organisation,db_index=True)
    org2=models.ForeignKey(Organisation,related_name='+')
    dist=models.FloatField()


    
