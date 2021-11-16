import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from calendar import Calendar
import sqlite3
from datetime import date, timedelta, datetime
import locale
#import subprocess
from os import getlogin
import sys

locale.setlocale(locale.LC_ALL, 'deu_deu')

# SQLite DB-Path
sqlitedb = "buchungstool.db"

class BuchungstoolApp:
    def __init__(self):
        # build ui
        root = tk.Tk()
        frame_1 = ttk.Frame(root)
        panedwindow_2 = ttk.Panedwindow(frame_1, orient='horizontal')
        frame_4 = ttk.Frame(panedwindow_2)
        labelframe_1 = ttk.Labelframe(frame_4)
        self.combobox_1 = ttk.Combobox(labelframe_1)
        self.combobox_1.config(state='readonly', values='"Merzenich" "Niederzier"')
        self.combobox_1.pack(fill='x', side='top')
        self.combobox_1.bind('<<ComboboxSelected>>', self.fill_listbox, add='')
        labelframe_1.config(height='100', padding='5', text='Standort')
        labelframe_1.pack(fill='x', side='top')
        space1 = ttk.Frame(frame_4)
        space1.config(height='8', width='200')
        space1.pack(side='top')
        labelframe_2 = ttk.Labelframe(frame_4)
        self.listbox = tk.Listbox(labelframe_2)
        self.listbox.pack(expand='true', fill='both', side='top')
        self.listbox.bind('<<ListboxSelect>>', self.datensatz_anzeigen, add='')
        labelframe_2.config(height='200', padding='5', text='Räume und Geräte', width='200')
        labelframe_2.pack(expand='true', fill='both', side='top')
        frame_4.pack(expand='true', fill='both', side='top')
        panedwindow_2.add(frame_4, weight='7')
        labelframe_3 = ttk.Labelframe(panedwindow_2)
        frame_6 = ttk.Frame(labelframe_3)
        self.label_top = ttk.Label(frame_6)
        self.label_top.config(font='{Segoe UI} 12 {bold}', padding='20', text='← Bitte zunächst Standort und Raum bzw. Geräte auswählen.')
        self.label_top.pack(side='top')
        frame_7 = ttk.Frame(frame_6)
        label_Jahr = ttk.Label(frame_7)
        label_Jahr.config(text='Jahr: ')
        label_Jahr.pack(side='left')
        self.combo_jahr = ttk.Combobox(frame_7)
        self.combo_jahr.config(state='readonly', values='"2020" "2021" "2022" "2023"', width='5')
        self.combo_jahr.pack(side='left')
        frame_8 = ttk.Frame(frame_7)
        frame_8.config(height='20', width='20')
        frame_8.pack(side='left')
        label_Monat = ttk.Label(frame_7)
        label_Monat.config(text='Monat: ')
        label_Monat.pack(side='left')
        self.combo_monat = ttk.Combobox(frame_7)
        self.combo_monat.config(state='readonly', width='12')
        self.combo_monat.pack(side='left')
        frame_8_1 = ttk.Frame(frame_7)
        frame_8_1.config(height='20', width='20')
        frame_8_1.pack(side='left')
        self.button_month = ttk.Button(frame_7)
        self.button_month.config(text='OK', width='5')
        self.button_month.pack(side='top')
        self.button_month.configure(command=self.setMonth)
        frame_7.config(height='200', padding='10', width='200')
        frame_7.pack(side='top')
        frame_6.config(height='200', width='200')
        frame_6.pack(side='top')
        frame_9 = ttk.Frame(labelframe_3)
        button_weekbefore = tk.Button(frame_9)
        button_weekbefore.config(font='{Segoe UI Black} 16 {}', padx='5', relief='flat', text='◄')
        button_weekbefore.pack(padx='5', pady='5', side='left')
        button_weekbefore.configure(command=self.weekbefore)
        self.label_Woche = ttk.Label(frame_9)
        self.label_Woche.config(anchor='center', font='{Segoe UI} 10 {bold}', text='----', width='25')
        self.label_Woche.pack(padx='5', side='left')
        button_weekafter = tk.Button(frame_9)
        button_weekafter.config(font='{Segoe UI} 16 {}', padx='5', relief='flat', text='►')
        button_weekafter.pack(ipadx='2', padx='5', pady='5', side='left')
        button_weekafter.configure(command=self.weekafter)
        frame_9.config(height='80', width='500')
        frame_9.pack(side='top')
        frame_11 = ttk.Frame(labelframe_3)
        frame_1_2 = ttk.Frame(frame_11)
        label_Std = ttk.Label(frame_1_2)
        label_Std.config(text='Std.')
        label_Std.grid(padx='20', row='0')
        label_Std.rowconfigure('0', minsize='0', pad='0', uniform='None', weight='0')
        label_Std.columnconfigure('0', minsize='0')
        label_Mo = ttk.Label(frame_1_2)
        label_Mo.config(justify='center', text='Mo')
        label_Mo.grid(column='1', padx='5', row='0', sticky='n')
        label_Mo.rowconfigure('0', minsize='0', pad='0', uniform='None', weight='0')
        label_Mo.columnconfigure('1', minsize='0', pad='0')
        label_Mo.columnconfigure('5', minsize='50')
        self.label_Mo_date = ttk.Label(frame_1_2)
        self.label_Mo_date.config(anchor='center', justify='center', text='--', width='5')
        self.label_Mo_date.grid(column='1', padx='5', row='0', sticky='s')
        label_Di = ttk.Label(frame_1_2)
        label_Di.config(justify='center', text='Di', wraplength='40')
        label_Di.grid(column='2', padx='5', row='0', sticky='n')
        label_Di.rowconfigure('0', minsize='0', pad='0', uniform='None', weight='0')
        label_Di.columnconfigure('2', minsize='0')
        self.label_Di_date = ttk.Label(frame_1_2)
        self.label_Di_date.config(anchor='center', justify='center', text='--', width='5')
        self.label_Di_date.grid(column='2', row='0', sticky='s')
        label_Mi = ttk.Label(frame_1_2)
        label_Mi.config(justify='center', text='Mi')
        label_Mi.grid(column='3', padx='5', row='0', sticky='n')
        label_Mi.rowconfigure('0', minsize='0', pad='0', uniform='None', weight='0')
        label_Mi.columnconfigure('3', minsize='0')
        self.label_Mi_date = ttk.Label(frame_1_2)
        self.label_Mi_date.config(anchor='center', justify='center', text='--', width='5')
        self.label_Mi_date.grid(column='3', row='0', sticky='s')
        label_Do = ttk.Label(frame_1_2)
        label_Do.config(justify='center', text='Do', wraplength='40')
        label_Do.grid(column='4', padx='5', row='0', sticky='n')
        label_Do.rowconfigure('0', minsize='0', pad='0', uniform='None', weight='0')
        label_Do.columnconfigure('4', minsize='0')
        self.label_Do_date = ttk.Label(frame_1_2)
        self.label_Do_date.config(anchor='center', justify='center', text='--', width='5')
        self.label_Do_date.grid(column='4', row='0', sticky='s')
        label_Fr = ttk.Label(frame_1_2)
        label_Fr.config(justify='center', text='Fr\n')
        label_Fr.grid(column='5', padx='5', row='0', sticky='n')
        label_Fr.rowconfigure('0', minsize='0', pad='0', uniform='None', weight='0')
        label_Fr.columnconfigure('4', minsize='0')
        self.label_Fr_date = ttk.Label(frame_1_2)
        self.label_Fr_date.config(anchor='center', justify='center', text='--', width='5')
        self.label_Fr_date.grid(column='5', row='0', sticky='s')
        label_1Std = ttk.Label(frame_1_2)
        label_1Std.config(text='1')
        label_1Std.grid(column='0', pady='5', row='1')
        label_1Std.rowconfigure('1', pad='0')
        label_1Std.columnconfigure('0', minsize='0')
        self.button1_1 = tk.Button(frame_1_2)
        self.button1_1.config(background='#c0c0c0', height='2', justify='center', relief='flat')
        self.button1_1.config(width='14')
        self.button1_1.grid(column='1', padx='5', pady='5', row='1')
        self.button1_1.rowconfigure('1', pad='0')
        self.button1_1.columnconfigure('1', minsize='0', pad='0')
        self.button1_1.columnconfigure('5', minsize='50')
        self.button1_1.configure(command=self.set1_1)
        self.button1_2 = tk.Button(frame_1_2)
        self.button1_2.config(background='#c0c0c0', height='2', justify='center', relief='flat')
        self.button1_2.config(width='14')
        self.button1_2.grid(column='2', padx='5', row='1')
        self.button1_2.rowconfigure('1', pad='0')
        self.button1_2.columnconfigure('2', minsize='0')
        self.button1_2.configure(command=self.set1_2)
        self.button1_3 = tk.Button(frame_1_2)
        self.button1_3.config(background='#c0c0c0', height='2', justify='center', relief='flat')
        self.button1_3.config(width='14')
        self.button1_3.grid(column='3', padx='5', row='1')
        self.button1_3.rowconfigure('1', pad='0')
        self.button1_3.columnconfigure('3', minsize='0')
        self.button1_3.configure(command=self.set1_3)
        self.button1_4 = tk.Button(frame_1_2)
        self.button1_4.config(background='#c0c0c0', height='2', justify='center', relief='flat')
        self.button1_4.config(width='14')
        self.button1_4.grid(column='4', padx='5', row='1')
        self.button1_4.rowconfigure('1', pad='0')
        self.button1_4.columnconfigure('4', minsize='0')
        self.button1_4.configure(command=self.set1_4)
        self.button1_5 = tk.Button(frame_1_2)
        self.button1_5.config(background='#c0c0c0', height='2', justify='center', relief='flat')
        self.button1_5.config(width='14')
        self.button1_5.grid(column='5', padx='5', row='1')
        self.button1_5.rowconfigure('1', pad='0')
        self.button1_5.columnconfigure('5', minsize='0', pad='0', uniform='None', weight='0')
        self.button1_5.configure(command=self.set1_5)
        label_2Std = ttk.Label(frame_1_2)
        label_2Std.config(text='2')
        label_2Std.grid(column='0', row='2')
        label_2Std.rowconfigure('1', pad='10')
        label_2Std.rowconfigure('2', pad='0')
        label_2Std.columnconfigure('0', minsize='0')
        self.button2_1 = tk.Button(frame_1_2)
        self.button2_1.config(background='#c0c0c0', height='2', justify='center', relief='flat')
        self.button2_1.config(width='14')
        self.button2_1.grid(column='1', pady='5', row='2')
        self.button2_1.rowconfigure('1', pad='10')
        self.button2_1.rowconfigure('2', pad='0')
        self.button2_1.columnconfigure('1', minsize='0', pad='0')
        self.button2_1.columnconfigure('5', minsize='50')
        self.button2_1.configure(command=self.set2_1)
        self.button2_2 = tk.Button(frame_1_2)
        self.button2_2.config(background='#c0c0c0', height='2', justify='center', relief='flat')
        self.button2_2.config(width='14')
        self.button2_2.grid(column='2', pady='5', row='2')
        self.button2_2.rowconfigure('1', pad='10')
        self.button2_2.rowconfigure('2', pad='0')
        self.button2_2.columnconfigure('1', minsize='0', pad='0')
        self.button2_2.columnconfigure('5', minsize='50')
        self.button2_2.configure(command=self.set2_2)
        self.button2_3 = tk.Button(frame_1_2)
        self.button2_3.config(background='#c0c0c0', height='2', justify='center', relief='flat')
        self.button2_3.config(width='14')
        self.button2_3.grid(column='3', pady='5', row='2')
        self.button2_3.rowconfigure('1', pad='10')
        self.button2_3.rowconfigure('2', pad='0')
        self.button2_3.columnconfigure('1', minsize='0', pad='0')
        self.button2_3.columnconfigure('5', minsize='50')
        self.button2_3.configure(command=self.set2_3)
        self.button2_4 = tk.Button(frame_1_2)
        self.button2_4.config(background='#c0c0c0', height='2', justify='center', relief='flat')
        self.button2_4.config(width='14')
        self.button2_4.grid(column='4', pady='5', row='2')
        self.button2_4.rowconfigure('1', pad='10')
        self.button2_4.rowconfigure('2', pad='0')
        self.button2_4.columnconfigure('1', minsize='0', pad='0')
        self.button2_4.columnconfigure('5', minsize='50')
        self.button2_4.configure(command=self.set2_4)
        self.button2_5 = tk.Button(frame_1_2)
        self.button2_5.config(background='#c0c0c0', height='2', justify='center', relief='flat')
        self.button2_5.config(width='14')
        self.button2_5.grid(column='5', pady='5', row='2')
        self.button2_5.rowconfigure('1', pad='10')
        self.button2_5.rowconfigure('2', pad='0')
        self.button2_5.columnconfigure('1', minsize='0', pad='0')
        self.button2_5.columnconfigure('5', minsize='50')
        self.button2_5.configure(command=self.set2_5)
        label_3Std = ttk.Label(frame_1_2)
        label_3Std.config(text='3')
        label_3Std.grid(column='0', row='3')
        label_3Std.rowconfigure('1', pad='10')
        label_3Std.rowconfigure('3', pad='0')
        label_3Std.columnconfigure('0', minsize='0')
        self.button3_1 = tk.Button(frame_1_2)
        self.button3_1.config(background='#c0c0c0', height='2', justify='center', relief='flat')
        self.button3_1.config(width='14')
        self.button3_1.grid(column='1', pady='5', row='3')
        self.button3_1.rowconfigure('1', pad='10')
        self.button3_1.rowconfigure('3', pad='0')
        self.button3_1.columnconfigure('1', minsize='0', pad='0')
        self.button3_1.columnconfigure('5', minsize='50')
        self.button3_1.configure(command=self.set3_1)
        self.button3_2 = tk.Button(frame_1_2)
        self.button3_2.config(background='#c0c0c0', height='2', justify='center', relief='flat')
        self.button3_2.config(width='14')
        self.button3_2.grid(column='2', pady='5', row='3')
        self.button3_2.rowconfigure('1', pad='10')
        self.button3_2.rowconfigure('3', pad='0')
        self.button3_2.columnconfigure('1', minsize='0', pad='0')
        self.button3_2.columnconfigure('5', minsize='50')
        self.button3_2.configure(command=self.set3_2)
        self.button3_3 = tk.Button(frame_1_2)
        self.button3_3.config(background='#c0c0c0', height='2', justify='center', relief='flat')
        self.button3_3.config(width='14')
        self.button3_3.grid(column='3', pady='5', row='3')
        self.button3_3.rowconfigure('1', pad='10')
        self.button3_3.rowconfigure('3', pad='0')
        self.button3_3.columnconfigure('1', minsize='0', pad='0')
        self.button3_3.columnconfigure('5', minsize='50')
        self.button3_3.configure(command=self.set3_3)
        self.button3_4 = tk.Button(frame_1_2)
        self.button3_4.config(background='#c0c0c0', height='2', justify='center', relief='flat')
        self.button3_4.config(width='14')
        self.button3_4.grid(column='4', pady='5', row='3')
        self.button3_4.rowconfigure('1', pad='10')
        self.button3_4.rowconfigure('3', pad='0')
        self.button3_4.columnconfigure('1', minsize='0', pad='0')
        self.button3_4.columnconfigure('5', minsize='50')
        self.button3_4.configure(command=self.set3_4)
        self.button3_5 = tk.Button(frame_1_2)
        self.button3_5.config(background='#c0c0c0', height='2', justify='center', relief='flat')
        self.button3_5.config(width='14')
        self.button3_5.grid(column='5', pady='5', row='3')
        self.button3_5.rowconfigure('1', pad='10')
        self.button3_5.rowconfigure('3', pad='0')
        self.button3_5.columnconfigure('1', minsize='0', pad='0')
        self.button3_5.columnconfigure('5', minsize='50')
        self.button3_5.configure(command=self.set3_5)
        label_4Std = ttk.Label(frame_1_2)
        label_4Std.config(text='4')
        label_4Std.grid(column='0', row='4')
        label_4Std.rowconfigure('1', pad='10')
        label_4Std.rowconfigure('3', pad='10')
        label_4Std.rowconfigure('4', pad='0')
        label_4Std.columnconfigure('0', minsize='0')
        label_5Std = ttk.Label(frame_1_2)
        label_5Std.config(text='5')
        label_5Std.grid(column='0', row='5')
        label_5Std.rowconfigure('1', pad='10')
        label_5Std.rowconfigure('3', pad='10')
        label_5Std.rowconfigure('5', pad='0')
        label_5Std.columnconfigure('0', minsize='0')
        label_6Std = ttk.Label(frame_1_2)
        label_6Std.config(text='6')
        label_6Std.grid(column='0', row='6')
        label_6Std.rowconfigure('1', pad='10')
        label_6Std.rowconfigure('3', pad='10')
        label_6Std.rowconfigure('6', pad='0')
        label_6Std.columnconfigure('0', minsize='0')
        label_7Std = ttk.Label(frame_1_2)
        label_7Std.config(text='7')
        label_7Std.grid(column='0', row='7')
        label_7Std.rowconfigure('1', pad='10')
        label_7Std.rowconfigure('3', pad='10')
        label_7Std.rowconfigure('7', pad='0')
        label_7Std.columnconfigure('0', minsize='0')
        self.button4_1 = tk.Button(frame_1_2)
        self.button4_1.config(background='#c0c0c0', height='2', justify='center', relief='flat')
        self.button4_1.config(width='14')
        self.button4_1.grid(column='1', pady='5', row='4')
        self.button4_1.rowconfigure('1', pad='10')
        self.button4_1.rowconfigure('3', pad='10')
        self.button4_1.rowconfigure('4', pad='0')
        self.button4_1.columnconfigure('1', minsize='0', pad='0')
        self.button4_1.columnconfigure('5', minsize='50')
        self.button4_1.configure(command=self.set4_1)
        self.button4_2 = tk.Button(frame_1_2)
        self.button4_2.config(background='#c0c0c0', height='2', justify='center', relief='flat')
        self.button4_2.config(width='14')
        self.button4_2.grid(column='2', pady='5', row='4')
        self.button4_2.rowconfigure('1', pad='10')
        self.button4_2.rowconfigure('3', pad='10')
        self.button4_2.rowconfigure('4', pad='0')
        self.button4_2.columnconfigure('1', minsize='0', pad='0')
        self.button4_2.columnconfigure('5', minsize='50')
        self.button4_2.configure(command=self.set4_2)
        self.button4_3 = tk.Button(frame_1_2)
        self.button4_3.config(background='#c0c0c0', height='2', justify='center', relief='flat')
        self.button4_3.config(width='14')
        self.button4_3.grid(column='3', pady='5', row='4')
        self.button4_3.rowconfigure('1', pad='10')
        self.button4_3.rowconfigure('3', pad='10')
        self.button4_3.rowconfigure('4', pad='0')
        self.button4_3.columnconfigure('1', minsize='0', pad='0')
        self.button4_3.columnconfigure('5', minsize='50')
        self.button4_3.configure(command=self.set4_3)
        self.button4_4 = tk.Button(frame_1_2)
        self.button4_4.config(background='#c0c0c0', height='2', justify='center', relief='flat')
        self.button4_4.config(width='14')
        self.button4_4.grid(column='4', pady='5', row='4')
        self.button4_4.rowconfigure('1', pad='10')
        self.button4_4.rowconfigure('3', pad='10')
        self.button4_4.rowconfigure('4', pad='0')
        self.button4_4.columnconfigure('1', minsize='0', pad='0')
        self.button4_4.columnconfigure('5', minsize='50')
        self.button4_4.configure(command=self.set4_4)
        self.button4_5 = tk.Button(frame_1_2)
        self.button4_5.config(background='#c0c0c0', height='2', justify='center', relief='flat')
        self.button4_5.config(width='14')
        self.button4_5.grid(column='5', pady='5', row='4')
        self.button4_5.rowconfigure('1', pad='10')
        self.button4_5.rowconfigure('3', pad='10')
        self.button4_5.rowconfigure('4', pad='0')
        self.button4_5.columnconfigure('1', minsize='0', pad='0')
        self.button4_5.columnconfigure('5', minsize='50')
        self.button4_5.configure(command=self.set4_5)
        self.button5_1 = tk.Button(frame_1_2)
        self.button5_1.config(background='#c0c0c0', height='2', justify='center', relief='flat')
        self.button5_1.config(width='14')
        self.button5_1.grid(column='1', pady='5', row='5')
        self.button5_1.rowconfigure('1', pad='10')
        self.button5_1.rowconfigure('3', pad='10')
        self.button5_1.rowconfigure('5', pad='0')
        self.button5_1.columnconfigure('1', minsize='0', pad='0')
        self.button5_1.columnconfigure('5', minsize='50')
        self.button5_1.configure(command=self.set5_1)
        self.button5_2 = tk.Button(frame_1_2)
        self.button5_2.config(background='#c0c0c0', height='2', justify='center', relief='flat')
        self.button5_2.config(width='14')
        self.button5_2.grid(column='2', pady='5', row='5')
        self.button5_2.rowconfigure('1', pad='10')
        self.button5_2.rowconfigure('3', pad='10')
        self.button5_2.rowconfigure('5', pad='0')
        self.button5_2.columnconfigure('1', minsize='0', pad='0')
        self.button5_2.columnconfigure('5', minsize='50')
        self.button5_2.configure(command=self.set5_2)
        self.button5_3 = tk.Button(frame_1_2)
        self.button5_3.config(background='#c0c0c0', height='2', justify='center', relief='flat')
        self.button5_3.config(width='14')
        self.button5_3.grid(column='3', pady='5', row='5')
        self.button5_3.rowconfigure('1', pad='10')
        self.button5_3.rowconfigure('3', pad='10')
        self.button5_3.rowconfigure('5', pad='0')
        self.button5_3.columnconfigure('1', minsize='0', pad='0')
        self.button5_3.columnconfigure('5', minsize='50')
        self.button5_3.configure(command=self.set5_3)
        self.button5_4 = tk.Button(frame_1_2)
        self.button5_4.config(background='#c0c0c0', height='2', justify='center', relief='flat')
        self.button5_4.config(width='14')
        self.button5_4.grid(column='4', pady='5', row='5')
        self.button5_4.rowconfigure('1', pad='10')
        self.button5_4.rowconfigure('3', pad='10')
        self.button5_4.rowconfigure('5', pad='0')
        self.button5_4.columnconfigure('1', minsize='0', pad='0')
        self.button5_4.columnconfigure('5', minsize='50')
        self.button5_4.configure(command=self.set5_4)
        self.button5_5 = tk.Button(frame_1_2)
        self.button5_5.config(background='#c0c0c0', height='2', justify='center', relief='flat')
        self.button5_5.config(width='14')
        self.button5_5.grid(column='5', pady='5', row='5')
        self.button5_5.rowconfigure('1', pad='10')
        self.button5_5.rowconfigure('3', pad='10')
        self.button5_5.rowconfigure('5', pad='0')
        self.button5_5.columnconfigure('1', minsize='0', pad='0')
        self.button5_5.columnconfigure('5', minsize='50')
        self.button5_5.configure(command=self.set5_5)
        self.button6_1 = tk.Button(frame_1_2)
        self.button6_1.config(background='#c0c0c0', height='2', justify='center', relief='flat')
        self.button6_1.config(width='14')
        self.button6_1.grid(column='1', pady='5', row='6')
        self.button6_1.rowconfigure('1', pad='10')
        self.button6_1.rowconfigure('3', pad='10')
        self.button6_1.rowconfigure('6', pad='0')
        self.button6_1.columnconfigure('1', minsize='0', pad='0')
        self.button6_1.columnconfigure('5', minsize='50')
        self.button6_1.configure(command=self.set6_1)
        self.button6_2 = tk.Button(frame_1_2)
        self.button6_2.config(background='#c0c0c0', height='2', justify='center', relief='flat')
        self.button6_2.config(width='14')
        self.button6_2.grid(column='2', pady='5', row='6')
        self.button6_2.rowconfigure('1', pad='10')
        self.button6_2.rowconfigure('3', pad='10')
        self.button6_2.rowconfigure('6', pad='0')
        self.button6_2.columnconfigure('1', minsize='0', pad='0')
        self.button6_2.columnconfigure('5', minsize='50')
        self.button6_2.configure(command=self.set6_2)
        self.button6_3 = tk.Button(frame_1_2)
        self.button6_3.config(background='#c0c0c0', height='2', justify='center', relief='flat')
        self.button6_3.config(width='14')
        self.button6_3.grid(column='3', pady='5', row='6')
        self.button6_3.rowconfigure('1', pad='10')
        self.button6_3.rowconfigure('3', pad='10')
        self.button6_3.rowconfigure('6', pad='0')
        self.button6_3.columnconfigure('1', minsize='0', pad='0')
        self.button6_3.columnconfigure('5', minsize='50')
        self.button6_3.configure(command=self.set6_3)
        self.button6_4 = tk.Button(frame_1_2)
        self.button6_4.config(background='#c0c0c0', height='2', justify='center', relief='flat')
        self.button6_4.config(width='14')
        self.button6_4.grid(column='4', pady='5', row='6')
        self.button6_4.rowconfigure('1', pad='10')
        self.button6_4.rowconfigure('3', pad='10')
        self.button6_4.rowconfigure('6', pad='0')
        self.button6_4.columnconfigure('1', minsize='0', pad='0')
        self.button6_4.columnconfigure('5', minsize='50')
        self.button6_4.configure(command=self.set6_4)
        self.button6_5 = tk.Button(frame_1_2)
        self.button6_5.config(background='#c0c0c0', height='2', justify='center', relief='flat')
        self.button6_5.config(width='14')
        self.button6_5.grid(column='5', pady='5', row='6')
        self.button6_5.rowconfigure('1', pad='10')
        self.button6_5.rowconfigure('3', pad='10')
        self.button6_5.rowconfigure('6', pad='0')
        self.button6_5.columnconfigure('1', minsize='0', pad='0')
        self.button6_5.columnconfigure('5', minsize='50')
        self.button6_5.configure(command=self.set6_5)
        self.button7_1 = tk.Button(frame_1_2)
        self.button7_1.config(background='#c0c0c0', height='2', justify='center', relief='flat')
        self.button7_1.config(width='14')
        self.button7_1.grid(column='1', pady='5', row='7')
        self.button7_1.rowconfigure('1', pad='10')
        self.button7_1.rowconfigure('3', pad='10')
        self.button7_1.rowconfigure('7', pad='0')
        self.button7_1.columnconfigure('1', minsize='0', pad='0')
        self.button7_1.columnconfigure('5', minsize='50')
        self.button7_1.configure(command=self.set7_1)
        self.button7_2 = tk.Button(frame_1_2)
        self.button7_2.config(background='#c0c0c0', height='2', justify='center', relief='flat')
        self.button7_2.config(width='14')
        self.button7_2.grid(column='2', pady='5', row='7')
        self.button7_2.rowconfigure('1', pad='10')
        self.button7_2.rowconfigure('3', pad='10')
        self.button7_2.rowconfigure('7', pad='0')
        self.button7_2.columnconfigure('1', minsize='0', pad='0')
        self.button7_2.columnconfigure('5', minsize='50')
        self.button7_2.configure(command=self.set7_2)
        self.button7_3 = tk.Button(frame_1_2)
        self.button7_3.config(background='#c0c0c0', height='2', justify='center', relief='flat')
        self.button7_3.config(width='14')
        self.button7_3.grid(column='3', pady='5', row='7')
        self.button7_3.rowconfigure('1', pad='10')
        self.button7_3.rowconfigure('3', pad='10')
        self.button7_3.rowconfigure('7', pad='0')
        self.button7_3.columnconfigure('1', minsize='0', pad='0')
        self.button7_3.columnconfigure('5', minsize='50')
        self.button7_3.configure(command=self.set7_3)
        self.button7_4 = tk.Button(frame_1_2)
        self.button7_4.config(background='#c0c0c0', height='2', justify='center', relief='flat')
        self.button7_4.config(width='14')
        self.button7_4.grid(column='4', pady='5', row='7')
        self.button7_4.rowconfigure('1', pad='10')
        self.button7_4.rowconfigure('3', pad='10')
        self.button7_4.rowconfigure('7', pad='0')
        self.button7_4.columnconfigure('1', minsize='0', pad='0')
        self.button7_4.columnconfigure('5', minsize='50')
        self.button7_4.configure(command=self.set7_4)
        self.button7_5 = tk.Button(frame_1_2)
        self.button7_5.config(background='#c0c0c0', height='2', justify='center', relief='flat')
        self.button7_5.config(width='14')
        self.button7_5.grid(column='5', pady='5', row='7')
        self.button7_5.rowconfigure('1', pad='10')
        self.button7_5.rowconfigure('3', pad='10')
        self.button7_5.rowconfigure('7', pad='0')
        self.button7_5.columnconfigure('1', minsize='0', pad='0')
        self.button7_5.columnconfigure('5', minsize='50')
        self.button7_5.configure(command=self.set7_5)
        frame_1_2.config(height='200', width='200')
        frame_1_2.pack(side='left')
        abstand2 = ttk.Frame(frame_11)
        abstand2.config(height='200', width='30')
        abstand2.pack()
        frame_11.config(height='200', width='200')
        frame_11.pack(side='top')
        labelframe_3.config(height='200', text='Buchung', width='200')
        labelframe_3.pack(side='top')
        panedwindow_2.add(labelframe_3, weight='12')
        panedwindow_2.config(height='200', width='200')
        panedwindow_2.pack(expand='true', fill='both', side='top')
        frame_1.config(padding='5')
        frame_1.pack(expand='true', fill='both', side='top')
        root.config(height='630', width='1000')
        root.geometry('1000x630')
        root.resizable(True, True)
        root.title('Buchungstool')

        frame_7.forget()
        frame_9.forget()
        frame_11.forget()

        self.frame_7 = frame_7
        self.frame_9 = frame_9
        self.frame_11 = frame_11

        self.start = 1

        # Main widget
        self.mainwindow = root

        # Fenster positionieren
        # Gets the requested values of the height and widht.
        windowWidth = self.mainwindow.winfo_reqwidth()
        windowHeight = self.mainwindow.winfo_reqheight()
        # Gets both half the screen width/height and window width/height
        positionRight = int(self.mainwindow.winfo_screenwidth()/2 - windowWidth/2-10)
        positionDown = int(self.mainwindow.winfo_screenheight()/2 - windowHeight/2-35)
        # Positions the window in the center of the page.
        self.mainwindow.geometry("+{}+{}".format(positionRight, positionDown))

        # Grab window + focus
        self.mainwindow.grab_set()
        self.mainwindow.focus_set()  


        # Monate für Combobox
        self.monat = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", 
                      "August", "September", "Oktober", "November", "Dezember"]

        self.combo_monat.config(values=self.monat)

        # Listbox: Die Option exportselection=False führt dazu, dass
        # der gewählte Eintrag immer aktiv bleibt und keine leeren Tupel 
        # ausgegeben werden.
        self.listbox.config(exportselection=False)

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
        
        if items == []:
            Ersteinrichtung(self)
        else:
            self.mykrzl = items[0][0]


    def set_cur_year_month(self):
        self.combo_jahr.set(date.today().year)
        self.combo_monat.set(datetime.now().strftime("%B"))

    def fill_listbox(self, event):
        if self.combobox_1.get() == "Merzenich":
            self.listbox.delete(0,"end")
            for i in self.itemsMZ: 
                self.listbox.insert("end",i[0])
        if self.combobox_1.get() == "Niederzier":
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
    app = BuchungstoolApp()
    app.run()