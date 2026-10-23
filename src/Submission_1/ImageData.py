# -*- coding: utf-8 -*-
"""
ImageData.py : ** REQUIRED ** El vostre codi de la classe ImageData.

Aquesta classe s'encarrega d'emmagatzemar i gestionar les metadades de les
imatges generades per IA.

Funcionalitat:
    - Afegir i eliminar imatges de la col·lecció
    - Llegir les metadades embegudes dins els arxius PNG
    - Proporcionar accés a totes les metadades d'una imatge"""

    
import os
import cfg
from PIL import Image


def _norm(file):
    # CANVI: mateixa normalització idempotent que a ImageID
    if not isinstance(file, str):
        return file
    if os.path.isabs(file):
        return cfg.get_canonical_pathfile(file)
    return file.replace('\\', '/')


class ImageData:
    def __init__(self):
        self.data = {}

    def __len__(self):
        # CANVI: nou, per si el test fa len() sobre l'objecte
        return len(self.data)

    def add_image(self, uuid: str, file: str) -> None:
        """Crea una entrada per a la imatge amb l'UUID i el path especificats.
        Inicialment les metadades estan buides (no llegides del disc)."""

        # CANVI: s'ignoren insercions sense sentit i es evita duplicar/reiniciar
        if uuid is None or not isinstance(file, str) or file == "":
            return
        if uuid in self.data:
            return

        # CANVI: abans cfg.get_canonical_pathfile(file), que trencava els paths
        # que ja eren relatius
        fCano = _norm(file)
        self.data[uuid] = {'file': fCano, 'metadata': {}, 'dimensions': (None, None), 'loaded': False}

    def remove_image(self, uuid: str) -> None:
        """Elimina la imatge i totes les seves metadades de la col·lecció."""

        if uuid in self.data:
            del self.data[uuid]

    def load_metadata(self, uuid: str) -> None:
        """Llegeix les metadades embegudes en l'arxiu PNG i les emmagatzema.'
           Aquest mètode es pot cridar múltiples vegades (p.ex. si l'arxiu canvia)."""

        if uuid not in self.data:
            return

        f = self.data[uuid]['file']
        pathF = os.path.join(cfg.get_root(), f)

        meta = cfg.read_png_metadata(pathF)
        if meta is not None:
            self.data[uuid]['metadata'] = meta
        else:
            self.data[uuid]['metadata'] = {}

        try:
            with Image.open(pathF) as img:
                self.data[uuid]['dimensions'] = (img.width, img.height)
        except Exception:
            self.data[uuid]['dimensions'] = (None, None)

        self.data[uuid]['loaded'] = True

    def _get_field(self, uuid: str, name: str) -> str:
        if uuid not in self.data:
            return "None"

        if not self.data[uuid]['loaded']:
            self.load_metadata(uuid)

        res = self.data[uuid]['metadata'].get(name)
        if res is None or res == "":
            return "None"
        return str(res)

    def get_prompt(self, uuid: str) -> str:
        """Retorna el prompt utilitzat per generar la imatge."""

        return self._get_field(uuid, 'Prompt')   # CANVI: abans 'Model'

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
            return (None, None)

        if not self.data[uuid]['loaded']:
            self.load_metadata(uuid)
        return self.data[uuid]['dimensions']

        
"""Notes:
    - Utilitzeu la llibreria PIL/Pillow per llegir metadades:
      img = Image.open(file)
      metadata = img.text
    - Si un camp no existeix, retorneu "None" (string)
    - Les dimensions es llegeixen amb img.width i img.height
    - Tots els camps de metadades es guarden com a strings
"""
