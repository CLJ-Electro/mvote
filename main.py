#!/usr/bin/python3
#
import sys,time,socket,json,socket,glob
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import tkinter.font as tkFont
import threading
import select
from queue import Queue
from tkinter import filedialog as fd

import logging
import pdb


qGUI = Queue(0)

class voteur(tk.Frame):

    valeurChoisie = -1

    def __init__(self, root, etiquette, vote):

        self.root = root
        self.etiquette = etiquette

        super().__init__(root, bg='grey')

        self.valeurChoisie = vote

        self.lblTexte = tk.Label(self, anchor=tk.W, bg="grey", fg="yellow")
        self.lblTexte.place(relx=0.05, rely=0.25)

        self.lblTexte.configure(text=str(etiquette))

        self.lblTexte.configure(justify="left")
        self.lblTexte.configure(font=("Courrier New", 10, "bold"))
        #self.lbl.bind("<Button-1>", self.buttonPort)

    def setVote(self, valeur, couleur):
        self.valeurChoisie = int(valeur)
        self.lblTexte.configure(bg=couleur)
        
    def getVote(self):
        return self.valeurChoisie 
        

class dlgVoteur:
    
    def __init__(self, parent):
        self.parent = parent
        self.top = tk.Toplevel(parent)
        self.top.title("Configuration voteur")
        self.top.geometry("800x400")
        self.top.resizable(True, True)

        self.myCheckEmail = tk.IntVar(self.top)
        self.myCheckEmail.set(1)
        self.mEmail_check = tk.Checkbutton(self.top, text = "Actif", variable = self.myCheckEmail, onvalue = 1, offvalue = 0, height=3, width = 5)
        self.mEmail_check.place(relx=0.80, rely=0.32, anchor=tk.W)

    def show(self):
        self.top.wm_deiconify()
        self.top.wait_window()
        return self.myCheckEmail.get()
    
class dlgConfFile:
    
    def __init__(self, parent):
        self.parent = parent
        self.parent.withdraw()
        self.top = tk.Toplevel(parent)
        self.top.title("Fichier de configuration")
        self.top.geometry("500x300")
        self.top.resizable(True, True)
        self.top.bind('<Return>', self.event_terminer)

        helv = tkFont.Font(family='Helvetica',size=24, weight='bold')
        
        self.myConfFile = tk.StringVar(value=glob.glob("./*.json"))
        
        self.mListBox = tk.Listbox(self.top, listvariable=self.myConfFile, height=5,
                                   font=helv, selectmode=tk.SINGLE)
        
        self.mListBox.place(relx=0.05, rely=0.05, relheight=0.75, relwidth=0.9)
        #self.mListBox.selection_set( first = 0 )
        self.mListBox.bind('<<ListboxSelect>>', self.lstSelection)
        self.mListBox.focus_set()
        
        self.mBtnOK = tk.Button(self.top, text="OK", command = self.terminer)
        self.mBtnOK.place(relx=0.75, rely=0.85, relheight=0.1, relwidth=0.2)
        self.mBtnOK.configure(bg="green", fg="yellow", activebackground="green")
         
        self.choix = ""
        self.autoDelai = True

        self.top.after(10000, self.auto_terminer)
        
    def lstSelection(self, event):
        self.autoDelai = False
        
    def event_terminer(self, event):
        self.terminer()
        
    def auto_terminer(self):
        if self.autoDelai :
            self.terminer()
        
    def terminer(self):
        if 1 == len(self.mListBox.curselection()):
            #Si un fichier a été sélectionné, on récupère son nom
            #sinon on laisse la chaîne "self.choix" vide.
            self.choix = self.mListBox.get(self.mListBox.curselection())
        self.top.quit()
        self.top.destroy()
        
    def show(self):
        self.top.wm_deiconify()
        self.top.wait_window()
        self.parent.deiconify()
        return self.choix

