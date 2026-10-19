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


import os
import cfg 
from ImageFiles import ImageFiles
from ImageID import ImageID
from ImageData import ImageData
from ImageViewer import ImageViewer
from Gallery import Gallery
from SearchMetadata import SearchMetadata

def main():
    print("PROVES PER TESTEJAR LES FUNCIONALITATS\n")

    image_files = ImageFiles()
    image_files.reload_fs(cfg.get_root())
    added_files = image_files.files_added()
    print(f"Fitxer trobats: {len(added_files)}")

    image_id = ImageID()
    for path in added_files:
        image_id.generate_uuid(path)

    image_data = ImageData()
    for path in added_files:
        uuid = image_id.get_uuid(path)
        if uuid:
            image_data.add_image(uuid, path)

    image_viewer = ImageViewer(image_data = image_data)
    if added_files:
        uuid1 = image_id.get_uuid(added_files)
        print("\nMostrant metadades de la primera imatge:")
        image_viewer.print_image(uuid1)

    gallery = Gallery(image_id = image_id, image_viewer = image_viewer)
    json = os.paht.join(cfg.get_root(), "galeries", "sample_gallery.json")
    if os.path.exists(json):
        print("\nCarregant galeria JSON")
        gallery.load_file(json)
        gallery.show()

    search_metadata = SearchMetadata(image_data = image_data)
    res = search_metadata.prompt("cat")
    print(f"\nCerques amb la subcadena 'cat' al prompt: {len(res)} trobats.")

    search_gallery = Gallery(image_id = image_id, image_viewer = image_viewer)
    search_gallery.gallery_name = "Cerca: Cat"
    search_gallery.description = "Galeria generada a partir dels resultats de cerca"
    for uuid in res:
        search_gallery.add_image_at_end(uuid)
    print("\nMostrant galeria dinàmica creada a partir de la cerca:")
    search_gallery.show()

if __name__ == "__main__":
    main()


