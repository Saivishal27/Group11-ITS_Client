from django.http import HttpResponse
from django.shortcuts import render
import requests
import json


def House(request):
    j = requests.get('http://10.0.3.23:9081/Farms/households')
    j1=requests.get('http://10.0.3.23:9081/Farms/person')
    r = j.json()
    r1=j1.json()
    lat = {}
    lon = {}
    mi = {}
    person={}
    p_count={}
    links={}
    for i in range(len(r1)):
        if r1[i].get('house_id') in person:
            person[int(r1[i].get('house_id'))].append(str(r1[i].get('person_name')))
            p_count[int(r1[i].get('house_id'))]+=1
        else:
            person[int(r1[i].get('house_id'))] = [str(r1[i].get('person_name'))]
            p_count[int(r1[i].get('house_id'))]=1
    for i in range(len(r)):
        if r[i].get('id') in lat:
            lat[int(r[i].get('id'))].append(float(r[i].get('latitude')))
            lon[int(r[i].get('id'))].append(float(r[i].get('longitude')))
            mi[int(r[i].get('id'))].append(float(r[i].get('monthly_income')))
           # p_count[int(r[i].get('id'))].append(int(r[i].get('person_count')))
        else:
            lat[int(r[i].get('id'))] = float(r[i].get('latitude'))
            lon[int(r[i].get('id'))] = float(r[i].get('longitude'))
            mi[int(r[i].get('id'))] = float(r[i].get('monthly_income'))
           # p_count[int(r[i].get('id'))]=int(r[i].get('person_count'))
            links[int(r[i].get('id'))]=str(r[i].get('image_link'))
    latitude=[]
    longitude=[]
    income=[]
    house_id=[]
    persons=[]
    person_count =[]
    image_links=[]
    for key,value in lat.iteritems():
        house_id.append(key)
        latitude.append(lat[key])
        longitude.append(lon[key])
        income.append(mi[key])
        persons.append(person[key])
        person_count.append(p_count[key])
        image_links.append(links[key])
    return render(request, 'its/House.html', {'image_links':image_links,'person_count':person_count,'house_id':house_id,'lat': latitude, 'lon': longitude, 'mi': income , 'persons':persons})


# Create your views here.


# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

# Create your views here.
def index(request):
    return render(request,'its/index.html')
def farm_chart(request):
    j = requests.get('http://10.0.3.23:9081/Farms/farmshape')
    j2 = requests.get('http://10.0.3.23:9081/Farms/farm')
    r = j.json()
    r2 = j2.json()

def split_data(s):
    cnt=0
    x=""
    for ch in s:
        if ch=='(':
            cnt+=1
            continue
        if ch==')':
            break
        if cnt==2:
            x+=ch
    lat=[]
    lon=[]
    for vals in x.split(','):
        y=vals.split(' ')
        y=filter(None,y)
        lat.append(float(y[0]))
        lon.append(float(y[1]))
    return lat,lon

