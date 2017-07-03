#Dieses Programm ordnet die Pixel eines P2-Bildes/P3-Bildes so an, dass es mit unserem
#Bildmanipulationsprogramm kompatibel ist. Die Pixel einer Zeile müssen dafür nämlich
#in einer Zeile des Codes stehen. Andere Programme können solche Bilder auch öffnen, wenn
#die Pixel untereinander aufgelistet sind.
from tkinter import filedialog
filename=filedialog.askopenfilename()
a=open(filename,'r')
alles=a.readlines()
a.close()
kopf=alles[0:4]
groesse=kopf[2].split()
breite=int(groesse[0])
j=0
f=''
liste = []
y = ''
for k in kopf:
    y+=k
    
for i in alles[4:]:
    hintereinander = i.strip()
    hintereinander = i.split()
    liste+=hintereinander

if kopf[0][0:2] == 'P2':
    for i in range(len(liste)):
        f += liste[i] + ' '
        j+=1
        if j==breite:
            f+='\n'
            j=0
elif kopf[0][0:2]=='P3':
    for i in range(len(liste)):
        f += liste[i] + ' '
        j+=1
        if j==breite*3:
            f+='\n'
            j=0
r=open(filename,'w')
r.write(y + f)
r.close()

