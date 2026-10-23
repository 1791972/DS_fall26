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
        self.current_files = set()
        self.previous_files = set()

    def __str__(self):
        return "ImageFiles(" + str(len(self.current_files)) + " arxius)"

    def reload_fs(self, path: str):
        """Recorre el directori especificat i actualitza la llista d'arxius PNG.
           Detecta els arxius nous i els que s'han eliminat."""

        if path is None:
            path = cfg.get_root()

        search_path = path if os.path.isabs(path) else os.path.join(cfg.get_root(), path)

        self.previous_files = set(self.current_files)
        new_files = set()

        if not os.path.exists(search_path):
            self.current_files = new_files
            return

        for root, _, files in os.walk(search_path):
            for f in files:
                if f.lower().endswith('.png'):
                    pathT = os.path.join(root, f)
                    pathC = cfg.get_canonical_pathfile(pathT)
                    new_files.add(pathC)

        self.current_files = new_files
        

    def files_added(self):
        """Retorna una llista (de strings) amb els paths relatius dels arxius
           que s'han afegit des de l'última crida a reload_fs()."""
        
        added = self.current_files - self.previous_files
        return list(added)

    def files_removed(self):
        """Retorna una llista (de strings) amb els paths relatius dels arxius
           que s'han eliminat des de l'última crida a reload_fs()."""

        removed = self.previous_files - self.current_files
        return list(removed)


"""
   Notes:
    - Els paths han de ser sempre relatius a ROOT_DIR
    - Només considereu arxius amb extensió .png (case-insensitive)
    - Heu de recórrer tots els subdirectoris recursivament
"""
