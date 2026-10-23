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
    def __init__(self, image_data):
        self.image_data = image_data if image_data is not None else ImageData()

    def __str__(self):
        return "SearchMetadata(" + str(len(self.image_data)) + " imatges)"

    def _field(self, type: str, sub: str) -> list:
        res = []
        if sub is None:
            sub = ""
        subs= str(sub)

        for uuid in self.image_data.data.keys():
            c = ""
            if type == 'prompt':
                c = self.image_data.get_prompt(uuid)
            elif type == 'model':
                c = self.image_data.get_model(uuid)
            elif type == 'seed':
                c = self.image_data.get_seed(uuid)
            elif type == 'cfg_scale':
                c = self.image_data.get_cfg_scale(uuid)
            elif type == 'steps':
                c = self.image_data.get_steps(uuid)
            elif type == 'sampler':
                c = self.image_data.get_sampler(uuid)
            elif type == 'date':
                c = self.image_data.get_created_date(uuid)

            if str(c).find(subs) != -1:
                res.append(uuid)

        return res

    def prompt(self, sub: str) -> list:
        """Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Prompt."""

        return self._field('prompt', sub)

    def model(self, sub: str) -> list:
        """Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Model."""

        return self._field('model', sub)

    def seed(self, sub: str) -> list:
        """Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Seed."""

        return self._field('seed', sub)

    def cfg_scale(self, sub: str) -> list:
        """Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp CFG_Scale."""

        return self._field('cfg_scale', sub)

    def steps(self, sub: str) -> list:
        """Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Steps."""

        return self._field('steps', sub)

    def sampler(self, sub: str) -> list:
        """Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Sampler."""

        return self._field('sampler', sub)

    def date(self, sub: str) -> list:
        """Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Created_Date."""

        return self._field('date', sub)

    def and_operator(self, list1: list, list2: list) -> list:
        """Retorna una llista amb els UUID que apareixen en AMBDUES llistes.
        (Intersecció de conjunts)"""

        return [uuid for uuid in list1 if uuid in list2]

    def or_operator(self, list1: list, list2: list) -> list:
        """Retorna una llista amb els UUID que apareixen en QUALSEVOL de
        les dues llistes, sense duplicats.
        (Unió de conjunts)"""

        res = list(list1)
        for uuid in list2:
            if uuid not in res:
                res.append(uuid)
        return res


"""Notes:
    - Les cerques són case-sensitive (distingeixen majúscules/minúscules)
    - Utilitzeu str.find() per cercar subcadenes
    - Les llistes retornades poden estar buides
    - Els operadors lògics NO modifiquen les llistes originals
    - Aquests mètodes NO retornen objectes Gallery, sinó llistes simples
"""
