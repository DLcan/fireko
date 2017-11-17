#!/usr/bin/env python
# -*- coding: utf-8 -*-

from firebase import firebase
# from PIL import Image
import subprocess
import json
import eksikno
from datetime import datetime
import fireadr

# yeni dönem başında firebase'de yeni bir firebase child dönem
# yaratılması lazım  fireadr.adres+'/Koyun/Dogumlar/10_2017 gibi
# sonnodaki sonDogum sıfırlanmalı
#babalarecno ve babaadları dogum kayıtları başladığında kontrol edilip yenilenmeli
donem = "10_2017"                                 #-------------------------
babalarrecno = [430, 441, 455]                   #-------------------------
babaadlari = ["AB", "AO", "ABA"]                 #--------------------------

now = datetime.now() # timezone-aware datetime.utcnow()
today = datetime(now.year, now.month, now.day) # midnight

#---yeni doğanlara isim koymak için isim listesi alıyor--
with open('/home/kaan/Belgeler/Data/Koyun/isimler.txt') as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]




firebase = firebase.FirebaseApplication(fireadr.adres, None)
sonno = []
sirtno = int(raw_input('Sırtno girin: '))
erkeksay = int(raw_input('Yenidoğan erkek sayısını girin: '))
disisay = int(raw_input('Yenidoğan dişi sayısını girin: '))



if sirtno < 200:
    result = firebase.get('/Koyun/Canlilar/Disi', sirtno)
    #print result


