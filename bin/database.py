#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import records
import os
from sqlalchemy.exc import IntegrityError
import sqlscript as table


class DatabaseBuilder:
    """this class purpose is the create the database tables if they
        do not already exist"""

    def __init__(self):
        user = os.environ.get('DATABASE_USER')
        password = os.environ.get('DATABASE_PASSWORD')
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
        self.db.query(table.config)
        self.init_category(category)

    def init_category(self, data):
        """this method insert the data for the 'category' table if
            it is not already exists"""
        self.db.query('INSERT IGNORE INTO category(Category) VALUES (:data)',
                      data=data)  # READY DO NOT TOUCH !!


class DatabaseHandler:
    """this is a superclass for all DB related class"""

    def __init__(self):
        """this init method connect between the program
            and the MySQL database"""
        user = os.environ.get('DATABASE_USER')
        password = os.environ.get('DATABASE_PASSWORD')
        DATABASE_URL = ("mysql+mysqlconnector://{}:{}@localhost/projet5?charset=utf8mb4".format(user, password))
        self.db = records.Database(DATABASE_URL)
        self.erreur_count = {'error': 0}
        self.count = 0
        self.store_list = None
        self.products = None
        try:
            self.db.query("""INSERT INTO config values('exist', 0)""")
        except IntegrityError:
            pass  # READY DO NOT TOUCH !!


class Product(DatabaseHandler):
    """this class purpose is to manipulate all 'product' table related item"""

    def insert_product(self, data, catg):
        """this method insert the productid, productname, link, nutriscore
            & category of a given product into the 'product' table"""
        try:
            self.db.query('INSERT INTO product (productid, productname, link, nutriscore, description, category) VALUES(:a, :b, :c, :d, :f, :g)',
                          a=data['id'],
                          b=data['product_name_fr'],
                          c=data['url'],
                          d=data['nutrition_grade_fr'],
                          f=data['ingredients_text'],
                          g=self.category_id(catg))
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
        return truc[0].id  # READY DO NOT TOUCH !!


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
        return store_list  # READY DO NOT TOUCH !!


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
        return truc[0].id  # READY DO NOT TOUCH !!


class Information(DatabaseHandler):
    """docstring for Information."""

    def get_info(self, data):
        """this method retreive the info about the selected product"""
        req_product = self.db.query(
                'SELECT product.productid, category.category, productname, \
                    nutriscore, store.store, link, description \
                FROM product, category, store, storeproduct \
                WHERE ( product.category = category.id \
                        and product.productid = storeproduct.productid \
                        and storeproduct.store = store.id \
                        and product.productid = :productid)', productid=data)
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
        return produit  # recheche les info sur le produit selectionné

    def get_products(self, data):
        """this method retreive the products list of a selected category"""
        req_product = self.db.query(
                'SELECT product.productname, product.productid \
                from product where \
                (product.category = :cat and product.nutriscore > :nutri) \
                LIMIT 20', cat=data, nutri='b')
        req_products = {}
        for r in req_product:
            req_products[r.productname] = r.productid
        return req_products  # recherche les produits existants d'une categorie dans la BdD

    def get_category(self):  # recherche les categories existantes dans la BdD
        """this method retreive the category list of the database"""
        req_category = self.db.query('SELECT * from category')
        req_categories = {}
        for r in req_category:
            req_categories[r.category] = r.id
        return req_categories


class Substitute(DatabaseHandler):

    def search_sub(self, data):

        research = self.db.query('SELECT productname, productid FROM product \
                        where category = (select category from product \
                        where productid = :id) and nutriscore < \
                        (select nutriscore from product \
                        where productid = :id) \
                        limit 10', id=data)
        req_products = {}
        for r in research:
            req_products[r.productname] = r.productid
        return req_products  # READY DO NOT TOUCH !!


class SaveProduct(DatabaseHandler):

    def save(self, product, substitute):
        self.db.query('INSERT IGNORE INTO productsaved \
                      (productid, subproductid) \
                      VALUES (:product, :substitute)',
                      product=product, substitute=substitute)

    def read(self):
        product = self.db.query('SELECT productsaved.id, product.productname from product, productsaved where (productsaved.productid = product.productid)')
        sub_product = self.db.query('SELECT productsaved.id, product.productname from product, productsaved where (productsaved.subproductid = product.productid)')
        temp_product, temp_sub = {}, {}
        text = ["Voici vos produits sauvegardés:", ""]
        for r in product:
            temp_product[r.id] = r.productname
        for r in sub_product:
            temp_sub[r.id] = r.productname
        # print("Voici vos produits sauvegardés:\n")
        for key, value in sorted(temp_product.items()):
            text.append(str(key) + " - " + value + " ----> " + temp_sub[key])
        return text

    def remove(self, id):
        pass
