import models

import MySQLdb

year=5

conn=MySQLdb.connect(user='gavin',passwd='spider',db='qmas',use_unicode=True)

c=conn.cursor()

c.execute('SELECT id,name,address,postcode,pco FROM surgery')

records=c.fetchall()

for record in records:
    organisation,created=models.Organisation.objects.get_or_create(orgcode=record[0],level=0)
    newrecord=models.Address()
    newrecord.orgcode=organisation
    newrecord.year=year
    newrecord.name=record[1]
    newrecord.postcode=record[3]
    newrecord.address='#'.join([x.strip() for x in record[2].split(',')])#tidies the format up. Very fast
    #newrecord.save()
    if len(record[4])>0:
        newrel=models.OrgHeirarchy()
        newrel.year=year
        newrel.orgcode=organisation
        try:
            newrel.parent=models.Organisation.objects.get(orgcode=record[4])
        except:
            print "I don't know about"+record[4]
        newrel.save()
    
