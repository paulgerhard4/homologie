'''Es sollen Abschnitte von Finanzzeitreihen durch TDA analysiert werden und 
damit Merkmale wiedererkannt werden koennen'''

import yfinance as yf
import matplotlib.pyplot as plt
import funct as f 
import time
import simp as s

data = yf.download('AAPL', period = '1wk', interval = '1m', prepost = True)
print('Es gibt ' + str(len(data)) + ' Zeitpunkte')
#plottet die zeitreihe
data_time = range(0, len(data))
plt.plot(data_time, data['Open'], linewidth=1)
plt.figure()

datenwolke = []
vector_x = [0]
vector_y = [0]
for x in range(0, len(data)-28):
	data_intervall = data[1+x:28+x] #ist in etwa eine stunde

	#hier sollten jetzt zuvor definierte funktionen die parameter fuer
	#den vektor zurueckgeben
	x = f.rturn(data_intervall)
	y = f.var(data_intervall)
	vector_x.append(x)
	vector_y.append(y)

datenwolke.append(vector_x)
datenwolke.append(vector_y)

#print(datenwolke)

#jetzt sollte die TDA losgehen
plt.scatter(vector_x, vector_y, s=5)
plt.xlabel('Rendite')
plt.ylabel('Risiko (Varianz)')
plt.figure()

for y in range(0, 10):
	for x in range(0+(y*10), 100+(y*10)):
		plt.scatter(vector_x[-1-x], vector_y[-1-x], c='red', 
		edgecolors='none', s=100)
	
	plt.figure()

rote_liste = []
for x in range(0, 100):
	rot = {}
	point = []
	point.append(vector_x[-1-x])
	point.append(vector_y[-1-x])
	rot['number'] = x
	rot['point'] = point
	rote_liste.append(rot)

	plt.scatter(vector_x[-1-x], vector_y[-1-x], c='red', 
		edgecolors='none', s=50)

#print(rote_liste)

#time.sleep(5)

#plt.close()

#jetzt beginnnt die erstellung des simplizialen Komplex
simpkomp = s.Simplizialer_Komplex()

#berechnung der Abstaende

r_1 = input('Wie gros soll die Filtrierung sein? r = ')
r = float(r_1)
for ecke_1 in rote_liste:
	simpkomp.add([ecke_1['number']])

for ecke_1 in rote_liste:
	for ecke_2 in rote_liste:
		if s.dist(ecke_1['point'],ecke_2['point']) < r:
			simpkomp.add([ecke_1['number'], ecke_2['number']])

for ecke_1 in rote_liste:
	for ecke_2 in rote_liste:
		for ecke_3 in rote_liste:
			if s.dist(ecke_1['point'],ecke_2['point']) < r and s.dist(ecke_2['point'],ecke_3['point']) < r and s.dist(ecke_1['point'],ecke_3['point']) < r:
				simpkomp.add([ecke_1['number'], ecke_2['number'], ecke_3['number']])

print(simpkomp.simplices)

plt.show()

