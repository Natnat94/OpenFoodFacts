# OpenFoodFacts (Project 5)
> Utilisez les données publiques de l'OpenFoodFacts


La startup Pur Beurre travaille connait bien les habitudes alimentaires françaises. Leur restaurant, Ratatouille, remporte un succès croissant et attire toujours plus de visiteurs sur la butte de Montmartre.

L'équipe a remarqué que leurs utilisateurs voulaient bien changer leur alimentation mais ne savaient pas bien par quoi commencer. Remplacer le Nutella par une pâte aux noisettes, oui, mais laquelle ? Et dans quel magasin l'acheter ? Leur idée est donc de créer un programme qui interagirait avec la base Open Food Facts pour en récupérer les aliments, les comparer et proposer à l'utilisateur un substitut plus sain à l'aliment qui lui fait envie.

## Installation

Téléchargez l'application à partir de Github puis utilisez dans votre environnement virtuel :
```sh
pipenv install
```
La base de données doit s'appeler **"projet5"** et l'id d'utilisateur doit être stocké dans la variable d'environnement **'DATABASE_USER'** et le mot de passe dans **'DATABASE_PASSWORD'**

## Changelog:

### Version 1.0:

   Houray ! Le programme est entièrement fonctionnel !  
   On peut chercher un produit désiré parmi une liste de catégories, voir les informations le concernant, trouver un substitut et l’enregistré afin de le retrouver plus facilement la prochaine fois.
