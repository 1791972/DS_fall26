# -*- coding: utf-8 -*-
"""
p1_main.py : ** OPTIONAL ** Si heu fet un main vostre, poseu aquí el codi.
                            Aquest arxiu no s'avalua automàticament.

Aquí podeu posar el vostre codi de proves per testejar les funcionalitats
implementades.

Exemples d'ús:
    - Carregar la col·lecció d'imatges
    - Generar UUID per a totes les imatges
    - Llegir metadades d'algunes imatges
    - Visualitzar imatges
    - Carregar i mostrar galeries
    - Fer cerques i crear galeries a partir dels resultats
"""


import cfg
from ImageFiles import ImageFiles
from ImageID import ImageID
from ImageData import ImageData
from ImageViewer import ImageViewer
from Gallery import Gallery
from SearchMetadata import SearchMetadata


def main():
    # 1. Llistat dels PNG de la col·lecció
    files = ImageFiles()
    files.reload_fs(cfg.get_root())
    print(files)

    # 2. UUID de cada imatge + 3. metadades
    image_id = ImageID()
    image_data = ImageData()
    for f in files.files_added():
        rel = cfg.get_canonical_pathfile(f)      # path relatiu a ROOT_DIR
        uuid = image_id.generate_uuid(rel)
        if uuid is not None:
            image_data.add_image(uuid, rel)
            image_data.load_metadata(uuid)
    print(image_id)
    print(image_data)

    # 4. Visualitzar una imatge
    viewer = ImageViewer(image_data)
    primera = image_data.get_uuids()[0]
    viewer.show_image(primera, cfg.DISPLAY_MODE)

    # 5. Cerques i 6. galeria a partir d'una cerca
    search = SearchMetadata(image_data)
    trobades = search.or_operator(search.prompt("portrait"), search.model("SD2"))
    print("Cerca: " + str(len(trobades)) + " imatges")

    galeria = Gallery(image_id, viewer)
    for uuid in trobades:
        galeria.add_image_at_end(uuid)
    galeria.show()


if __name__ == "__main__":
    main()
