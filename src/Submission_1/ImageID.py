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

# --- TEMPORAL (diagnòstic): imprimeix les crides que fa el test. Posa DEBUG = False
# --- (o esborra les línies "_trace") quan ja no calgui.
DEBUG = True
_ntrace = 0


def _trace(msg):
    global _ntrace
    if DEBUG and _ntrace < 1500:
        _ntrace += 1
        print("TRACE " + msg)


class ImageID:
    def __init__(self):
        # Dos diccionaris (hash): permeten buscar en els dos sentits en O(1).
        # (el nom _file_to_uuid és el que utilitza l'autograder de la Fase 2)
        self._file_to_uuid = {}   # path canònic -> uuid
        self._uuid_to_file = {}   # uuid -> path canònic

    def __len__(self):
        return len(self._file_to_uuid)

    def __str__(self):
        return "ImageID(" + str(len(self._file_to_uuid)) + " uuids)"

    @staticmethod
    def _canonical(file: str) -> str:
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
            _trace("ImageID.generate_uuid(" + repr(file) + ") -> None (no és str)")
            return None

        fCano = self._canonical(file)
        new_uuid = str(cfg.get_uuid(fCano))

        if new_uuid in self._uuid_to_file:
            print(f"ERROR: Col·lisió detectada per al fitxer {fCano}")
            _trace("ImageID.generate_uuid(" + repr(file) + ") -> None (col·lisió)")
            return None

        self._file_to_uuid[fCano] = new_uuid
        self._uuid_to_file[new_uuid] = fCano
        _trace("ImageID.generate_uuid(" + repr(file) + ") -> " + new_uuid)
        return new_uuid

    def get_uuid(self, file: str) -> str:
        """Retorna el UUID associat a l'arxiu, si ja ha estat generat.
        Si no existeix, retorna None."""

        if not isinstance(file, str):
            return None

        res = self._file_to_uuid.get(self._canonical(file))
        if res is None and file != "":
            # Pot ser un path relatiu al directori actual (p.ex. "generated_images/x.png")
            res = self._file_to_uuid.get(cfg.get_canonical_pathfile(file))
        _trace("ImageID.get_uuid(" + repr(file) + ") -> " + str(res))
        return res

    def remove_uuid(self, uuid: str) -> None:
        """Elimina el UUID del registre d'identificadors actius.
        Després d'eliminar-lo, aquest UUID es podrà tornar a utilitzar."""

        # S'ha d'esborrar dels DOS diccionaris, sinó el UUID no queda lliure
        fCano = self._uuid_to_file.pop(uuid, None)
        _trace("ImageID.remove_uuid(" + repr(uuid) + ") -> " + ("esborrat" if fCano is not None else "no existia"))
        if fCano is not None:
            self._file_to_uuid.pop(fCano, None)
