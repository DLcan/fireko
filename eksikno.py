#!/usr/bin/env python
# -*- coding: utf-8 -*-

from firebase import firebase
from PIL import Image 
import subprocess
import json
import fireadr

firebase = firebase.FirebaseApplication(fireadr.adres, None)

def eksiknoya_ekle(sirtno):
    
    if sirtno<200:
        result = firebase.get('/Koyun/Eksikno/Disi', None)
    if sirtno>=200:
        result = firebase.get('/Koyun/Eksikno/Erkek', None)
    data = {}        
    if result is None:    
        print ("Eksikno'ya Klasör ekleniyor")
        
        if sirtno<200:
            data["Disi"]="Null"
            data=json.dumps(data)
            subprocess.call(['curl', '-X', 'PATCH', '-d', data, fireadr.adres+'/Koyun/Eksikno/.json'])
            result = firebase.get('/Koyun/Eksikno/Disi', None)
        if sirtno>=200:
            data["Erkek"]="Null"
            data=json.dumps(data)
            subprocess.call(['curl', '-X', 'PATCH', '-d', data, fireadr.adres+'/Koyun/Eksikno/.json'])
            result = firebase.get('/Koyun/Eksikno/Erkek', None)


    if result==u"Null":
        data = {} 
        recno = 0
        data[recno] = sirtno
        data=json.dumps(data)

        if sirtno<200:
            subprocess.call(['curl', '-X', 'PATCH', '-d', data, fireadr.adres+'/Koyun/Eksikno/Disi/.json'])
        if sirtno>=200:
            subprocess.call(['curl', '-X', 'PATCH', '-d', data, fireadr.adres+'/Koyun/Eksikno/Erkek/.json'])
        return 
        
    else:
        boy = len(result)   
        for say in result:
            #print(say)
            if say==sirtno:
                print ("Bu sayı var")
                return
        recno = str(len(result))
        data[recno] = sirtno
        data=json.dumps(data)

        if sirtno<200:
            subprocess.call(['curl', '-X', 'PATCH', '-d', data, fireadr.adres+'/Koyun/Eksikno/Disi/.json'])
        if sirtno>=200:
            subprocess.call(['curl', '-X', 'PATCH', '-d', data, fireadr.adres+'/Koyun/Eksikno/Erkek/.json'])
    return 


def eksikno_al(cinsiyet):
    if cinsiyet=="Disi":
        result = firebase.get('/Koyun/Eksikno/Disi', None)
    if cinsiyet=="Erkek":
        result = firebase.get('/Koyun/Eksikno/Erkek', None)
        
    sayi = 0
    data = {}        
    if result is None:    
        print ("Eksikno'ya Klasör ekleniyor")
        
        if cinsiyet=="Disi":
            data["Disi"]="Null"
            data=json.dumps(data)
            subprocess.call(['curl', '-X', 'PATCH', '-d', data, fireadr.adres+'/Koyun/Eksikno/.json'])
            result = firebase.get('/Koyun/Eksikno/Disi', None)
        if cinsiyet=="Erkek":
            data["Erkek"]="Null"
            data=json.dumps(data)
            subprocess.call(['curl', '-X', 'PATCH', '-d', data, fireadr.adres+'/Koyun/Eksikno/.json'])
            result = firebase.get('/Koyun/Eksikno/Erkek', None)    
    data = {}
    if result==u"Null":
        print("Eksikno yok")
        return sayi     
    else:
        boy = len(result)  - 1
        sayi = result[boy]

        if cinsiyet=="Disi":
            subprocess.call(['curl','-i', '-X', 'DELETE', fireadr.adres+'/Koyun/Eksikno/Disi/%s.json'%boy])
        if cinsiyet=="Erkek":
            subprocess.call(['curl','-i', '-X', 'DELETE', fireadr.adres+'/Koyun/Eksikno/Erkek/%s.json'%boy])
    return sayi
    
