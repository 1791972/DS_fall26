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
}

Mètodes a implementar:
    - load_file(file: str) -> None
        Llegeix un arxiu JSON amb la definició de la galeria.
        Ha de validar que cada imatge referenciada existeix a la col·lecció.
        Si una imatge no existeix, l'ignora i continua processant.
        Emmagatzema internament els UUID de les imatges vàlides.

    - show() -> None
        Visualitza totes les imatges de la galeria en ordre utilitzant
        ImageViewer.show_image().

    - add_image_at_end(uuid: str) -> None
        Afegeix una imatge al final de la galeria.

    - remove_first_image() -> None
        Elimina la primera imatge de la galeria.

    - remove_last_image() -> None
        Elimina l'última imatge de la galeria.

Notes:
    - Utilitzeu la llibreria json per llegir els arxius
    - Els paths dins el JSON són relatius a ROOT_DIR
    - Cada galeria és un objecte independent (instància de Gallery)
    - Podeu tenir múltiples galeries actives simultàniament
    - Les operacions d'afegir/eliminar són ràpides (no busquen a la llista)
"""


import os
import json
import cfg
from ImageID import ImageID


class Gallery:
    def __init__(self, image_id=None, image_viewer=None):
        self.image_id = image_id if image_id is not None else ImageID()
        self.image_viewer = image_viewer
        self.gallery_name = ""
        self.description = ""
        self.created_date = ""
        self.images = []

    def __len__(self):
        return len(self.images)

    def __str__(self):
        return "Gallery(" + self.gallery_name + ", " + str(len(self.images)) + " imatges)"

    def _clear(self):
        self.gallery_name = ""
        self.description = ""
        self.created_date = ""
        self.images = []

    def load_file(self, file: str) -> None:
        """Llegeix un arxiu JSON amb la definició de la galeria.
        Ha de validar que cada imatge referenciada existeix a la col·lecció.
        Si una imatge no existeix, l'ignora i continua processant.
        Emmagatzema internament els UUID de les imatges vàlides."""

        self._clear()

        if file == "":
            print("ERROR: No s'ha trobat cap arxiu JSON")
            return

        path = file if os.path.isabs(file) else os.path.join(cfg.get_root(), file)
        if not os.path.isfile(path) and os.path.isfile(file):
            path = file
        if not os.path.isfile(path):
            print(f"ERROR: No s'ha trobat cap arxiu JSON {path}")
            return

        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (OSError, ValueError) as e:
            print(f"ERROR: No s'ha pogut llegir l'arxiu JSON {path}: {e}")
            return

        self.gallery_name = str(data.get("gallery_name", ""))
        self.description = str(data.get("description", ""))
        self.created_date = str(data.get("created_date", ""))

        llista = data.get("images", [])

        prefix = os.path.basename(os.path.normpath(cfg.get_root())) + "/"

        for p in llista:
            rel = p.replace("\\", "/")
            candidats = [rel]
            if rel.startswith(prefix):
                candidats.append(rel[len(prefix):])

            fCano = None
            for c in candidats:
                if os.path.isfile(os.path.join(cfg.get_root(), c)):
                    fCano = c
                    break
            if fCano is None:
                continue

            uuid = self.image_id.get_uuid(fCano)
            if uuid is None:
                uuid = self.image_id.generate_uuid(fCano)
            if uuid is not None:
                self.images.append(uuid)

    def show(self) -> None:
        """Visualitza totes les imatges de la galeria en ordre utilitzant
        ImageViewer.show_image()."""

        print(f"Galeria:  {self.gallery_name}")
        print(f"Descripció:  {self.description}")
        print(f"Data:  {self.created_date}")
        print(f"Total imatges:  {len(self.images)}")

        for uuid in self.images:
            if self.image_viewer is not None:
                self.image_viewer.show_image(uuid, cfg.DISPLAY_MODE)
            else:
                print(f"UUID: {uuid}")

    def add_image_at_end(self, uuid: str) -> None:
        """Afegeix una imatge al final de la galeria."""

        if uuid is None:
            return
        self.images.append(uuid)

    def remove_first_image(self) -> None:
        """Elimina la primera imatge de la galeria."""

        if len(self.images) > 0:
            del self.images[0]

    def remove_last_image(self) -> None:
        """Elimina l'última imatge de la galeria."""

        if len(self.images) > 0:
            self.images.pop()
