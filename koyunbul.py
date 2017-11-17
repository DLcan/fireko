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







sirtno = input ('Sırtno girin: ')
if sirtno<200:
    result = firebase.get('/Koyun/Canlilar/Disi', sirtno)
if sirtno>=200:
    result = firebase.get('/Koyun/Canlilar/Erkek', sirtno)
    
print(result)    