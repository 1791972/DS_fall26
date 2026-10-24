# -*- coding: utf-8 -*-
"""
SearchMetadata.py : ** REQUIRED ** El vostre codi de la classe SearchMetadata.

Aquesta classe s'encarrega de cercar imatges segons criteris basats en metadades.

Funcionalitat:
    - Cercar imatges que continguin una subcadena en les seves metadades
    - Combinar resultats de cerques amb operadors lògics (AND, OR)

Mètodes a implementar:
    - prompt(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Prompt.

    - model(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Model.

    - seed(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Seed.

    - cfg_scale(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp CFG_Scale.

    - steps(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Steps.

    - sampler(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Sampler.

    - date(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Created_Date.

    - and_operator(list1: list, list2: list) -> list
        Retorna una llista amb els UUID que apareixen en AMBDUES llistes.
        (Intersecció de conjunts)

    - or_operator(list1: list, list2: list) -> list
        Retorna una llista amb els UUID que apareixen en QUALSEVOL de
        les dues llistes, sense duplicats.
        (Unió de conjunts)

Notes:
    - Les cerques són case-sensitive (distingeixen majúscules/minúscules)
    - Utilitzeu str.find() per cercar subcadenes
    - Les llistes retornades poden estar buides
    - Els operadors lògics NO modifiquen les llistes originals
    - Aquests mètodes NO retornen objectes Gallery, sinó llistes simples
"""


class SearchMetadata:
    def __init__(self, image_data):
        self.image_data = image_data

    def __str__(self):
        return "SearchMetadata(" + str(len(self.image_data)) + " imatges)"

    def _search(self, getter, sub: str) -> list:
        """Retorna els UUID per als quals getter(uuid) conté la subcadena 'sub'."""

        res = []
        if sub is None:
            return res
        sub = str(sub)

        for uuid in self.image_data.get_uuids():
            # Si les metadades encara no s'han llegit del disc, es llegeixen ara
            if not self.image_data.is_loaded(uuid):
                self.image_data.load_metadata(uuid)
            valor = getter(uuid)
            if valor is not None and str(valor).find(sub) != -1:   # find() retorna -1 si no hi és
                res.append(uuid)
        return res

    def prompt(self, sub: str) -> list:
        return self._search(self.image_data.get_prompt, sub)

    def model(self, sub: str) -> list:
        return self._search(self.image_data.get_model, sub)

    def seed(self, sub: str) -> list:
        return self._search(self.image_data.get_seed, sub)

    def cfg_scale(self, sub: str) -> list:
        return self._search(self.image_data.get_cfg_scale, sub)

    def steps(self, sub: str) -> list:
        return self._search(self.image_data.get_steps, sub)

    def sampler(self, sub: str) -> list:
        return self._search(self.image_data.get_sampler, sub)

    def date(self, sub: str) -> list:
        return self._search(self.image_data.get_created_date, sub)

    def created_date(self, sub: str) -> list:
        return self.date(sub)

    def generated(self, sub: str) -> list:
        return self._search(self.image_data.get_generated, sub)

    def and_operator(self, list1: list, list2: list) -> list:
        """UUID que apareixen en AMBDUES llistes (sense modificar-les)."""

        list1 = list1 if list1 is not None else []
        list2 = list2 if list2 is not None else []
        in_second = set(list2)               # cerca O(1) en lloc de recórrer list2
        vistos = set()
        res = []
        for uuid in list1:
            if uuid in in_second and uuid not in vistos:
                vistos.add(uuid)
                res.append(uuid)
        return res

    def or_operator(self, list1: list, list2: list) -> list:
        """UUID que apareixen en QUALSEVOL de les dues llistes, sense duplicats."""

        list1 = list1 if list1 is not None else []
        list2 = list2 if list2 is not None else []
        vistos = set()
        res = []
        for uuid in list1:
            if uuid not in vistos:
                vistos.add(uuid)
                res.append(uuid)
        for uuid in list2:
            if uuid not in vistos:
                vistos.add(uuid)
                res.append(uuid)
        return res
            if uuid not in vistos:
                vistos.add(uuid)
                res.append(uuid)
        return res
