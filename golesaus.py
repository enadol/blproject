from input import jornada
import urllib
import json
import sqlite3

url="C:/Python33/blproject/2018-2019/bl.json"

with open(url) as json_roh:
	data=json_roh.read()
	js=json.loads(data)
	


i=0

afavor=0
encontra=0
equipos=[]
jornadas=str(jornada)
start = 0

def getEquipos():
	#ANTES for fecha in range(1,5):
	for fecha in range(0,jornada):
		#jornadascompletas=js['rounds'][fecha]['name']
		
		for i in range(0,9):
			equipo=js['rounds'][fecha]['matches'][i]['team1']['name']
			contrario=js['rounds'][fecha]['matches'][i]['team2']['name']
			if equipo not in equipos:
				equipos.append(equipo)
			if contrario not in equipos:
				equipos.append(contrario)
	return equipos


def traspasar(viejo, nuevo):
	for index in range(0,len(viejo)):
		for i in nuevo:
			nuevo=viejo

	return nuevo

def getGoles(equipo, goles):
	return goles

def getGolesAcumulados(goleslocal, goles):
	goleslocal=goleslocal+goles
	return goleslocal

print("Loading golesaus.py...")
# jornadainput=raw_input("Ingrese la jornada: ")
# jornada=int(jornadainput)-1


if jornada <0 or jornada >=35:
	print("No se jugó la jornada "+jornadas+" en ese torneo. Verifique y vuelva a ingresar.")
	jornada=None
else:
	clubes=getEquipos()



	for club in clubes:
		subtotaluno=0
		golesuno=0
		golesdos=0
		subtotaldos=0
		golesa=0
		golesb=0
		subtotala=0
		subtotalb=0
		diferencia=0

		for fecha in range(0,jornada):

			#jornadascompletas=js['rounds'][fecha]['name']
			conn = sqlite3.connect('../tabla18.sqlite')
			cur = conn.cursor()
			conn.text_factory = str
	

			cur.execute('''CREATE TABLE IF NOT EXISTS GolesVisitante 
			(Equipo TEXT, Jornada INTEGER, 
			Goles_a_favor INTEGER, Goles_en_contra INTEGER, Diferencia INTEGER)''')

			for i in range(0,9):



				equipo=js['rounds'][fecha]['matches'][i]['team1']['name']
				contrario=js['rounds'][fecha]['matches'][i]['team2']['name']
				afavor=js['rounds'][fecha]['matches'][i]['score1']
				encontra=js['rounds'][fecha]['matches'][i]['score2']

			

				if contrario==club:
					
					golesdos=getGoles(contrario, encontra)
					golesb=getGoles(equipo, afavor)

					subtotaldos=getGolesAcumulados(subtotaldos, golesdos)
					subtotalb=getGolesAcumulados(subtotalb, golesb)

				diferencia=subtotaldos-subtotalb
			
			start=fecha+1
			print("Goles acumulados a favor para el "+club+" en la jornada "+str(start)+": "+ str(subtotaldos))
			print("Goles acumulados en contra para el "+club+" en la jornada "+str(start)+": "+ str(subtotalb))
			print("Diferencia acumulada de goles para el "+club+" en la jornada "+str(start)+": "+ str(diferencia)+"\n")
			cur.execute('''INSERT OR IGNORE INTO GolesVisitante (Equipo, Jornada, Goles_a_favor, Goles_en_contra, Diferencia)  VALUES (?, ?, ?, ?, ? )''', (club, fecha+1, subtotaldos, subtotalb, diferencia))
		

		
			conn.commit()
	
		
#uh.close()
cur.close()
