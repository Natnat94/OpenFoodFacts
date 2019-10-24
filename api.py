#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from pprint import pprint
import os
import records
from sqlalchemy.exc import IntegrityError
from sqlscript import *

class ApiRetriever:

    def __init__(self):
        self.data = ""
        self.data2 = {}
        self.url = 'https://fr.openfoodfacts.org/cgi/search.pl?'
        self.research = {'search_terms':'',
                    'search_simple':'1',
                    'action':'process',
                    'json':'1',
                    'tagtype_0':'categories',
                    'tag_contains_0':'contains',
                    'tag_0':'Pizzas',
                    'page_size': '200'}
        self.data_save = []

    def url_builder(self):

        content = requests.get(self.url, params = self.research)
        self.data = content.json()

    def content_viewer(self):

        cles = ['brands','categories','url','product_name_fr','stores','nutrition_grade_fr', 'id']
        for i in range(2):
            sdata = self.data["products"][i]
            print("---------------------------------------------")
            for key in cles:
                print("{} ----> {}".format(key, sdata[key]))

    def ccleaner(self):
        width = os.get_terminal_size().columns
        cles = ['brands','categories','url','product_name_fr','stores','nutrition_grade_fr', 'id']
        for i in range(50):
            sdata = self.data["products"][i]
            for key in cles:
                if sdata[key] == "": # and self.isEnglish(sdata[key]) == True:
                    #nstring= key.center(20,'*')
                    #print("voici le nom :", nstring)
                    self.data2[key] = None
                else:
                    self.data2[key] = sdata[key]
            self.data_save.append(self.data2.copy())
        #pprint(self.data_save)

    def categoryfilter(self):
        pass
        #doit parcourir la liste des categories d'un produit et retenir uniquement les categories pré selectionné

    def brandfilter(self):
        pass
        #doit parcourir la liste des marques et retenir que la premiere marque (séparer par ",")

    def storefilter(self, data):
        store = data['stores']
        store_list= store.split(",")
        return store_list
        #doit parcourir la liste des magasin et eliminer les magasins qui ne sont pas ecrit en latin

    def isEnglish(self, s):
        print(s)
        try:
            s.encode(encoding='latin-1')
        except UnicodeDecodeError:
            return False
        else:
            return True


class DatabaseHandler:

    def __init__(self):
        DATABASE_URL= ("mysql+mysqlconnector://myuser:password@localhost/projet5?charset=utf8mb4")
        self.db= records.Database(DATABASE_URL)

    def viewdb(self):
        rows = self.db.query('SELECT brands, product_name, store, nutrition FROM produit')
        print(rows.dataset)
        self.db.query('TRUNCATE TABLE produit')

    def inserintodb(self, categories, brands, link, nom, cat):
        try:
            self.db.query('INSERT INTO product (productid, productname, link, nutriscore, category) VALUES(:productid, :productname, :link, :nutriscore, :category)',
                    productid= categories, productname= brands, link= link, nutriscore= nom, category= cat)
        except IntegrityError as e:
            code = e.orig
            print("pendant l'integration dans la table 'product': ")
            print(code)

    def inserintodb2(self, store):
        #ajout les magasin dans la table 'store' si il n'existe pas deja a partir de la list de l'api
        for i in store:
            try:
                self.db.query('INSERT INTO store (store) VALUES(:store)',
                        store= i)
            except IntegrityError as e:
                code = e.orig
                print("pendant l'integration dans la table 'store': ")
                print(code)

    def inserintodb3(self, data):
        #retrouve l'id du magasin rechercher sur la table 'store'
        truc = self.db.query('SELECT id FROM store WHERE Store = :stores', stores = data)
        return truc[0].id
        #print(truc[0].id)

    def inserintodb4(self, data1, data2):
        #doit inserer l'id du magasin lier au produit
        try:
            self.db.query('INSERT INTO storeproduct (productid, store) VALUES(:productid, :store)',
                    productid = data1, store= data2)
        except IntegrityError as e:
            code = e.orig
            print("pendant l'integration dans la table 'storeproduct': ")
            print(code)

    def initdata(self):
        self.db.bulk_query("""INSERT INTO category(Category)
    VALUES (:data1)""",
    {"data1": "Aliments pour bébé"},
    {"data1": "Biscuits"},
    {"data1": "Pizzas"},
    {"data1": "Conserves"})



class ProductComparator:
    #cette classe doit pouvoir comparer et trouver le produit de la meme categorie avec un meilleur nutriscore
    pass

class DatabaseBuilder:
    #cette class crée la base de donnée qui va etre utilisé par l'application
    def __init__(self):
        DATABASE_URL= ("mysql+mysqlconnector://myuser:password@localhost/projet5?charset=utf8mb4")
        self.db= records.Database(DATABASE_URL)

    def store(self):
        self.db.query(store)

    def category(self):
        self.db.query(category)

    def product(self):
        self.db.query(product)

    def storeproduct(self):
        self.db.query(storeproduct)

    def productsaved(self):
        self.db.query(productsaved)
