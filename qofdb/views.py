
import models
from django.shortcuts import render_to_response, get_object_or_404, redirect
import defaults
from django import forms
from django.template import RequestContext
import re
from django.http import Http404

def browse(request,orgcode,year=None,area=None):
    """Browsing the data for an organisation either by summary or by area"""
    if year==None:
        year=defaults.year
    else:
        year=int(year)
    orgs=getorgDetails(orgcode,year)
    England=('ENG' in orgs['orglist'])#Is there England somewhere here
    data=[]
    if area==None: #if no specific area if given we send out prevalence
        message="2012 Data for Scotland, England and Wales now online!"
        prevalence=orgs['organisation'].achievement_set.filter(areaid__flavour=1,year=year).values('areaid_id','areaid__prevtext','ratio','centile','areaid__area')
        headings=['Area','Prevalence']
        if orgs['organisation'].level <25:
            headings.append('Centile')
        areas=[]
        allprevs=models.Achievement.objects.filter(orgcode__in=orgs['orglist'],areaid__flavour=1,year=year).values('ratio','areaid__area','areaid__prevtext','orgcode')
        nonclin=('Palliative Care','Records','Cervical Screening','Child Health Surveillance','Sexual Health','Education and Training','Patient Communication','Maternity Services','Medicines Management','Patient Experience','Practice Management')
        if year>=12 :
            nonclin+=('Quality and Productivity',)
        graphorgs=[orgs['organisation'].name]#start with practice in the list
        for org in orgs['ancestors']:
            graphorgs.append(org['name'])
        graph=[]
        prevareas=[]
        for area in prevalence:
            stats={'indicator':area['areaid_id'],'description':area['areaid__prevtext'],'percent':area['ratio'],'centile':area['centile'],'area':area['areaid__area']}
            data.append(stats)
            prevareas.append(area['areaid__prevtext'])
            ratio=0 if (area['ratio']==None) else area['ratio']*100
            graph.append((len(prevareas)-1,1,ratio))
            graph.append((len(prevareas)-1,0,str(area['areaid__prevtext'])))#str function changes from unicode for the benefit of the javascript
        table={'headings':headings,'data':data}
        for prev in allprevs:
            try:
                graph.append((prevareas.index(prev['areaid__prevtext']),orgs['orglist'].index(prev['orgcode'])+2,prev['ratio']*100))
            except ValueError:
                pass
        return render_to_response('orgpage.html',{'england':England,'message':message,'org':orgs['organisation'],'search':searchForm(),'title':orgs['organisation'].name,'years':defaults.years(),'ancestors':orgs['ancestors'],'table':table,'code':orgcode,'year':year,'graph':graph,'areano':len(prevareas),'level':orgs['organisation'].level,'children':orgs['children'],'nonclin':nonclin,'alt_parent':orgs['alt']},context_instance=RequestContext(request))
    else:
        #here we are looking for a specific disease area
        indicators=orgs['organisation'].achievement_set.filter(areaid__area=area,year=year).order_by("areaid__sort_order").values('areaid','areaid__description','areaid__flavour','numerator','denominator','ratio','centile')
        headings=['Indicator','Numerator','Denominator','Ratio']
        if orgs['organisation'].level <25:
            headings.append('Centile')
        allach=models.Achievement.objects.filter(orgcode__in=orgs['orglist'],areaid__area=area,year=year).values('ratio','areaid','orgcode')
        indicatorList=[]
        graph=[]
        for indicator in indicators:
            if ((orgs['organisation'].level==0) and (indicator['areaid__flavour']==3)): #are we looking at a practice level boolean indicator?
                boolean=True
            else:
                boolean=False
            indicatorList.append(indicator['areaid'])
            graph.append((len(indicatorList)-1,0,str(indicator['areaid'])))#str function changes from unicode
            ratio=0 if indicator['ratio']==None else indicator['ratio']*100
            graph.append((len(indicatorList)-1,1,ratio))
            stats={'boolean':boolean,'indicator':indicator['areaid'],'description':indicator['areaid__description'],'numerator':indicator['numerator'],'denominator':indicator['denominator'],'ratio':indicator['ratio'],'centile':indicator['centile']   }
            data.append(stats)
        table={'headings':headings,'data':data}
        for ach in allach:
            if ach['ratio']==None:
                ach['ratio']=0 #Where the database says NULL we want to have a zero on the graph
            try:
                graph.append((indicatorList.index(ach['areaid']),orgs['orglist'].index(ach['orgcode'])+2,ach['ratio']*100))
            except ValueError:
                pass
        return render_to_response('areapage.html',{'areano':len(indicatorList),'search':searchForm(),'org':orgs['organisation'],'title':area+'-'+orgs['organisation'].name,'area':area,'years':defaults.years(),'ancestors':orgs['ancestors'],'table':table,'year':year,'graph':graph},context_instance=RequestContext(request))
    
def area(request,orgcode,indicator,year=None):
    """Given and organsisation and an area outputs the data for all of the child organisations as well as parent organisations. Not grandchildren though."""
    if year==None:
        year=defaults.year
    else:
        year=int(year)
    headings=['Organisation','Numerator','Denominator','Ratio','Centile']
    orgs=getorgDetails(orgcode,year)
    indicator_details=get_object_or_404(models.Indicator,areaid=indicator)
    allorgs=[org[0] for org in orgs['children'].values_list('orgcode_id')]+[orgs['organisation'].orgcode]+orgs['orglist']#values list throws out list of tuples. Need to convert them.
    indicator_data=models.Achievement.objects.filter(orgcode__in=allorgs,year=year,areaid=indicator).values('ratio','numerator','denominator','centile','orgcode__name','orgcode','areaid__flavour','orgcode__level').order_by('-ratio')
    table={'headings':headings,'data':indicator_data}
    return render_to_response('childarea.html',{'search':searchForm(),'org':orgs['organisation'],'title':indicator+'-'+orgs['organisation'].name,'indicator':indicator_details,'years':defaults.years(),'ancestors':orgs['ancestors'],'table':table,'year':year},context_instance=RequestContext(request))

