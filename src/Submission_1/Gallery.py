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


def _norm(file):
    # CANVI: mateixa normalització que a ImageID (no re-relativitza els
    # paths que ja són relatius a ROOT_DIR)
    if not isinstance(file, str):
        return file
    if os.path.isabs(file):
        return cfg.get_canonical_pathfile(file)
    return file.replace('\\', '/')


class Gallery:
    def __init__(self, image_id, image_viewer):
        self.gallery_name = ""
        self.description = ""
        self.created_date = ""
        self.uuids = []
        self.image_id = image_id if image_id is not None else ImageID()
        # CANVI: ImageViewer exigeix un paràmetre (image_data)
        self.image_viewer = image_viewer if image_viewer is not None else ImageViewer(None)

    def __len__(self):
        # CANVI: requerit pel test
        return len(self.uuids)

    def __str__(self):
        # CANVI: requerit pel test
        return "Gallery(" + self.gallery_name + ", " + str(len(self.uuids)) + " imatges)"

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

        # CANVI: prefix "generated_images/" que pot venir als paths del JSON
        # (l'exemple de l'enunciat el porta, però els paths són relatius a ROOT_DIR)
        prefix = os.path.basename(os.path.normpath(cfg.get_root())) + "/"

        for p in data.get("images", []):
            # CANVI: abans cfg.get_canonical_pathfile(p), que trencava els paths
            # relatius. Ara es proven els candidats i es tria el que existeix.
            fCano = _norm(p)
            if not isinstance(fCano, str):
                continue
            candidats = [fCano]
            if fCano.startswith(prefix):
                candidats.append(fCano[len(prefix):])

            fCano = None
            for c in candidats:
                if os.path.isfile(os.path.join(cfg.get_root(), c)):
                    fCano = c
                    break
            if fCano is None:
                continue   # la imatge no existeix: s'ignora

            # CANVI: "is not None" (amb __len__ un ImageID buit seria "fals")
            if self.image_id is not None:
                new_uuid = self.image_id.get_uuid(fCano)
                if new_uuid is None:
                    new_uuid = self.image_id.generate_uuid(fCano)   # CANVI: abans self.imge_id
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
            if self.image_viewer is not None:   # CANVI: "is not None"
                self.image_viewer.show_image(uuid, cfg.DISPLAY_MODE)
            else:
                print(f"UUID: {uuid}")

    def add_image_at_end(self, uuid: str) -> None:
        """Afegeix una imatge al final de la galeria."""

        self.uuids.append(uuid)

    def remove_first_image(self) -> None:
        """Elimina la primera imatge de la galeria."""

        if len(self.uuids) > 0:
            self.uuids.pop(0)   # CANVI: abans self.image_uuids.pop(0)

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
