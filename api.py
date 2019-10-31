#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import os
import requests
import records
import html
import os
import json
from sqlalchemy.exc import IntegrityError
import sqlscript as table
from pprint import pprint

class ApiRetriever:
    """this class purpose is to retrieve the information from
        the OpenFoodFacts API"""

    url = 'https://fr.openfoodfacts.org/cgi/search.pl?'

    def __init__(self):
        self.data = None
        self.research = {'search_terms': '',
                         'search_simple': '1',
                         'action': 'process',
                         'json': '1',
                         'tagtype_0': 'categories',
                         'tag_contains_0': 'contains',
                         'tag_0': '',
                         'page_size': '250'}

    def get_data(self, category):
        """this method send a request to get the data
            researched from the API in JSON"""
        self.research['tag_0'] = category
        content = requests.get(self.url, params=self.research)
        self.data = content.json()
        return self.data

    def content_viewer(self):
        """this method allow to see the selected data from the API (BROKEN)"""
        cles = ['brands',
                'categories',
                'url',
                'product_name_fr',
                'stores',
                'nutrition_grade_fr',
                'id']
        for c in self.data["products"]:
            sdata = c
            print("---------------------------------------------")
            for key in cles:
                print("{} ----> {}".format(key, sdata[key]))


class DatabaseHandler:
    """this is a superclass for all DB related class"""

    def __init__(self, user = "myuser", password = "password"):
        """this init method connect between the program
            and the MySQL database"""
        DATABASE_URL = ("mysql+mysqlconnector://{}:{}@localhost/projet5?charset=utf8mb4".format(user, password))
        self.db = records.Database(DATABASE_URL)
        self.erreur_count = {'error': 0}
        self.count = 0
        self.store_list = None
        self.products = None # READY DO NOT TOUCH !!


class Product(DatabaseHandler):
    """this class purpose is to manipulate all 'product' table related item"""

    def insert_product(self, data, catg):
        """this method insert the productid, productname, link, nutriscore
            & category of a given product into the 'product' table"""
        try:
            self.db.query('INSERT INTO product (productid, productname, link, nutriscore, category) VALUES(:a, :b, :c, :d, :f)',
                          a=data['id'],
                          b=data['product_name_fr'],
                          c=data['url'],
                          d=data['nutrition_grade_fr'],
                          f=self.category_id(catg))
        except IntegrityError:  # as e:
            # code = e.orig
            # if self.count < 3:
            #     print("pendant l'integration dans la table 'product': ")
            #    print(code)
            #    self.count = self.count + 1
            # else:
            #     pass
            self.erreur_count['error'] += 1

    def category_id(self, data):
        """this method return the category id related to the category name
            given from the method argument"""
        # retrouve l'id de la category rechercher sur la table 'category'
        truc = self.db.query('SELECT id FROM category WHERE category = :cat',
                             cat=data)
        return truc[0].id # READY DO NOT TOUCH !!


class Store(DatabaseHandler):
    """this class purpose is to manipulate all 'store' table related item"""

    def insert_store(self, product):
        """this method insert the store's item into the 'store' table"""
        # ajout les magasin dans la table 'store' si il n'existe pas deja a
        # partir de la list de l'api
        self.store_list = self.storecleaner(product)
        for i in self.store_list:
            try:
                self.db.query('INSERT INTO store (store) VALUES(:store)',
                              store=i)
            except IntegrityError:  # as e:
                # code = e.orig
                # if self.count < 3:
                #    print("pendant l'integration dans la table 'store': ")
                #    print(code)
                #    self.count = self.count + 1
                # else:
                #    pass
                self.erreur_count['error'] += 1

    def storecleaner(self, data):
        """clean the string of stores received into a list and return it"""
        # doit parcourir la liste des magasin et eliminer les magasins qui
        # ne sont pas ecrit en latin
        store = data['stores']
        store_list = store.split(",")
        for c in range(len(store_list)):
            store_list[c] = store_list[c].strip()
        return store_list # READY DO NOT TOUCH !!


