#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from pprint import pprint
import os
import records

class ApiRetriever:

    def __init__(self):
        self.data = ""
        self.data2 = {}
        self.url = 'https://fr.openfoodfacts.org/cgi/search.pl?'
        self.research = {'search_terms':'chips',
                    'search_simple':'1',
                    'action':'process',
                    'json':'1',
                    'tagtype_0':'categories',
                    'tag_contains_0':'contains',
                    'tag_0':'snacks'}
        self.data_save = []

    def url_builder(self):

        content = requests.get(self.url, params = self.research)
        self.data = content.json()

    def content_viewer(self):

        cles = ['brands','nutrient_levels','categories','link']
        for i in range(5):
            sdata = self.data["products"][i]
            for key in cles:
                pprint(sdata[key])

    def ccleaner(self):
        width = os.get_terminal_size().columns
        cles = ['brands','link','product_name']
        width = os.get_terminal_size().columns
        for i in range(20):
            sdata = self.data["products"][i]
            for key in cles:
                if sdata[key] != "":
                    #nstring= key.center(20,'*')
                    #print("voici le nom :", nstring)
                    self.data2[key] = sdata[key]
                else:
                    pass
            self.data_save.append(self.data2.copy())


class DatabaseHandler:

    def __init__(self):
        DATABASE_URL= ("mysql+mysqlconnector://root:nathan@localhost/projet5?charset=utf8")
        self.db= records.Database(DATABASE_URL)

    def viewdb(self):
        rows = self.db.query('SELECT * FROM produit')
        print(rows.dataset)
        self.db.query('TRUNCATE TABLE produit')

    def inserintodb(self, brands,categories,link):
        self.db.query('INSERT INTO produit (categories, brands, link) VALUES(:categories, :brands, :link)',
                    categories=categories, brands=brands, link=link)
