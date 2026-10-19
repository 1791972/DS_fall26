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
from ImageID import ImageID
from ImageViewer import ImageViewer

class Gallery:
    def __init__(self, image_id, image_viewer):
        self.gallery_name = ""
        self.description = ""
        self.created_date = ""
        self.uuids = []
        self.image_id = image_id if image_id is not None else ImageID()
        self.image_viewer = image_viewer if image_viewer is not None else ImageViewer()

    def load_file(self, file: str) -> None:
        """Llegeix un arxiu JSON amb la definició de la galeria.
        Ha de validar que cada imatge referenciada existeix a la col·lecció.
        Si una imatge no existeix, l'ignora i continua processant.
        Emmagatzema internament els UUID de les imatges vàlides."""

        path = os.path.join(cfg.get_root(), file) if not os.path.isabs(file) else file
        if not os.path.isfile(path):
            print(f"ERROR: No s'ha trobat cap arxiu JSON {file}")
            return

        with open(path, 'r') as f:
            data = json.load(f)

        self.gallery_name = data.get("gallery_name", "")
        self.description = data.get("description", "")
        self.created_date = data.get("created_date", "")
        self.uuids = []

        for p in data.get("images", []):
            fCano = cfg. get_canonical_pathfile(p)
            pathF = os.path.join(cfg.get_root(), fCano)

            if os.path.isfile(pathF):
                if self.image_id:
                    new_uuid = self.image_id.get_uuid(fCano)
                    if new_uuid is None:
                        new_uuid = self.imge_id.generate_uuid(fCano)
                else:
                    new_uuid = str(cfg.get_uuid(fCano))

                if new_uuid:
                    self.uuids.append(new_uuid)

    def show(self) -> None:
        """Visualitza totes les imatges de la galeria en ordre utilitzant
        ImageViewer.show_image()."""

        print(f"Galeria:  {self.gallery_name}")
        print(f"Descripció:  {self.description}")
        print(f"Data:  {self.created_date}")
        print(f"Total imatges:  {len(self.uuids)}")

        for uuid in self.uuids:
            if self.image_viewer:
                self.image_viewer.show_image(uuid, cfg.DISPLAY_MODE)
            else:
                print(f"UUID: {uuid}")

    def add_image_at_end(self, uuid: str) -> None:
        """Afegeix una imatge al final de la galeria."""

        self.uuids.append(uuid)

    def remove_first_image(self) -> None:
        """Elimina la primera imatge de la galeria."""

        if len(self.uuids) > 0:
            self.image_uuids.pop(0)

    def remove_last_image(self) -> None:
        """Elimina l'última imatge de la galeria."""

        if len(self.uuids) > 0:
            self.uuids.pop()


"""Notes:
    - Utilitzeu la llibreria json per llegir els arxius
    - Els paths dins el JSON són relatius a ROOT_DIR
    - Cada galeria és un objecte independent (instància de Gallery)
    - Podeu tenir múltiples galeries actives simultàniament
    - Les operacions d'afegir/eliminar són ràpides (no busquen a la llista)
"""
