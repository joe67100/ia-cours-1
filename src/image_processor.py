from typing import Final
import os

IMAGE_SIZE: Final[int] = 640


class ImageProcessor:

    def __init__(self, path_to_images_folder: str) -> None:
        if not os.path.isdir(path_to_images_folder):
            raise ValueError(f"This folder {path_to_images_folder} doesnt exist")
        self.path_to_images_folder = path_to_images_folder

    def process_folder(self, image_size: int = IMAGE_SIZE) -> None:
        """Loop inside the images folder and process them

        Args   :
            image_size (int): The size of the image to resize to.
            (image_size x image_size) Default is IMAGE_SIZE (640px).
        """
        for image in os.listdir(self.path_to_images_folder):
            path_to_image = f"{self.path_to_images_folder}/{image}"
            self._process_image(path_to_image, image_size)

    def _process_image(self, image: str, image_size: int) -> None:
        """Process image like so :
            - Open it
            - Resize it to a square format
            - Add some padding if required
            - Save the image in a new folder 'dataset'

        Args:
            image (str): The path to the image to process
            image_size (int): The size of the image to resize to (image_size x image_size)

        Returns:

        Examples:
        """
        with open(image, "r"):
            print(f"Processing image : {image}")

    def _image_resizing(self):
        pass

    def _image_padding(self):
        pass

    def _save(self):
        pass
