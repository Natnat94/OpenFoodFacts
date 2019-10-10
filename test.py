from api import ApiRetriever, DatabaseHandler


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
    apiret.url_builder()
    #apiret.content_viewer()
    apiret.ccleaner()
    for i in range(20):
        datab.inserintodb(apiret.data_save[i]['brands'], apiret.data_save[i]['product_name'], apiret.data_save[i]['link'])
    datab.viewdb()


if __name__ == "__main__":
    main()
