# -*- coding: utf-8 -*-
"""
SearchMetadata.py : ** REQUIRED ** El vostre codi de la classe SearchMetadata.

Aquesta classe s'encarrega de cercar imatges segons criteris basats en metadades.

Funcionalitat:
    - Cercar imatges que continguin una subcadena en les seves metadades
    - Combinar resultats de cerques amb operadors lògics (AND, OR)"""


from ImageData import ImageData
import cfg

class SearchMetadata:
    def __init(self, image_data):
        self.image_data = image_data if image_data is not None else ImageData()

    def prompt(self, sub: str) -> list:
        """Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Prompt."""

    def model(self, sub: str) -> list:
        """Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Model."""

    def seed(self, sub: str) -> list:
        """Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Seed."""

    def cfg_scale(self, sub: str) -> list:
        """Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp CFG_Scale."""

    def steps(self, sub: str) -> list:
        """Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Steps."""

    def sampler(self, sub: str) -> list:
        """Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Sampler."""

    def date(self, sub: str) -> list:
        """Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Created_Date."""

    def and_operator(self, list1: list, list2: list) -> list:
        """Retorna una llista amb els UUID que apareixen en AMBDUES llistes.
        (Intersecció de conjunts)"""

    def or_operator(self, list1: list, list2: list) -> list:
        """Retorna una llista amb els UUID que apareixen en QUALSEVOL de
        les dues llistes, sense duplicats.
        (Unió de conjunts)"""

"""Notes:
    - Les cerques són case-sensitive (distingeixen majúscules/minúscules)
    - Utilitzeu str.find() per cercar subcadenes
    - Les llistes retornades poden estar buides
    - Els operadors lògics NO modifiquen les llistes originals
    - Aquests mètodes NO retornen objectes Gallery, sinó llistes simples
"""
