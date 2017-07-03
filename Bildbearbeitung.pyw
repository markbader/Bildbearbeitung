from tkinter import Tk, Menu, Canvas, filedialog, PhotoImage, messagebox

class Ipaint:
    def __init__(self):
        self.main = Tk()
        self.main.geometry(str(self.main.winfo_screenwidth()//2)+'x'+str(self.main.winfo_screenheight()//2))
        self.menu = Menu(self.main)       #erstellt eine Instanz der Klasse Menu
        self.file_menu=Menu(self.menu,tearoff=0)      #erstellt ein Untermenue
        self.file_menu.add_command(label='Öffnen...',command=self.oeffnen)
        self.file_menu.add_separator()#erstellt ein Trennstrich im Menü
        self.file_menu.add_command(label='Speichern unter...', command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Schließen', command=self.main.destroy)
        self.menu.add_cascade(label='Datei', menu=self.file_menu)#ein neuer Menuereiter
        self.edit_menu=Menu(self.menu,tearoff=0)
        self.edit_menu.add_command(label='x-Achse', command=self.spiegelx)
        self.edit_menu.add_command(label='y-Achse', command=self.spiegely)
        self.edit_menu.add_command(label='Punktspiegelung',command=self.punktspiegeln)
        self.menu.add_cascade(label='Spiegeln', menu=self.edit_menu)
        self.text_menu=Menu(self.menu,tearoff=0)
        self.text_menu.add_command(label='Invertieren', command=self.invertieren)
        self.text_menu.add_command(label='Rotfilter', command=self.rotstich)
        self.text_menu.add_command(label='Grünfilter', command=self.gruenstich)
        self.text_menu.add_command(label='Blaufilter', command=self.blaustich)
        self.menu.add_cascade(label='Farben', menu=self.text_menu)
        self.text_menu=Menu(self.menu,tearoff=0)
        self.filter_menu=Menu(self.menu,tearoff=0)
        self.filter_menu.add_command(label='Kantenfilter',command=self.kantenfinder)
        self.menu.add_cascade(label='Filter',menu=self.filter_menu)
        self.text_menu.add_command(label='90° links',command=self.drehe90_links)
        self.text_menu.add_command(label='90° rechts',command=self.drehe90_rechts)
        self.menu.add_cascade(label='Drehen', menu=self.text_menu)
        self.main.config(menu=self.menu)
        self.main.update()
        self.main.title('Ipaint')
        self.canv=Canvas(self.main, width=1000, height=700, bg='white')
        self.canv.pack(fill='both')
        einliste         = []
        self.kopf        = []
        groesse          = 0
        self.breite      = 0
        self.hoehe       = 0
        self.farbtiefe   = 0
        self.punktliste  = []
        self.main.resizable(width=False, height=False)

    def oeffnen(self): #Oeffnet ein Menuefenster, wo man eine Datei auswaehlen kann, die geoeffnet werden soll
        datei_suchen=filedialog.askopenfilename(filetypes=[('Alle Bilder',('*.pbm','*.pgm','*.ppm')),\
                                                           ('Pixelbild','*.pbm'),('Graustufenbild','*.pgm'),\
                                                           ('Farbbild','*ppm')])
        self.lesen(datei_suchen)
        photo=self.binaer()
        self.img = PhotoImage(data=photo)
        self.canv.create_image(self.breite//2, self.hoehe//2, image=self.img)
        self.canv.config(width=self.breite, height=self.hoehe)
        self.main.geometry(str(self.breite) + 'x' + str(self.hoehe))
        self.main.update()

    def aktualisieren(self):#Zerstoert das Canv und baut es neu auf, damit es nach Aenderung neu gezeigt wird
        self.canv.delete('all')
        photo=self.binaer()
        self.img = PhotoImage(data=photo)
        self.canv.create_image(self.breite//2, self.hoehe//2, image=self.img)
        self.canv.config(width=self.breite, height=self.hoehe)
        self.main.geometry(str(self.breite) + 'x' + str(self.hoehe))
        self.main.update()

    def binaer(self):#Wandelt P2/P3- Bilder ins P5/P6 Format um, damit die Bilder angezeigt werden koennen
        if self.typ =='P2':
            text=''
            for i in self.punktliste:
                for j in i:
                    text+= chr(j)
            return 'P5\n#P5 Bild\n'+str(self.breite)+' '+str(self.hoehe)+'\n'+str(self.farbtiefe)+'\n'+text
        elif self.typ =='P3':
            text=''
            for i in self.punktliste:
                for j in i:
                    text+= chr(int(j[0]))+chr(int(j[1]))+chr(int(j[2]))   
            return 'P6\n#P6 Bild\n'+str(self.breite)+' '+str(self.hoehe)+'\n'+str(self.farbtiefe)+'\n'+text
            
    
    def new(self):
        self.canv.delete('all')
        self.canv.configure(width=self.main.winfo_screenwidth()//2, height=self.main.winfo_screenheight()//2)       

    def kantenfinder(self):
        if self.typ=='P2':
            neue_punktliste=[]
            neue_punktliste.append(self.punktliste[0])
            for i in range(1,len(self.punktliste)-1):
                zeile=[]
                zeile.append(self.punktliste[i][0])
                for j in range(1,len(self.punktliste[i])-1):
                    x=(self.punktliste[i-1][j-1])*(-2)+(self.punktliste[i-1][j+1])*(-2)+(self.punktliste[i+1][j-1])*2+self.punktliste[i+1][j+1]*2
                    if x<0:x=0
                    if x>self.farbtiefe:x=self.farbtiefe
                    zeile.append(x)
                zeile.append(self.punktliste[i][-1])
                neue_punktliste.append(zeile)
            neue_punktliste.append(self.punktliste[-1])
            self.punktliste=neue_punktliste
        if self.typ=='P3':
            neue_punktliste=[]
            neue_punktliste.append(self.punktliste[0])
            for i in range(1,len(self.punktliste)-1):
                zeile=[]
                zeile.append(self.punktliste[i][0])
                for j in range(1,len(self.punktliste[i])-1):
                    x=(int(self.punktliste[i-1][j-1][0])+int(self.punktliste[i-1][j-1][1])+int(self.punktliste[i-1][j-1][2]))*(-1)+(int(self.punktliste[i-1][j+1][0])+int(self.punktliste[i-1][j+1][1])+int(self.punktliste[i-1][j+1][2]))+(int(self.punktliste[i][j-1][0])+int(self.punktliste[i][j-1][1])+int(self.punktliste[i][j-1][2]))*(-1)+int(self.punktliste[i][j+1][0])+int(self.punktliste[i][j+1][1])+int(self.punktliste[i][j+1][2])+(int(self.punktliste[i+1][j-1][0])+int(self.punktliste[i+1][j-1][1])+int(self.punktliste[i+1][j-1][2]))*(-1)+int(self.punktliste[i+1][j+1][0])+int(self.punktliste[i+1][j+1][1])+int(self.punktliste[i+1][j+1][2])
                    if x<0:x=0
                    if x>self.farbtiefe:x=self.farbtiefe
                    zeile.append([x,x,x])
                zeile.append(self.punktliste[i][-1])
                neue_punktliste.append(zeile)
            neue_punktliste.append(self.punktliste[-1])
            self.punktliste=neue_punktliste
        self.aktualisieren()

    def lesen (self,datei): #liest eine Datei aus
        """
        Vor.: Der Bearbeiter ist initialisiert, datei ist der Name
              einer pgm-Datei im aktuellen Verzeichnis
              der Dateikopf besteht aus den vier Zeilen
              Kennung, Kommentar, Groesse, Farbtiefe
              dann kommen die Pixelinformationen
        Erg.: Die Daten der Datei sind in den entsprechenden Attributen
              aufgehoben.
              Dabei ist self.punktliste eine Liste aus self.hoehe Elementen,
              jedes Element ist eine Liste aus self.breite Integer-Werten,
              die fuer die Grauwerte der Pixel stehen.
        """
        f = open(datei,"r")    
        einliste = f.readlines() #die Rohdaten
        f.close()
        self.kopf        = einliste[0:4]
        self.typ = self.kopf[0][0:2]
        groesse          = self.kopf[2].split()
        self.breite      = int(groesse[0])
        self.hoehe       = int(groesse[1])
        self.farbtiefe   = int(einliste[3])
        self.punktliste  = []
        zeile =[]
        if self.typ == 'P2':
            for i in einliste[4:]:
                textzeile = i.strip()
                textzeile = i.split()
                for punkt in textzeile:
                    zeile.append(int(punkt))
            for i in range(self.hoehe):
                    anf  = self.breite*i
                    ende = self.breite+anf
                    self.punktliste.append(zeile[anf:ende])
        elif self.typ == 'P3':
            for i in einliste[4:]:
                textzeile = i.strip()
                textzeile = i.split()
                for i in range(0,self.breite*3,3):
                    zeile.append(textzeile[i:i+3])
            for i in range(self.hoehe):
                    anf  = self.breite*i
                    ende = self.breite+anf
                    self.punktliste.append(zeile[anf:ende])
        else:
            print('Ein Fehler ist aufgetreten!')
        

    def spiegelx (self):#Spiegelt das Bild an der x-Achse
            neue_punktliste = []
            for i in self.punktliste:
                neue_punktliste.insert(0,i)
            self.punktliste = neue_punktliste
            self.aktualisieren()
            
            

    def spiegely (self):#spiegelt das Bild an der y-Achse
            neue_punktliste = []
            for i in range(self.hoehe):
                zeile=[]
                for j in range(self.breite,0,-1):
                    zeile.append(self.punktliste[i][j-1])
                neue_punktliste.append(zeile)
            self.punktliste = neue_punktliste
            self.aktualisieren()
            

    def invertieren(self):#Erstellt ein Negativ-Bild -> dreht alle Farbwerte um
        if self.typ == 'P2':
            neue_punktliste = []
            for i in self.punktliste:
                zeile=[]
                for j in i:
                    j = self.farbtiefe-j
                    zeile.append(j) 
                neue_punktliste.append(zeile)
            self.punktliste = neue_punktliste
            self.aktualisieren()
        elif self.typ == 'P3':
            neue_punktliste = []
            for i in self.punktliste:
                zeile=[]
                for j in i:
                    j[0] = self.farbtiefe-int(j[0])
                    j[1] = self.farbtiefe-int(j[1])
                    j[2] = self.farbtiefe-int(j[2])
                    zeile.append([j[0],j[1],j[2]])
                neue_punktliste.append(zeile)
            self.punktliste = neue_punktliste
            self.aktualisieren()

    def rotstich(self): #Gibt dem Bild einen Rotstich
        if self.typ == 'P3':
            neue_punktliste = []
            for i in self.punktliste:
                zeile=[]
                for j in i:
                    j[0] = j[0]
                    j[1] = 0
                    j[2] = 0
                    zeile.append([j[0],j[1],j[2]])
                neue_punktliste.append(zeile)
            self.punktliste = neue_punktliste
            self.aktualisieren()
        else:
            messagebox.showinfo('Error', 'Diese Funktion ist nur mit Farbbildern kompatibel!')

    def gruenstich(self): #Gibt dem Bild einen Gruenstich
        if self.typ == 'P3':
            neue_punktliste = []
            for i in self.punktliste:
                zeile=[]
                for j in i:
                    j[0] = 0
                    j[1] = j[1]
                    j[2] = 0
                    zeile.append([j[0],j[1],j[2]])
                neue_punktliste.append(zeile)
            self.punktliste = neue_punktliste
            self.aktualisieren()
        else:
            messagebox.showinfo('Error', 'Diese Funktion ist nur mit Farbbildern kompatibel!')

    def blaustich(self): #Gibt dem Bild einen Blaustich
        if self.typ == 'P3':
            neue_punktliste = []
            for i in self.punktliste:
                zeile=[]
                for j in i:
                    j[0] = 0
                    j[1] = 0
                    j[2] = j[2]
                    zeile.append([j[0],j[1],j[2]])
                neue_punktliste.append(zeile)
            self.punktliste = neue_punktliste
            self.aktualisieren()
        else:
            messagebox.showinfo('Error', 'Diese Funktion ist nur mit Farbbildern kompatibel!')
    
    
    def drehen(self):#dreht das Bild
        neue_punktliste=[]
        for i in range(self.breite):
            neue_punktliste.append([])
        for i in range(self.hoehe):
            for j in range(self.breite):
                neue_punktliste[j].insert(0,self.punktliste[i][j])
        self.punktliste=neue_punktliste
        self.breite=self.hoehe
        self.hoehe=len(self.punktliste)
        self.kopf[2]=str(self.breite)+' '+str(self.hoehe)+'\n'

    def drehe90_rechts(self):#dreht das Bild um 90° nach rechts
        self.drehen()
        self.aktualisieren()

    def drehe90_links(self):#dreht das Bild um 90° nach links
        for i in range(3):
            self.drehen()
        self.aktualisieren()
        

    def punktspiegeln(self):#Spiegelt das Bild (0|0)
        neue_punktliste=[]
        for i in self.punktliste:
            neue_punktliste.insert(0,i)
        neue_punktliste2=[]
        for i in range(self.hoehe):
            zeile=[]
            for j in range(self.breite,0,-1):
                zeile.append(neue_punktliste[i][j-1])
            neue_punktliste2.append(zeile)
        self.punktliste=neue_punktliste2
        self.aktualisieren()

    def save_as_file(self):     #der Benutzer kann durch ein Dialogfenster die einen Ort und einen Namen
                            #auswählen und dann den Inhalt des Textfeldes unter dem Namen an dem Ort speichern
        ordner_suchen=filedialog.asksaveasfilename(title='Speichern unter...', \
                                               filetypes=[('Graustufenbild', '*.pgm'),('Buntbild','*.ppm')\
                                                          ,('Alle Datein','*.*')])
        zeichenanzahl=len(ordner_suchen)
        endung_pruefen=str(ordner_suchen[zeichenanzahl-4:])
        if endung_pruefen in ['.pgm','.ppm']:      #prueft ob der Benutzer bereits ein Endung eingegeben hat
            datei_schreiben=open(ordner_suchen, 'w') #schreibt die Datei ohne eine Endung anzuhängen
            text= ''
            for o in self.kopf:
                text+= o
            if self.typ=='P2':
                for p in self.punktliste:
                    for q in p:
                        text+= str(q)+' '
                    text+= '\n'
            elif self.typ=='P3':
                for p in self.punktliste:
                    for q in p:
                        text+= str(q[0])+' '+str(q[1])+' ' + str(q[2])+' '
                    text+='\n'
            else:
                print("Ein Fehler ist aufgetreten")
            datei_schreiben.write(text)
            datei_schreiben.close()
        else:
            print('Ein schwerwiegender Fehler ist aufgetreten. Sie haben möglicherweise einen Virus.')
     
if __name__=="__main__":
    fenster = Ipaint() #erstellt eine neue Instanz fenster der Klasse Ipaint
    fenster.main.mainloop()
        

    
        
