**Exploration des Statistiques des Joueurs NBA 2023-2024 : Projet data engineer**

La National Basketball Association (NBA) représente aujourd'hui le plus haut niveau de compétition de basketball dans le monde. 
Avec de plus en plus de passionées qui la suit au quotidien, le niveau de spectacle ne fait qu'augmenter avec des joueurs qui sortent de 
plus en plus d'énormes performance. Ces statistiques nous offrent un aperçu unique de la manière dont chaque joueur contribue à la saison de son équipe et influence le cours des matchs.

Notre projet se consacre à la découverte des statistiques des joueurs de la saison 2023-2024. En utilisant des techniques de scrapping de données avancées avec Scrapy, nous collecterons les données relatives à chaque joueur, des points marqués aux rebonds, en passant par les passes décisives et bien plus encore. Ces informations seront ensuite stockées de manière organisée dans une base de données MongoDB.
Notre projet intègrera également la création d'une application web interactive à l'aide de Flask. Cette application permettra de suivre l'évolution du niveau des joueurs au fil de la saison, et de dégager des tendances significatives.


***Comment récuperer notre projet sur Github et le mettre sur Docker:***

Pour récupérer notre projet sur Gitbhub vous devrez ouvrir git puis aller au niveau du répertoire où vous voulez retrouvez le projet et enfin lancer une des deux commandes suivantes:

 -  avec une clé ssh: $ git clone git@github.com:adrien-ldg/data_engineer.git

 -  avec https: $ git clone https://github.com/adrien-ldg/data_engineer.git 

Ensuite, vous n'avez plus qu'à rentre votre mot de passe et vous retrouvez notre projet sur votre machine local.

Maintenant, il faut mettre notre projet sur docker. Pour cela, on a décidé de créer trois containers différents: un container qui lance le scrapping des données et le met dans une database mongo (nba_player_scrap), un container mongo (mongodb_nba_player) et un dernier container qui lance notre application flask (nba_player_flask). Pour cela, nous avons eu besion de créer un fichier yml pour relier nos trois containeurs et deux fichiers Dockerfile, chacun gérant soit le scrapping soit flask.
Ainsi, l'arborescence de nos fichiers est:

Projet ---- docker-compose.yml
        |
        |-- scrapy --- Dockerfile
        |
        |-- flask --- Dockerfile

Le fichier docker-compose.yml spécifie trois services principaux, correspondant aux trois conteneurs:

nba_player_scrap : Ce service utilise une image Docker construite à partir du Dockerfile situé dans le répertoire "scrapy". Il est responsable, à partir d'une image de base Python 3, de l'installation des bibliothèques nécessaires présentes dans un fichier requirements.txt. Ensuite, il lance le processus de scraping des données et les insère dans une base de données MongoDB.

mongodb_nba_player : Ce service utilise l'image officielle de MongoDB. Il représente le conteneur de la base de données MongoDB où les données scrappées seront stockées. MongoDB sera accessible sur le port 27017.

nba_player_flask : Ce service utilise une image Docker construite à partir du Dockerfile situé dans le répertoire "flask". Il est responsable, à partir d'une image de base Python 3, de l'installation des bibliothèques nécessaires présentes dans un fichier requirements.txt. Ensuite, il lance l'application Flask qui utilise les données de la base MongoDB. Le conteneur sera accessible sur le port 5000.

Le fichier docker-compose.yml définit également les dépendances entre ces services. Par exemple, le service "nba_player_scrap" dépend du service "mongodb_nba_player" pour stocker les données scrappées dans la base de données.

Pour mettre en place les containers dockers vous avez juste ouvrir un powershell et au niveau du répertoire Projet lancer la commande:

 -  $ docker compose up --build

Avant d'aller sur l'application flask, il faut attendre quelques minutes que le containeur nba_player_scrap est finit le scrapping des données afin que l'application flask est accès à toutes les données.
Le scrapping dure une dizaine de minutes car il y a beaucoup de requêtes différentes (+500 différentes) et pour éviter d'être éjecter de certains url on a décidé d'attendre une seconde entre chaque requête.

***Scrapping des données:***

Dans un premier temps, nous avons cherché un site où l'on pourrait récupérer nos données. Nous sommes pas tout de suite partie sur la NBA.
Notre première idée était le site de l'ATPtour et récupérer différents classement sur le tennis (meilleures joueurs, serveurs, retourneurs...). Cependant le site de l'ATP n'était scrappable et nous nous sommes donc tourné vers la NBA. Nous avons trouvé un site qui regroupé les stats des franchises et des joueurs et après réflexion, nous sommes partis sur les stats de tout les joueurs NBA sur l'année 2023-2024 car cela représentait une plus grosse quantité de données et donc un projet plus ambitieux. Le domaine de notre site est: basketusa.com.