def search(request,year=None): #We pass the year as a convenience to the user. Not actually doing anythingwith it here.
    """The search form"""
    form=searchForm(request.GET)
    if year==None:
        year=defaults.year
    else:
        year=int(year)
    if form.is_valid():
        search=form.cleaned_data['search']
        if re.match('[A-Za-z]{1,2}[0-9]{1,2} ',search):
            results=models.Organisation.objects.raw("SELECT distinct qofdb_organisation.name,qofdb_organisation.addr,qofdb_organisation.orgcode FROM `qofdb_address`,`qofdb_organisation` where qofdb_address.postcode like %s and qofdb_address.orgcode_id=qofdb_organisation.orgcode",[search+'%'])
        else:
            results=models.Organisation.objects.raw("SELECT distinct qofdb_organisation.name,qofdb_organisation.addr,qofdb_organisation.orgcode FROM `qofdb_address`,`qofdb_organisation` where  qofdb_address.`orgcode_id`=qofdb_organisation.orgcode and match (qofdb_address.name,qofdb_address.address,qofdb_address.postcode,qofdb_address.`orgcode_id`) against (%s) limit 30",[search])
    else :
        results=False
    return render_to_response('search.html',{'results':results,'static':defaults.static,'year':year,'title':'Search Results','search':form},context_instance=RequestContext(request))
    
def timeline(request,orgcode,indicator):
    """Showing and indicator over time"""
    year=defaults.year
    orgs=getorgDetails(orgcode,year)
    England=('ENG' in orgs['orglist'])#Is there England somewhere here
    headings=['Indicator','Year','Numerator','Denominator','Ratio','Centile']
    data=[]
    baseIndicator=get_object_or_404(models.Indicator,areaid=indicator)
    achievements=list(models.Achievement.objects.filter(areaid__base=baseIndicator.base,orgcode=orgcode).order_by("year").values('year','areaid','areaid__description','numerator','denominator','ratio','centile','areaid__flavour'))#using list as we want an actual list here
    firstyear=defaults.minyear
    lastyear=achievements[-1]['year']#this is why we wanted the list
    graph=[]
    years=set()
    for achievement in achievements:
        data.append({'area':achievement['areaid'],'description':achievement['areaid__description'],'year':achievement['year'],'numerator':achievement['numerator'],'denominator':achievement['denominator'],'ratio':achievement['ratio'],'centile':achievement['centile'],'flavour':achievement['areaid__flavour']})
        graph.append((achievement['year'],0,str(achievement['year']+2000)))
        if achievement['ratio'] is not None:
            graph.append((achievement['year'],1,achievement['ratio']*100))
        years.add(achievement['year'])
    allach=models.Achievement.objects.filter(areaid__base=baseIndicator.base,orgcode__in=orgs['orglist']).order_by('year').values('year','orgcode','ratio')
    for ach in allach:
        if ach['ratio'] is not None:
            graph.append((ach['year'],orgs['orglist'].index(ach['orgcode'])+2,ach['ratio']*100))
        years.add(ach['year'])
    table={'headings':headings,'data':data}
    graph=[(line[0]-min(years),line[1],line[2]) for line in graph]#correcting for variable start year
    return render_to_response('timeline.html',{'indicator':baseIndicator,'yearno':len(years),'graph':graph,'ancestors':orgs['ancestors'],'year':year,'title':indicator+' - '+orgs['organisation'].name,'search':searchForm(),'table':table,'org':orgs['organisation']},context_instance=RequestContext(request))
    
    
        
    
def getorgDetails(orgcode,year):
    """Returns the organsiation demographics and some details of the parent organisations up to national level"""
    organisation=get_object_or_404(models.Organisation,orgcode=orgcode) #error trap here
    #now we make a recursive list of the parents of the current organisation
    ancestors=[]
    curorg=organisation #set off the loop
    parents=curorg.orgheirarchy_set.filter(year=year).order_by("-parent__level") #we will send the same query in a moment - cached
    if len(parents)>1 :
        alt={}
        alt['name']=parents[1].parent.name
        alt['code']=parents[1].parent.orgcode
    else:
        alt=False
    orglist=[]                                                 
    while True:
        parents=curorg.orgheirarchy_set.filter(year=year).order_by("-parent__level")
        if len(parents):
            anc_details={}
            curorg=parents[0].parent # get the first parent from the list. Does not cope with multiple heirarchies just yet
            anc_details['code']=curorg.orgcode
            orglist.append(curorg.orgcode)
            anc_details['name']=curorg.name
            ancestors.append(anc_details)
        else:
            break
    if organisation.level>0: #ie are there children?
        children=organisation.children.filter(year=year).select_related()
    else :
        childdet=False #we will pass it later so it has to exist
        children=False
    return{'organisation':organisation,'alt':alt,'ancestors':ancestors,'orglist':orglist,'children':children,}

class searchForm(forms.Form):
    search=forms.CharField(max_length=70)
    
    
def translate(request):
    """Redirection of the most common URLs from the old site"""
    org=request.GET.get('orgcode','UK')
    year=request.GET.get('year',defaults.year)
    return redirect('qofdb.views.browse',permanent=True,orgcode=org,year=year)

def download(request):
    """The download page. Not a lot to actually do other than render the page."""
    form=searchForm()
    title="Data Downloads"
    return render_to_response('download.html',{'form':form,'title':title},context_instance=RequestContext(request))

    
    
    
    
