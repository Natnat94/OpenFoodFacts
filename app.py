from bin.api import *
from bin.database import *
from bin.interface import *
import time


class Application:

    def run(self):
        """run the application"""
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
        dbbuilder.create_tables()
        exist = dh.status_db()
        if exist == 0:
            for category in categories:
                print("Chargement des informations pour la categorie \
                      {}".format(category))
                raw_data = api.get_data(category)
                cleaner.realcleaner(raw_data)
                dbbuilder.init_category(category)
                for prdt in cleaner.data_save:
                    stores.insert_store(prdt)
                    products.insert_product(prdt, category)
                    for store in stores.store_list:
                        storeproduct.insert_storeproduct(prdt, store)
        cat_list = information.get_category()
        category = userux.select_category(cat_list)
        choice = userux.select_product(information.get_products(category))
        userux.show_product(information.get_info(choice))
        choix = int(input("choisir un substitue ? 1-oui 0-non "))
        if choix == 1:
            sub = substitute.search_sub(choice)
            sub_choice = userux.select_product(sub)
            userux.show_product(information.get_info(sub_choice))
            time.sleep(2)
            save_p = int(input("sauvegarder le produit ?"))
            if save_p == 1:
                save.save(choice, sub_choice)
                userux.screen_size(save.read())
                drawer.line()
            else:
                pass


def main():
    app = Application()
    app.run()


if __name__ == "__main__":
    main()
