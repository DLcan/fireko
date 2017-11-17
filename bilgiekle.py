#!/usr/bin/env python
# -*- coding: utf-8 -*-

from firebase import firebase

import subprocess
import json
import eksikno
import fireadr

from datetime import datetime
now = datetime.now() # timezone-aware datetime.utcnow()
today = datetime(now.year,now.month,now.day ) # midnight
 
firebase = firebase.FirebaseApplication(fireadr.adres, None)


#sirtno = input ('Sırtno girin: ') ------------------------geçici

for sirtno in range(9,123):
    
    if sirtno<200:
        result = firebase.get('/Koyun/Canlilar/Disi', sirtno)
    if sirtno>=200:
        result = firebase.get('/Koyun/Canlilar/Erkek', sirtno)



    if result is None:
        print(str(sirtno)+" sırt numaralı canlı hayvan bulunmuyor")
    else:    
        #result["KulakNumarasi"] = raw_input("Kulak numarası girin :") ---------------geçici
        result["SirtNo"] = sirtno
        #-----kayıt ekleme---------------------
        data = {}
        #data[sirtno] = result
        
        data=json.dumps(result)
        #data="'%s'" % data
        print(data)
        
        
        cevap2 ='e'#raw_input("Kayıt düzeltilsin mi?   e/h ")   -------------------geçici   
        if cevap2 =='e':
            if sirtno<200:
                subprocess.call(['curl','-X', 'PATCH', '-d', data, fireadr.adres+'/Koyun/Canlilar/Disi/%s.json'%sirtno])
            if sirtno>=200:
                subprocess.call(['curl','-X', 'PATCH', '-d', data, fireadr.adres+'/Koyun/Canlilar/Erkek/%s.json'%sirtno])
            