class StoreProduct(DatabaseHandler):
    """this class purpose is to manipulate all 'storeproduct' table
       related item"""
    def insert_storeproduct(self, data, store):
        """this method insert the store id related to a product (id), receive
            the "product id" and the "store name" as argument into
            the 'storeproduct' table"""
        # doit inserer l'id du magasin lier au produit
        store_id = self.check_id(store)
        try:
            self.db.query('INSERT INTO storeproduct (productid, store) VALUES(:productid, :store)',
                          productid=data['id'], store=store_id)
        except IntegrityError:  # as e:
            # code = e.orig
            # if self.count < 3:
            #     print("pendant l'integration dans la table 'storeproduct': ")
            #     print(code)
            #     self.count = self.count + 1
            # else:
            #     pass
            self.erreur_count['error'] += 1

    def check_id(self, data):
        """this method return the store id related to the store name
            given from the method argument"""
        # retrouve l'id du magasin rechercher sur la table 'store'
        truc = self.db.query('SELECT id FROM store WHERE Store = :stores', stores=data)
        return truc[0].id # READY DO NOT TOUCH !!


class DatabaseBuilder:
    """this class purpose is the create the database tables if they
        do not already exist"""

    def __init__(self, user = "myuser", password = "password"):
        DATABASE_URL = ("mysql+mysqlconnector://{}:{}@localhost/projet5?charset=utf8mb4".format(user, password))
        self.db = records.Database(DATABASE_URL)

    def create_tables(self, category):
        """this method create the tables needed for the Database
            if they don't already exists"""
        self.db.query(table.store)
        self.db.query(table.category)
        self.db.query(table.product)
        self.db.query(table.storeproduct)
        self.db.query(table.productsaved)
        self.init_category(category)

    def init_category(self, data):
        """this method insert the data for the 'category' table if
            it is not already exists"""
        self.db.query('INSERT IGNORE INTO category(Category) VALUES (:data)',
                           data = data) # READY DO NOT TOUCH !!


class DataCleaner:
    """this class purpose is to clean the raw data received from the API"""

    def __init__(self):
        self.erreur_count = {'prob1': 0,
                             'prob2': 0,
                             'prob3': 0,
                             'prob4': 0}
        self.data2 = {}
        self.data_save = []

    def realcleaner(self, data):
        """This method role is to clean the data received from
            any useless information"""
        for c in range(50):  # self.data["products"]:
            i = data["products"][c]
            if self.isvalid(i):
                continue
            else:
                self.data_save.append(self.data2.copy())

    def isvalid(self, product):
        """this method role is to check if all the information needed
            exist and return True if an error occur"""
        # width = os.get_terminal_size().columns
        keys = ['brands',
                'categories',
                'url',
                'product_name_fr',
                'stores',
                'nutrition_grade_fr',
                'id']
        erreur = False
        self.data2 = {}
        for key in keys:
            data = product.get(key)
            if data:
                if product[key] == "":
                    erreur = True
                    self.erreur_count['prob1'] += 1
                else:
                    self.data2[key] = html.unescape(product[key])
            else:
                self.erreur_count['prob2'] += 1
                erreur = True
        return erreur

    def categoryfilter(self):
        # doit parcourir la liste des categories d'un produit et retenir
        # uniquement les categories pré selectionné
        pass

    def brandfilter(self):
        # doit parcourir la liste des marques et retenir que la premiere
        # marque (séparer par ",")
        pass

    def isEnglish(self, s):
        """this method check if there is any non-latin word (not in use)"""
        try:
            s.encode(encoding='latin-1')
        except UnicodeDecodeError:
            return False
        else:
            return True # READY DO NOT TOUCH !!


