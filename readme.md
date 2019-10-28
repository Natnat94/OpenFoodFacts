24/09/1019 debut du projet 5


11/10/2019

  - l'api fonctionne
  - il y a une fonction de nettoyage des infos recu par l'api
  - les infos sont enregistré dans la base de donné que si il y a un lien

  ---> probleme :
     * des signes chinois apparaissent et ne sont pas lisible par la base de donné
     * utf8md3 ne fonctionne pas
     * je n'arrive pas a crée un user pour la database
     * lorsque la fonction de filtre fonctione, elle n'efface pas toute la ligne mais insert la valeur de la ligne precedente

  ---> a faire:
     * choisir les données necessaire
     * crée une fonction qui classe dans quelle table enregistrer les infos
     * definir la structure de la base de données

23/10/2019

  - la base de donné se créé toute seule
  - ajout des fonctions d'ajout de donnée au table: 'product', 'store', 'storeproduct'
  - une fonction detecte l'id du magasin correspondant au produit


  ---> a faire:
    * gerer mes erreures lors de l'insertion de donné afin d'annuler toute la ligne si il y a eu un pb
    * cree une fonction qui detecte les espaces dans les noms des magasin et qui les retire avant de les mettre dans la DB
    * cree une fonction pour attribué la bonne categorie au produit

  ---> probleme:
    * une erreur "KeyError:" apparait de temps en temps lors du chargement des donnée de l'api
