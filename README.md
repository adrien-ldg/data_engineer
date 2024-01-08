**Exploration des Statistiques des Joueurs NBA 2023-2024 : Projet data engineer**

La National Basketball Association (NBA) représente aujourd'hui le plus haut niveau de compétition de basketball dans le monde. 
Avec de plus en plus de passionées qui la suit au quotidien, le niveau de spectacle ne fait qu'augmenter avec des joueurs qui sortent de 
plus en plus d'énormes performance. Ces statistiques nous offrent un aperçu unique de la manière dont chaque joueur contribue à la saison de son équipe et influence le cours des matchs.

Notre projet se consacre à la découverte des statistiques des joueurs de la saison 2023-2024. En utilisant des techniques de scrapping de données avancées avec Scrapy, nous collecterons les données relatives à chaque joueur, des points marqués aux rebonds, en passant par les passes décisives et bien plus encore. Ces informations seront ensuite stockées de manière organisée dans une base de données MongoDB.
Notre projet intègrera également la création d'une application web interactive à l'aide de Flask. Cette application permettra de suivre l'évolution du niveau des joueurs au fil de la saison, et de dégager des tendances significatives.


***Comment récuperer notre projet avec docker:***





***Scrapping des données:***

Dans un premier temps nous avons cherché un site où l'on pourrait récupérer nos données. Nous sommes pas tout de suite partie sur la NBA.
Notre première idée était le site de l'ATPtour et récupérer différents classement sur le tennis (meilleures joueurs, serveurs, retourneurs...). Cependant le site de l'ATP n'était scrappable et nous nous sommes tourné vers la NBA. Nous avons trouvé un site qui regroupé les stats des franchises et des joueurs et après réflexion, nous sommes partis sur les stats de tout les joueurs NBA de l'année 2023-2024 car cela représentait une plus grosse quantité de données et donc un projet plus ambitieux. Le domaine de notre site est: basketusa.com.

Les données des joueurs sont organisées en fonction de leurs franchises, nécessitant ainsi des requêtes distinctes sur 30 URL différentes, une par franchise de la NBA. Pour chaque joueur, nous récupérons ses statistiques telles que le temps de jeu moyen, le nombre moyen de points marqués, ou le nombre moyen de fautes commises. Ensuite, nous effectuons une nouvelle requête pour chaque joueur afin d'accéder à une page contenant des informations plus détaillées sur le joueur, telles que sa taille, son poids, son âge, etc. Cela nous fait au total un nombre de requêtes sur plus de 500 urls différentes.

Une fois les données récupérées, nous les avons mit en forme grâce à des pipelines. Nous avont mis en place trois pipelines différentes par l'aquelle chaque item passé. La première pipeline met sous la forme textuelle désiré tout les items puis la deuxième transforme certaines champs en int ou float (age, nombre de points par match...). La dernière pipeline automatise l'ajout de tout nos items dans une database mongo.

La récupération des données se fait par la commande *$scrapy crawl nba_player* dans un powershell dans le repertoire du spider.
On retrouve les données dansla database basket puis la collection nba_player dans mongoDB.