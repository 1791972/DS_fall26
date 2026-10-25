import cfg
from ImageFiles import ImageFiles
from ImageID import ImageID
from ImageData import ImageData
from SearchMetadata import SearchMetadata

archivos = ImageFiles()
ids = ImageID()
datos = ImageData()

archivos.reload_fs(cfg.get_root())
for ruta in archivos.files_added():
    relativa = cfg.get_canonical_pathfile(ruta)
    uuid = ids.generate_uuid(relativa)
    datos.add_image(uuid, relativa)
    datos.load_metadata(uuid)

print("Imatges carregades:", len(datos))

buscador = SearchMetadata(datos)

por_prompt = buscador.prompt("cyberpunk")
print("prompt:", len(por_prompt))

por_model = buscador.model("SD")
print("model:", len(por_model))

por_sampler = buscador.sampler("k_lms")
print("sampler:", len(por_sampler))

por_data = buscador.date("2023")
print("data:", len(por_data))

y = buscador.and_operator(por_model, por_data)
print("model SD AND data 2023:", len(y))

o = buscador.or_operator(por_prompt, por_data)
print("prompt cyberpunk OR data 2023:", len(o))

from Gallery import Gallery

g = Gallery(ids, None)
g.load_file("prova.json")
print("Galeria prova.json:", len(g), "imatges")
g.show()

g2 = Gallery(ids, None)
for u in por_model[:5]:
    g2.add_image_at_end(u)
print("Galeria des de cerca:", len(g2))   # 5

g2.remove_first_image()
g2.remove_last_image()
print("Despres de treure primera i ultima:", len(g2))   # 3