Les données des joueurs sont organisées en fonction de leurs franchises, nécessitant ainsi des requêtes distinctes sur 30 URL différentes, une par franchise de la NBA. Pour chaque joueur, nous récupérons ses statistiques telles que le temps de jeu moyen, le nombre moyen de points marqués, ou le nombre moyen de fautes commises. Ensuite, nous effectuons une nouvelle requête pour chaque joueur afin d'accéder à une page contenant des informations plus détaillées sur le joueur, telles que sa taille, son poids, son âge, etc. Cela nous fait au total un nombre de requêtes de plus de 500 urls différentes.

Une fois les données récupérées, nous les avons mit en forme grâce à des pipelines. Nous avont mis en place trois pipelines différentes par l'aquelle chaque item passé. La première pipeline met sous la forme textuelle désiré tout les items puis la deuxième transforme certaines champs en int ou float (age, nombre de points par match...). La dernière pipeline automatise l'ajout de tout nos items dans une database mongo. Au final, on se retrouve avec une database de plus de 500 documents différents avec chacun plus de 20 champs.

La récupération des données se fait par la commande *$scrapy crawl nba_player* dans un powershell dans le repertoire du spider.
On retrouve les données dans la database basket puis la collection nba_player dans mongoDB. Cependant, cela se fait automatiquement en lançant le containeur nba_player_scrap que vous avez créé précédemment.

***Application Flask:***

Pour notre application web, nous avons décidé de partir sur Flask qui est un framework web Python qui fournit une configuration, des conventions et des outils pour créer et déployer des applications web.

Notre application comprend trois routes distinctes, chacune dédiée à une page spécifique :

- "/" (Page d'accueil) : Cette page fournit une introduction à l'objectif de notre application. Elle sert de point d'entrée où les utilisateurs peuvent comprendre la raison d'être de l'application.

- "/top10" (Classements) : Sur cette page, les utilisateurs peuvent visualiser les meilleurs joueurs de la NBA en fonction de la statistique de leur choix (le joueur doit avoir jouer au minimum pour être éligible au classement). Un premier Dropdown permet à l'utilisateur de sélectionner la statistique souhaitée tandis que le deuxième lui permet de choisir la franchise, affichant le top des joueurs pour la saison 2023-2024 selon la statistique et la franchise choisie.

- "/graphs" (Page des graphiques) : Cette page présente divers graphiques mettant en avant différentes caractéristiques des joueurs de la ligue. Les graphiques incluent par exemple la répartition des nationalités des joueurs ou la distribution des joueurs dans les franchises en fonction de leur nombre de points. Les graphiques ont tous été fait avec la librairie pyplot.

Pour faciliter la navigation, une barre de navigation est mise en place, permettant à l'utilisateur de passer d'une page à l'autre facilement.

Maintenant, que nous avons expliqué le fonctionnement de notre application, on va présenter comment nous l'avons mit en place.
Pour le développement de notre application Flask, nous avons fait appel à un ensemble de bibliothèques et méthodes afin de créer une application dynamique et interactive. Tout d'abord, Flask, en tant que framework web Python, a été la base de notre application, nous fournissant les outils pour la gestion des routes et de nombreuses fonctionnalités. La méthode render_template de Flask a été utilisée pour générer des pages web dynamiques à partir de modèles HTML et css.

L'objet request de Flask a été aussi essentiel pour accéder aux données envoyées par les utilisateurs via des requêtes HTTP. Cela nous a permis de récupérer des choix de statistiques, par exemple, sur la page "/top10". La fonction jsonify de Flask a facilité le retour de données structurées sous format JSON.

La bibliothèque pymongo a été utilisée pour interagir avec MongoDB depuis Flask, permettant la récupération de données scrappées et leur présentation dynamique sur notre site. Plotly a été utilisée pour créer des graphiques interactifs sur la page "/graphs", mettant en évidence différentes caractéristiques des joueurs de la ligue.

Le module os avec la méthode os.getenv nous a permis de récupérer en toute sécurité la valeur de la variable d'environnement "MONGO_URI". Cela a permis d'établir une connexion sécurisée à MongoDB en stockant l'URI de la base de données en dehors du code source.