class appVote:

    lafin = False
    photo = None
    adresseIP = None
    port = None
    root = None
    voteurs = []
    resultats = []
    lafinSrv = False

    def __init__(self, geo="1000x700+225+150", confFile="config.json"):

        self.root = tk.Tk()
        self.root.geometry(geo)
        #self.root.resizable(False, False)
        #self.root.attributes('-fullscreen',True)
        self.root.minsize(1000, 700)
        self.root.title("Cégep Joliette Télécom@" + str(socket.gethostname()))
        
        filename = dlgConfFile(self.root).show()

        if filename:
            confFile = filename

        self.voteEnCours = False

        print(f"Fichier de configuration utilisé == {confFile}")
        
        with open(confFile, 'r') as file:
            self.parametres = json.load(file)

        self.adresseIP = self.parametres['adresse_serveur']
        self.port = self.parametres['port_tcp_serveur']
        self.backlog = self.parametres['backlog']
        
        self.nbVoteurs = self.parametres['nb_voteurs']
        self.nbColonnes = self.parametres['nb_colonnes']
        self.nbRangees = self.parametres['nb_rangees']

        self.root.geometry(geo)
        self.root.minsize(1000, 700)
        self.root.title("Cégep Joliette Télécom@" + str(socket.gethostname()))
        #self.root.wm_attributes('-alpha', 0.75)

        try :

            self.photo = tk.PhotoImage(file="logodemo_t.png")

            # Load the custom icon image
            icon_image = tk.PhotoImage(file="iconeDemo.png")

            # Set the custom icon for the window titlebar
            self.root.iconphoto(False, icon_image)

        except Exception as excpt:
            
            print("Fichiers des images manquants!")
            print("Erreur : ", excpt)
            sys.exit()
            
        # get the width and height of the image
        image_width = self.photo.width()
        image_height = self.photo.height()
        print(f"image_width == {image_width}")
        print(f"image_height == {image_height}")

        self.Header = tk.Label(self.root, image=self.photo, width=image_width, height=image_height)
        self.Header.place(relx=0.5, rely=0.03, anchor=tk.N)
        self.Header.bind("<Button-1>", self.buttonLogoClick)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            self.adresseIP = s.getsockname()[0]
        except:
            self.adresseIP='127.0.0.1'
        finally:
            s.close()
            
        self.lblAdresseIP = tk.Label(self.root, anchor="w")                     # Bas de page
        self.lblAdresseIP.place(relx=0.05, rely=0.95, height=23, width=225)
        self.lblAdresseIP.configure(text="Serveur " + self.adresseIP)
        self.lblAdresseIP.configure(justify='left')
        self.lblAdresseIP.configure(font=("Courrier New", 10, "bold"))
        #self.lblAdresseIP.bind("<Button-1>", self.buttonAdresse)

        self.lblPortTCP = tk.Label(self.root, anchor="w")                       # Bas de page
        self.lblPortTCP.place(relx=0.25, rely=0.95, height=23, width=100)
        self.lblPortTCP.configure(text="Port " + ":" + str(self.port))
        self.lblPortTCP.configure(justify='left')
        self.lblPortTCP.configure(font=("Courrier New", 10, "bold"))

        self.initialiseOutils()

        self.initialiseVoteurs(self.nbVoteurs, self.nbColonnes, self.nbRangees)

    def initialiseOutils(self):

        self.panneauLateral = tk.Frame(self.root, bg='grey', borderwidth=2)
        self.panneauLateral.place(relx=0.65, rely=0.30, relheight=0.58, relwidth=0.30)   
        
        self.lblTitre = tk.Label(self.panneauLateral, anchor="w")
        self.lblTitre.place(relx=0.43, rely=0.02, relheight=0.05, relwidth=0.15)
        self.lblTitre.configure(text="Outils", bg="grey", fg="white")
        self.lblTitre.configure(justify='center')
        self.lblTitre.configure(font=("Courrier New", 10, "bold"))

        self.btnDemarrer = tk.Button(self.panneauLateral, text="Démarrer", command = self.controlerVote)
        self.btnDemarrer.place(relx=0.75, rely=0.13, relheight=0.05, relwidth=0.2)
        self.btnDemarrer.configure(bg="green", fg="yellow", activebackground="green")
        
        self.entete_voteurs = ["Choix", "Résultat"]

        style = ttk.Style(self.panneauLateral)
        style.theme_use("clam")
        style.configure("Treeview", background="grey", 
                fieldbackground="grey", foreground="white")

        self.tree = ttk.Treeview(self.panneauLateral, columns=self.entete_voteurs, show="tree headings", height=10)
        self.tree.column("# 0", anchor=tk.W, width=0)
        #self.tree.heading("# 0", text="")
        self.tree.column("# 1", anchor=tk.W, width=30)
        self.tree.heading("# 1", text="Choix")
        self.tree.column("# 2", anchor=tk.W, width=30)
        self.tree.heading("# 2", text="Résultat")

        vsb = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self.tree, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")

        self.tree.place(relx=0.05, rely=0.22, relheight=0.75, relwidth=0.9)
        self.tree['show'] = 'tree headings'

        rng = range(len(self.parametres["couleurs_votes"]))
        i = 0
        for couleur in rng :
            
            self.tree.tag_configure(self.parametres["couleurs_votes"][couleur], background=self.parametres["couleurs_votes"][couleur])

            self.tree.insert("", tk.END, text='', tags=self.parametres["couleurs_votes"][couleur], values=[chr(i+97), ""])
            i += 1
        
        self.tree.bind("<Button-1>", self.itemMouseEvent)
        self.tree.bind("<Button-3>", self.itemMouseEvent)
        self.tree.bind("<Double-1>", self.itemMouseEvent)

        self.myCheckAlias = tk.IntVar(value=1)
        self.mAlias_check = tk.Checkbutton(self.panneauLateral, text = "Afficher Alias", variable = self.myCheckAlias, onvalue = 1, offvalue = 0, height=1, width = 12, bg="grey", fg = "white", selectcolor="grey", command=self.aliasActive)

        self.mAlias_check.place(relx=0.05, rely=0.15, anchor=tk.W)
        self.aliasActive()

    def majTreeview(self):

        self.tree.delete(*self.tree.get_children())
        
        rng = range(len(self.parametres["couleurs_votes"]))
        i = 0
        print(f"Len(resultats) == {len(self.resultats)}")
        for couleur in rng :
            #logging.info(f"Insertion de l'item {i} : resultats[{i}] == {self.resultats[i]}.")            
            self.tree.insert("", tk.END, text='', tags=self.parametres["couleurs_votes"][couleur], values=[chr(i+97), self.resultats[i]])
            i += 1


    def itemMouseEvent(self, event):

        pass
        #itemSelect = self.tree.selection()
        # Si le bouton droit de la sourie est activé
        #if event.num == 1 :
        #    self.majTreeview()

    def aliasActive(self):
        if self.myCheckAlias.get() == 1:
            self.mAlias_check.configure(fg = "yellow")
        elif self.myCheckAlias.get() == 0:
            self.mAlias_check.configure(fg = "white")
        self.parametres["avec_alias"] = self.myCheckAlias.get()
        self.initialiseVoteurs(self.parametres["nb_voteurs"], self.parametres["nb_colonnes"], self.parametres["nb_rangees"])
        
    def controlerVote(self):
        if self.btnDemarrer['text'] == 'Démarrer' :
            self.btnDemarrer.configure(text="Arrêter", bg="red", fg="yellow", activebackground="red")
            self.mAlias_check['state'] = tk.DISABLED
            print("Le vote est en cours.")
            self.voteEnCours = True
            self.message_a_tous("F")
            self.effacerResultatVote()
            self.initialiseVoteurs(self.parametres["nb_voteurs"], self.parametres["nb_colonnes"], self.parametres["nb_rangees"])
            self.majTreeview()

        else :
            self.btnDemarrer.configure(text="Démarrer", bg="green", fg="yellow", activebackground="green")
            self.mAlias_check['state'] = tk.NORMAL
            print("Le vote est terminé.")
            self.voteEnCours = False

    def effacerResultatVote(self):

        print("Le résultat du vote précédent a été effacé.")
        # Effacer la liste des résultats
        rng =range(len(self.resultats))
        for i in rng :
            self.resultats[i] = 0
            
        for voteur in self.voteurs :
            voteur.setVote(-1, "grey")


    def recupereId(self, adresse):

        rng = range(self.parametres["nb_voteurs"])
        for i in rng:
            if adresse == self.parametres["voteurs"][i][2].replace(":","").replace(" ","").replace("-",""):
                return self.parametres["voteurs"][i][0]-1
        return str(-1)
    
    # Envoyer un message à tous les clients
    def message_a_tous(self, message):
        #for queue_t in self.message_queues_transmission:
        for client in self.write_list :
            client.send(message.encode())
            
    def demarrerServeur(self):

        self.t = threading.Thread ( target = self.tServer, daemon=True )
        self.lafinSrv = False
        self.t.start()

        #if self.dureeVoteVar.get() != "0" :

        #    try :
        #        self.tempsDeVote = self.dureeVoteVar.get()
        #        print(f"Temps du vote == {self.tempsDeVote}")
        #    except Exception as e:
        #        print(e)
                
    def tServer(self) :  # Référence : https://pymotw.com/3/select/

        #Listes des clients connectés
        self.read_list = []
        self.write_list = []

        # Dictionnaire des queues de réception (socket:Queue)
        self.message_queues_reception = {}

        # Dictionnaire des queues de transmission 
        self.message_queues_transmission = {}

        #try:

        self.mServeur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mServeur.bind((self.adresseIP, self.port))
        self.mServeur.listen(self.backlog)

        self.read_list.append(self.mServeur)
            
        print("En attente d'un client...")
        
        while not self.lafinSrv :

            readable, writable, errored = select.select(self.read_list, self.write_list, [])

            for s in readable:

                if s is self.mServeur and (s.fileno() != -1) :
                    client, addr = s.accept()
                    client.setblocking(0)
                    self.read_list.append(client)
                    self.write_list.append(client)
                    self.message_queues_reception[client] = Queue() 
                    self.message_queues_transmission[client] = Queue() 
                    print(time.asctime() + "    Connexion établie avec le système : ", addr)
                    
                elif s.fileno() != -1 :
                    
                    print(f"s.fileno() == {s.fileno()}")
                    data = s.recv(1024).decode()
                        
                    if(data):

                        if s not in self.write_list :
                            self.write_list.append(s)
                                
                        print("data reçue par le serveur == " + data)
                        if data.startswith("?:"):
                            print(f"ID ==>{self.recupereId(data[2:])}")
                            msg = "ID:" + str(self.recupereId(data[2:]))
                            s.send(msg.encode())
                        elif self.voteEnCours :
                            self.message_queues_reception[s].put(data)
                        else :
                            s.send("F".encode())

                    else :
                        if s in self.write_list:
                            self.write_list.remove(s)
                        print(f"client retiré de la liste : {s}")
                        if s in self.read_list:
                            self.read_list.remove(s)
                        del self.message_queues_reception[s]
                        del self.message_queues_transmission[s]
                        s.close()
                else:
                    print(f"Cas par défaut. Ne devrait jamais passer ici! s = {s}")

            for s in writable :
                if s.fileno() >= 0 :
                    while not self.message_queues_transmission[s].empty() :
                        msg = self.message_queues_transmission[s].get_nowait()
                        print(f"msg à envoyer == {msg}")
                        s.send(msg)
                    
            for s in errored:
                
                print(f"Socket ERROR! : {s}")
                self.read_list.remove(s)
                if s in self.write_list:
                    self.write_list.remove(s)
                s.close()
                    
                del self.message_queues_transmission[s]
                del self.message_queues_reception[s]
                    
                    
            time.sleep(0.01)
                
        if len(self.read_list) > 0 :

            readable, writable, errored = select.select(self.read_list, [], [])
            for s in readable:
                s.close()

        print(time.asctime() + "    Serveur arrêté.")
            
    def arreterServeur(self):

        # Indiquer au thread serveur qu'il doit s'arrêter
        self.lafinSrv = True

        # Ici on initie une connexion au serveur afin de débloquer le thread serveur pour qu'il s'arrête 
        try:
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((self.adresseIP, self.port))
        except Exception as e:
            print("Exception lors de l'arrêt du serveur.")
            print(e)

        # Retirer le serveur de la liste des sockets actifs
        try:
            self.read_list.remove(self.mServeur)
        except:
            print(f"self.read_list.remove(self.mServeur) {self.mServeur}")
            pass

        # Terminer l'exécution du serveur
        #self.mServeur.close()

        print("Le serveur est arrêté.")

    def afficherVoteur(self, index, vote):

        i = int(index)
        
        if self.voteurs[i].getVote() != -1 :
            self.resultats[self.voteurs[i].getVote()] -= 1

        self.resultats[vote] += 1
        self.majTreeview()
        vv = self.voteurs[i]
        self.voteurs.remove(vv)
        vot = voteur(self.root, vv.etiquette, str(vote+1))
        vv.destroy()
        vot.setVote(vote, self.parametres["couleurs_votes"][vote])
        self.voteurs.insert(i, vot)
        
        vot.place(relx=0.05 + (i % self.nbColonnes) * (0.6 / self.nbColonnes),
                  rely=0.30 + (i // self.nbColonnes) * (0.6 / self.nbRangees),
                  relheight=0.5/self.nbRangees,
                  relwidth=0.5/self.nbColonnes)
        
        vot.configure(bg=self.parametres["couleurs_votes"][int(vote)])
        vot.bind("<Button-3>", self.confDlg)

    def initialiseVoteurs(self, nombre, nb_colonnes, nb_lignes):

        for vot in self.voteurs:
            vot.destroy()

        self.voteurs = []
            
        rng = range(nombre)

        for i in rng:

            if self.myCheckAlias.get() == 0:
                # Afficher l'index du voteur dans le GUI
                self.vot = voteur(self.root, self.parametres["voteurs"][i][0], -1)
            else:
                # Affichier l'alias
                self.vot = voteur(self.root, self.parametres["voteurs"][i][1], -1)
        
            self.vot.place(relx=0.05 + (i % nb_colonnes) * (0.6 / nb_colonnes),
                           rely=0.30 + (i // nb_colonnes) * (0.6 / nb_lignes),
                           relheight=0.5/nb_lignes,
                           relwidth=0.5/nb_colonnes)
            self.vot.bind("<Button-3>", self.confDlg)

            self.voteurs.append(self.vot)
            self.resultats.append(0)


    def confDlg(self, event):

        print(str(event))
        chck = dlgVoteur(self.root).show()
        print(f"chck[0] == {chck}")
        
    def buttonLogoClick(self, event):

        self.on_closing()
        
    def run(self):

        self.demarrerServeur()
        
        while not self.lafin:
    
            self.root.update_idletasks()
            self.root.update()
            #print(f"self.message_queues_reception == {self.message_queues_reception}")
            for s in self.message_queues_reception :
                while not self.message_queues_reception[s].empty():
                    data = self.message_queues_reception[s].get_nowait()
                    print("Données GUI reçues!" + data)
                    self.majGUI(data)
            time.sleep(0.01)

        self.arreterServeur()
        
        self.root.quit()

    def majGUI(self, data):
        try :
            dataSplit = data.split(':')
            print(dataSplit)
            if dataSplit[0].isnumeric() and (int(dataSplit[0]) >= self.nbVoteurs) :
                tk.messagebox.showinfo("Attention!", f"Le voteur {dataSplit[0]} a transmis son vote mais il ne fait pas partie des voteurs autorisés.")
            elif dataSplit[1].isnumeric() and (int(dataSplit[1]) >= len(self.parametres["couleurs_votes"])) :
                tk.messagebox.showinfo("Attention!", f"Le voteur {dataSplit[0]} a transmis un vote qui ne fait pas partie des choix proposés.")
            elif dataSplit[0].isnumeric() and dataSplit[1].isnumeric() :
                self.afficherVoteur(dataSplit[0], int(dataSplit[1]))

        except Exception as e :
            print("Erreur : Mauvais format de données reçu! " + str(e))
        
    def on_closing(self):

        if tk.messagebox.askokcancel("Terminé ?", "Est-ce que vous voulez fermer le programme ?"):

            self.lafin = True
            time.sleep(1)

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
logging.info("Main    : Début du programme")

if len(sys.argv) > 1 :
    try :
        application = appVote("1190x750+225+150", sys.argv[1])
    except Exception as e:
        tk.messagebox.showinfo("Erreur!", f"Le fichier de configuration reçu comme paramètre {sys.argv[1]} ne peut être utilisé. Le programme termine prématurément. Erreur : {e}", )
        sys.exit()
else:
    application = appVote("1190x750+225+150")
application.run()

    

    
