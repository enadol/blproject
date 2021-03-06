#from input import jornada
import json
#import requests
import sqlite3

url="C:/Python33/blproject/2019-2020/bl.json"

with open(url) as json_roh:
	data = json_roh.read()
	js = json.loads(data)
	uno = js['rounds']
	jornada = len(uno)

i = 0
puntos = 0
jornadas = str(jornada)


puntoslocal = 0
puntosvisitante = 0
sumavisitante = 0
puntos = 0
sumalocal = 0
equipos = []
start = 0

def getEquipos():
	for fecha in range(0, jornada):
		#jornadascompletas=js['rounds'][fecha]['name']

		for i in range(0,9):
			equipo=js['rounds'][fecha]['matches'][i]['team1']['name']
			contrario=js['rounds'][fecha]['matches'][i]['team2']['name']
			if equipo not in equipos:
				equipos.append(equipo)
			if contrario not in equipos:
				equipos.append(contrario)
	return equipos



def getPuntos(equipo, afavor, encontra):

	if afavor > encontra:
		puntos = 3
		
	elif afavor == encontra:
		puntos = 1
		
	else:
		puntos = 0
		
	
	return puntos


def getPartidosAcumulados(partidosviejo, partidosnuevo):
	partidosviejo = partidosviejo + partidosnuevo
	return partidosnuevo

print("Loading partidos.py...")
# jornadainput=raw_input("Ingrese la jornada: ")
# jornada=int(jornadainput)-1



if jornada < 0 or jornada >= 35:
	print("No se jugo la jornada "+str(jornada)+" en ese torneo. Verifique y vuelva a ingresar.")
	jornada = None
else:
	clubes = getEquipos()
	countempatados = 0
	countganados = 0
	countperdidos = 0

	for club in clubes:
		
		countempatados1 = 0
		countganados1 = 0
		countperdidos1 = 0
		countjugados1 = 0

		countempatados2 = 0
		countganados2 = 0
		countperdidos2 = 0
		countjugados2 = 0

		subtotalganados1 = 0
		subtotalganados2 = 0
		subtotalempatados1 = 0
		subtotalempatados2 = 0
		subtotalperdidos1 = 0
		subtotalperdidos2 = 0
		subtotaljugados1 = 0
		subtotaljugadosa = 0
		sumatotal = 0




		for fecha in range(0, jornada):
			#jornadascompletas=js['rounds'][fecha]['name']

			conn = sqlite3.connect('../tabla19.sqlite')
			cur = conn.cursor()
			conn.text_factory = str

			cur.execute('''CREATE TABLE IF NOT EXISTS Partidos 
			(Equipo TEXT, Jornada INTEGER, PJ_Local INTEGER, PJ_Visitante INTEGER, PJ INTEGER, PG_Local INTEGER, PG__Visitante INTEGER, PG INTEGER, PE_Local INTEGER, PE_Visitante INTEGER, PE INTEGER, PP_Local INTEGER, PP_Visitante INTEGER, PP INTEGER)''')


				
			for i in range(0,9):
				equipo = js['rounds'][fecha]['matches'][i]['team1']['name']
				afavor = js['rounds'][fecha]['matches'][i]['score1']
				contrario = js['rounds'][fecha]['matches'][i]['team2']['name']
				encontra = js['rounds'][fecha]['matches'][i]['score2']




				if equipo == club:
					puntosuno = getPuntos(equipo, afavor, encontra)
					
					if puntosuno == 3:
						countganados1+=1

		
					elif puntosuno == 1:
						countempatados1+=1
		
					else:
						countperdidos1+=1	
					countjugados1+=1

					subtotalganados1 = getPartidosAcumulados(subtotalganados1, countganados1)
					subtotalempatados1 = getPartidosAcumulados(subtotalempatados1, countempatados1)
					subtotalperdidos1 = getPartidosAcumulados(subtotalperdidos1, countperdidos1)
					subtotaljugados1 = getPartidosAcumulados(subtotaljugados1, countjugados1)
				

				if contrario == club:
					puntosdos = getPuntos(contrario, encontra, afavor)
					
					if puntosdos == 3:
						countganados2+=1
		
					elif puntosdos == 1:
						countempatados2+=1
		
					else:
						countperdidos2+=1	
						
					countjugados2+=1

					subtotalganados2 = getPartidosAcumulados(subtotalganados2, countganados2)
					subtotalempatados2 = getPartidosAcumulados(subtotalempatados2, countempatados2)
					subtotalperdidos2 = getPartidosAcumulados(subtotalperdidos2, countperdidos2)
					subtotaljugadosa = getPartidosAcumulados(subtotaljugadosa, countjugados2)

			sumaganados = subtotalganados1 + subtotalganados2
			sumaempatados = subtotalempatados1 + subtotalempatados2
			sumaperdidos = subtotalperdidos1 + subtotalperdidos2
			sumatotal = sumaganados+sumaempatados+sumaperdidos

			start =fecha+1
			print("Ganados "+club+" : "+str(sumaganados)+" a la "+str(start))
			print("Empatados: "+str(sumaempatados))
			print("Perdidos: "+str(sumaperdidos))
			print("Jugados local: "+str(subtotaljugados1))
			print("Jugados visitante: "+str(subtotaljugadosa))
			
			cur.execute('''INSERT OR IGNORE INTO Partidos (Equipo, Jornada, PJ_Local, PJ_Visitante, PJ, PG_Local, PG__Visitante, PG, PE_Local, PE_Visitante, PE, PP_Local, PP_Visitante, PP)  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )''',
			 (club, start, subtotaljugados1, subtotaljugadosa, sumatotal, subtotalganados1, subtotalganados2, sumaganados, subtotalempatados1, subtotalempatados2, sumaempatados, subtotalperdidos1, subtotalperdidos2, sumaperdidos))
			conn.commit()			
	
cur.close()