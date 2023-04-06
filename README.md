# Bienvenue sur le projet SAE 4 Drones 

![figure0](images/iut_mulhouse.png)

### Equipe : Alexandre BADER / Kévin TRAN / Romain KLEINKLAUS / Aklaa MAYABA

### Référents : M. Eric HUEBER / M. Benjamin MOURLLION 



## Guide d'installation et de fonctionnement de notre SAE


### Installation et initialisation du matériel 

Nous allons commencer par installer le matériel du kit Crazyflie qui nous a été fournit. (https://store.bitcraze.io/products/the-swarm-bundle?variant=39540519206999)

- Commencer par charger les drône à l'aide d'un câble micro USB 
> 40 minutes de charge pour passer de 0% à 100%

> 7 minutes de temps de vol avec une charge complète du drone

#### Installation des balises pour l'initialisation du Loco positioning System (LPS)

- Placer les 8 balises de position dans la salle B019.


![figure0](images/plan_balises.jpg)

> L'échelle du repère est en mètre.
> Les balises 3 et 5 sont positionnées sur les 2 tableaux blancs présents dans la salle.

- Connecter les modules aux batteries externes.

![figure1](images/module_loco_zoom.jpg)

> Il faudra utiliser un câble USB vers micro USB pour alimenter les balises. 

#### Initialisation des drônes
- Appuyer sur le bouton de mise en marche / d'arrêt du drone, celui-ci s'initialise.

> On peut désormais s'y connecter depuis un PC, un téléphone ou une tablette

![figure2](images/bouton_allumage_drone.jpg)



### Commande des drones à distance

![figure5](images/overview_clientsoftware.jpg)

> La communication entre les drones et les appareils utilisant le client Crazyflie se fait, sois grâce à la Crazyradio PA connecté à un PC en USB ou avec le protocole de communication Bluetooth LE. (Plus d'informations sur https://www.bitcraze.io/documentation/system/client-and-library/)


#### Utilisation du Crazyflie Client


Il est possible de contrôler et visualiser les différentes données envoyées par le drone et les balises en passant par le client fournis par Crazyflie. Ce client est disponible sur le Github de Crazyflie (https://github.com/bitcraze/crazyflie-clients-python). Il existe différentes versions pouvant être exécutées sur différentes plateformes comme un PC sous Windows, Linux ou Mac et des appareils sous Android ou iOS. Nous nous intéresserons au client réservé à l'utilisation sur un PC.

> Le tutoriel concernant les étapes d'installation de ce client est détaillé sur ce site : https://github.com/bitcraze/crazyflie-clients-python/blob/master/docs/installation/install.md

![figure3](images/crazyflie_client.png)

Sur le client, des informations concernant les drones et les balises peuvent être visualisées comme les valeurs du gyroscope du drone, sa batterie ou encore la puissance délivrée à chaque moteur en temps réel. Il est également possible de configurer la position des balises sur un plan en 3D et de visualiser la position du drone en temps réel dans ce plan. 
De plus, il est possible de contrôler le drone en temps réel dans l'espace ainsi que de le faire décoller et atterrir à l'aide de boutons physiques sur le client, ou d'une manette Xbox One connectée en USB au PC, qui nous a été fournit au début du projet.


#### Utilisation d'un programme Python


Il est également possible d'utiliser la librairie de fonctions codé en Python disponible sur le Github de Crazyflie (https://github.com/bitcraze/crazyflie-lib-python). En utilisant un compileur comme Visual Studio Code, on peut utiliser cette libairie pour contrôler et visualiser les données envoyées par le drone et les balises.

![figure4](images/code_python.png)

> Il est important de préciser qu'il n'est pas possible de se connecter à un drone Crazyflie depuis le Crazyflie Client et un compileur Python en même temps


## Performance des drones dans les airs

### A propos de la performance du drone dans les airs

#### Utilisation des fonctions de déplacement des drones de la librairie fournit

Lors de l'utilisation de fonctions permettant de déplacer le drone dans les airs sans l'exploitation de quelconques informartions de position, il faut préciser une commande de vitesse pour les moteurs lors de chaque déplacement. Le résultat de l'utilisation de ces fonctions n'est pas toujours le même, nous avons remarqué que le niveau du batterie d'un drone va influer sur la puissance délivrer au moteur quelque soit la commande de vitesse envoyée.
Il était donc très compliqué de stabiliser le drone dans les airs avec ces fonctions, les déplacements étant très instable et non précis, les fonctions créant un résultat différent à chaque exécution.

#### Utilisation des fonctions de déplacement exploitant la position du drone

Lors de l'utilisation de fonctions de déplacement exploitant la position du drone dans le plan crée par les balises, l'influence de la batterie sur la puissance délivrée au moteur ne nous posait plus autant de problème quant à la stabilisation du drone dans les airs et de la précision des déplacements.


### Graphiques des différents tests de performance

A COMPLETER

### Amélioration du système concernant la position

#### Etude de l'asservissement des drones Parrots
Nous avons, en parallèle à notre étude des drones Crazyflie, étudié les drones Parrots et leur fonctionnement sous Matlab. Cette étude, portant plus particulièrement sur l'asservissement d'un système, nous a permis d'en apprendre plus sur le principe d'asservissement d'un drone, nous permettant de nous inspirer quant à l'application d'un asservissement sur les drones Crazyflie en nous basant sur celui appliqué aux drones Parrots.

## Résultats du projet

### Images et vidéos du projet
1er test de vol en utilisant les fonctions sur Python :
https://www.youtube.com/shorts/r6u5RcOwqho

1er test de vol en utilisant la fonction linear motion qui permet de controller la velocité du vol :
https://youtube.com/shorts/18h9I9uDpAo

## Ressources annexes

