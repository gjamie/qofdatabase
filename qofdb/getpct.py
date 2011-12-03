import models

import MySQLdb

year=10

conn=MySQLdb.connect(user='gavin',passwd='spider',db='qmas6',use_unicode=True)

c=conn.cursor()

c.execute('SELECT orgcode,orgname,addr1,addr2,addr3,addr4,addr5,postcode,SHA FROM PCT')

records=c.fetchall()

for record in records:
    organisation,created=models.Organisation.objects.get_or_create(orgcode=record[0],level=10)
    newrecord=models.Address()
    newrecord.orgcode=organisation
    newrecord.year=year
    newrecord.name=record[1]
    newrecord.postcode=record[7]
    addr=[]
    for i in record[2:6]:
        if i==None:
            i=''
        addr.append(i)
    newrecord.address='#'.join(addr)
    newrecord.save()
    newrel=models.OrgHeirarchy()
    newrel.year=year
    newrel.orgcode=organisation
    newrel.parent=models.Organisation.objects.filter(orgcode=record[8])[0]
    newrel.save()
