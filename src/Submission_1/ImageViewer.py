# -*- coding: utf-8 -*-
"""
ImageViewer.py : ** REQUIRED ** El vostre codi de la classe ImageViewer.

Aquesta classe s'encarrega de visualitzar imatges i mostrar les seves metadades.

Funcionalitat:
    - Imprimir per pantalla les metadades d'una imatge
    - Mostrar la imatge en pantalla
    - Combinar ambdues accions segons la configuració"""


import os
import cfg
from PIL import Image

class ImageViewer:
    def __init__(self, image_data):
        self.image_data = image_data

    def print_image(self, uuid: str) -> None:
        """Imprimeix per pantalla totes les metadades de la imatge identificada
        per l'UUID. Ha de mostrar:
        - Dimensions (width x height)
        - Prompt (truncat si és molt llarg)
        - Model
        - Seed
        - CFG Scale
        - Steps
        - Sampler
        - Generated
        - Created Date
        - UUID
        - Path de l'arxiu"""

        if self.image_data is None or uuid not in self.image_data.data:
            print(f"ERROR: No s'han trobat dades per al UUID {uuid}")
            return

        prompt = self.image_data.get_prompt(uuid)
        if len(prompt) > 60:
            prompt_trunc = prompt[:57] + "..."
        else:
            prompt_trunc = prompt

        print(f"UUID:          {uuid}")
        print(f"Path Arxiu:    {self.image_data.data[uuid]['file']}")
        print(f"Dimensions:    {self.image_data.get_dimensions(uuid)}")
        print(f"Prompt:        {prompt_trunc}")
        print(f"Model:         {self.image_data.get_model(uuid)}")
        print(f"Seed:          {self.image_data.get_seed(uuid)}")
        print(f"CFG Scale:     {self.image_data.get_cfg_scale(uuid)}")
        print(f"Steps:         {self.image_data.get_steps(uuid)}")
        print(f"Sampler:       {self.image_data.get_sampler(uuid)}")
        print(f"Generated:     {self.image_data.get_generated(uuid)}")
        print(f"Created Date:  {self.image_data.get_created_date(uuid)}")

    def show_file(self, file: str) -> None:
        """Mostra la imatge especificada utilitzant PIL.
        Aquesta funció NO espera que la imatge es tanqui (asíncrona)."""

        path = os.path.join(cfg.get_root(), file)
        try:
            img = Image.open(path)
            img.show()
        except Exception as e:
            print(f"ERROR: No s'ha pogut obrir la imatge {file}: {e}")

    def show_image(self, uuid: str, mode: int) -> None:
        """Combina print_image() i show_file() segons el mode especificat:
        - mode 0: només metadades
        - mode 1: metadades + imatge
        - mode 2: només imatge
        Aquesta funció ha d'esperar que l'usuari tanqui la imatge abans
        de retornar (síncrona). Podeu utilitzar input() per fer una pausa."""

        if mode == 0:
            self.print_image(uuid)

        elif mode == 1:
            self.print_image(uuid)
            if self.image_data and uuid in self.image_data.data:
                path = self.image_data.data[uuid]['file']
                self.show_file(path)
                input("Prem ENTER per continuar")

        elif mode == 2:
            if self.image_data and uuid in self.image_data.data:
                path = self.image_data.data[uuid]['file']
                self.show_file(path)
                input("Prem ENTER per continuar")


"""Notes:
    - Utilitzeu cfg.DISPLAY_MODE per determinar el comportament per defecte
    - Per mostrar imatges: img.show() de PIL
    - Gestioneu les excepcions si la imatge no es pot mostrar
    - El format de sortida ha de ser llegible i ben organitzat
"""
