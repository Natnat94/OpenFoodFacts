#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from pprint import pprint
import os
import records
from sqlalchemy.exc import IntegrityError
import sqlscript as table
import html

class ApiRetriever:
    """this class purpose is to retrieve the information from the OpenFoodFacts API"""

    url = 'https://fr.openfoodfacts.org/cgi/search.pl?'

    def __init__(self):
        self.data = None
        self.research = {'search_terms':'',
                    'search_simple':'1',
                    'action':'process',
                    'json':'1',
                    'tagtype_0':'categories',
                    'tag_contains_0':'contains',
                    'tag_0':'Conserves',
                    'page_size': '250'}

    def get_data(self):
        """this method send a request to get the data researched from the API in JSON"""
        content = requests.get(self.url, params = self.research)
        self.data = content.json()
        return self.data

    def content_viewer(self):
        """this method allow to see the selected data from the API (BROKEN)"""
        cles = ['brands','categories','url','product_name_fr','stores','nutrition_grade_fr', 'id']
        for c in self.data["products"][i]:
            sdata = c
            print("---------------------------------------------")
            for key in cles:
                print("{} ----> {}".format(key, sdata[key]))

class DatabaseHandler:

    def __init__(self):
        """this init method connect between the program and the MySQL database"""
        DATABASE_URL= ("mysql+mysqlconnector://myuser:password@localhost/projet5?charset=utf8mb4")
        self.db= records.Database(DATABASE_URL)
        self.erreur_count = {'error1':0, 'error2':0, 'error3':0, 'error4':0}
        self.count = 0
        self.store_list = None
        self.products = None

class Product(DatabaseHandler):

    def insert_product(self, prdtid, prdtname, link, ntrscr, catg):
        """this method insert the productid, productname, link, nutriscore & category of a given product into the 'product' table"""
        try:
            self.db.query('INSERT INTO product (productid, productname, link, nutriscore, category) VALUES(:a, :b, :c, :d, :f)',
                    a= prdtid, b= prdtname, c= link, d= ntrscr, f= self.category_id(catg))
        except IntegrityError as e:
            #code = e.orig
            #if self.count < 3:
            #    print("pendant l'integration dans la table 'product': ")
            #    print(code)
            #    self.count = self.count + 1
            #else:
            #    pass
            self.erreur_count['error1'] +=  1

    def category_id(self, data):
        """this method return the category id related to the category name
            given from the method argument"""
        #retrouve l'id de la category rechercher sur la table 'category'
        truc = self.db.query('SELECT id FROM category WHERE category = :cat', cat = data)
        return truc[0].id

class Store(DatabaseHandler):

    def insert_store(self, product):
        #ajout les magasin dans la table 'store' si il n'existe pas deja a partir de la list de l'api
        self.store_list = self.storecleaner(product)
        for i in self.store_list:
            try:
                self.db.query('INSERT INTO store (store) VALUES(:store)',
                        store= i)
            except IntegrityError as e:
                code = e.orig
                #if self.count < 3:
                #    print("pendant l'integration dans la table 'store': ")
                #    print(code)
                #    self.count = self.count + 1
                #else:
                #    pass
                self.erreur_count['error2'] +=  1

    def storecleaner(self, data):
        """clean the string of stores received into a list and return it"""
        #doit parcourir la liste des magasin et eliminer les magasins qui ne sont pas ecrit en latin
        store = data['stores']
        store_list= store.split(",")
        for c in range(len(store_list)): #clean unwanted space before and after the store name
            store_list[c] = store_list[c].strip()
        return store_list

class StoreProduct(DatabaseHandler):

    def insert_storeproduct(self, productid, store):
        """this method insert the store id related to a product (id), receive
            the "product id" and the "store name" as argument into
            the 'storeproduct' table"""
        #doit inserer l'id du magasin lier au produit
        store_id = self.check_id(store)
        try:
            self.db.query('INSERT INTO storeproduct (productid, store) VALUES(:productid, :store)',
                    productid = productid, store= store_id)
        except IntegrityError as e:
            code = e.orig
            #if self.count < 3:
            #    print("pendant l'integration dans la table 'storeproduct': ")
            #    print(code)
            #    self.count = self.count + 1
            #else:
            #    pass
            self.erreur_count['error3'] +=  1

    def check_id(self, data):
        """this method return the store id related to the store name
            given from the method argument"""
        #retrouve l'id du magasin rechercher sur la table 'store'
        truc = self.db.query('SELECT id FROM store WHERE Store = :stores', stores = data)
        return truc[0].id

class DatabaseBuilder:
    """this class purpose is the create the database tables if they
        do not already exist"""

    def __init__(self):
        DATABASE_URL= ("mysql+mysqlconnector://myuser:password@localhost/projet5?charset=utf8mb4")
        self.db= records.Database(DATABASE_URL)

    def create_tables(self):
        """this method create the tables needed for the Database
            if they don't already exists"""
        self.db.query(table.store)
        self.db.query(table.category)
        self.db.query(table.product)
        self.db.query(table.storeproduct)
        self.db.query(table.productsaved)
        self.init_category()

    def init_category(self):
        """this method insert the data for the 'category' table if
            it is not already exists"""
        self.db.bulk_query("""INSERT IGNORE INTO category(Category) VALUES (:data1)""",
                            {"data1": "Aliments pour bébé"},
                            {"data1": "Biscuits"},
                            {"data1": "Pizzas"},
                            {"data1": "Conserves"})

class DataCleaner:

    def __init__(self):
        self.erreur_count = {'prob1' : 0,
                             'prob2' : 0,
                             'prob3' : 0,
                             'prob4' : 0}
        self.data2 = {}
        self.data_save = []

    def realcleaner(self, data):
        """This method role is to clean the data received from useless information"""
        for c in range(50): #self.data["products"]:
            i = data["products"][c]
            if self.isvalid(i):
                continue
            else:
                self.data_save.append(self.data2.copy())

    def isvalid(self, product):
        """this method role is to check if all the information needed exist and return True if an error occur"""
        #width = os.get_terminal_size().columns
        keys = ['brands','categories','url','product_name_fr','stores','nutrition_grade_fr', 'id']
        erreur = False
        self.data2 = {}
        for key in keys:
            data = product.get(key)
            if data:
                if product[key] == "":
                    erreur = True
                    self.erreur_count['prob1'] +=  1
                else:
                    self.data2[key] = html.unescape(product[key])
            else:
                self.erreur_count['prob2'] +=  1
                erreur = True
        return erreur

    def categoryfilter(self):
        #doit parcourir la liste des categories d'un produit et retenir uniquement les categories pré selectionné
        pass

    def brandfilter(self):
        #doit parcourir la liste des marques et retenir que la premiere marque (séparer par ",")
        pass

    def isEnglish(self, s):
        print(s)
        try:
            s.encode(encoding='latin-1')
        except UnicodeDecodeError:
            return False
        else:
            return True
