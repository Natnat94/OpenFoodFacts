#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time


class Drawer:
    """This class purpose is to draw information in a beautifull
    manner into the terminal"""
    def __init__(self):
        self.width = os.get_terminal_size().columns
        if self.width % 2 != 0:
            self.width = self.width - 1
        self.mwidth = int(self.width/2)
        self.lines = os.get_terminal_size().lines // 2

    def line(self):
        """this method draw a line of *"""
        print('{0:*^{1}}'.format('*', self.width), end='\n')

    def two_cell(self, titre1, titre2):
        """this method display the data into two cells"""
        width = self.mwidth - 3
        width2 = self.mwidth - 2
        self.line()
        print('* {0:<{1}}* {0:<{2}}*'.format('', width, width2), end='\n')
        print('* {0:^{2}}* {1:^{3}}*'.format(titre1, titre2, width, width2),
              end='\n')
        print('* {0:<{1}}* {0:<{2}}*'.format('', width, width2), end='\n')

    def one_cell(self, link):
        """this method display the data into one cell"""
        width = self.width - 3
        self.line()
        print('* {0:^{1}}*'.format('', width), end='\n')
        if not isinstance(link, str):
            for row in link:
                print('* {0:^{1}}*'.format(row, width), end='\n')
        else:
            print('* {0:^{1}}*'.format(link, width), end='\n')
        print('* {0:^{1}}*'.format('', width), end='\n')

    def screen_size(self, link):
        """this method display the data into one cell
        the size of the terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')
        width = self.width - 3
        count = self.lines - 2
        taille = len(link)
        if taille % 2 == 0:
            taille = taille + 1
        taille = range(taille//2, count)
        self.line()
        if not isinstance(link, str):
            for r in taille:
                print('* {0:^{1}}*'.format('', width), end='\n')
            for row in link:
                print('* {0:^{1}}*'.format(row, width), end='\n')
            for r in taille:
                print('* {0:^{1}}*'.format('', width), end='\n')
        else:
            for r in range(count):
                print('* {0:^{1}}*'.format('', width), end='\n')
            print('* {0:^{1}}*'.format(link, width), end='\n')
            for r in range(count):
                print('* {0:^{1}}*'.format('', width), end='\n')


class UserUx(Drawer):
    """this class purpose is to act as the displayer of the application"""

    def show_product(Drawer, data):
        """this method display the product information details"""
        os.system('cls' if os.name == 'nt' else 'clear')
        Drawer.two_cell('Nom du produit', 'categorie du produit')
        Drawer.two_cell(data['productname'], data['category'])
        Drawer.one_cell(data['link'])
        Drawer.two_cell('Produit disponible dans les magasins',
                        'Score nutritif')
        Drawer.two_cell(data['store'], data['nutriscore'])
        description = UserUx.description_clean(UserUx, data['description'])
        Drawer.one_cell(description)
        Drawer.line()

    def product_list(Drawer, data):
        """this method display a list of available products from a category"""
        os.system('cls' if os.name == 'nt' else 'clear')
        show_dict, temp_dict = {}, {}
        count = 1
        liste = []
        for key in data.keys():
            temp_dict[count] = key
            show_dict[count] = str(count) + " - " + key
            count += 1
        for v in show_dict.values():
            liste.append(v)
        Drawer.screen_size(liste)
        Drawer.line()
        return temp_dict

    def select_product(self, data):
        """this method allow the user to choose a product from the list
        of products displayed"""
        products = self.product_list(data)
        lst_len = int(len(products)) + 1
        text = "Quel produit vous intéresse ?"
        choice = self.input_validator(text, lst_len)
        key = products[choice]
        return data[key]

    def select_category(self, data):
        """this method allow the user to choose a category from the list
        of categories displayed"""
        products = self.product_list(data)
        lst_len = int(len(products)) + 1
        text = "Quelle catégorie vous intéresse ?"
        choice = self.input_validator(text, lst_len)
        key = products[choice]
        return data[key]

    def welcome(Drawer):
        """this method display a welcome message"""
        os.system('cls' if os.name == 'nt' else 'clear')
        Drawer.screen_size("Bienvenue !!!")
        Drawer.line()
        time.sleep(1)

    def description_clean(Drawer, data):
        """this method return the string data into a list splitted by ',' """
        cleaned_data = data.split(", ")
        return cleaned_data

    def input_validator(self, text, number=3):
        """this method check if the input from the user is valid"""
        try:
            print(text, end=" ")
            choice = int(input())
        except ValueError:
            print(text, end=" ")
            choice = input()
        while choice not in range(1, number):
            print(text, end=" ")
            try:
                choice = int(input())
            except ValueError:
                print(text, end=" ")
                choice = input()
        else:
            return choice

    def goodbye(Drawer):
        """this method display a goodbye message"""
        os.system('cls' if os.name == 'nt' else 'clear')
        Drawer.screen_size("A bientôt !!!")
        Drawer.line()
        time.sleep(2)
