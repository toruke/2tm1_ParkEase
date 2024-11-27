# 2tm1_ParkEase
## Description du déroule du programme :

Le programme s'exécute via l'invite de commande Windows avec la version 3.12 de python.
Voici le résultat de la commande: "python main.py -h" (exécuté à l'emplacement du fichier "main.py")


usage: main.py [-h] [-m MANAGEMENT MANAGEMENT] [-s] [-sub SUBSCRIPTION]


Parking manager


options:

  -h, --help            show this help message and exit
  
  -m MANAGEMENT MANAGEMENT, --management MANAGEMENT MANAGEMENT
  
                        First value, the state of the car you want to manage: ["in", "out"], second value, his plate: str
                        
  -s, --spaces          Show how many spaces are available.
  
  -sub SUBSCRIPTION, --subscription SUBSCRIPTION
  
                        Requires the plate number of the car for which you want to manipulate the subscription.
