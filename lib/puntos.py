﻿from partidos import jornada
import urllib
import json
import sqlite3

url="C:/Python33/blproject/2019-2020/bl.json"

with open(url) as json_roh:
	data=json_roh.read()
	js=json.loads(data)
	


i = 0
puntoslocal = 0
puntosvisitante = 0
sumavisitante = 0
puntos = 0
equipos = []
jornadas = str(jornada)
start = 0

def getEquipos():
	for fecha in range(0, jornada):
	
		for i in range(0, 9):
			equipo = js['rounds'][fecha]['matches'][i]['team1']['name']
			contrario = js['rounds'][fecha]['matches'][i]['team2']['name']
			if equipo not in equipos:
				equipos.append(equipo)
			if contrario not in equipos:
				equipos.append(contrario)
	return equipos



def getPuntos(equipo, afavor, encontra):
	puntos = 0
	
	if afavor > encontra:
		puntos = 3
	elif afavor == encontra:
		puntos = 1
	else:
		puntos = 0
	
	return puntos

def getPuntosAcumulados(puntoslocal, puntos):
	puntoslocal = puntoslocal + puntos
	return puntoslocal
	

print("Loading puntos.py...")


if jornada < 0 or jornada >= 35:
	print("No se jugó la jornada "+str(jornada)+" en ese torneo. Verifique y vuelva a ingresar.")
	jornada = None
else:
	clubes = getEquipos()

	for club in clubes:
		subtotaluno = 0
		subtotaldos = 0
		sumapuntos = 0
		sumtotallocal = 0
		sumtotalvisitante = 0

		for fecha in range(0, jornada):
			#jornadascompletas=js['rounds'][fecha]['name']
			conn = sqlite3.connect('../tabla19.sqlite')
			cur = conn.cursor()
			conn.text_factory = str

			cur.execute('''CREATE TABLE IF NOT EXISTS Puntos 
			(Equipo TEXT, Jornada INTEGER, Puntos_Local INTEGER, Puntos_Visitante INTEGER, Total_Puntos INTEGER)''')

				
			for i in range(0,9):
				equipo = js['rounds'][fecha]['matches'][i]['team1']['name']
				afavor = js['rounds'][fecha]['matches'][i]['score1']
				contrario = js['rounds'][fecha]['matches'][i]['team2']['name']
				encontra = js['rounds'][fecha]['matches'][i]['score2']

				if equipo == club:
					puntosuno = getPuntos(equipo, afavor, encontra)
				

					subtotaluno = getPuntosAcumulados(subtotaluno, puntosuno)
					
		

				if contrario == club:
					puntosdos = getPuntos(contrario, encontra, afavor)
						
		
					subtotaldos = getPuntosAcumulados(subtotaldos, puntosdos)
					
				
				sumapuntos = subtotaluno + subtotaldos
			start = fecha+1
			print("El equipo "+club+" sumaba "+str(subtotaluno)+" puntos como local a la "+str(start))
			print("El equipo "+club+" sumaba "+str(subtotaldos)+" puntos como visitante a la "+str(start)	)
			print("El equipo "+club+" sumaba "+str(sumapuntos)+" puntos en total a la "+str(start))
			cur.execute('''INSERT OR IGNORE INTO Puntos (Equipo, Jornada, Puntos_Local, Puntos_Visitante, Total_Puntos)  VALUES (?, ?, ?, ?, ? )''', (club, start, subtotaluno, subtotaldos, sumapuntos))
			conn.commit()			
	
cur.close()
