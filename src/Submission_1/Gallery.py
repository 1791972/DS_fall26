# -*- coding: utf-8 -*-
"""
Gallery.py : ** REQUIRED ** El vostre codi de la classe Gallery.

Aquesta classe s'encarrega de gestionar galeries d'imatges en format JSON.

Funcionalitat:
    - Llegir galeries des d'arxius JSON
    - Visualitzar totes les imatges d'una galeria
    - Afegir i eliminar imatges de la galeria

Format JSON d'una galeria:
{
  "gallery_name": "Cyberpunk Cities",
  "description": "Collection of futuristic urban landscapes",
  "created_date": "2025-09-30",
  "images": [
    "generated_images/city_001.png",
    "generated_images/city_neon_12.png",
    "generated_images/urban_street_45.png"
  ]
}"""


import os
import cfg
import json

class Gallery:
    def __init__(self):
        self.gallery_name = ""
        self.description = ""
        self.created_date = ""
        self.images

    def load_file(self, file: str) -> None:
        """Llegeix un arxiu JSON amb la definició de la galeria.
        Ha de validar que cada imatge referenciada existeix a la col·lecció.
        Si una imatge no existeix, l'ignora i continua processant.
        Emmagatzema internament els UUID de les imatges vàlides."""



    def show(self) -> None:
        """Visualitza totes les imatges de la galeria en ordre utilitzant
        ImageViewer.show_image()."""



    def add_image_at_end(self, uuid: str) -> None:
        """Afegeix una imatge al final de la galeria."""



    def remove_first_image(self) -> None:
        """Elimina la primera imatge de la galeria."""



    def remove_last_image(self) -> None:
        """Elimina l'última imatge de la galeria."""



"""Notes:
    - Utilitzeu la llibreria json per llegir els arxius
    - Els paths dins el JSON són relatius a ROOT_DIR
    - Cada galeria és un objecte independent (instància de Gallery)
    - Podeu tenir múltiples galeries actives simultàniament
    - Les operacions d'afegir/eliminar són ràpides (no busquen a la llista)
"""
