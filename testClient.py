#!/usr/bin/python3
import tkinter
import tkinter.messagebox
import socket, sys
from time import sleep
from queue import Queue
import threading
import pdb

lafinRcpt = False
lafin = False
client = None
host = None
port = None

qRcpt = Queue(0)

def terminer():

   global lafinRcpt, lafin, host, port, client
   
   lafinRcpt = True
   lafin = True
   client.close()
   # Forcer le thread à terminer proprement
   socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host,int(port)))

def connect():

   global host, port, client, lafin, lafinRcpt

   host = txtAdresse.get()
   port = txtPort.get()
        
   client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

   try:
      client.connect((host,int(port)))
      sleep(0.5)
      demarrerReception()
      buttonConnect.configure(bg="red", fg="yellow")
      buttonConnect.configure(state="disabled")

   except Exception as e:
      print(f"Erreur de connexion client : {e}")
      buttonConnect.configure(bg="lightgrey", fg="black")
      terminer()
        
   sleep(0.5)

def demarrerReception():

   global lafinRcpt

   t = threading.Thread ( target = tReception, daemon=True )
   lafinRcpt = False
   t.start()

def tReception() :

   global lafinRcpt, lafin, client, qRcpt
   
   try:
      
      while not lafinRcpt :

         data = client.recv(1024).decode()
         print("data serveur == " + data)                        
         if(len(data) > 0):
            qRcpt.put(data)

         sleep(0.01)
                
   except Exception as ose:
      print ("Erreur de réception " + str(ose))
      lafinRcpt = True
      lafin = True
            
def getID() :

   global client
   
   try:
      host = txtAdresse.get()
      port = txtPort.get()
      if 0 == len(host) or 0 == len(port) or 0 == len(txtMacAdresse.get()):
         tkinter.messagebox.showerror("Erreur client", "Les champs <Adresse>, <Port> et <HWAddr Mac> doivent être initialisés avant de demander l'identificateur.")

      else:
         
         print(f'txtMacAdresse.get() == {txtMacAdresse.get().replace(":","").replace(" ","").replace("-","")}')
         msg = "?:" + txtMacAdresse.get().replace(":","").replace(" ","").replace("-","")
         client.send(msg.encode())
         print(f"msg == {msg}")
         sleep(0.1)

   except Exception as e:
      
      tkinter.messagebox.showerror("Erreur client : " + txtMacAdresse.get(), f"Erreur de communication : {e}")
         

def reset_option():
   Option.set(0)    

def envoi():

   global client
   
   try:
      data_s = txtPosition.get() + ':' + str(Option.get())
      data_s = str.encode(data_s)
      client.sendall(data_s)
      print("data sent : ", data_s)

   except Exception as e :
      tkinter.messagebox.showerror("Erreur client", f"L'erreur suivante s'est produite : {e}")
        
print("Démarrage du client")

root = tkinter.Tk()
root.title("Client pour la machine à voter")

Option = tkinter.IntVar()
txtAdresse = tkinter.StringVar()
txtPort = tkinter.StringVar()
txtPosition = tkinter.StringVar()
txtMacAdresse = tkinter.StringVar()
txtDonnee = tkinter.StringVar()
txtDonnee.set("- - -")

if len(sys.argv) > 1 :
   txtAdresse.set(sys.argv[1])

if len(sys.argv) > 2 :
   txtPort.set(sys.argv[2])

if len(sys.argv) > 3 :
   txtMacAdresse.set(sys.argv[3])

frm = tkinter.Frame(root, bd = 16)
frm.grid()

labelAdresse = tkinter.Label(frm, text = "Adresse :")
labelAdresse.grid(row = 0, column = 0, sticky = tkinter.E, pady=2)
entryAdresse = tkinter.Entry(frm, textvariable = txtAdresse)
entryAdresse.grid(row = 0, column = 1, columnspan = 2, sticky = tkinter.W, pady=2)
entryAdresse.focus()

labelPort = tkinter.Label(frm, text = "Port :")
labelPort.grid(row = 1, column = 0, sticky = tkinter.E, pady=2)
entryPort = tkinter.Entry(frm, textvariable = txtPort)
entryPort.grid(row = 1, column = 1, columnspan = 2, sticky = tkinter.W, pady=2)

labelPosition = tkinter.Label(frm, text = "Position :")
labelPosition.grid(row = 0, column = 3, sticky = tkinter.E, pady=2)
entryPosition = tkinter.Entry(frm, textvariable = txtPosition)
entryPosition.config(width = 8)
entryPosition.grid(row = 0, column = 4, columnspan = 1, sticky = tkinter.W, pady=2)

buttonPosition = tkinter.Button(frm, text = "Récupérer", command = getID)
buttonPosition.grid(row = 0, column = 6, columnspan = 2, sticky = tkinter.W, pady=2)

labelMAC = tkinter.Label(frm, text = "HWAddr MAC :")
labelMAC.grid(row = 1, column = 3, sticky = tkinter.E, pady=2)
entryMAC = tkinter.Entry(frm, textvariable = txtMacAdresse)
entryMAC.config(width = 16)
entryMAC.grid(row = 1, column = 4, columnspan = 1, sticky = tkinter.W, pady=2)

buttonConnect = tkinter.Button(frm, text = "Connect", command = connect)
buttonConnect.grid(row = 1, column = 6, columnspan = 2, sticky = tkinter.W, pady=2)

B1 = tkinter.Button(frm, text = "Envoi", command = envoi)
B1.config(width = 12)
B1.grid(row = 4, column = 0, columnspan = 2, sticky = tkinter.W, pady=2)

B2 = tkinter.Button(frm, text = "Terminer", command = terminer)
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

labelData = tkinter.Label(frm, text = "Donnée reçue :")
labelData.config(bd = 4)
labelData.grid(row = 3, column = 0, sticky = tkinter.W, pady=2)

labelDataRcvd = tkinter.Label(frm, text = " - - -", textvariable = txtDonnee)
labelDataRcvd.config(bd = 4)
labelDataRcvd.grid(row = 3, column = 1, columnspan = 4, sticky = tkinter.W, pady=2)

root.protocol("WM_DELETE_WINDOW", terminer)

while not lafin:
    
   root.update_idletasks()
   root.update()
   if(not qRcpt.empty()):
      data = qRcpt.get()
      print(f"Données reçues == {data}")
      if data.startswith("F"):
         reset_option()
      elif data.startswith("ID:"):
         print(f"id == {data[3:]}")
         txtPosition.set(int(data[3:]))

      
   sleep(0.01)
            
root.quit()
