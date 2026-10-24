# -*- coding: utf-8 -*-
"""
ImageData.py : ** REQUIRED ** El vostre codi de la classe ImageData.

Aquesta classe s'encarrega d'emmagatzemar i gestionar les metadades de les
imatges generades per IA.

Funcionalitat:
    - Afegir i eliminar imatges de la col·lecció
    - Llegir les metadades embegudes dins els arxius PNG
    - Proporcionar accés a totes les metadades d'una imatge

Mètodes a implementar:
    - add_image(uuid: str, file: str) -> None
        Crea una entrada per a la imatge amb l'UUID i el path especificats.
        Inicialment les metadades estan buides (no llegides del disc).

    - remove_image(uuid: str) -> None
        Elimina la imatge i totes les seves metadades de la col·lecció.

    - load_metadata(uuid: str) -> None
        Llegeix les metadades embegudes en l'arxiu PNG i les emmagatzema.
        Aquest mètode es pot cridar múltiples vegades (p.ex. si l'arxiu canvia).

    - get_prompt(uuid: str) -> str
        Retorna el prompt utilitzat per generar la imatge.

    - get_model(uuid: str) -> str
        Retorna el model d'IA utilitzat (p.ex. "SD2", "DALL-E", "Midjourney").

    - get_seed(uuid: str) -> str
        Retorna la llavor aleatòria utilitzada en la generació.

    - get_cfg_scale(uuid: str) -> str
        Retorna el CFG Scale (guidance scale) utilitzat.

    - get_steps(uuid: str) -> str
        Retorna el nombre de passos d'iteració del model.

    - get_sampler(uuid: str) -> str
        Retorna l'algorisme de mostreig utilitzat.

    - get_generated(uuid: str) -> str
        Retorna "true" si la imatge està marcada com a generada.

    - get_created_date(uuid: str) -> str
        Retorna la data de creació en format YYYY-MM-DD.

    - get_dimensions(uuid: str) -> tuple
        Retorna una tupla (width, height) amb les dimensions de la imatge.

Notes:
    - Utilitzeu la llibreria PIL/Pillow per llegir metadades:
      img = Image.open(file)
      metadata = img.text
    - Si un camp no existeix, retorneu "None" (string)
    - Les dimensions es llegeixen amb img.width i img.height
    - Tots els camps de metadades es guarden com a strings
"""


import os
import cfg
from PIL import Image


class ImageData:
    def __init__(self):
        self.data = {}

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return "ImageData(" + str(len(self.data)) + " imatges)"

    def get_uuids(self) -> list:
        """Retorna la llista d'UUID de les imatges (usat per SearchMetadata)."""

        return list(self.data.keys())

    def is_loaded(self, uuid: str) -> bool:
        """True si les metadades d'aquesta imatge ja s'han llegit del disc."""

        return uuid in self.data and self.data[uuid]['loaded']

    def add_image(self, uuid: str, file: str) -> None:
        """Crea una entrada per a la imatge amb l'UUID i el path especificats.
        Inicialment les metadades estan buides (no llegides del disc)."""

        if not uuid or not file or uuid in self.data:
            return

        if os.path.isabs(file):
            file = cfg.get_canonical_pathfile(file)
        self.data[uuid] = {'file': file, 'metadata': {}, 'dimensions': (None, None), 'loaded': False}

    def remove_image(self, uuid: str) -> None:
        """Elimina la imatge i totes les seves metadades de la col·lecció."""

        self.data.pop(uuid, None)

    def get_filename(self, uuid: str) -> str:
        """Retorna el path guardat de l'arxiu de la imatge (None si no existeix)."""

        if uuid not in self.data:
            return None
        return self.data[uuid]['file']

    def _full_path(self, file: str) -> str:
        path = os.path.join(cfg.get_root(), file)
        if not os.path.isfile(path) and os.path.isfile(file):
            return file
        return path

    def load_metadata(self, uuid: str) -> None:
        """Llegeix les metadades embegudes en l'arxiu PNG i les emmagatzema.
        Aquest mètode es pot cridar múltiples vegades (p.ex. si l'arxiu canvia)."""

        if uuid not in self.data:
            return

        entry = self.data[uuid]
        path = self._full_path(entry['file'])

        meta = cfg.read_png_metadata(path)
        if meta is None:
            entry['metadata'] = {}
            entry['dimensions'] = (None, None)
        else:
            entry['metadata'] = meta
            try:
                with Image.open(path) as img:
                    entry['dimensions'] = (img.width, img.height)
            except Exception:
                entry['dimensions'] = (None, None)
        entry['loaded'] = True

    def _get_field(self, uuid: str, name: str) -> str:
        if uuid not in self.data:
            return None
        value = self.data[uuid]['metadata'].get(name)
        if value is None or value == "":
            return "None"
        return str(value)

    def get_prompt(self, uuid: str) -> str:
        """Retorna el prompt utilitzat per generar la imatge."""
        return self._get_field(uuid, 'Prompt')

    def get_model(self, uuid: str) -> str:
        """Retorna el model d'IA utilitzat (p.ex. "SD2", "DALL-E", "Midjourney")."""
        return self._get_field(uuid, 'Model')

    def get_seed(self, uuid: str) -> str:
        """Retorna la llavor aleatòria utilitzada en la generació."""
        return self._get_field(uuid, 'Seed')

    def get_cfg_scale(self, uuid: str) -> str:
        """Retorna el CFG Scale (guidance scale) utilitzat."""
        return self._get_field(uuid, 'CFG_Scale')

    def get_steps(self, uuid: str) -> str:
        """Retorna el nombre de passos d'iteració del model."""
        return self._get_field(uuid, 'Steps')

    def get_sampler(self, uuid: str) -> str:
        """Retorna l'algorisme de mostreig utilitzat."""
        return self._get_field(uuid, 'Sampler')

    def get_generated(self, uuid: str) -> str:
        """Retorna "true" si la imatge està marcada com a generada."""
        return self._get_field(uuid, 'Generated')

    def get_created_date(self, uuid: str) -> str:
        """Retorna la data de creació en format YYYY-MM-DD."""
        return self._get_field(uuid, 'Created_Date')

    def get_dimensions(self, uuid: str) -> tuple:
        """Retorna una tupla (width, height) amb les dimensions de la imatge."""

        if uuid not in self.data:
            return None
        return self.data[uuid]['dimensions']
