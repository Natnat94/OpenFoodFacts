#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import random
import records
from sqlalchemy.exc import IntegrityError
import sqlscript as table


class DatabaseBuilder:
    """this class purpose is to create the database's tables if they
        do not already exist"""

    def __init__(self):
        user = os.environ.get('DATABASE_USER')
        password = os.environ.get('DATABASE_PASSWORD')
        DATABASE_URL = (
            "mysql+mysqlconnector://{}:{}@localhost/projet5?charset=utf8mb4"
            .format(user, password)
        )
        self.db = records.Database(DATABASE_URL)

    def create_tables(self):
        """this method create the tables needed for the Database
            if they don't already exists"""
        self.db.query(table.store)
        self.db.query(table.category)
        self.db.query(table.product)
        self.db.query(table.storeproduct)
        self.db.query(table.productsaved)
        self.db.query(table.config)

    def init_category(self, data):
        """this method insert the data for the 'category' table if
            it is not already exists"""
        self.db.query('INSERT IGNORE INTO category(Category) VALUES (:data)',
                      data=data)


class DatabaseHandler:
    """this is a superclass for all DB related class"""

    def __init__(self):
        """this init method connect between the program
            and the MySQL database"""
        user = os.environ.get('DATABASE_USER')
        password = os.environ.get('DATABASE_PASSWORD')
        DATABASE_URL = (
            "mysql+mysqlconnector://{}:{}@localhost/projet5?charset=utf8mb4"
            .format(user, password)
        )
        self.db = records.Database(DATABASE_URL)
        self.erreur_count = {'error': 0}
        self.count = 0
        self.store_list = None
        self.products = None
        try:
            self.db.query("""INSERT INTO config values('exist', 0)""")
        except IntegrityError:
            pass

    def status_db(self):
        """this method read the config table and return
        the 'state' row value"""
        state = self.db.query("""SELECT * FROM config""")
        return state[0].state

    def update_status_db(self):
        """this method update the 'state' value from the config table"""
        self.db.query("""UPDATE config SET state = 1 WHERE name = 'exist'""")


class Product(DatabaseHandler):
    """this class purpose is to manipulate all 'product' table related item"""

    def insert_product(self, data, catg):
        """this method insert the productid, productname, link, nutriscore
            & category of a given product into the 'product' table"""
        try:
            self.db.query('INSERT INTO product (productid, productname, link, \
                          nutriscore, description, category) \
                          VALUES(:a, :b, :c, :d, :f, :g)',
                          a=data['id'],
                          b=data['product_name_fr'],
                          c=data['url'],
                          d=data['nutrition_grade_fr'],
                          f=data['ingredients_text'],
                          g=self.category_id(catg))
        except IntegrityError:
            self.erreur_count['error'] += 1

    def category_id(self, data):
        """this method return the category id related to the category name
            given from the method argument"""
        truc = self.db.query('SELECT id FROM category WHERE category = :cat',
                             cat=data)
        return truc[0].id


class Store(DatabaseHandler):
    """this class purpose is to manipulate all 'store' table related item"""

    def insert_store(self, product):
        """this method insert the store's item into the 'store' table"""
        self.store_list = self.storecleaner(product)
        for i in self.store_list:
            try:
                self.db.query('INSERT INTO store (store) VALUES(:store)',
                              store=i)
            except IntegrityError:
                self.erreur_count['error'] += 1

    def storecleaner(self, data):
        """clean the string of stores received into a list and return it"""
        store = data['stores']
        store_list = store.split(",")
        for c in range(len(store_list)):
            store_list[c] = store_list[c].strip()
        return store_list


class StoreProduct(DatabaseHandler):
    """this class purpose is to manipulate all 'storeproduct' table
       related item"""
    def insert_storeproduct(self, data, store):
        """this method insert the store id related to a product (id), receive
            the "product id" and the "store name" as argument into
            the 'storeproduct' table"""
        store_id = self.check_id(store)
        try:
            self.db.query('INSERT INTO storeproduct (productid, store) \
                          VALUES(:productid, :store)',
                          productid=data['id'], store=store_id)
        except IntegrityError:
            self.erreur_count['error'] += 1

    def check_id(self, data):
        """this method return the store id related to the store name
            given from the method argument"""
        truc = self.db.query('SELECT id FROM store WHERE Store = :stores',
                             stores=data)
        return truc[0].id


class Information(DatabaseHandler):
    """this class purpose is to retreive infomations from the database"""

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
        return produit

    def get_products(self, data):
        """this method retreive a random list of 15 products
        from a selected category"""
        req_product = self.db.query(
                'SELECT product.productname, product.productid \
                from product where \
                (product.category = :cat and product.nutriscore > :nutri) \
                LIMIT 150', cat=data, nutri='b')
        req_products = {}
        for r in req_product:
            req_products[r.productname] = r.productid
        req_products = random.sample(list(req_products.items()), k=15)
        req_products = dict(req_products)
        return req_products

    def get_category(self):
        """this method retreive the category list of the database"""
        req_category = self.db.query('SELECT * from category')
        req_categories = {}
        for r in req_category:
            req_categories[r.category] = r.id
        return req_categories


class Substitute(DatabaseHandler):
    """this class purpose is to look for a substitue product in the DB"""

    def search_sub(self, data):
        """this method search for a related substitute according
        to product id provided and return a list of products"""
        research = self.db.query('SELECT productname, productid FROM product \
                        where category = (select category from product \
                        where productid = :id) and nutriscore < \
                        (select nutriscore from product \
                        where productid = :id) \
                        limit 50', id=data)
        req_products = {}
        for r in research:
            req_products[r.productname] = r.productid
        try:
            req_products = random.sample(list(req_products.items()), k=15)
            req_products = dict(req_products)
        except Exception:
            pass
        return req_products


class SaveProduct(DatabaseHandler):
    """this class purpose is to use the 'productsaved' table"""

    def save(self, product, substitute):
        """this method save the original product and it's substitute into
        the database"""
        self.db.query('INSERT IGNORE INTO productsaved \
                      (productid, subproductid) \
                      VALUES (:product, :substitute)',
                      product=product, substitute=substitute)

    def read(self):
        """this method read the original products and their substitutes
        saved into the database"""
        product = self.db.query('SELECT productsaved.id, product.productname,\
                                productsaved.productid \
                                from product, productsaved where \
                                (productsaved.productid = product.productid)')
        sub_product = self.db.query('SELECT productsaved.id, product.productname,\
                                    productsaved.subproductid \
                                    from product, productsaved where \
                                    (productsaved.subproductid = \
                                    product.productid)')
        temp_product, temp_sub, product_id, sub_id = {}, {}, {}, {}
        text = ["Voici vos produits sauvegardés:", ""]
        for r in product:
            temp_product[r.id] = r.productname
            product_id[r.id] = r.productid
        for r in sub_product:
            temp_sub[r.id] = r.productname
            sub_id[r.id] = r.subproductid
        for key, value in sorted(temp_product.items()):
            text.append(str(key) + " - " + value + " ----> " + temp_sub[key])
        return text, product_id, sub_id, len(temp_product)

    def remove(self, id):
        pass
