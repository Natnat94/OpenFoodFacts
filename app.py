from module.api import ApiRetriever, DataCleaner
from module.database import (
    DatabaseBuilder, Information, Store, StoreProduct, SaveProduct, Product,
    Substitute, DatabaseHandler
)
from module.interface import UserUx, Drawer


class Application:
    """run the application"""

    def run(self):
        """run the application"""
        categories = ["Boissons gazeuses",
                      "Biscuits secs",
                      "Quiches",
                      "Chips",
                      "Gratins",
                      "Yaourts à la framboise"]
        userux = UserUx()
        userux.welcome()
        dbbuilder = DatabaseBuilder()
        dbbuilder.create_tables()
        dh = DatabaseHandler()
        exist = dh.status_db()
        if exist == 0:
            for category in categories:
                print(f"Chargement des informations pour {category}")
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
        text = "Souhaitez vous chercher un produit ? (1) "\
               "ou voir vos sauvegardes (2) "
        choice = userux.input_validator(text)
        if choice == 1:
            information = Information()
            cat_list = information.get_category()
            category = userux.select_category(cat_list)
            product = userux.select_product(information.get_products(category))
            userux.show_product(information.get_info(product))
            text = "Choisir un substitue ? oui(1) ou non(2) "
            choice = userux.input_validator(text)
            if choice == 1:
                sub = Substitute()
                sub = sub.search_sub(product)
                sub_choice = userux.select_product(sub)
                userux.show_product(information.get_info(sub_choice))
                text = "Sauvegarder le produit ?  oui(1) ou non(2) "
                choice = userux.input_validator(text)
                if choice == 1:
                    save = SaveProduct()
                    save.save(product, sub_choice)
                    saved = save.read()
                    userux.screen_size(saved[0])
                    drawer = Drawer()
                    drawer.line()
                    text = "Chercher un nouveau produit ?  oui(1) ou non(2) "
                    choice = userux.input_validator(text)
                    if choice == 1:
                        main()
            else:
                text = "Chercher un nouveau produit ?  oui(1) ou non(2) "
                choice = userux.input_validator(text)
                if choice == 1:
                    main()
        elif choice == 2:
            save = SaveProduct()
            save, product, sub_prdt, length = save.read()
            userux.screen_size(save)
            drawer = Drawer()
            drawer.line()
            text = "Chercher un nouveau produit (1) ou " \
                   "consulter un produit sauvegardé (2) " \
                   "ou quitter le programme (3)"
            choice = userux.input_validator(text, 4)
            if choice == 1:
                main()
            elif choice == 2:
                text = "Quel produit souhaitez vous consulter ? "
                pr_num = userux.input_validator(text, length + 1)
                information = Information()
                userux.show_product(information.get_info(product[pr_num]))
                text = "voir le substitue ? oui (1) non (2) "
                choice = userux.input_validator(text)
                if choice == 1:
                    userux.show_product(information.get_info(sub_prdt[pr_num]))
                    text = "Chercher un nouveau produit ? oui(1) ou non(2)"
                    choice = userux.input_validator(text)
                    if choice == 1:
                        main()
        userux.goodbye()


def main():
    app = Application()
    app.run()


if __name__ == "__main__":
    main()
