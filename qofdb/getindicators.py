import models

import MySQLdb

conn=MySQLdb.connect(user='gavin',passwd='spider',db='qmas6',use_unicode=True)

c=conn.cursor()

c.execute('SELECT longname, areaid, `desc` , Targets.type, areano FROM `Targets` , `areas`WHERE area = id')

records=c.fetchall()
for record in records:
    try :
        models.Indicator.objects.get(areaid=record[1])
    except models.Indicator.DoesNotExist:
        newrecord=models.Indicator()
        newrecord.flavour=record[3]
        newrecord.areaid=record[1]
        newrecord.description=record[2]
        newrecord.area=record[0]
        print(record[1])
        newrecord.sort_order=int(record[4])
        newrecord.save()
