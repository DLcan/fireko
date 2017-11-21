#!/usr/bin/env python
# -*- coding: utf-8 -*-

from firebase import firebase
import pprint
import subprocess
import json
import eksikno
import fireadr

from datetime import datetime
now = datetime.now() # timezone-aware datetime.utcnow()
today = datetime(now.year,now.month,now.day ) # midnight



firebaseA = firebase.FirebaseApplication(fireadr.adres, None)

#--------------_sondurum-------------------
sondurum = firebaseA.get('/Koyun/_sondurum',None)

sondurum_Disi  = int(sondurum["_Disi"])  #--dişilerin toplamı
sondurum_Erkek = int(sondurum["_Erkek"]) #--erkeklerin toplamı
sondurum_Toplam     = int(sondurum["_Toplam"])   #--son toplam
sondurum_Disikuzu   = int(sondurum["_Disikuzu"]) #--yeni doğum dönemindeki dişi kuzu sayısı    
sondurum_Erkekkuzu   = int(sondurum["_Erkekkuzu"]) #--yeni doğum dönemindeki erkek kuzu sayısı  




#----sirtno = input ('Sırtno girin: ')  dosyadan okurken kapalı 

with open('kesilenler.txt') as f:
    content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content] 
    print(content)
for kesilen in range(len(content)):
    sirtno=int(content[kesilen])

    if sirtno<200:
        result = firebaseA.get('/Koyun/Canlilar/Disi', sirtno)
    if sirtno>=200:
        result = firebaseA.get('/Koyun/Canlilar/Erkek', sirtno)
    recno='a'
    if result is None:
        print(str(sirtno)+" sırt numaralı canlı hayvan bulunmuyor")
    else:    
        for key in result:
            if key==u'Aciklama':
                result[key]=u'Kesildi'
            if key==u'AciklamaTarihi':
                result[key]=today.strftime("%Y-%m-%d")
            if key==u'CanliMi':
                result[key]=u'Kesildi'
            if key==u'RecNo':
                recno=result[key]
        
                
        #---Sondurum dişi sayısı yenileme
        if sirtno<200: 
            sondurum_Disi = sondurum_Disi - 1
        


        #---Sondurum erkek sayısı yenileme
        if sirtno>=200:    
            sondurum_Erkek = sondurum_Erkek -1
            
        sondurum_Toplam = sondurum_Disi + sondurum_Erkek + sondurum_Disikuzu + sondurum_Erkekkuzu
        sn=u'SirtNo'
        result[sn]=sirtno    
        
        
        #-----kayıt ekleme---------------------
        data = {}
        data[recno] = result
        data=json.dumps(data)
        #data="'%s'" % data
        print(data)

        cevap1 = raw_input("Kesilenlere eklensin mi?   e/h ")
        if cevap1 =='e':
            subprocess.call(['curl', '-X', 'PATCH', '-d', data, fireadr.adres+'/Koyun/Kesilenler/.json'])

        cevap2 = raw_input("Canlılardan silinsin mi?   e/h ")
        if cevap2 =='e':
            if sirtno<200:
                subprocess.call(['curl','-i', '-X', 'DELETE', fireadr.adres+'/Koyun/Canlilar/Disi/%s.json'%sirtno])
            if sirtno>=200:
                subprocess.call(['curl','-i', '-X', 'DELETE', fireadr.adres+'/Koyun/Canlilar/Erkek/%s.json'%sirtno])

            eksikno.eksiknoya_ekle(sirtno)


#--------------_sondurum  kayıt yenileme ------------------

sondurum["_Disi"] = sondurum_Disi  #--dişilerin toplamı
sondurum["_Erkek"] = sondurum_Erkek #--erkeklerin toplamı
sondurum["_Toplam"] = sondurum_Toplam   #--son toplam
sondurum["_Disikuzu"] = sondurum_Disikuzu #--yeni doğum dönemindeki dişi kuzu sayısı    
sondurum["_Erkekkuzu"] = sondurum_Erkekkuzu #--yeni doğum dönemindeki erkek kuzu sayısı    
sondurum=json.dumps(sondurum)
subprocess.call(['curl', '-X', 'PATCH', '-d', sondurum, fireadr.adres+'/Koyun/_sondurum/.json'])




