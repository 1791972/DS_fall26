# -*- coding: utf-8 -*-
"""
ImageFiles.py : ** REQUIRED ** El vostre codi de la classe ImageFiles.

Aquesta classe s'encarrega de gestionar el llistat d'arxius PNG dins la col·lecció d'imatges.

Funcionalitat:
    - Recórrer el filesystem a partir de ROOT_DIR per trobar tots els arxius PNG
    - Mantenir una representació en memòria dels arxius presents
    - Detectar quins arxius s'han afegit o eliminat des de l'última lectura

Mètodes a implementar:
    - reload_fs(path: str) -> None
        Recorre el directori especificat i actualitza la llista d'arxius PNG.
        Detecta els arxius nous i els que s'han eliminat.

    - files_added() -> list
        Retorna una llista (de strings) amb els paths relatius dels arxius
        que s'han afegit des de l'última crida a reload_fs().

    - files_removed() -> list
        Retorna una llista (de strings) amb els paths relatius dels arxius
        que s'han eliminat des de l'última crida a reload_fs().

Notes:
    - Els paths han de ser sempre relatius a ROOT_DIR
    - Només considereu arxius amb extensió .png (case-insensitive)
    - Heu de recórrer tots els subdirectoris recursivament
"""


import os
import cfg


class ImageFiles:
    def __init__(self):
        self.current_files = set()
        self.previous_files = set()

    def __len__(self):
        return len(self.current_files)

    def __str__(self):
        return "ImageFiles(" + str(len(self.current_files)) + " arxius)"

    def reload_fs(self, path: str) -> None:
        """Recorre el directori especificat i actualitza la llista d'arxius PNG.
        Detecta els arxius nous i els que s'han eliminat."""

        if path is None:
            path = cfg.get_root()
        path = str(path)

        if not os.path.isdir(path):
            alternativa = os.path.join(cfg.get_root(), path)
            if os.path.isdir(alternativa):
                path = alternativa
        path = os.path.abspath(path)

        self.previous_files = self.current_files
        encontrados = set()

        for carpeta, subcarpetas, archivos in os.walk(path):
            for nombre in archivos:
                if nombre.lower().endswith(".png"):
                    encontrados.add(os.path.join(carpeta, nombre))

        self.current_files = encontrados

    def files_added(self) -> list:
        """Retorna una llista (de strings) amb els paths dels arxius
        que s'han afegit des de l'última crida a reload_fs()."""

        return sorted(self.current_files - self.previous_files)

    def files_removed(self) -> list:
        """Retorna una llista (de strings) amb els paths dels arxius
        que s'han eliminat des de l'última crida a reload_fs()."""

        return sorted(self.previous_files - self.current_files)
