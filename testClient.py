#!/usr/bin/python3
import tkinter
import tkinter.messagebox
import socket
from time import sleep
import pdb

def reset_option():
   Option.set(0)    

def envoi():
    try:
        host = txtAdresse.get()
        port = txtPort.get()
        
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(3)
        client.connect((host,int(port)))
    

        data_s = Position.get() + ':' + str(Option.get())
        data_s = str.encode(data_s)
        client.sendall(data_s)
        print("data sent : ", data_s)
        
        data_r = client.recv(2)
        print("data received :", data_r)
        
        if not data_r:
            print("socket lost")
        
        if data_r == b'F':
            #print("Reset")
            reset_option()
         
        # sleep(0.5)

        client.close()
    except Exception as e :
        tkinter.messagebox.showerror("Erreur", f"L'erreur suivante s'est produite : {e}")
        
print("Démarrage du client")

root = tkinter.Tk()
root.title("Client pour la machine à voter")

Option = tkinter.IntVar()
txtAdresse = tkinter.StringVar()
txtPort = tkinter.StringVar()
Position = tkinter.StringVar()

frm = tkinter.Frame(root, bd = 16)
frm.grid()

labelAdresse = tkinter.Label(frm, text = "Adresse :")
labelAdresse.grid(row = 0, column = 1, sticky = tkinter.E, pady=2)
entryAdresse = tkinter.Entry(frm, textvariable = txtAdresse)
entryAdresse.grid(row = 0, column = 2, columnspan = 2, sticky = tkinter.W, pady=2)
entryAdresse.focus()

labelPort = tkinter.Label(frm, text = "Port :")
labelPort.grid(row = 1, column = 1, sticky = tkinter.E, pady=2)
entryPort = tkinter.Entry(frm, textvariable = txtPort)
entryPort.grid(row = 1, column = 2, columnspan = 2, sticky = tkinter.W, pady=2)

labelPosition = tkinter.Label(frm, text = "Position :")
labelPosition.grid(row = 0, column = 5, sticky = tkinter.E, pady=2)
entryPosition = tkinter.Entry(frm, textvariable = Position)
entryPosition.config(width = 8)
entryPosition.grid(row = 0, column = 6, columnspan = 1, sticky = tkinter.W, pady=2)

B1 = tkinter.Button(frm, text = "Envoi", command = envoi)
B1.config(width = 12)
B1.grid(row = 4, column = 0, columnspan = 2, sticky = tkinter.W, pady=2)

B2 = tkinter.Button(frm, text = "Terminer", command = root.destroy)
B2.config(width = 12)
B2.grid(row = 4, column = 6, columnspan = 2, sticky = tkinter.E, pady=2)

B3 = tkinter.Button(frm, text = "Reset", command = reset_option)
B3.config(width = 12)
B3.grid(row = 4, column = 3, columnspan = 2, sticky = tkinter.E, pady=2)

R1 = tkinter.Radiobutton(frm, text = 'Option 1', variable = Option)
R1.config(indicatoron = 0, bd = 4, width = 15, value = 1)
R1.grid(row = 2, column = 0, columnspan = 2)

R2 = tkinter.Radiobutton(frm, text = 'Option 2', variable = Option)
R2.config(indicatoron = 0, bd = 4, width = 15, value = 2)
R2.grid(row = 2, column = 2, columnspan = 2)

R3 = tkinter.Radiobutton(frm, text = 'Option 3', variable = Option)
R3.config(indicatoron = 0, bd = 4, width = 15, value = 3)
R3.grid(row = 2, column = 4, columnspan = 2)

R4 = tkinter.Radiobutton(frm, text = 'Option 4', variable = Option)
R4.config(indicatoron = 0, bd = 4, width = 15, value = 4)
R4.grid(row = 2, column = 6, columnspan = 2)

label = tkinter.Label(frm)
label.config(bd = 4)
label.grid(row = 3, column = 0, columnspan = 8, pady=2)

root.mainloop()

