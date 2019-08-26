  #!/usr/bin/python
  # -*- coding: utf-8 -*-

#Para limpiar el json general obtenido del repositorio

fname = input("Enter a file name: ")
if ( len(fname) < 1 ) : fname = '../2019-2020/bl.json'

fh = open(fname)
stringdata=fh.read()

fh=open(fname, "w")
news=stringdata.replace("ö", "oe")
stringdata=news
news=stringdata.replace("ü", "ue")
stringdata=news
news=stringdata.replace("Eintracht Frankfurt", "Frankfurt")
stringdata=news
news=stringdata.replace("VfL Wolfsburg", "Wolfsburg")
stringdata=news
news=stringdata.replace("Hamburger SV", "Hamburg")
stringdata=news
news=stringdata.replace("SV Darmstadt 98", "SV Darmstadt")
stringdata=news
news=stringdata.replace("1. FSV Mainz 05", "Mainz")
stringdata=news
news=stringdata.replace("Bor. Moenchengladbach", "Borussia Moenchengladbach")
stringdata=news
news=stringdata.replace("Bayer 04 Leverkusen", "Bayer Leverkusen")
stringdata=news
news=stringdata.replace("Hertha BSC", "Hertha Berlin")
stringdata=news
news=stringdata.replace("1899 Hoffenheim", "Hoffenheim")
stringdata=news
news=stringdata.replace("FC Ingolstadt 04", "FC Ingolstadt")
stringdata=news
news=stringdata.replace("Spieltag", "Jornada")
stringdata=news
news=stringdata.replace("FC Schalke 04", "Schalke 04")
stringdata=news
news=stringdata.replace("SC Freiburg", "Freiburg")
stringdata=news
news=stringdata.replace("Bayern Muenchen", "FC Bayern Muenchen")

fh.write(news)
	
#print news



fh.close()
