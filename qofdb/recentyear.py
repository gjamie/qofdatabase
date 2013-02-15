import models
#get the most recent address for all organisations
orgs=models.Organisation.objects.all()

for org in orgs:
    try:
        details=org.address_set.order_by("-year")[0] #get the most recent address
    except:
        print "I dont know about"+org.orgcode
    org.name=details.name
    org.addr=details.address
    org.postcode=details.postcode
    org.website=details.website
    org.save()

