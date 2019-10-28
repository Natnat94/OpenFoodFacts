from api import ApiRetriever, Product, Store, StoreProduct, DatabaseBuilder, DataCleaner


#for i in range(5):
#    tdata= data["products"][i]
    #pprint(tdata)
    #for key, value in tdata.items():
        #if isinstance(value, list) and len(value)>0:
        #    print("{} ---> {}".format(key, value[0]))
    #    pprint(key,value)
#    for key in cles:
#        pprint(tdata[key])

def main():
    api = ApiRetriever()
    data = api.get_data()
    dbbuilder = DatabaseBuilder()
    store= Store()
    product= Product()
    storeproduct= StoreProduct()
    dbbuilder.create_tables()
    cleaner= DataCleaner()
    cleaner.realcleaner(data)
    state = True
    category = api.research['tag_0']
    if state:
        for i in cleaner.data_save:
            store.insert_store(i)
            product.insert_product(i['id'], i['product_name_fr'], i['url'], i['nutrition_grade_fr'], category)
            for c in store.store_list:
                storeproduct.insert_storeproduct(i['id'], c)
        print(product.erreur_count)
        print(store.erreur_count)

if __name__ == "__main__":
    main()
