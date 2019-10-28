from api import ApiRetriever, Product, Store, StoreProduct, \
    DatabaseBuilder, DataCleaner


def main():
    api = ApiRetriever()
    cleaner = DataCleaner()
    dbbuilder = DatabaseBuilder()
    stores = Store()
    products = Product()
    storeproduct = StoreProduct()
    raw_data = api.get_data()
    dbbuilder.create_tables()
    cleaner.realcleaner(raw_data)
    state = True
    category = api.research['tag_0']
    if state:
        for prdt in cleaner.data_save:
            stores.insert_store(prdt)
            products.insert_product(prdt, category)
            for store in stores.store_list:
                storeproduct.insert_storeproduct(prdt, store)
        # print(products.erreur_count)
        # print(stores.erreur_count)


if __name__ == "__main__":
    main()
