import models
import csv

indicators=models.Threshold.objects.filter(year=13)

output=csv.writer(open('thresh.csv','wb'))

for indicator in indicators :
    row=[]
    try :
        latestach=indicator.areaid.achievement_set.filter(year=11,orgcode='ENG')
    except :
        latestach=False
    try :
        row.append(indicator.areaid.areaid)
    except :
        print indicator.areaid
    row.append(indicator.areaid.description)
    row.append(indicator.lower)
    row.append(indicator.upper)
    row.append(indicator.points)
    if latestach :
        row.append(latestach[0].numerator)
        row.append(latestach[0].denominator)
    output.writerow(row)


    
    
