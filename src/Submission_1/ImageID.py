# -*- coding: utf-8 -*-
"""
ImageID.py : ** REQUIRED ** El vostre codi de la classe ImageID.

Aquesta classe s'encarrega de generar i gestionar identificadors únics (UUID)
per a cada imatge de la col·lecció.

Funcionalitat:
    - Generar un UUID únic a partir del path canònic d'un arxiu
    - Mantenir un registre dels UUID generats per evitar col·lisions
    - Permetre consultar i eliminar UUID

Mètodes a implementar:
    - generate_uuid(file: str) -> str
        Genera un UUID únic per a l'arxiu especificat.
        Ha de comprovar que el UUID no estigui ja en ús.
        Si hi ha col·lisió (cas extremadament improbable), retorna None i
        mostra un missatge d'error.

    - get_uuid(file: str) -> str
        Retorna el UUID associat a l'arxiu, si ja ha estat generat.
        Si no existeix, retorna None.

    - remove_uuid(uuid: str) -> None
        Elimina el UUID del registre d'identificadors actius.
        Després d'eliminar-lo, aquest UUID es podrà tornar a utilitzar.

Notes:
    - Els UUID han de seguir el format estàndard (128 bits)
    - Podeu utilitzar la funció cfg.get_uuid() com a base
    - Els UUID s'emmagatzemen com a strings
    - Un UUID només es pot generar una vegada (fins que s'elimini)
"""


import os
import cfg


class ImageID:
    def __init__(self):
        self._file_to_uuid = {}
        self._uuid_to_file = {}

    def __len__(self):
        return len(self._file_to_uuid)

    def __str__(self):
        return "ImageID(" + str(len(self._file_to_uuid)) + " uuids)"

    @staticmethod
    def _canonica(file: str) -> str:
        """Un path absolut es converteix a canònic (relatiu a ROOT_DIR).
        Un path que ja és relatiu es deixa tal qual: tornar-lo a passar per
        cfg.get_canonical_pathfile() el trencaria ("../xxx.png")."""

        if file == "":
            return file
        if os.path.isabs(file):
            return cfg.get_canonical_pathfile(file)
        return os.path.normpath(file).replace(os.sep, "/")

    def generate_uuid(self, file: str) -> str:
        """Genera un UUID únic per a l'arxiu especificat.
        Ha de comprovar que el UUID no estigui ja en ús.
        Si hi ha col·lisió (cas extremadament improbable), retorna None i
        mostra un missatge d'error."""

        if not isinstance(file, str):
            return None

        ruta_canonica = self._canonica(file)
        nuevo_uuid = str(cfg.get_uuid(ruta_canonica))

        if nuevo_uuid in self._uuid_to_file:
            print(f"ERROR: Col·lisió detectada per al fitxer {ruta_canonica}")
            return None

        self._file_to_uuid[ruta_canonica] = nuevo_uuid
        self._uuid_to_file[nuevo_uuid] = ruta_canonica
        return nuevo_uuid

    def get_uuid(self, file: str) -> str:
        """Retorna el UUID associat a l'arxiu, si ja ha estat generat.
        Si no existeix, retorna None."""

        if not isinstance(file, str):
            return None

        resultado = self._file_to_uuid.get(self._canonica(file))
        if resultado is None and file != "":
            resultado = self._file_to_uuid.get(cfg.get_canonical_pathfile(file))
        return resultado

    def remove_uuid(self, uuid: str) -> None:
        """Elimina el UUID del registre d'identificadors actius.
        Després d'eliminar-lo, aquest UUID es podrà tornar a utilitzar."""

        ruta_canonica = self._uuid_to_file.pop(uuid, None)
        if ruta_canonica is not None:
            self._file_to_uuid.pop(ruta_canonica, None)
