from api import ApiRetriever, Product, Store, StoreProduct, \
    DatabaseBuilder, DataCleaner, Information, UserUx
import json

def main():
    api = ApiRetriever()
    cleaner = DataCleaner()
    dbbuilder = DatabaseBuilder()
    stores = Store()
    userux = UserUx()
    information = Information()
    products = Product()
    storeproduct = StoreProduct()
    raw_data = api.get_data()
    w_into_db = True
    use_api = True
    w_into_file = False
    r_into_db = True

    # debut du programme
    if use_api:
        # utilisation de l'api et nettoyage des données
        cleaner.realcleaner(raw_data)

    if w_into_file:
        # sauvegarde des données dans un fichier JSON
        with open('products.json','w') as f:
            json.dump(cleaner.data_save, f, indent=2)
    category = api.research['tag_0']

    if w_into_db:
        # creation des tables
        dbbuilder.create_tables()
        # Boucle de remplissage de la base de données
        for prdt in cleaner.data_save:
            stores.insert_store(prdt)
            products.insert_product(prdt, category)
            for store in stores.store_list:
                storeproduct.insert_storeproduct(prdt, store)
        # print(products.erreur_count)
        # print(stores.erreur_count)

    if r_into_db:
        # selection d'un element de la base de données
        choice = userux.select_product(information.get_products())
        userux.show_product(information.get_info(choice))

if __name__ == "__main__":
    main()
