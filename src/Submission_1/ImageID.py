# -*- coding: utf-8 -*-
"""
ImageID.py : ** REQUIRED ** El vostre codi de la classe ImageID.

Aquesta classe s'encarrega de generar i gestionar identificadors únics (UUID)
per a cada imatge de la col·lecció.

Funcionalitat:
    - Generar un UUID únic a partir del path canònic d'un arxiu
    - Mantenir un registre dels UUID generats per evitar col·lisions
    - Permetre consultar i eliminar UUID"""

import cfg

class ImageID:
    def __init__(self):
        self.file_uuid = {}
        self.uuid_file = {}

    def generate_uuid(self, file: str) -> str:
        """Genera un UUID únic per a l'arxiu especificat.
            Ha de comprovar que el UUID no estigui ja en ús.
            Si hi ha col·lisió (cas extremadament improbable), retorna None i
            mostra un missatge d'error."""
        
        fCano = cfg.get_canonical_pathfile(file)
        if fCano in self.file_uuid:
            return self.file_uuid[fCano]

        new_uuid = str(cfg.get_uuid(fCano))
        if new_uuid in self.uuid_file:
            print(f"ERROR: Col·lisió detectada per al fitxer {fCano}")
            return None

        self.file_uuid[fCano] = new_uuid
        self.uuid_file[new_uuid] = fCano
        return new_uuid
        
    def get_uuid(file: str) -> str:
        """Retorna el UUID associat a l'arxiu, si ja ha estat generat.
            Si no existeix, retorna None."""

        fCano = cfg.get_canonical_pathfile(file)
        return self.file_uuid.get(fCano, None)

    def remove_uuid(uuid: str) -> None:
        """Elimina el UUID del registre d'identificadors actius.
            Després d'eliminar-lo, aquest UUID es podrà tornar a utilitzar."""

        remove = None
        for path, actual_uuid in self.file_uuid.items():
            if actual_uuid == uuid:
                remove = path
                break

        if remove:
            del self.file_uuid[remove]


"""Notes:
    - Els UUID han de seguir el format estàndard (128 bits)
    - Podeu utilitzar la funció cfg.get_uuid() com a base
    - Els UUID s'emmagatzemen com a strings
    - Un UUID només es pot generar una vegada (fins que s'elimini)
"""
