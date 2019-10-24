from api import ApiRetriever, DatabaseHandler, DatabaseBuilder


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
    apiret = ApiRetriever()
    datab = DatabaseHandler()
    dbbuilder = DatabaseBuilder()
    dbbuilder.store()
    dbbuilder.category()
    dbbuilder.product()
    dbbuilder.storeproduct()
    dbbuilder.productsaved()
    datab.initdata()
    apiret.url_builder()
    #apiret.content_viewer()
    apiret.ccleaner()
    #datab.inserintodb2(apiret.storefilter(apiret.data_save))
    #datab.inserintodb3('franprix')
    for i in range(50):
        datab.inserintodb2(apiret.storefilter(apiret.data_save[i]))
        datab.inserintodb(apiret.data_save[i]['id'], apiret.data_save[i]['product_name_fr'], apiret.data_save[i]['url'], apiret.data_save[i]['nutrition_grade_fr'])
        for c in apiret.storefilter(apiret.data_save[i]):
            store = datab.inserintodb3(c)
            datab.inserintodb4(apiret.data_save[i]['id'], store)
    #datab.viewdb()


if __name__ == "__main__":
    main()
