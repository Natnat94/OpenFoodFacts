from bin.api import *
from bin.database import *
from bin.interface import *
import json
import tablib
from pprint import pprint

def main():
    api = ApiRetriever()
    cleaner = DataCleaner()
    dbbuilder = DatabaseBuilder()
    substitute = Substitute()
    stores = Store()
    userux = UserUx()
    save = SaveProduct()
    drawer = Drawer()
    information = Information()
    products = Product()
    storeproduct = StoreProduct()
    categories = ["Aliments pour bébé", "Biscuits", "Pizzas", "Conserves"]
    use_api = int(input("use the api ? 1-yes 0-no "))
    w_into_db = int(input("write into the DB ? 1-yes 0-no "))
    w_into_file = int(input("write into the JSON file ? 1-yes 0-no "))
    r_into_db = int(input("read into the DB ? 1-yes 0-no "))
    userux.welcome()

    # debut du programme
    for category in categories:

        if use_api == 1: # READY DO NOT TOUCH !!
            # utilisation de l'api et nettoyage des données
            print("utilisation de l'api pour {}".format(category))
            raw_data = api.get_data(category)
            cleaner.realcleaner(raw_data)

        if w_into_file == 1: # READY DO NOT TOUCH !!
            # sauvegarde des données dans un fichier JSON
            with open('products.json','w') as f:
                json.dump(cleaner.data_save, f, indent=2)

        if w_into_db == 1: # READY DO NOT TOUCH !!
            # creation des tables
            dbbuilder.create_tables(category)
            # Boucle de remplissage de la base de données
            print("utilisation de la base de données")
            for prdt in cleaner.data_save:
                stores.insert_store(prdt)
                products.insert_product(prdt, category)
                for store in stores.store_list:
                    storeproduct.insert_storeproduct(prdt, store)
            # print(products.erreur_count)
            # print(stores.erreur_count)

    if r_into_db == 1: # READY DO NOT TOUCH !!
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

        # sauvegarde le produit et son substitue dans la base de donnée
        save.save(choice, sub_choice)
    userux.screen_size(save.read())
    drawer.line()

if __name__ == "__main__":
    main()
