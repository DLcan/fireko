# -*- coding: utf-8 -*-
# python

# example of reading JSON from a file
from firebase import firebase
import json
import fireadr

#Export collection from mLab
#mongoexport -h ds139122.mlab.com:39122 -d koyun -c Dogumlar -u kaan -p 14382017 -o Dogumlar.json
firebase = firebase.FirebaseApplication(fireadr.adres, None)
my_data = firebase.get('/Koyun/Dogumlar', None)
#my_data = json.loads(open("/home/kaan/Belgeler/Data/Koyun/dogumlar.json").read())

print (my_data)
dogumlar=my_data['6_2017']
print(len(dogumlar))



#---------------HTML oluşturma --------------------------------

html_out="<html> \n"+"<body> \n"+"  <h2>Dogumlar</h2>\n"+"  <table border='0.1'>\n"+"    <tr bgcolor='#9acd32'>\n"

#--------------------------------------------kolon başlıkları-------------------

html_out=html_out+"      <th style='text-align:left'>Ana</th>\n"
html_out=html_out+"      <th style='text-align:center'>Tarih</th>\n"
html_out=html_out+"      <th style='text-align:right'>Yavru Rec No</th>\n"
html_out=html_out+"      <th style='text-align:left'>Cinsiyet</th>\n"
html_out=html_out+"      <th style='text-align:left'>Sırt No</th>\n"
html_out=html_out+"      <th style='text-align:left'>İsim</th>\n"
html_out=html_out+"    </tr>\n"


def duzgun_tarih(tar):
    tar0=tar.split("T")
    tar1=tar0[0].split("-")
    tar2=tar1[2]+"-"+tar1[1]+"-"+tar1[0]
    
    return tar2


with open("/home/kaan/Belgeler/dogumlar.html", 'w') as outfile:
    outfile.write(html_out)
satir_basi = "    <tr>\n"
satir_sonu = "    </tr>\n"
hucre_basi = "<td>"
hucre_sonu = "</td>\n"
with open("/home/kaan/Belgeler/dogumlar.html", 'a') as outfile:
    for i in range(len(dogumlar)):
        for ana in dogumlar[i]:
            if dogumlar[i]!="Null":
                if dogumlar[i][ana] is not None:
                    line_ana = satir_basi+hucre_basi+ ana + hucre_sonu  + satir_sonu
                    outfile.write(line_ana)
                    sayac =0
                for yavru in (dogumlar[i][ana]):
                    sayac +=1
                    if sayac==1:
                        line_yavru = "    <tr>\n"+"      <td>"+"</td>\n"+"      <td style='text-align:center'>"+ duzgun_tarih(dogumlar[i][ana][yavru]['Tarih'])+ hucre_sonu
                    else:
                        line_yavru = "    <tr>\n"+"      <td>"+"</td>\n"+"      <td style='text-align:center'>"+  hucre_sonu
                    line_yavru =line_yavru+"      <td style='text-align:center'>"+"  "+yavru+hucre_sonu
                    line_yavru =line_yavru +"      <td>"+"  "+(dogumlar[i][ana][yavru]['Cinsiyet'])+hucre_sonu
                    line_yavru =line_yavru +"      <td style='text-align:center'>"+"  "+str(dogumlar[i][ana][yavru]['SirtNo'])+hucre_sonu
                    line_yavru =line_yavru +"      <td>"+"  "+(dogumlar[i][ana][yavru]['isim'])+hucre_sonu
                    line_yavru = line_yavru +"    </tr>\n"
                    outfile.write(line_yavru)
                   
                print(dogumlar[i][ana])
        son="</html> \n"+"</body> \n"
        outfile.write(son)