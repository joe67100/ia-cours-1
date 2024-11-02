## Cours 1 - IA

### Objectif
- Créer une pipeline python pour le traitement d'images

### Mise en place
- Cloner le projet
- Installer `Python 3.11`
- Créer un environnement virtuel
- Installer les requirements
`pip install -r requirements.txt`
- Installer pre-commit : `pre-commit install`

### Utilisation
- Exécuter le script `main.py` en ligne de commande ou depuis la configuration PyCharm

### Exemples

```python
""" Permet de process une image spécifique en spécifiant le chemin de l'image et le chemin de sauvegarde """
def main():
    image_processor = ImageProcessor()
    image_processor.process_image("input_images/000000000009.jpg", "output_images")
```
```python
""" Permet de process tout un répertoire d'images """
def main():
    image_processor = ImageProcessor(f"{os.getcwd()}/input_images")
    image_processor.process_folder()

ou

def main():
    image_processor = ImageProcessor()
    image_processor.set_input_folder(f"{os.getcwd()}/input_images")
    image_processor.process_folder()
```
