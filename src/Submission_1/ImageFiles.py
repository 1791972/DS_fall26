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

    def reload_fs(self, path: str):
        """Recorre el directori especificat i actualitza la llista d'arxius PNG.
           Detecta els arxius nous i els que s'han eliminat."""
        
        direction = path if path != "" else cfg.get_root()
        new_files = []

        for root, directions, files in os.walk(direction):
            for f in files:
                if f.lower().endswith('.png'):
                    pathT = os.path.join(root, f)
                    pathC = cfg.get_canonical_pathfile(pathT)
                    new_files.append(pathC)

        self.added_files = []
        for f in new_files:
            if f not in self.current_files:
                self.added_files.append(f)

        self.removed_files = []
        for f in new_files:
            if f not in self.current_files:
                self.removed_files.append(f)

        self.current_files = new_files

    def files_added():
        """Retorna una llista (de strings) amb els paths relatius dels arxius
           que s'han afegit des de l'última crida a reload_fs()."""
        
        return self.added_files

    def files_removed():
        """Retorna una llista (de strings) amb els paths relatius dels arxius
           que s'han eliminat des de l'última crida a reload_fs()."""

        return self.removed_files


"""
   Notes:
    - Els paths han de ser sempre relatius a ROOT_DIR
    - Només considereu arxius amb extensió .png (case-insensitive)
    - Heu de recórrer tots els subdirectoris recursivament
"""
