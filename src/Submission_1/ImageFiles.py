# -*- coding: utf-8 -*-
"""
ImageFiles.py : ** REQUIRED ** El vostre codi de la classe ImageFiles.

Aquesta classe s'encarrega de gestionar el llistat d'arxius PNG dins la col·lecció d'imatges.

Funcionalitat:
    - Recórrer el filesystem a partir de ROOT_DIR per trobar tots els arxius PNG
    - Mantenir una representació en memòria dels arxius presents
    - Detectar quins arxius s'han afegit o eliminat des de l'última lectura"""


import os
import cfg

class ImageFiles:
    def __init__(self):
        self.current_files = []
        self.added_files = []
        self.removed_files = []

    def reload_fs(self, dir: str):
        """Recorre el directori especificat i actualitza la llista d'arxius PNG.
           Detecta els arxius nous i els que s'han eliminat."""
        
        if dir != "":
            directori = dir
        else:
            cfg.get_root()

        files = []
        for root

    def files_added():
        """Retorna una llista (de strings) amb els paths relatius dels arxius
           que s'han afegit des de l'última crida a reload_fs()."""
        
        pass

    def files_removed():
        """Retorna una llista (de strings) amb els paths relatius dels arxius
           que s'han eliminat des de l'última crida a reload_fs()."""
        pass




"""
   Notes:
    - Els paths han de ser sempre relatius a ROOT_DIR
    - Només considereu arxius amb extensió .png (case-insensitive)
    - Heu de recórrer tots els subdirectoris recursivament
"""