def Farm(request):
    x=request.GET.get('farmid')
    flag=0
    if x is not None:
        flag=1
        farmid=int(x)
    j = requests.get('http://10.0.3.23:9081/Farms/farmshape')
    j2= requests.get('http://10.0.3.23:9081/Farms/farm')
    j3= requests.get('http://10.0.3.23:9081/Farms/seasonwisecrop')
    r = j.json()
    r2=j2.json()
    r3=j3.json()
    lat = {}
    lon = {}
    well_id=[]
    well_lats=[]
    well_lons=[]
    well_props=[]
    farm_areas={}
    farm_attr={}
    ids=[]
    f_ids=[]
    for i in range(len(r2)):
        if r2[i].get('id') not in f_ids:
            f_ids.append(r2[i].get('id'))
    f_ids.sort()
    for i in range(len(r)):
        if flag==1:
            ids.append(farmid)
            break
        else:
            ids.append(int(r[i].get('farm_id')))
    for i in range(len(r2)):
        if int(r2[i].get('id')) in ids:
            s=r2[i].get('farm_points')
            x,y=split_data(s)
            lat[r2[i].get('id')]=y
            lon[r2[i].get('id')]=x
        #if int(r2[i].get('id')) in ids:    
            #farm_attr[int(r2[i].get('id'))]=[y[0]+0.0001,x[0]+0.0003]
            farm_attr[int(r2[i].get('id'))]=[sum(y)/len(y),sum(x)/len(x)]
        if flag==0:
            s=r2[i].get('farm_points')
            x,y=split_data(s)
            lat[r2[i].get('id')]=y
            lon[r2[i].get('id')]=x
    farm_crops={}
    for i in range(len(r3)):
        crop={'rice':0,'wheat':0,'maize':0,'sugarcane':0,'barley':0}
        if r3[i].get('farm_id') in ids:
            if r3[i].get('farm_id') in farm_crops:
                farm_crops[int(r3[i].get('farm_id'))][0].append(str(r3[i].get('crop_name')))
                farm_crops[int(r3[i].get('farm_id'))][1].append(float(r3[i].get('area_cultivated')))
            else:
                farm_crops[int(r3[i].get('farm_id'))]=[[str(r3[i].get('crop_name'))],[float(r3[i].get('area_cultivated'))]]
    for key,value in farm_crops.iteritems():
        if "Rice" in farm_crops[key][0]:
            farm_attr[key].append(farm_crops[key][1][farm_crops[key][0].index('Rice')])
        else:
            farm_attr[key].append(0)
        if "Wheat" in farm_crops[key][0]:
            farm_attr[key].append(farm_crops[key][1][farm_crops[key][0].index('Wheat')])
        else:
            farm_attr[key].append(0)
        if "Maize" in farm_crops[key][0]:
            farm_attr[key].append(farm_crops[key][1][farm_crops[key][0].index('Maize')])
        else:
            farm_attr[key].append(0)
        if "Sugarcane" in farm_crops[key][0]:
            farm_attr[key].append(farm_crops[key][1][farm_crops[key][0].index('Sugarcane')])
        else:
            farm_attr[key].append(0)
        if "Barley" in farm_crops[key][0]:
            farm_attr[key].append(farm_crops[key][1][farm_crops[key][0].index('Barley')])
        else:
            farm_attr[key].append(0)
    farm_attributes=[]
    for key,value in farm_attr.iteritems():
        farm_attributes.append(farm_attr[key])
    latitude = []
    longitude = []
    farm_id=[]
    farm_link=[]
    farm_area=[]
    for key, value in lat.iteritems():
        farm_id.append(key)
        latitude.append(lat[key])
        longitude.append(lon[key])
    farm_links={}
    for i in range(len(r2)):
        if int(r2[i].get('id')) in ids:
            farm_areas[int(r2[i].get('id'))]=float((r2[i].get('farm_area')))
            farm_links[int(r2[i].get('id'))]=(str(r2[i].get('farm_link')))
    for key,value in farm_links.iteritems():
        farm_link.append(farm_links[key])
        farm_area.append(farm_areas[key])
    #farm_link.reverse()
    return render(request, 'its/Farm.html', {'f_ids':f_ids,'flag':flag,'image_link':farm_link,'farm_attr':farm_attributes,'lat': latitude, 'lon': longitude, 'farm_id':farm_id,'farm_area':farm_area})
def Well(request):
    j = requests.get('http://10.0.3.23:9081/Farms/farmshape')
    j1= requests.get('http://10.0.3.23:9081/Farms/wells')
    j2= requests.get('http://10.0.3.23:9081/Farms/farm')
    j3= requests.get('http://10.0.3.23:9081/Farms/seasonwisecrop')
    r = j.json()
    r1= j1.json()
    r2=j2.json()
    r3=j3.json()
    lat = {}
    lon = {}
    well_id=[]
    well_lats=[]
    well_lons=[]
    well_props=[]
    farm_area=[]
    farm_attr={}
    ids=[]
    for i in range(len(r)):
        ids.append(int(r[i].get('farm_id')))
    for i in range(len(r2)):
        s=r2[i].get('farm_points')
        x,y=split_data(s)
        lat[r2[i].get('id')]=y
        lon[r2[i].get('id')]=x
        if int(r2[i].get('id')) in ids:    
            #farm_attr[int(r2[i].get('id'))]=[y[0]+0.0001,x[0]+0.0003]
            farm_attr[int(r2[i].get('id'))]=[sum(y)/len(y),sum(x)/len(x)]
    for i in range(len(r1)):
        well_id.append(r1[i].get('id'))
        well_lats.append(float(r1[i].get('latitude')))
        well_lons.append(float(r1[i].get('longitude')))
        temp=[float(r1[i].get('depth')),float(r1[i].get('avg_water_yield'))]
        well_props.append(temp)
    latitude = []
    longitude = []
    farm_id=[]
    for key, value in lat.iteritems():
        farm_id.append(key)
        latitude.append(lat[key])
        longitude.append(lon[key])

    for i in range(len(r2)):
        farm_area.append(r2[i].get('farm_area'))
    return render(request, 'its/Well.html', {'lat': latitude, 'lon': longitude, 'farm_id':farm_id, 'well_id':well_id, 'well_lats':well_lats,'well_lons':well_lons,'well_props':well_props,'farm_area':farm_area})