class Information(DatabaseHandler):
    """docstring for Information."""

    def get_info(self, data):
        """this method retreive the info about the selected product"""
        req_product = self.db.query(
                'SELECT product.productid, category.category, productname, \
                    nutriscore, store.store, link \
                FROM product, category, store, storeproduct \
                WHERE ( product.category = category.id \
                        and product.productid = storeproduct.productid \
                        and storeproduct.store = store.id \
                        and product.productid = :productid)',
                        productid = data)
        req_products = req_product.as_dict()
        produit = {}
        store = []
        for r in req_products:
            for key, value in r.items():
                if key != 'store':
                    produit[key] = value
                else:
                    store.append(value)
        store = list(dict.fromkeys(store))
        store = " & ".join(store)
        produit['store'] = store
        return produit

    def get_products(self, data):
        """this method retreive the products list of a selected category"""
        req_product = self.db.query(
                'SELECT product.productname, product.productid \
                from product where \
                (product.category = :cat and product.nutriscore > :nutri) \
                LIMIT 20', cat = data, nutri = 'b')
        req_products = {}
        for r in req_product:
            req_products[r.productname] = r.productid
        return req_products # recherche les produits existants d'une categorie dans la BdD

    def get_category(self): # recherche les categories existantes dans la BdD
        """this method retreive the category list of the database"""
        req_category = self.db.query('SELECT * from category')
        req_categories = {}
        for r in req_category:
            req_categories[r.category] = r.id
        return req_categories


class Drawer:
    """This class purpose is to draw information in a beautifull manner into the terminal"""
    def __init__(self):
        self.width = os.get_terminal_size().columns
        if self.width % 2 != 0:
            self.width = self.width - 1
        self.mwidth = int(self.width/2)

    def line(self):

        print('{0:*^{1}}'.format('*', self.width),end ='\n') # dessine une ligne dans le terminal

    def two_cell(self, titre1, titre2):
        width = self.mwidth - 3
        width2 = self.mwidth - 2
        self.line()
        print('* {0:<{1}}* {0:<{2}}*'.format('', width, width2), end ='\n')
        print('* {0:^{2}}* {1:^{3}}*'.format(titre1, titre2, width, width2), end ='\n')
        print('* {0:<{1}}* {0:<{2}}*'.format('', width, width2), end ='\n') # dessine deux cellules d'info dans le terminal

    def one_cell(self,link): # dessine une cellule d'info dans le terminal
        width = self.width - 3
        self.line()
        print('* {0:^{1}}*'.format('', width), end ='\n')
        if not isinstance(link, str):
            for row in link:
                print('* {0:^{1}}*'.format(row, width), end ='\n')
        else:
            print('* {0:^{1}}*'.format(link, width), end ='\n')
        print('* {0:^{1}}*'.format('', width), end ='\n') # READY DO NOT TOUCH !!


class UserUx(Drawer):
    """docstring for UserUx."""

    def show_product(Drawer, data):
        os.system('cls' if os.name == 'nt' else 'clear')
        Drawer.two_cell('Nom du produit', 'categorie du produit')
        Drawer.two_cell(data['productname'], data['category'])
        Drawer.one_cell(data['link'])
        Drawer.two_cell('Produit disponible dans les magasins', 'Score nutritif')
        Drawer.two_cell(data['store'], data['nutriscore'])
        Drawer.line() # affiche une fiche d'un produit dans le terminal

    def product_list(self, data):
        os.system('cls' if os.name == 'nt' else 'clear')
        show_dict, temp_dict = {}, {}
        count = 1
        print("which product do you prefer ?")
        for key in data.keys():
            temp_dict[count] = key
            show_dict[count] = str(count) + "- " + key
            count += 1
        for v in show_dict.values():
            print(' {1:<{0}}'.format(self.mwidth,v), end ="")
            if count % 2 == 0:
                print("")
            count += 1
        return temp_dict # affiche une liste des produits dans le terminal

    def select_product(self, data):
        products = self.product_list(data)
        choice = int(input())
        lst_len = int(len(products)) + 1
        while choice not in range(1, lst_len):
            choice = int(input())
        else:
            key = products[choice]
            return data[key] # selectionne un produit dans le terminal

    def select_category(self, data):

        products = self.product_list(data)
        choice = int(input())
        lst_len = int(len(products)) + 1
        while choice not in range(1, lst_len):
            choice = int(input())
        else:
            key = products[choice]
            return data[key] # selectionne une categorie dans le terminal

    def welcome(Drawer):
        os.system('cls' if os.name == 'nt' else 'clear')
        welcome =["","","","","","Bienvenue !!!","","","","",""]
        Drawer.one_cell(welcome)
        Drawer.line()
