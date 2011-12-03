import models

import MySQLdb
from MySQLdb import cursors

year=10

conn=MySQLdb.connect(user='gavin',passwd='spider',db='qmas6')

c=conn.cursor(cursors.SSCursor)

c.execute('select practiceid,achievement.area,numerator,denominator,rank,ratio,`type` from achievement,Targets where achievement.area=Targets.areaid limit 1000000,500000')

record=c.fetchone()
while record is not None:
    organisation,created=models.Organisation.objects.get_or_create(orgcode=record[0],level=0)
    indicator=models.Indicator.objects.get(areaid=record[1])
    newrecord=models.Achievement()
    newrecord.orgcode=organisation
    newrecord.year=year
    newrecord.areaid=indicator
    newrecord.numerator=record[2]
    newrecord.denominator=record[3]
    newrecord.centile=record[4]
    newrecord.ratio=record[5]
    if record[6]==3:
        newrecord.denominator=1
    newrecord.save()
    record=c.fetchone()
    
