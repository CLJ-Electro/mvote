# vote

Ce script permet de recevoir les votes d'un groupe de personnes et d'afficher le résultat à l'écran. La figure ci-dessous présente l'interface utilisateur préliminaire.

![image](https://github.com/CLJ-Electro/mvote/assets/171524994/655b5935-55b6-4a62-b8e9-fe41adc3e437)

Le panneau à gauche de l'application permet d'identifier les voteurs et leur vote. Cette section peut être configurée à l'aide des paramètres suivants dans le fichier "config.json" :
  - "nb_voteurs" : Ce paramètre permet de définir le nombre total de voteurs à considérer;
  - "nb_colonnes": Définit le nombre de colonnes présentes dans le panneau gauche;
  - "nb_rangees" : Définit le nombre de rangées présentes dans le panneau gauche

Le panneau droit est utilisé pour contrôler le début et la fin du vote et pour afficher le résultat du vote.

Le paramètre "port_tcp_serveur" du fichier de configuration est utilisé pour définir le port tcp sur lequel le serveur écoute. La valeur par défaut est le port 1234.

Mise en route du programme

1- Dand un terminal, créer votre répertoire de travail dans votre répertoire personnel et positionner votre répertoire de travail à cet endroit.

└─$ mkdir Tel-git
                                                                       
└─$ cd Tel-git 

2- Récupérer les fichiers du programme mvote
                                                                       
└─$ git clone https://github.com/CLJ-Electro/mvote.git 

Cloning into 'mvote'...
remote: Enumerating objects: 45, done.
remote: Counting objects: 100% (45/45), done.
remote: Compressing objects: 100% (30/30), done.
remote: Total 45 (delta 18), reused 39 (delta 14), pack-reused 0
Receiving objects: 100% (45/45), 706.73 KiB | 442.00 KiB/s, done.
Resolving deltas: 100% (18/18), done.

3- Déplacer votre répertoire de travail dans le répertoire "mvote" nouvellement créé :

└─$ cd mvote   

4- Lancer l'exécution du programme avec la commande suivante :                                                                        
└─$ python main.py

10:46:24: Main    : Début du programme
image_width == 1184
image_height == 164
                   
Un dialogue apparaît alors afin de demander quel fichier de configuration l'usager veut utiliser. L'usager doit alors choisir le fichier de configuration désiré. Cela permet à plusieurs enseignants d'utilser une configuration différente pour chaque cours. Si l'usager appuie sur la touche [Esc] du clavier, ou après un délai de 10 secondes, le programme démarre en utilisant le fichier de configuration "config.json".

![image](https://github.com/CLJ-Electro/mvote/assets/171524994/61d5678b-3e8d-4cfa-8959-b048dece805c)

 

