from input import jornada as howmany
import sqlite3

conn = sqlite3.connect('../tabla18.sqlite')
cur = conn.cursor()
equipos=["Hertha BSC", "Werder Bremen", "Schalke 04", "VfB Stuttgart", "Eintracht Frankfurt",
"FC Augsburg", "1. FC Nuernberg", "VfL Wolfsburg", "SC Freiburg", "Bayer 04 Leverkusen",
"1899 Hoffenheim", "FC Bayern Muenchen", "Fortuna Duesseldorf", "RB Leipzig", "Hannover 96",
"Borussia Dortmund", "Borussia M'gladbach", "1. FSV Mainz 05"]
id=1


print("Creating JSON output on tablaevolution18.json...")

# howmany = int(raw_input("Cuantas jornadas? "))

##cur = conn.cursor()

fhand = open('../json/tablaevolution18.json','w')
fhand.write('[')

for equipo in equipos:
    fhand.write('{\n"name":"'+equipo+'",\n"region": "bundesliga", \n"puntos": [')
    cur.execute('''SELECT Partidos.Equipo, Partidos.Jornada, Puntos.Total_Puntos AS Puntos
    FROM Partidos JOIN Puntos WHERE Partidos.Equipo = Puntos.Equipo AND Puntos.Equipo="'''+equipo+'''" AND Partidos.Jornada=Puntos.Jornada
     AND Partidos.Jornada<='''+str(howmany))

   
    nodes = list()

    count = 0
    for row in cur :
        nodes.append(row)
    #print nodes
        
    for row in nodes :
                
        fhand.write('['+str(row[1])+','+str(row[2])+']')
        if count < len(nodes)-1 : fhand.write(',')
        count=count+1

    fhand.write('],\n "ganados": [')
#ganados
    #for equipo in equipos:
        
    cur.execute('''SELECT Equipo, Jornada, PG AS Ganados
    FROM Partidos WHERE Equipo="'''+equipo+'''" AND Jornada<='''+str(howmany))

    nodesganados=list()

    countganados=0
    for row in cur:
        nodesganados.append(row)


    for row in nodesganados:
        fhand.write('['+str(row[1])+','+str(row[2])+']')
        if countganados < len(nodesganados)-1 : fhand.write(',')
        countganados=countganados+1

#empatados

    fhand.write('],\n "empatados": [')
    cur.execute('''SELECT Equipo, Jornada, PE AS Empatados
    FROM Partidos WHERE Equipo="'''+equipo+'''" AND Jornada<='''+str(howmany))

    nodesempatados=list()

    countempatados=0
    for row in cur:
        nodesempatados.append(row)


    for row in nodesempatados:
        fhand.write('['+str(row[1])+','+str(row[2])+']')
        if countempatados < len(nodesempatados)-1 : fhand.write(',')
        countempatados=countempatados+1

#perdidos
    fhand.write('],\n "perdidos": [')
    cur.execute('''SELECT Equipo, Jornada, PP AS Perdidos
    FROM Partidos WHERE Equipo="'''+equipo+'''" AND Jornada<='''+str(howmany))

    nodesperdidos=list()

    countperdidos=0
    for row in cur:
        nodesperdidos.append(row)


    for row in nodesperdidos:
        fhand.write('['+str(row[1])+','+str(row[2])+']')
        if countperdidos < len(nodesperdidos)-1 : fhand.write(',')
        countperdidos=countperdidos+1
    
    #fhand.write(']},\n')

#goles a favor
    fhand.write('],\n "gf": [')
    cur.execute('''SELECT Equipo, Jornada, Goles_a_favor AS gf
    FROM Goles WHERE Equipo="'''+equipo+'''" AND Jornada<='''+str(howmany))

    nodesgf=list()

    countgf=0
    for row in cur:
        nodesgf.append(row)


    for row in nodesgf:
        fhand.write('['+str(row[1])+','+str(row[2])+']')
        if countgf < len(nodesgf)-1 : fhand.write(',')
        countgf=countgf+1


#goles en contra
    fhand.write('],\n "gc": [')
    cur.execute('''SELECT Equipo, Jornada, Goles_en_contra AS gc
    FROM Goles WHERE Equipo="'''+equipo+'''" AND Jornada<='''+str(howmany))

    nodesgc=list()

    countgc=0
    for row in cur:
        nodesgc.append(row)


    for row in nodesgc:
        fhand.write('['+str(row[1])+','+str(row[2])+']')
        if countgc < len(nodesgc)-1 : fhand.write(',')
        countgc=countgc+1


#diferencia
    fhand.write('],\n "dif": [')
    cur.execute('''SELECT Equipo, Jornada, Diferencia AS dif
    FROM Goles WHERE Equipo="'''+equipo+'''" AND Jornada<='''+str(howmany))

    nodesdif=list()

    countdif=0
    for row in cur:
        nodesdif.append(row)


    for row in nodesdif:
        
        fhand.write('['+str(row[1])+','+str(row[2])+']')
        if countdif < len(nodesdif)-1 : fhand.write(',')
        countdif=countdif+1


    
    fhand.write(']}')
    if id < 18:
        fhand.write(',\n')
    id+=1

fhand.write(']')
fhand.close()


cur.close()

print("NO OLVIDAR PARA BLVISUAL.HTML CAMBIAR EQUIPO POR NAME Y PUNTOS POR SIZE")
