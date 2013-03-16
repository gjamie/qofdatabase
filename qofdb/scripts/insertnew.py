import models

allnew=models.Address.objects.filter(year=12)

for new in allnew:
    try:
        models.Organisation.objects.get(orgcode=new.orgcode_id)
    except:
        print(new.orgcode_id)
        neworg=models.Organisation()
        neworg.orgcode=new.orgcode_id
        neworg.level=0 #only works at practice level
        neworg.name=new.name
        neworg.addr=new.address
        neworg.postcode=new.postcode
        neworg.save()
        
    
