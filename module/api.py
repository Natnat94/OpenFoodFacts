#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import html


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
                'ingredients_text',
                'nutrition_grade_fr',
                'id']
        for c in self.data["products"]:
            sdata = c
            print("---------------------------------------------")
            for key in cles:
                print("{} ----> {}".format(key, sdata[key]))


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
                'ingredients_text',
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
                    value = product[key].replace('\n', ' ')
                    value = value.replace("_", "")
                    self.data2[key] = html.unescape(value)
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
            return True  # READY DO NOT TOUCH !!
