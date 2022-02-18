from PyQt6 import QtCore, QtWidgets
from calendar import Calendar
import sqlite3
from datetime import date, timedelta, datetime
import locale
from os import getlogin, environ
import sys
from ui.mainwindow import Ui_MainWindow

locale.setlocale(locale.LC_ALL, 'deu_deu')

# SQLite DB-Path
sqlitedb = "buchungstool.db"


class Buchungstool(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(Buchungstool, self).__init__()
        self.setupUi(self)

        # Get Screen Geometry
        # res = app.primaryScreen().availableGeometry()
        # if res.width() >= 1920:
        #     self.resize(400, 400)

        self.show()
        self.comboBoxStandort.activated.connect(self.fill_listbox)

        self.start = 1

    
        # Listbox: Die Option exportselection=False führt dazu, dass
        # der gewählte Eintrag immer aktiv bleibt und keine leeren Tupel 
        # ausgegeben werden.
        # self.listbox.config(exportselection=False)

        self.itemsMZ = [("Computerraum","MCR"),
                        ("iPad-Koffer A: EG Neu - Noch nicht buchbar","MTw1"),
                        ("iPad-Koffer B: EG Alt - Noch nicht buchbar","MTw2"),
                        ("iPad-Koffer C: OG - Standort: OL-Büro","MTw3")]

        self.itemsNZ = [("Großer Computerraum N106 (max. 16 SuS = 1 pro PC)","gCR"),
                        ("Kleiner Computerraum N107 (max. 9 SuS = 1 pro PC)","kCR"),
                        ("iPad-Koffer A: TC/BIO - Standort: N002","NTw1"),
                        ("iPad-Koffer B: EG ALT - Standort: Adminbüro","NTw2"),
                        ("iPad-Koffer C: OG ALT - Noch nicht buchbar","NTw3"),
                        ("iPad-Koffer D: 2.OG ALT - Noch nicht buchbar","NTw4"),
                        ("iPad-Koffer E: EG NEU - Standort: N071","NTw5"),
                        ("iPad-Koffer F: OG NEU - Standort: N126","NTw6"),
                        ("Besprechungsraum", "NBespr")]

        # Kürzel aus aus DB holen bzw. Ersteinrichtung anzeigen
         # DB-Verbindung
        verbindung = sqlite3.connect(sqlitedb)
        c = verbindung.cursor()    

        username = getlogin()

        items = list(c.execute(""" SELECT krzl
                                FROM users 
                                WHERE username = ?
                                """,
                                (username,)))
        
        # DB-Verindung schließen
        c.close()
        verbindung.close()
        
        # if items == []:
        #     Ersteinrichtung(self)
        # else:
        #     self.mykrzl = items[0][0]
        self.mykrzl = "LOB"


    def set_cur_year_month(self):
        self.combo_jahr.set(date.today().year)
        self.combo_monat.set(datetime.now().strftime("%B"))

    def fill_listbox(self):
        if self.comboBoxStandort.currentText() == "Merzenich":
            self.tableWidget.setRowCount(len(self.itemsMZ))
            for i in range(len(self.itemsMZ)): 
                self.tableWidget.setItem(
                    i, 0, QtWidgets.QTableWidgetItem(self.itemsMZ[i][0])
                )
        if self.comboBoxStandort.currentText() == "Niederzier":
            self.listbox.delete(0,"end")
            for i in self.itemsNZ: 
                self.listbox.insert("end",i[0])

    def datensatz_anzeigen(self, event):
        """ entnimmt der Listbox den richtigen Tabellennamen und setzt den 
        Buchungsframe bzw. die Elemente aktiv 
        """ 
        if self.start == 1:
            self.start = 0
            self.frame_7.pack(side='top')
            self.frame_9.pack(side='top')
            self.frame_11.pack(side='top')

        self.set_cur_year_month()

        n = self.listbox.curselection()[0]
        if self.combobox_1.get() == "Merzenich":
            # Tabellennamen setzen
            self.tn = self.itemsMZ[n][1]
            # Überschrift setzen
            self.label_top.config(text="Buchungen für: "+self.itemsMZ[n][0])
        if self.combobox_1.get() == "Niederzier":
            # Tabellennamen setzen
            self.tn = self.itemsNZ[n][1]
            # Überschrift setzen
            self.label_top.config(text="Buchungen für: "+self.itemsNZ[n][0])

        self.setMonth(True)

    def setMonth(self, set=None):
        y = int(self.combo_jahr.get())
        self.m = int(self.combo_monat.current()+1)

        cal = Calendar()

        self.weeks = []
        w = 0
        currentweek = 0
        for week in cal.monthdatescalendar(y,self.m):
            z = 1
            oneweek = []
            date_fr = ""
            for date in week:
                if str(date) == datetime.now().strftime("%Y-%m-%d"):
                    currentweek = w
                if z <= 5:
                    oneweek.append(str(date))
                if z == 5:
                    date_fr = str(date)
                z += 1
            # Nur wenn der Freitag der ersten Woche auch noch im ausgewählten  
            # Monat liegt, anhängen an weeks
            # leading zero, führende Null hinzufügen: "%02d" % (self.m,)
            if ("%02d" % (self.m,)) != date_fr.split("-")[1] and w == 0:
                # Wenn ausgefiltert, currentweek um eine Woche erniedrigen
                w -= 1
            else:
                self.weeks.append(oneweek)
            w += 1
        if set==True:
            # Wenn zu Beginn aus datensatz_anzeigen aufgerufen, 
            # aktuelle Woche setzen
            self.weekno = currentweek
            self.weekafter(True)
        elif set=="withlast":
            # bei Button mit der letzten Woche beginnen
            self.weekno = len(self.weeks)
        else:
            # mit anderem Monat aus Auswahl starten
            self.weekno = -1
            self.weekafter()


    def weekbefore(self):
        if self.weekno <= 0:    
            # Wenn am Anfang der Wochenliste angekommen, in vorherigen Monat wechseln
            previousmonth = self.combo_monat.current()
            if previousmonth >= 1:
                monat = date(9999,previousmonth,1).strftime("%B")
                self.combo_monat.set(monat)
            else:
                previousmonth = 12
                monat = date(9999,previousmonth,1).strftime("%B")
                self.combo_monat.set(monat)
                # vorheriges Jahr setzen
                previousyear = int(self.combo_jahr.get())-1
                self.combo_jahr.set(previousyear)
            # Datum des aktuellen Montags speichern
            aktmo = self.label_Mo_date["text"]
            # neuen Monat setzen, dafür withlast übergeben, um am Ende zu
            # beginnen
            self.setMonth("withlast")
            self.weekbefore()
            # wenn der neue Montag in der gleichen Woche liegt, noch eine 
            # Woche vor
            if aktmo == self.label_Mo_date["text"]:
               self.weekbefore()
        else:
            self.resetButtons()
            self.weekno -= 1
            self.label_Woche.config(
                text=self.weeks[self.weekno][0].split("-")[2]+"."+
                     self.weeks[self.weekno][0].split("-")[1]+"."+" bis "+
                     self.weeks[self.weekno][4].split("-")[2]+"."+
                     self.weeks[self.weekno][4].split("-")[1]+".")
            self.label_Mo_date.config(
                text=self.weeks[self.weekno][0].split("-")[2]+"."+
                    self.weeks[self.weekno][0].split("-")[1]+".")
            self.label_Di_date.config(
                text=self.weeks[self.weekno][1].split("-")[2]+"."+
                     self.weeks[self.weekno][1].split("-")[1]+".")
            self.label_Mi_date.config(
                text=self.weeks[self.weekno][2].split("-")[2]+"."+
                    self.weeks[self.weekno][2].split("-")[1]+".")
            self.label_Do_date.config(
                text=self.weeks[self.weekno][3].split("-")[2]+"."+
                     self.weeks[self.weekno][3].split("-")[1]+".")
            self.label_Fr_date.config(
                text=self.weeks[self.weekno][4].split("-")[2]+"."+
                     self.weeks[self.weekno][4].split("-")[1]+".")

            self.set_buchungen()

    def weekafter(self, set=None):
        if self.weekno+1 <= len(self.weeks)-1 or set == True:
            self.resetButtons()
            # wenn zu Beginn aus setmonth aufgerufen, aktuelle Woche benutzen
            if set==True:
                # nichts tun und self.weekno benutzen
                pass
            else:    
                # Button wurde gedrückt, eine Woche weiter
                self.weekno += 1

            self.label_Woche.config(
                text=self.weeks[self.weekno][0].split("-")[2]+"."+
                     self.weeks[self.weekno][0].split("-")[1]+"."+" bis "+
                     self.weeks[self.weekno][4].split("-")[2]+"."+
                     self.weeks[self.weekno][4].split("-")[1]+".")
            self.label_Mo_date.config(
                text=self.weeks[self.weekno][0].split("-")[2]+"."+
                     self.weeks[self.weekno][0].split("-")[1]+".")
            self.label_Di_date.config(
                text=self.weeks[self.weekno][1].split("-")[2]+"."+
                     self.weeks[self.weekno][1].split("-")[1]+".")
            self.label_Mi_date.config(
                text=self.weeks[self.weekno][2].split("-")[2]+"."+
                     self.weeks[self.weekno][2].split("-")[1]+".")
            self.label_Do_date.config(
                text=self.weeks[self.weekno][3].split("-")[2]+"."+
                     self.weeks[self.weekno][3].split("-")[1]+".")
            self.label_Fr_date.config(
                text=self.weeks[self.weekno][4].split("-")[2]+"."+
                     self.weeks[self.weekno][4].split("-")[1]+".")

            self.set_buchungen()
        # Wenn am Ende der Wochenliste angekommen, in nächsten Monat wechseln
        else:
            nextmonth = self.combo_monat.current()+2
            if nextmonth <= 12:
                monat = date(9999,nextmonth,1).strftime("%B")
                self.combo_monat.set(monat)
            else:
                nextmonth = 1
                monat = date(9999,nextmonth,1).strftime("%B")
                self.combo_monat.set(monat)
                # neues Jahr setzen
                nextyear = int(self.combo_jahr.get())+1
                self.combo_jahr.set(nextyear)
            # Datum des aktuellen Montags speichern
            aktmo = self.label_Mo_date["text"]
            # neuen Monat setzen
            self.setMonth()
            # wenn der neue Montag in der gleichen Woche liegt, noch eine 
            # Woche vor
            if aktmo == self.label_Mo_date["text"]:
                self.weekafter()


    def set_buchungen(self):
        """Führt alle set-Methoden aus, indem vorher die Liste aus der db
        geholt wird und den Methoden die Werte übergeben werden 
        """
        
        # DB-Verbindung
        verbindung = sqlite3.connect(sqlitedb)
        c = verbindung.cursor()

        # Liste generieren (wenn es das Datum+Std nicht gibt, gibt sqlite das
        # Datum selbst zurück)
        self.setlist = []
        self.datelistweek = []

        for i in self.weeks[self.weekno]:
            buchungsliste = []
            datelist = []
            datelist.append(i+"_1")
            datelist.append(i+"_2")
            datelist.append(i+"_3")
            datelist.append(i+"_4")
            datelist.append(i+"_5")
            datelist.append(i+"_6")
            datelist.append(i+"_7")

            self.datelistweek.append(datelist)
            
            for d in datelist:

                item = list(c.execute("""SELECT krzl, lgrp 
                                         FROM """+self.tn+"""
                                         WHERE date = ?
                                            """,
                                            (d,)))
                # Wenn item leer, dennoch tuple mit zwei leeren strings einf.
                if item == []:
                    item = [('','')]
                
                buchungsliste.append(item)
            
            self.setlist.append(buchungsliste)
        
        # DB-Verindung schließen
        c.close()
        verbindung.close()
        
        
        # set-Methoden aufrufen
        self.set1_1(True)
        self.set1_2(True)
        self.set1_3(True)
        self.set1_4(True)
        self.set1_5(True)
       
        self.set2_1(True)
        self.set2_2(True)
        self.set2_3(True)
        self.set2_4(True)
        self.set2_5(True)

        self.set3_1(True)
        self.set3_2(True)
        self.set3_3(True)
        self.set3_4(True)
        self.set3_5(True)

        self.set4_1(True)
        self.set4_2(True)
        self.set4_3(True)
        self.set4_4(True)
        self.set4_5(True)

        self.set5_1(True)
        self.set5_2(True)
        self.set5_3(True)
        self.set5_4(True)
        self.set5_5(True)

        self.set6_1(True)
        self.set6_2(True)
        self.set6_3(True)
        self.set6_4(True)
        self.set6_5(True)

        self.set7_1(True)
        self.set7_2(True)
        self.set7_3(True)
        self.set7_4(True)
        self.set7_5(True)


    def set1_1(self, set=None):
        """ Die Set-Methoden werden aufgerufen, um die Buttons
        richtig einzustellen, bzw. bei Drücken der Buttons die
        Eintrags- bzw. Löschen-Dialoge aufzurufen.  
        """

        krzl = self.setlist[0][0][0][0]
        lgrp = self.setlist[0][0][0][1]
        # Wenn aus set-Methode aufgerufen:
        if set == True:
            # Wenn krzl leer ist, nichts einfüllen, leerer Datensatz
            if krzl == '':
                pass
            # Wenn krzl nicht leer, dann in blau einfügen
            else:
                # Farbe blau setzen
                color = '#a8cdd9'
                # Wenn eigenes Kürzel, dann Farbe grün nutzen
                if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                    # Farbe grün setzen
                    color = '#7dd288'
                self.button1_1.config(background=color, text=krzl+"\n"+lgrp)
        # Wenn von Button aufgerufen:
        if set == None:
            # Dialog aufrufen 
            # wenn krzl == eigenes Kürzel, dann datelistweek an 
            # Dialog "Löschen"/"Behalten" übergeben
            buchungsdatum = self.datelistweek[0][0]
            if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                Loeschen(buchungsdatum,self)
            # wenn anderes Kürzel, aber nicht leer: nichts tun
            elif krzl != "":
                pass
            # sonst: krzl und datelistweek[0][0] übergeben für Neueingabe über
            # Objekt Eintrag
            else: 
                Eintrag(self.mykrzl,buchungsdatum,self)

    def set1_2(self, set=None):
        krzl = self.setlist[1][0][0][0]
        lgrp = self.setlist[1][0][0][1]
        if set == True:
            if krzl == '':
                pass
            else:
                color = '#a8cdd9'
                if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                    color = '#7dd288'
                self.button1_2.config(background=color, text=krzl+"\n"+lgrp)      
        if set == None:
            buchungsdatum = self.datelistweek[1][0]
            if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                Loeschen(buchungsdatum,self)
            elif krzl != "":
                pass
            else:
                Eintrag(self.mykrzl,buchungsdatum,self)
                
      
    def set1_3(self, set=None):
        krzl = self.setlist[2][0][0][0]
        lgrp = self.setlist[2][0][0][1]
        if set == True:
            if krzl == '':
                pass
            else:
                color = '#a8cdd9'
                if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                    color = '#7dd288'
                self.button1_3.config(background=color, text=krzl+"\n"+lgrp)      
        if set == None:
            buchungsdatum = self.datelistweek[2][0]
            if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                Loeschen(buchungsdatum,self)
            elif krzl != "":
                pass
            else:
                Eintrag(self.mykrzl,buchungsdatum,self)
                

    def set1_4(self, set=None):
        krzl = self.setlist[3][0][0][0]
        lgrp = self.setlist[3][0][0][1]
        if set == True:
            if krzl == '':
                pass
            else:
                color = '#a8cdd9'
                if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                    color = '#7dd288'
                self.button1_4.config(background=color, text=krzl+"\n"+lgrp)      
        if set == None:
            buchungsdatum = self.datelistweek[3][0]
            if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                Loeschen(buchungsdatum,self)
            elif krzl != "":
                pass
            else:
                Eintrag(self.mykrzl,buchungsdatum,self)
                

    def set1_5(self, set=None):
        krzl = self.setlist[4][0][0][0]
        lgrp = self.setlist[4][0][0][1]
        if set == True:
            if krzl == '':
                pass
            else:
                color = '#a8cdd9'
                if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                    color = '#7dd288'
                self.button1_5.config(background=color, text=krzl+"\n"+lgrp)      
        if set == None:
            buchungsdatum = self.datelistweek[4][0]
            if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                Loeschen(buchungsdatum,self)
            elif krzl != "":
                pass
            else:
                Eintrag(self.mykrzl,buchungsdatum,self)
                

    def set2_1(self, set=None):
        krzl = self.setlist[0][1][0][0]
        lgrp = self.setlist[0][1][0][1]
        if set == True:
            if krzl == '':
                pass
            else:
                color = '#a8cdd9'
                if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                    color = '#7dd288'
                self.button2_1.config(background=color, text=krzl+"\n"+lgrp)      
        if set == None:
            buchungsdatum = self.datelistweek[0][1]
            if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                Loeschen(buchungsdatum,self)
            elif krzl != "":
                pass
            else:
                Eintrag(self.mykrzl,buchungsdatum,self)
                

    def set2_2(self, set=None):
        krzl = self.setlist[1][1][0][0]
        lgrp = self.setlist[1][1][0][1]
        if set == True:
            if krzl == '':
                pass
            else:
                color = '#a8cdd9'
                if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                    color = '#7dd288'
                self.button2_2.config(background=color, text=krzl+"\n"+lgrp)      
        if set == None:
            buchungsdatum = self.datelistweek[1][1]
            if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                Loeschen(buchungsdatum,self)
            elif krzl != "":
                pass
            else:
                Eintrag(self.mykrzl,buchungsdatum,self)
                

    def set2_3(self, set=None):
        krzl = self.setlist[2][1][0][0]
        lgrp = self.setlist[2][1][0][1]
        if set == True:
            if krzl == '':
                pass
            else:
                color = '#a8cdd9'
                if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                    color = '#7dd288'
                self.button2_3.config(background=color, text=krzl+"\n"+lgrp)      
        if set == None:
            buchungsdatum = self.datelistweek[2][1]
            if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                Loeschen(buchungsdatum,self)
            elif krzl != "":
                pass
            else:
                Eintrag(self.mykrzl,buchungsdatum,self)
                

    def set2_4(self, set=None):
        krzl = self.setlist[3][1][0][0]
        lgrp = self.setlist[3][1][0][1]
        if set == True:
            if krzl == '':
                pass
            else:
                color = '#a8cdd9'
                if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                    color = '#7dd288'
                self.button2_4.config(background=color, text=krzl+"\n"+lgrp)      
        if set == None:
            buchungsdatum = self.datelistweek[3][1]
            if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                Loeschen(buchungsdatum,self)
            elif krzl != "":
                pass
            else:
                Eintrag(self.mykrzl,buchungsdatum,self)
                

    def set2_5(self, set=None):
        krzl = self.setlist[4][1][0][0]
        lgrp = self.setlist[4][1][0][1]
        if set == True:
            if krzl == '':
                pass
            else:
                color = '#a8cdd9'
                if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                    color = '#7dd288'
                self.button2_5.config(background=color, text=krzl+"\n"+lgrp)      
        if set == None:
            buchungsdatum = self.datelistweek[4][1]
            if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                Loeschen(buchungsdatum,self)
            elif krzl != "":
                pass
            else:
                Eintrag(self.mykrzl,buchungsdatum,self)
                

    def set3_1(self, set=None):
        krzl = self.setlist[0][2][0][0]
        lgrp = self.setlist[0][2][0][1]
        if set == True:
            if krzl == '':
                pass
            else:
                color = '#a8cdd9'
                if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                    color = '#7dd288'
                self.button3_1.config(background=color, text=krzl+"\n"+lgrp)      
        if set == None:
            buchungsdatum = self.datelistweek[0][2]
            if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                Loeschen(buchungsdatum,self)
            elif krzl != "":
                pass
            else:
                Eintrag(self.mykrzl,buchungsdatum,self)
                

    def set3_2(self, set=None):
        krzl = self.setlist[1][2][0][0]
        lgrp = self.setlist[1][2][0][1]
        if set == True:
            if krzl == '':
                pass
            else:
                color = '#a8cdd9'
                if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                    color = '#7dd288'
                self.button3_2.config(background=color, text=krzl+"\n"+lgrp)      
        if set == None:
            buchungsdatum = self.datelistweek[1][2]
            if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                Loeschen(buchungsdatum,self)
            elif krzl != "":
                pass
            else:
                Eintrag(self.mykrzl,buchungsdatum,self)
                

    def set3_3(self, set=None):
        krzl = self.setlist[2][2][0][0]
        lgrp = self.setlist[2][2][0][1]
        if set == True:
            if krzl == '':
                pass
            else:
                color = '#a8cdd9'
                if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                    color = '#7dd288'
                self.button3_3.config(background=color, text=krzl+"\n"+lgrp)      
        if set == None:
            buchungsdatum = self.datelistweek[2][2]
            if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                Loeschen(buchungsdatum,self)
            elif krzl != "":
                pass
            else:
                Eintrag(self.mykrzl,buchungsdatum,self)
                

    def set3_4(self, set=None):
        krzl = self.setlist[3][2][0][0]
        lgrp = self.setlist[3][2][0][1]
        if set == True:
            if krzl == '':
                pass
            else:
                color = '#a8cdd9'
                if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                    color = '#7dd288'
                self.button3_4.config(background=color, text=krzl+"\n"+lgrp)      
        if set == None:
            buchungsdatum = self.datelistweek[3][2]
            if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                Loeschen(buchungsdatum,self)
            elif krzl != "":
                pass
            else:
                Eintrag(self.mykrzl,buchungsdatum,self)
                

    def set3_5(self, set=None):
        krzl = self.setlist[4][2][0][0]
        lgrp = self.setlist[4][2][0][1]
        if set == True:
            if krzl == '':
                pass
            else:
                color = '#a8cdd9'
                if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                    color = '#7dd288'
                self.button3_5.config(background=color, text=krzl+"\n"+lgrp)      
        if set == None:
            buchungsdatum = self.datelistweek[4][2]
            if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                Loeschen(buchungsdatum,self)
            elif krzl != "":
                pass
            else:
                Eintrag(self.mykrzl,buchungsdatum,self)
                

    def set4_1(self, set=None):
        krzl = self.setlist[0][3][0][0]
        lgrp = self.setlist[0][3][0][1]
        if set == True:
            if krzl == '':
                pass
            else:
                color = '#a8cdd9'
                if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                    color = '#7dd288'
                self.button4_1.config(background=color, text=krzl+"\n"+lgrp)      
        if set == None:
            buchungsdatum = self.datelistweek[0][3]
            if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                Loeschen(buchungsdatum,self)
            elif krzl != "":
                pass
            else:
                Eintrag(self.mykrzl,buchungsdatum,self)
                

    def set4_2(self, set=None):
        krzl = self.setlist[1][3][0][0]
        lgrp = self.setlist[1][3][0][1]
        if set == True:
            if krzl == '':
                pass
            else:
                color = '#a8cdd9'
                if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                    color = '#7dd288'
                self.button4_2.config(background=color, text=krzl+"\n"+lgrp)      
        if set == None:
            buchungsdatum = self.datelistweek[1][3]
            if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                Loeschen(buchungsdatum,self)
            elif krzl != "":
                pass
            else:
                Eintrag(self.mykrzl,buchungsdatum,self)
                

    def set4_3(self, set=None):
        krzl = self.setlist[2][3][0][0]
        lgrp = self.setlist[2][3][0][1]
        if set == True:
            if krzl == '':
                pass
            else:
                color = '#a8cdd9'
                if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                    color = '#7dd288'
                self.button4_3.config(background=color, text=krzl+"\n"+lgrp)      
        if set == None:
            buchungsdatum = self.datelistweek[2][3]
            if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                Loeschen(buchungsdatum,self)
            elif krzl != "":
                pass
            else:
                Eintrag(self.mykrzl,buchungsdatum,self)
                

    def set4_4(self, set=None):
        krzl = self.setlist[3][3][0][0]
        lgrp = self.setlist[3][3][0][1]
        if set == True:
            if krzl == '':
                pass
            else:
                color = '#a8cdd9'
                if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                    color = '#7dd288'
                self.button4_4.config(background=color, text=krzl+"\n"+lgrp)      
        if set == None:
            buchungsdatum = self.datelistweek[3][3]
            if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                Loeschen(buchungsdatum,self)
            elif krzl != "":
                pass
            else:
                Eintrag(self.mykrzl,buchungsdatum,self)
                

    def set4_5(self, set=None):
        krzl = self.setlist[4][3][0][0]
        lgrp = self.setlist[4][3][0][1]
        if set == True:
            if krzl == '':
                pass
            else:
                color = '#a8cdd9'
                if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                    color = '#7dd288'
                self.button4_5.config(background=color, text=krzl+"\n"+lgrp)      
        if set == None:
            buchungsdatum = self.datelistweek[4][3]
            if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                Loeschen(buchungsdatum,self)
            elif krzl != "":
                pass
            else:
                Eintrag(self.mykrzl,buchungsdatum,self)
                

    def set5_1(self, set=None):
        krzl = self.setlist[0][4][0][0]
        lgrp = self.setlist[0][4][0][1]
        if set == True:
            if krzl == '':
                pass
            else:
                color = '#a8cdd9'
                if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                    color = '#7dd288'
                self.button5_1.config(background=color, text=krzl+"\n"+lgrp)      
        if set == None:
            buchungsdatum = self.datelistweek[0][4]
            if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                Loeschen(buchungsdatum,self)
            elif krzl != "":
                pass
            else:
                Eintrag(self.mykrzl,buchungsdatum,self)
                

    def set5_2(self, set=None):
        krzl = self.setlist[1][4][0][0]
        lgrp = self.setlist[1][4][0][1]
        if set == True:
            if krzl == '':
                pass
            else:
                color = '#a8cdd9'
                if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                    color = '#7dd288'
                self.button5_2.config(background=color, text=krzl+"\n"+lgrp)      
        if set == None:
            buchungsdatum = self.datelistweek[1][4]
            if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                Loeschen(buchungsdatum,self)
            elif krzl != "":
                pass
            else:
                Eintrag(self.mykrzl,buchungsdatum,self)
                

    def set5_3(self, set=None):
        krzl = self.setlist[2][4][0][0]
        lgrp = self.setlist[2][4][0][1]
        if set == True:
            if krzl == '':
                pass
            else:
                color = '#a8cdd9'
                if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                    color = '#7dd288'
                self.button5_3.config(background=color, text=krzl+"\n"+lgrp)      
        if set == None:
            buchungsdatum = self.datelistweek[2][4]
            if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                Loeschen(buchungsdatum,self)
            elif krzl != "":
                pass
            else:
                Eintrag(self.mykrzl,buchungsdatum,self)
                

    def set5_4(self, set=None):
        krzl = self.setlist[3][4][0][0]
        lgrp = self.setlist[3][4][0][1]
        if set == True:
            if krzl == '':
                pass
            else:
                color = '#a8cdd9'
                if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                    color = '#7dd288'
                self.button5_4.config(background=color, text=krzl+"\n"+lgrp)      
        if set == None:
            buchungsdatum = self.datelistweek[3][4]
            if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                Loeschen(buchungsdatum,self)
            elif krzl != "":
                pass
            else:
                Eintrag(self.mykrzl,buchungsdatum,self)
                

    def set5_5(self, set=None):
        krzl = self.setlist[4][4][0][0]
        lgrp = self.setlist[4][4][0][1]
        if set == True:
            if krzl == '':
                pass
            else:
                color = '#a8cdd9'
                if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                    color = '#7dd288'
                self.button5_5.config(background=color, text=krzl+"\n"+lgrp)      
        if set == None:
            buchungsdatum = self.datelistweek[4][4]
            if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                Loeschen(buchungsdatum,self)
            elif krzl != "":
                pass
            else:
                Eintrag(self.mykrzl,buchungsdatum,self)
                

    def set6_1(self, set=None):
        krzl = self.setlist[0][5][0][0]
        lgrp = self.setlist[0][5][0][1]
        if set == True:
            if krzl == '':
                pass
            else:
                color = '#a8cdd9'
                if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                    color = '#7dd288'
                self.button6_1.config(background=color, text=krzl+"\n"+lgrp)      
        if set == None:
            buchungsdatum = self.datelistweek[0][5]
            if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                Loeschen(buchungsdatum,self)
            elif krzl != "":
                pass
            else:
                Eintrag(self.mykrzl,buchungsdatum,self)
                

    def set6_2(self, set=None):
        krzl = self.setlist[1][5][0][0]
        lgrp = self.setlist[1][5][0][1]
        if set == True:
            if krzl == '':
                pass
            else:
                color = '#a8cdd9'
                if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                    color = '#7dd288'
                self.button6_2.config(background=color, text=krzl+"\n"+lgrp)      
        if set == None:
            buchungsdatum = self.datelistweek[1][5]
            if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                Loeschen(buchungsdatum,self)
            elif krzl != "":
                pass
            else:
                Eintrag(self.mykrzl,buchungsdatum,self)
                

    def set6_3(self, set=None):
        krzl = self.setlist[2][5][0][0]
        lgrp = self.setlist[2][5][0][1]
        if set == True:
            if krzl == '':
                pass
            else:
                color = '#a8cdd9'
                if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                    color = '#7dd288'
                self.button6_3.config(background=color, text=krzl+"\n"+lgrp)      
        if set == None:
            buchungsdatum = self.datelistweek[2][5]
            if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                Loeschen(buchungsdatum,self)
            elif krzl != "":
                pass
            else:
                Eintrag(self.mykrzl,buchungsdatum,self)
                

    def set6_4(self, set=None):
        krzl = self.setlist[3][5][0][0]
        lgrp = self.setlist[3][5][0][1]
        if set == True:
            if krzl == '':
                pass
            else:
                color = '#a8cdd9'
                if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                    color = '#7dd288'
                self.button6_4.config(background=color, text=krzl+"\n"+lgrp)      
        if set == None:
            buchungsdatum = self.datelistweek[3][5]
            if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                Loeschen(buchungsdatum,self)
            elif krzl != "":
                pass
            else:
                Eintrag(self.mykrzl,buchungsdatum,self)
                

    def set6_5(self, set=None):
        krzl = self.setlist[4][5][0][0]
        lgrp = self.setlist[4][5][0][1]
        if set == True:
            if krzl == '':
                pass
            else:
                color = '#a8cdd9'
                if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                    color = '#7dd288'
                self.button6_5.config(background=color, text=krzl+"\n"+lgrp)      
        if set == None:
            buchungsdatum = self.datelistweek[4][5]
            if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                Loeschen(buchungsdatum,self)
            elif krzl != "":
                pass
            else:
                Eintrag(self.mykrzl,buchungsdatum,self)
                

    def set7_1(self, set=None):
        krzl = self.setlist[0][6][0][0]
        lgrp = self.setlist[0][6][0][1]
        if set == True:
            if krzl == '':
                pass
            else:
                color = '#a8cdd9'
                if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                    color = '#7dd288'
                self.button7_1.config(background=color, text=krzl+"\n"+lgrp)      
        if set == None:
            buchungsdatum = self.datelistweek[0][6]
            if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                Loeschen(buchungsdatum,self)
            elif krzl != "":
                pass
            else:
                Eintrag(self.mykrzl,buchungsdatum,self)
                

    def set7_2(self, set=None):
        krzl = self.setlist[1][6][0][0]
        lgrp = self.setlist[1][6][0][1]
        if set == True:
            if krzl == '':
                pass
            else:
                color = '#a8cdd9'
                if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                    color = '#7dd288'
                self.button7_2.config(background=color, text=krzl+"\n"+lgrp)      
        if set == None:
            buchungsdatum = self.datelistweek[1][6]
            if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                Loeschen(buchungsdatum,self)
            elif krzl != "":
                pass
            else:
                Eintrag(self.mykrzl,buchungsdatum,self)
                

    def set7_3(self, set=None):
        krzl = self.setlist[2][6][0][0]
        lgrp = self.setlist[2][6][0][1]
        if set == True:
            if krzl == '':
                pass
            else:
                color = '#a8cdd9'
                if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                    color = '#7dd288'
                self.button7_3.config(background=color, text=krzl+"\n"+lgrp)      
        if set == None:
            buchungsdatum = self.datelistweek[2][6]
            if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                Loeschen(buchungsdatum,self)
            elif krzl != "":
                pass
            else:
                Eintrag(self.mykrzl,buchungsdatum,self)
                

    def set7_4(self, set=None):
        krzl = self.setlist[3][6][0][0]
        lgrp = self.setlist[3][6][0][1]
        if set == True:
            if krzl == '':
                pass
            else:
                color = '#a8cdd9'
                if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                    color = '#7dd288'
                self.button7_4.config(background=color, text=krzl+"\n"+lgrp)      
        if set == None:
            buchungsdatum = self.datelistweek[3][6]
            if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                Loeschen(buchungsdatum,self)
            elif krzl != "":
                pass
            else:
                Eintrag(self.mykrzl,buchungsdatum,self)
                

    def set7_5(self, set=None):
        krzl = self.setlist[4][6][0][0]
        lgrp = self.setlist[4][6][0][1]
        if set == True:
            if krzl == '':
                pass
            else:
                color = '#a8cdd9'
                if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                    color = '#7dd288'
                self.button7_5.config(background=color, text=krzl+"\n"+lgrp)      
        if set == None:
            buchungsdatum = self.datelistweek[4][6]
            if krzl == self.mykrzl or (krzl != "" and param == "adm"):
                Loeschen(buchungsdatum,self)
            elif krzl != "":
                pass
            else:
                Eintrag(self.mykrzl,buchungsdatum,self)
                


    def resetButtons(self):
        self.button1_1.config(background='#c0c0c0', text='')
        self.button1_2.config(background='#c0c0c0', text='')
        self.button1_3.config(background='#c0c0c0', text='')
        self.button1_4.config(background='#c0c0c0', text='')
        self.button1_5.config(background='#c0c0c0', text='')
        
        self.button2_1.config(background='#c0c0c0', text='')
        self.button2_2.config(background='#c0c0c0', text='')
        self.button2_3.config(background='#c0c0c0', text='')
        self.button2_4.config(background='#c0c0c0', text='')
        self.button2_5.config(background='#c0c0c0', text='')
        
        self.button3_1.config(background='#c0c0c0', text='')
        self.button3_2.config(background='#c0c0c0', text='')
        self.button3_3.config(background='#c0c0c0', text='')
        self.button3_4.config(background='#c0c0c0', text='')
        self.button3_5.config(background='#c0c0c0', text='')
        
        self.button4_1.config(background='#c0c0c0', text='')
        self.button4_2.config(background='#c0c0c0', text='')
        self.button4_3.config(background='#c0c0c0', text='')
        self.button4_4.config(background='#c0c0c0', text='')
        self.button4_5.config(background='#c0c0c0', text='')
        
        self.button5_1.config(background='#c0c0c0', text='')
        self.button5_2.config(background='#c0c0c0', text='')
        self.button5_3.config(background='#c0c0c0', text='')
        self.button5_4.config(background='#c0c0c0', text='')
        self.button5_5.config(background='#c0c0c0', text='')
        
        self.button6_1.config(background='#c0c0c0', text='')
        self.button6_2.config(background='#c0c0c0', text='')
        self.button6_3.config(background='#c0c0c0', text='')
        self.button6_4.config(background='#c0c0c0', text='')
        self.button6_5.config(background='#c0c0c0', text='')
        
        self.button7_1.config(background='#c0c0c0', text='')
        self.button7_2.config(background='#c0c0c0', text='')
        self.button7_3.config(background='#c0c0c0', text='')
        self.button7_4.config(background='#c0c0c0', text='')
        self.button7_5.config(background='#c0c0c0', text='')

    def run(self):
        self.mainwindow.mainloop()


class Eintrag:
    def __init__(self, mykrzl, d, app):
        self.k = mykrzl
        self.d = d
        self.app = app

        # build ui
        eintrag = tk.Toplevel()
        frame1 = ttk.Frame(eintrag)
        heading = ttk.Label(frame1)
        heading.config(font='{Segoe UI} 12 {bold}', text='Buchung eintragen')
        heading.pack(pady='10', side='top')
        self.subheading = ttk.Label(frame1)
        self.subheading.config(font='{Segoe UI} 10 {italic}', justify='center', 
                               text='Datum, Stunde', wraplength='200')
        self.subheading.pack(side='top')

        if param == "adm":
            frameadm = ttk.Frame(frame1)
            Label_adm = ttk.Label(frameadm)
            Label_adm.config(font='{Segoe UI} 9 {bold}', text='Kürzel: ')
            Label_adm.pack(side='left')
            self.admEntry = ttk.Entry(frameadm)
            self.admEntry.config(font='TkDefaultFont', validate='none')
            self.admEntry.pack(side='left')
            frameadm.config(height='200', width='200')
            frameadm.pack(pady='10', side='top')

        frame2 = ttk.Frame(frame1)
        Label_lgrp = ttk.Label(frame2)
        Label_lgrp.config(font='{Segoe UI} 9 {bold}', text='Lerngruppe: ')
        Label_lgrp.pack(side='left')
        self.lgrpEntry = ttk.Entry(frame2)
        self.lgrpEntry.config(font='TkDefaultFont', validate='none')
        self.lgrpEntry.pack(side='left')
        frame2.config(height='200', width='200')
        frame2.pack(pady='10', side='top')
        frame_3 = ttk.Frame(frame1)
        label_1 = ttk.Label(frame_3)
        label_1.config(text='Wöchentlich wiederholen bis zum:')
        label_1.pack(side='top')
        self.combobox_repeat = ttk.Combobox(frame_3)
        self.combobox_repeat.config(state='readonly')
        self.combobox_repeat.pack(side='top')
        frame_3.config(height='200', width='200')
        frame_3.pack(pady='10', side='top')
        frame3 = ttk.Frame(frame1)
        self.buttonOK = ttk.Button(frame3)
        self.buttonOK.config(text='OK')
        self.buttonOK.pack(padx='10', side='left')
        self.buttonOK.configure(command=self.ok)
        self.buttonAbbrechen = ttk.Button(frame3)
        self.buttonAbbrechen.config(text='Abbrechen')
        self.buttonAbbrechen.pack(padx='10', side='left')
        self.buttonAbbrechen.configure(command=self.abbrechen)
        frame3.config(height='200', width='200')
        frame3.pack(pady='10', side='top')
        frame1.config(height='200', width='200')
        frame1.pack(expand='true', side='top')
        eintrag.config(height='230', width='280')
        if param == "adm":
            eintrag.geometry('280x280')
            eintrag.title('Eintrag ADM')
        else:
            eintrag.geometry('280x230')
            eintrag.title('Eintrag')

        # Label für Datum und Stunde anpassen
        self.datum_std = self.d.split("_")
        datum = self.datum_std[0].split("-")
        day = datum[2]
        month = datum[1]
        year = datum[0]
        self.subheading.config(text=day+"."+month+"., "+
                               self.datum_std[1]+". Std.")

        # Daten in die Wiederholungs-Combobox einfüllen
        thedate = date(int(year), int(month.lstrip("0")), int(day.lstrip("0")))
        self.longlist = []
        i = 1
        while i <= 24:
            thedate = thedate + timedelta(days=7)
            self.longlist.append(thedate.strftime("%d.%m.%Y"))
            i += 1
        
        self.combobox_repeat.config(values=self.longlist)


        # Main widget
        self.mainwindow = eintrag

        # Fenster positionieren
        # Gets the requested values of the height and widht.
        windowWidth = self.mainwindow.winfo_reqwidth()
        windowHeight = self.mainwindow.winfo_reqheight()
        # Gets both half the screen width/height and window width/height
        positionRight = int(self.mainwindow.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(self.mainwindow.winfo_screenheight()/2 - windowHeight/2-15)
        # Positions the window in the center of the page.
        self.mainwindow.geometry("+{}+{}".format(positionRight, positionDown))

        # Grab window + focus
        self.mainwindow.grab_set()
        self.mainwindow.focus_set() 

        # mainloop
        self.mainwindow.mainloop()

    def ok(self):
        """ Stellt eine DB-Verbindung her, prüft, ob sich um eine Serie
        handelt und schreibt in die DB
        """
        if param == "adm":
            self.k = self.admEntry.get()

        # DB-Verbindung
        verbindung = sqlite3.connect(sqlitedb)
        c = verbindung.cursor()

        # Immer, mit und ohne Combobox-Auswahl, ersten Datensatz schreiben
        # Prüfen, ob das Datum bereits existiert, sonst Meldung    
        existiert = list(c.execute(""" SELECT EXISTS (SELECT * from """+self.app.tn+"""
                                       WHERE date = ?);
                                   """,
                                   (self.d,)))
        if existiert[0][0] == 1:
            messagebox.showerror("Buchung nicht möglich!", 
                "Der gewünschte Termin wurde in der Zwischenzeit gebucht.")

        else:
            c.execute("""INSERT INTO """+self.app.tn+""" ("date","krzl","lgrp") 
                        VALUES (?,?,?);      
                    """,
                    (self.d,self.k,self.lgrpEntry.get()))
            verbindung.commit()

            # Wenn Combobox genutzt, index benutzen, um longlist bis hier abzufragen
            # Prüfen, ob alle Daten buchbar sind, sonst Warnung
            if self.combobox_repeat.current() != -1:
                besetzt = []
                for i in range(self.combobox_repeat.current() + 1):
                    repeatdate = self.longlist[i].split(".")
                    repeatdate = (repeatdate[2]+"-"+repeatdate[1]+"-"+
                                  repeatdate[0]+"_"+self.datum_std[1])
                    seriendatum_exisitert = list(c.execute(""" 
                                    SELECT EXISTS (SELECT * from """+self.app.tn+"""
                                       WHERE date = ?);
                                    """,
                                    (repeatdate,)))
                    if seriendatum_exisitert[0][0] == 1:
                        besetzt.append(self.longlist[i])
                           
                if besetzt == []:
                    for i in range(self.combobox_repeat.current() + 1):
                        repeatdate = self.longlist[i].split(".")
                        repeatdate = (repeatdate[2]+"-"+repeatdate[1]+
                                     "-"+repeatdate[0]+"_"+self.datum_std[1])
                        c.execute("""INSERT INTO """+self.app.tn+""" 
                                     ("date","krzl","lgrp") 
                                     VALUES (?,?,?);      
                                  """,
                                  (repeatdate,self.k,self.lgrpEntry.get()))
                        verbindung.commit()
                else:
                    besetztstring = ", ".join(besetzt)
                    messagebox.showerror("Buchung nicht möglich!", 
                        "Die Buchung der Serie ist nicht möglich, "+
                        "da folgende Termine bereits gebucht sind:\n"+
                        besetztstring)
                    # ersten Termin wieder löschen (TODO: Das könnte man 
                    # geschickter machen)
                    c.execute("""DELETE FROM """+self.app.tn+""" 
                                 WHERE date = ? 
                              """,
                              (self.d,))
                    verbindung.commit()

        # DB-Verindung schließen
        c.close()
        verbindung.close()

        # Änderungen laden
        self.app.resetButtons()
        self.app.set_buchungen()

        self.mainwindow.destroy()

    def abbrechen(self):
        # In der Zwischenzeit könnte sich etwas geändert haben:
        self.app.resetButtons()
        self.app.set_buchungen()
        self.mainwindow.destroy()


class Loeschen:
    def __init__(self, d, app):
        self.d = d
        self.app = app

        # build ui
        buchungloeschen = tk.Toplevel()
        frame_1 = ttk.Frame(buchungloeschen)
        label_1 = ttk.Label(frame_1)
        label_1.config(font='{Segoe UI} 12 {bold}', text='Eigene Buchung löschen')
        label_1.pack(pady='15', side='top')
        label_2 = ttk.Label(frame_1)
        label_2.config(text='Was soll mit der Buchung vom ')
        label_2.pack(side='top')
        self.label_datum = ttk.Label(frame_1)
        self.label_datum.config(font='{Segoe UI} 9 {bold}', text='24.12., 3. Std.')
        self.label_datum.pack(side='top')
        label_4 = ttk.Label(frame_1)
        label_4.config(text='geschehen?')
        label_4.pack(side='top')
        frame_2 = ttk.Frame(frame_1)
        self.button_loeschen = ttk.Button(frame_2)
        self.button_loeschen.config(text='LÖSCHEN', width='15')
        self.button_loeschen.pack(padx='10', side='left')
        self.button_loeschen.configure(command=self.loeschen)
        self.button_beibehalten = ttk.Button(frame_2)
        self.button_beibehalten.config(text='BEIBEHALTEN', width='15')
        self.button_beibehalten.pack(padx='10', side='top')
        self.button_beibehalten.configure(command=self.beibehalten)
        frame_2.config(height='200', width='200')
        frame_2.pack(pady='15', side='top')
        frame_1.config(height='200', width='200')
        frame_1.pack(expand='true', side='top')
        buchungloeschen.config(height='180', width='300')
        buchungloeschen.geometry('300x180')
        buchungloeschen.resizable(False, False)
        buchungloeschen.title('Löschen')

        # Label für Datum und Stunde anpassen
        self.datum_std = self.d.split("_")
        datum = self.datum_std[0].split("-")
        day = datum[2]
        month = datum[1]
        self.label_datum.config(text=day+"."+month+"., "+
                               self.datum_std[1]+". Std.")        

        # Main widget
        self.mainwindow = buchungloeschen

        # Fenster positionieren
        # Gets the requested values of the height and widht.
        windowWidth = self.mainwindow.winfo_reqwidth()
        windowHeight = self.mainwindow.winfo_reqheight()
        # Gets both half the screen width/height and window width/height
        positionRight = int(self.mainwindow.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(self.mainwindow.winfo_screenheight()/2 - windowHeight/2-15)
        # Positions the window in the center of the page.
        self.mainwindow.geometry("+{}+{}".format(positionRight, positionDown))

        # Grab window + focus
        self.mainwindow.grab_set()
        self.mainwindow.focus_set()

        # Mainloop
        self.mainwindow.mainloop()


    def loeschen(self):
        # DB-Verbindung
        verbindung = sqlite3.connect(sqlitedb)
        c = verbindung.cursor()    

        # Datensatz des betreffenden Datums aus der DB löschen
        c.execute("""DELETE FROM """+self.app.tn+""" 
                     WHERE date = ? 
                """,
                (self.d,))
        verbindung.commit()

        # DB-Verindung schließen
        c.close()
        verbindung.close()

        # Änderungen laden
        self.app.resetButtons()
        self.app.set_buchungen()

        self.mainwindow.destroy()

    def beibehalten(self):
        # In der Zwischenzeit könnte sich etwas geändert haben:
        self.app.resetButtons()
        self.app.set_buchungen()
        self.mainwindow.destroy()

class Ersteinrichtung:
    def __init__(self, app):

        self.app = app

        # build ui
        ersteinrichtung = tk.Toplevel()
        frame1 = ttk.Frame(ersteinrichtung)
        heading = ttk.Label(frame1)
        heading.config(font='{Segoe UI} 12 {bold}', text='Ersteinrichtung')
        heading.pack(pady='10', side='top')
        subheading = ttk.Label(frame1)
        subheading.config(justify='center', text='Zur Ersteinrichtung des Buchungstools brauchen wir dein Lehrerkürzel.', wraplength='210')
        subheading.pack(side='top')
        frame2 = ttk.Frame(frame1)
        Label_krz = ttk.Label(frame2)
        Label_krz.config(font='{Segoe UI} 9 {bold}', text='Kürzel: ')
        Label_krz.pack(side='left')
        self.krzEntry = ttk.Entry(frame2)
        self.krzEntry.config(font='TkDefaultFont', validate='none')
        self.krzEntry.pack(side='left')
        frame2.config(height='200', width='200')
        frame2.pack(pady='10', side='top')
        frame3 = ttk.Frame(frame1)
        self.buttonOK = ttk.Button(frame3)
        self.buttonOK.config(text='OK')
        self.buttonOK.pack(padx='10', side='left')
        self.buttonOK.configure(command=self.ok)
        self.buttonAbbrechen = ttk.Button(frame3)
        self.buttonAbbrechen.config(text='Abbrechen')
        self.buttonAbbrechen.pack(padx='10', side='left')
        self.buttonAbbrechen.configure(command=self.abbrechen)
        frame3.config(height='200', width='200')
        frame3.pack(pady='10', side='top')
        frame1.config(height='200', width='200')
        frame1.pack(expand='true', side='top')
        ersteinrichtung.config(height='180', width='280')
        ersteinrichtung.geometry('280x180')
        ersteinrichtung.title('pyKursbuch')

        # Main widget
        self.mainwindow = ersteinrichtung

        # Fenster positionieren
        # Gets the requested values of the height and widht.
        windowWidth = self.mainwindow.winfo_reqwidth()
        windowHeight = self.mainwindow.winfo_reqheight()
        # Gets both half the screen width/height and window width/height
        positionRight = int(self.mainwindow.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(self.mainwindow.winfo_screenheight()/2 - windowHeight/2-15)
        # Positions the window in the center of the page.
        self.mainwindow.geometry("+{}+{}".format(positionRight, positionDown))

        # Grab window + focus
        self.mainwindow.grab_set()
        self.mainwindow.focus_set() 

        # Window Deletion abfangen und schließen
        def on_closing():
            self.abbrechen()

        self.mainwindow.protocol("WM_DELETE_WINDOW", on_closing)

        # mainloop
        self.mainwindow.mainloop()

    def ok(self):
        mykrzl = self.krzEntry.get().upper()
        if mykrzl == "":
            messagebox.showerror("Kein Kürzel","Bitte ein Kürzel eingeben.")
        elif len(mykrzl) != 3:
            messagebox.showerror("Falsches Kürzel","Bitte ein Kürzel mit drei Buchstaben eingeben.")
        else:
                        
            # DB-Verbindung
            verbindung = sqlite3.connect(sqlitedb)
            c = verbindung.cursor()    

            username = getlogin()

            c.execute(""" INSERT INTO users (username, krzl)
                        VALUES (?,?)
                        """,
                        (username, mykrzl))
            verbindung.commit()

            # DB-Verindung schließen
            c.close()
            verbindung.close()        
            self.app.mykrzl = mykrzl
            self.mainwindow.destroy()

    def abbrechen(self):
        self.mainwindow.destroy()
        self.app.mainwindow.destroy()


if __name__ == '__main__':
    try:
        param = sys.argv[1:][0]
    except:
        param = 0
    import sys
    # Scale Factor Rounding Policy
    # default is PassThrough in Qt6 (Round in Qt 5)
    environ['QT_SCALE_FACTOR_ROUNDING_POLICY'] = 'Round'
    app = QtWidgets.QApplication(sys.argv)

    # if "en_" in locale.getlocale()[0]:
    #     translator = QtCore.QTranslator()
    #     translator.load("Resources/mainwindow_en.qm")
    #     app.installTranslator(translator)

    app.setStyle("Fusion")
    ui = Buchungstool()
    sys.exit(app.exec())