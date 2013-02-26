import models

import MySQLdb

year=10

conn=MySQLdb.connect(user='gavin',passwd='spider',db='qmas6',use_unicode=True)

c=conn.cursor()

c.execute('SELECT orgcode,orgname,addr1,addr2,addr3,addr4,addr5,postcode FROM SHA')

records=c.fetchall()

UK=models.Organisation.objects.filter(orgcode='UK')[0]
ENG=models.Organisation.objects.filter(orgcode='ENG')[0]
newrel=models.OrgHeirarchy()
newrel.year=year
newrel.orgcode=ENG
newrel.parent=UK
newrel.save()

for record in records:
    organisation,created=models.Organisation.objects.get_or_create(orgcode=record[0])
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
    if organisation.orgcode in ('WAL','SCO','NIR'):
        newrel.parent=UK
    else:
        newrel.parent=ENG
    newrel.save()
