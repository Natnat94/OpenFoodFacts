from bin.api import *
from bin.database import *
from bin.interface import *
import time
import json


def main():
    api = ApiRetriever()
    cleaner = DataCleaner()
    dbbuilder = DatabaseBuilder()
    substitute = Substitute()
    stores = Store()
    userux = UserUx()
    dh = DatabaseHandler()
    save = SaveProduct()
    drawer = Drawer()
    information = Information()
    products = Product()
    storeproduct = StoreProduct()
    categories = ["Fromage", "Biscuits", "Pizzas", "Conserves"]
    userux.welcome()
    exist = dh.status_db()
    # debut du programme
    if exist == 0:
        for category in categories:

            # utilisation de l'api et nettoyage des données
            print("Chargement des informations pour la categorie {}".format(category))
            raw_data = api.get_data(category)
            cleaner.realcleaner(raw_data)

            # sauvegarde des données dans un fichier JSON
            with open('products.json','w') as f:
                json.dump(cleaner.data_save, f, indent=2)

            # creation des tables
            dbbuilder.create_tables(category)
            # Boucle de remplissage de la base de données
            for prdt in cleaner.data_save:
                stores.insert_store(prdt)
                products.insert_product(prdt, category)
                for store in stores.store_list:
                    storeproduct.insert_storeproduct(prdt, store)

    # selection d'un produit dans base de données
    cat_list = information.get_category()
    category = userux.select_category(cat_list) # selection de la categorie désirée
    choice = userux.select_product(information.get_products(category)) #selection du produit désiré a partir d'une liste
    userux.show_product(information.get_info(choice)) #récuperation et affichage du produit choisie
    choix = int(input("choisir un substitue ? 1-oui 0-non "))
    if choix == 1:
        # selection d'un produit substitue dans la base de données
        sub = substitute.search_sub(choice)
        sub_choice = userux.select_product(sub)
        userux.show_product(information.get_info(sub_choice))
        time.sleep(2)
        save_p = int(input("sauvegarder le produit ?"))
        if save_p == 1:
            # sauvegarde le produit et son substitue dans la base de donnée
            save.save(choice, sub_choice)
            userux.screen_size(save.read())
            drawer.line()
        else:
            pass

if __name__ == "__main__":
    main()
