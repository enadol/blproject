from input import jornada
import urllib
import json
import sqlite3

url="../2016-2017/bl.json"
uh=urllib.urlopen(url)
data=uh.read()
js=json.loads(data)
i=0
ganador=None
perdedor=None
puntoslocal=0
puntosvisitante=0
sumavisitante=0
puntos=0
sumalocal=0
equipos=[]

def getEquipos():
	for fecha in range(1,5):
		jornadascompletas=js['rounds'][fecha]['name']
		
		for i in range(0,9):
			equipo=js['rounds'][fecha]['matches'][i]['team1']['name']
			contrario=js['rounds'][fecha]['matches'][i]['team2']['name']
			if equipo not in equipos:
				equipos.append(equipo)
			if contrario not in equipos:
				equipos.append(contrario)
	return equipos



def getPuntos(equipo, afavor, encontra):
	puntos=0
	
	if afavor > encontra:
		puntos=3
	elif afavor==encontra:
		puntos=1
	else:
		puntos=0
	
	return puntos

def getPuntosAcumulados(puntoslocal, puntos):
	puntoslocal=puntoslocal+puntos
	return puntoslocal
	

print "Loading puntos.py..."
# jornadainput=raw_input("Ingrese la jornada: ")
# jornada=int(jornadainput)-1


if jornada <0 or jornada >=34:
	print "No se jugó la jornada "+jornadainput+" en ese torneo. Verifique y vuelva a ingresar."
	jornada=None
else:
	clubes=getEquipos()

	for club in clubes:
		subtotaluno=0
		subtotaldos=0
		subtotala=0
		subtotalb=0
		sumbtotala=0
		sumtotalb=0
		sumapuntos=0
		sumtotallocal=0
		sumtotalvisitante=0

		for fecha in range(0,jornada):
			jornadascompletas=js['rounds'][fecha]['name']
			conn = sqlite3.connect('../tabla16.sqlite')
			cur = conn.cursor()
			conn.text_factory = str
			start = 0
			cur.execute('''CREATE TABLE IF NOT EXISTS Puntos 
			(Equipo TEXT, Jornada INTEGER, Puntos_Local INTEGER, Puntos_Visitante INTEGER, Total_Puntos INTEGER)''')

				
			for i in range(0,9):
				equipo=js['rounds'][fecha]['matches'][i]['team1']['name']
				afavor=js['rounds'][fecha]['matches'][i]['score1']
				contrario=js['rounds'][fecha]['matches'][i]['team2']['name']
				encontra=js['rounds'][fecha]['matches'][i]['score2']

				if equipo==club:
					puntosuno=getPuntos(equipo, afavor, encontra)
				

					subtotaluno=getPuntosAcumulados(subtotaluno, puntosuno)
					
		

				if contrario==club:
					puntosdos=getPuntos(contrario, encontra, afavor)
						
		
					subtotaldos=getPuntosAcumulados(subtotaldos, puntosdos)
					
				sumtotallocal=subtotaluno+subtotaldos
				
				sumapuntos=sumtotallocal+sumtotalvisitante
			print "El equipo "+club+" sumaba "+str(subtotaluno)+" puntos como local a la "+jornadascompletas
			print "El equipo "+club+" sumaba "+str(subtotaldos)+" puntos como visitante a la "+jornadascompletas	
			print "El equipo "+club+" sumaba "+str(sumapuntos)+" puntos en total a la "+jornadascompletas
			cur.execute('''INSERT OR IGNORE INTO Puntos (Equipo, Jornada, Puntos_Local, Puntos_Visitante, Total_Puntos)  VALUES (?, ?, ?, ?, ? )''', (club, fecha+1, subtotaluno, subtotaldos, sumapuntos))
			conn.commit()			
	
uh.close()
