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

# --- TEMPORAL (diagnòstic): imprimeix les crides que fa el test. Posa DEBUG = False
# --- (o esborra les línies "_trace") quan ja no calgui.
DEBUG = True
_ntrace = 0


def _trace(msg):
    global _ntrace
    if DEBUG and _ntrace < 250:
        _ntrace += 1
        print("TRACE " + msg)



def _read_dimensions(path):
    """Llegeix (width, height) del chunk IHDR d'un PNG, sense PIL ni cfg:
    signatura (8 bytes) + longitud (4) + 'IHDR' (4) + width (4) + height (4)."""

    try:
        with open(path, 'rb') as f:
            header = f.read(24)
    except OSError:
        return (None, None)
    if len(header) == 24 and header[:8] == b'\x89PNG\r\n\x1a\n' and header[12:16] == b'IHDR':
        return (int.from_bytes(header[16:20], 'big'), int.from_bytes(header[20:24], 'big'))
    return (None, None)


class ImageData:
    def __init__(self):
        # uuid -> {'file': path, 'metadata': dict, 'dimensions': (w, h), 'loaded': bool}
        self.data = {}

    def __len__(self):
        _trace("ImageData.__len__() -> " + str(len(self.data)))
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

        # Insercions sense sentit o imatge ja existent: s'ignoren
        if not isinstance(uuid, str) or not isinstance(file, str) or file == "":
            _trace("ImageData.add_image(" + repr(uuid) + ", " + repr(file) + ") -> ignorada (sense sentit)")
            return
        if uuid in self.data:
            _trace("ImageData.add_image(" + repr(uuid) + ", " + repr(file) + ") -> ignorada (ja existeix)")
            return
        _trace("ImageData.add_image(" + repr(uuid) + ", " + repr(file) + ") -> afegida")

        # El path es guarda tal com arriba (és el path relatiu a ROOT_DIR)
        self.data[uuid] = {'file': file, 'metadata': {}, 'dimensions': (None, None), 'loaded': False}

    def remove_image(self, uuid: str) -> None:
        """Elimina la imatge i totes les seves metadades de la col·lecció."""

        _trace("ImageData.remove_image(" + repr(uuid) + ") -> " + ("esborrada" if uuid in self.data else "no existia"))
        self.data.pop(uuid, None)

    def get_filename(self, uuid: str) -> str:
        """Retorna el path guardat de l'arxiu de la imatge ("None" si no existeix)."""

        if uuid not in self.data:
            _trace("ImageData.get_filename(" + repr(uuid) + ") -> uuid desconegut")
            return "None"
        return self.data[uuid]['file']

    def _full_path(self, file: str) -> str:
        path = os.path.join(cfg.get_root(), file)
        if not os.path.isfile(path) and os.path.isfile(file):
            return file                 # era un path vàlid des del directori actual
        return path

    def load_metadata(self, uuid: str) -> None:
        """Llegeix les metadades embegudes en l'arxiu PNG i les emmagatzema.
        Aquest mètode es pot cridar múltiples vegades (p.ex. si l'arxiu canvia)."""

        if uuid not in self.data:
            _trace("ImageData.load_metadata(" + repr(uuid) + ") -> uuid desconegut")
            return

        entry = self.data[uuid]
        path = self._full_path(entry['file'])
        _trace("ImageData.load_metadata(" + repr(uuid) + ") llegint " + path)

        meta = cfg.read_png_metadata(path)      # None si l'arxiu no es pot llegir
        if meta is None:
            entry['metadata'] = {}
            entry['dimensions'] = (None, None)
        else:
            entry['metadata'] = meta
            entry['dimensions'] = _read_dimensions(path)
        entry['loaded'] = True

    def _get_field(self, uuid: str, name: str) -> str:
        # Només consulta el que ja s'ha carregat amb load_metadata()
        if uuid not in self.data:
            _trace("ImageData." + name + "(" + repr(uuid) + ") -> uuid desconegut")
            return "None"
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
            _trace("ImageData.get_dimensions(" + repr(uuid) + ") -> uuid desconegut")
            return (None, None)
        return self.data[uuid]['dimensions']
