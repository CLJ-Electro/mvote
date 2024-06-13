# vote

Ce script permet de recevoir les votes d'un groupe de personnes et d'afficher le résultat à l'écran. La figure ci-dessous présente l'interface utilisateur préliminaire.

![image](https://github.com/CLJ-Electro/mvote/assets/171524994/655b5935-55b6-4a62-b8e9-fe41adc3e437)

Le panneau à gauche de l'application permet de définir et d'identifier les voteurs. Cette section peut être configurée à l'aide des paramètres suivants dans le fichier "config.json" :
  - "nb_voteurs" : Ce paramètre permet de définir le nombre total de voteurs à considérer;
  - "nb_colonnes": Définit le nombre de colonnes présentes dans le panneau gauche;
  - "nb_rangees" : Définit le nombre de rangées présentes dans le panneau gauche

Le panneau droit est utilisé pour contrôler le début et la fin du vote et pour afficher le résultat du test.

Le paramètre "port_tcp_serveur" du fichier de configuration est utilisé pour définir le port tcp sur lequel le serveur écoute. La valeur par défaut est le port 1234.
