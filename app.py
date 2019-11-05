from bin.api import ApiRetriever, DataCleaner
from bin.database import DatabaseBuilder, Information, Product, StoreProduct, \
                         SaveProduct, Store, Substitute, DatabaseHandler
from bin.interface import UserUx, Drawer
import time


class Application:
    """run the application"""

    def run(self):
        """run the application"""
        categories = ["Fromage", "Biscuits", "Pizzas", "Conserves"]
        userux = UserUx()
        userux.welcome()
        dbbuilder = DatabaseBuilder()
        dbbuilder.create_tables()
        dh = DatabaseHandler()
        exist = dh.status_db()
        if exist == 0:
            for category in categories:
                print("Chargement des informations pour la categorie \
                      {}".format(category))
                api = ApiRetriever()
                raw_data = api.get_data(category)
                cleaner = DataCleaner()
                cleaner.realcleaner(raw_data)
                dbbuilder.init_category(category)
                for prdt in cleaner.data_save:
                    stores = Store()
                    stores.insert_store(prdt)
                    products = Product()
                    products.insert_product(prdt, category)
                    for store in stores.store_list:
                        storeproduct = StoreProduct()
                        storeproduct.insert_storeproduct(prdt, store)
            dh.update_status_db()
        information = Information()
        cat_list = information.get_category()
        category = userux.select_category(cat_list)
        choice = userux.select_product(information.get_products(category))
        userux.show_product(information.get_info(choice))
        text = "Choisir un substitue ? 1-oui 2-non "
        substitue = userux.input_validator(text)
        if substitue == 1:
            substitute = Substitute()
            sub = substitute.search_sub(choice)
            sub_choice = userux.select_product(sub)
            userux.show_product(information.get_info(sub_choice))
            text = "Sauvegarder le produit ?  1-oui 2-non "
            save_p = userux.input_validator(text)
            if save_p == 1:
                save = SaveProduct()
                save.save(choice, sub_choice)
                userux.screen_size(save.read())
                drawer = Drawer()
                drawer.line()
            else:
                pass
        userux.goodbye()

def main():
    app = Application()
    app.run()


if __name__ == "__main__":
    main()