if not result is None:
    sonno = firebase.get('/Koyun/Sonno', None)

    sondurum = firebase.get('/Koyun/_sondurum', None)

    anaadi = result["HayvanAdi"]

    result["Aciklama"] = "Dogurdu"                      #----------------------------------gereksiz
    result["AciklamaTarihi"] = today.strftime("%Y-%m-%d")#----------------------------------gereksiz
    result["Dogurdu"] = 1                               #----------------------------------gereksiz
    result["DogurmaSekli"] = disisay + erkeksay
    result["SonDogurmaTarihi"] = today.strftime("%Y-%m-%d")

    #-----Anne kayıt yenileme---------------------
    adata = {}
    adata[sirtno] = result
    adata = json.dumps(adata)

    subprocess.call(['curl',
                     '-X',
                     'PATCH',
                     '-d',
                     adata,
                     fireadr.adres+'/Koyun/Canlilar/Disi/.json'])

    #---Yeni doğum dönemi doğuranlar kayıt oluşturma  ------
    yenidata = {}
    anarecno = str(result["RecNo"])
    #yenidata[anarecno] = {}
    #yenidata[anarecno][0] = [today.strftime("%Y-%m-%d"),result["HayvanAdi"],sirtno]
    yenidata[anaadi] = {}
    #yenidata[anaadi][0] = today.strftime("%d-%m-%Y")
    
    #--------------_sondurum-------------------
    sondurum_Disi = int(sondurum["_Disi"])  #--dişilerin toplamı
    sondurum_Erkek = int(sondurum["_Erkek"]) #--erkeklerin toplamı
    sondurum_Toplam = int(sondurum["_Toplam"])   #--son toplam
    sondurum_Disikuzu = int(sondurum["_Disikuzu"]) #--yeni doğum dönemindeki dişi kuzu sayısı 
    sondurum_Erkekkuzu = int(sondurum["_Erkekkuzu"]) #--yeni doğum dönemindeki erkek kuzu sayısı

    #--------------Sonno-------------------

    sonDisiNo = int(sonno["sonDisi"])  #--dişilerin otomatik verilen son sırt numarası
    sonErkekNo = int(sonno["sonErkek"]) #--erkeklerin otomatik verilen son sırt numarası
    sonRec = int(sonno["sonRec"])   #--son verilen RecNo
    sonDogum = int(sonno["sonDogum"]) #--yeni doğum dönemindeki doğum sayısı

    anaadi = result["HayvanAdi"]
    #anarecno = result["RecNo"]


    if disisay > 0:
        for sayd in range(disisay):
            result = {}
            #-- yenidoğan dişi sırt numarasını
            #  önce eksiknolar arasında arıyor 
            # bulamazsa sonDisiNo+1 veriyor

            eksiknodan_gelen_sirtno = eksikno.eksikno_al("Disi")
            if eksiknodan_gelen_sirtno == 0:
                sonDisiNo = sonDisiNo+1
                d_sirtno = sonDisiNo
            else :
                d_sirtno = eksiknodan_gelen_sirtno

            sonRec = sonRec + 1

            result["AnneRecNo"] = anarecno
            result["AnaAdi"] = anaadi
            result["ArazideDogdu"] = 1
            result["Aciklama"] = "Arazide dogdu"
            result["AciklamaTarihi"] = today.strftime("%Y-%m-%d")
            result["BabalarRecNo"] = babalarrecno
            result["BabaAdlari"] = babaadlari
            result["CanliMi"] = "Canli"
            result["Cinsiyet"] = "Disi"
            result["DogumTarihi"] = today.strftime("%Y-%m-%d")
            result["Dogurdu"] = 0
            result["DogurmaSekli"] = ""
            result["HayvanAdi"] = content[sonRec-495]
            result["KocaVerilmeDurumu"] = 0
            result["KulakNumarasi"] = ""
            result["RecNo"] = sonRec
            result["SirtNo"] = d_sirtno
            result["SonDogurmaTarihi"] = 0

            #-----dişi kayıt ekleme---------------------
            ddata = {}
            ddata[d_sirtno] = result
            ddata = json.dumps(ddata)

            subprocess.call(['curl', '-X', 'PATCH', '-d', ddata, fireadr.adres+'/Koyun/Canlilar/Disi/.json'])

            #---Yeni doğum dönemi doğuranlar kayıt oluşturma  devam ediyor yeni doğan dişiler ekleniyor------
            yenidata[anaadi][sonRec] = {"Tarih":today.strftime("%Y-%m-%d"), "SirtNo":d_sirtno, "isim":content[sonRec-495],"Cinsiyet":"Dişi"}

            #---Sondurum dişi sayısı yenileme
            #--sondurum_Disi = sondurum_Disi +1
            sondurum_Disikuzu = sondurum_Disikuzu +1
            sondurum_Toplam = sondurum_Toplam + 1


    if erkeksay > 0:
        for saye in range(erkeksay):
            result = {}

            #-- yenidoğan erkek sırt numarasını önce eksiknolar arasında arıyor bulamazsa sonErkekNo+1 veriyor
            eksiknodan_gelen_sirtno = eksikno.eksikno_al("Erkek")
            if eksiknodan_gelen_sirtno == 0:
                sonErkekNo = sonErkekNo + 1
                e_sirtno = sonErkekNo
            else :
                e_sirtno = eksiknodan_gelen_sirtno

            sonRec = sonRec+1


            result["AnneRecNo"] = anarecno
            result["AnaAdi"] = anaadi
            result["ArazideDogdu"] = 1
            result["Aciklama"] = "Arazide dogdu"
            result["AciklamaTarihi"] = today.strftime("%Y-%m-%d")
            result["BabalarRecNo"] = babalarrecno
            result["BabaAdlari"] = babaadlari
            result["CanliMi"] = "Canli"
            result["Cinsiyet"] = "Erkek"
            result["DogumTarihi"] = today.strftime("%Y-%m-%d")
            result["HayvanAdi"] = content[sonRec-495]
            result["RecNo"] = sonRec
            #result["SirtNo"] = e_sirtno

            #-----erkek kayıt ekleme---------------------
            edata = {}
            edata[e_sirtno] = result
            edata = json.dumps(edata)

            subprocess.call(['curl',
                             '-X',
                             'PATCH',
                             '-d',
                             edata,
                             'https://koyun-48596.firebaseio.com/Koyun/Canlilar/Erkek/.json'])

            #---Yeni doğum dönemi doğuranlar kayıt oluşturma  devam ediyor ------
            yenidata[anaadi][sonRec] = {"Tarih":today.strftime("%Y-%m-%d"), "SirtNo":e_sirtno, "isim":content[sonRec-495], "Cinsiyet":"Erkek"}

            #---Sondurum erkek sayısı yenileme
            #--sondurum_Erkek = sondurum_Erkek +1
            sondurum_Erkekkuzu = sondurum_Erkekkuzu + 1
            sondurum_Toplam = sondurum_Toplam + 1



    #--- yeni dönem doğumlar kayıt ekleme
    yd = {}
    #--- yd[0] = "Null"
    sonDogum = sonDogum + 1
    yd[sonDogum] = yenidata
    yd = json.dumps(yd)  # {"Anaadı" :{Tarih, SirtNo , isim, Cinsiyet}}

    subprocess.call(['curl',
                     '-X',
                     'PATCH',
                     '-d',
                     yd,
                     fireadr.adres+'/Koyun/Dogumlar/%s/.json'%donem])


    #-----sonno kayıt ekleme---------------------

    sonno["sonDisi"] = sonDisiNo
    sonno["sonErkek"] = sonErkekNo
    sonno["sonRec"] = sonRec
    sonno["sonDogum"] = sonDogum
    sonno = json.dumps(sonno)
    subprocess.call(['curl',
                     '-X',
                     'PATCH',
                     '-d',
                     sonno,
                     fireadr.adres+'/Koyun/Sonno/.json'])

    #--------------_sondurum  kayıt ekleme ------------------

    sondurum["_Disi"] = sondurum_Disi  #--dişilerin toplamı
    sondurum["_Erkek"] = sondurum_Erkek #--erkeklerin toplamı
    sondurum["_Toplam"] = sondurum_Toplam   #--son toplam
    sondurum["_Disikuzu"] = sondurum_Disikuzu #--yeni doğum dönemindeki dişi kuzu sayısı
    sondurum["_Erkekkuzu"] = sondurum_Erkekkuzu #--yeni doğum dönemindeki erkek kuzu sayısı
    sondurum = json.dumps(sondurum)
    subprocess.call(['curl',
                     '-X',
                     'PATCH',
                     '-d',
                     sondurum,
                     fireadr.adres+'/Koyun/_sondurum/.json'])
