from typing import Final
import os
from PIL import Image
from datetime import datetime


IMAGE_SIZE: Final[int] = 640


class ImageProcessor:

    def __init__(self, path_to_images_folder: str) -> None:
        if not os.path.isdir(path_to_images_folder):
            raise ValueError(f"This folder {path_to_images_folder} doesnt exist")
        self.path_to_images_folder = path_to_images_folder
        self.current_date = datetime.now().strftime("%Y%m%d%H%M%S")

    def process_folder(self, image_size: int = IMAGE_SIZE) -> None:
        """Create an output folder, loop inside the images folder and process them

        Args :
            image_size (int): size of the image to resize to.
            (image_size x image_size) Default is IMAGE_SIZE (640px).
        """
        self._create_output_images_folder()
        for image in os.listdir(self.path_to_images_folder):
            path_to_image = f"{self.path_to_images_folder}/{image}"
            self.process_image(path_to_image, image_size)

    def process_image(self, image_path: str, image_size: int) -> None:
        """Process image like so :
            - Open it
            - Resize it to a square format
            - Add some padding if it is not a square
            - Save the image in a new folder 'dataset'

        Args:
            image_path (str): path to the image to process
            image_size (int): size of the image to resize to
        """
        image = Image.open(image_path)
        resized_image = self._image_resizing(image, image_size)
        padded_image = self._add_padding(resized_image, image_size)
        self._save(padded_image, image_path)

    @staticmethod
    def _image_resizing(image: Image.Image, image_size: int) -> Image.Image:
        """Resize the image to a square format, using a specific size
            - Used with resize() from pillow
            - Handle case where width is greater, smaller or equal to height
            - Keep the aspect ratio

        Args:
            image (Image.Image): image to resize
            image_size (int): size of the image to resize to

        Returns:
            Image.Image: resized image
        """
        width, height = image.size
        if width > height:
            new_width = image_size
            new_height = int(height * (image_size / width))
        elif width < height:
            new_width = int(width * (image_size / height))
            new_height = image_size
        else:
            new_width = new_height = image_size

        return image.resize((new_width, new_height))

    @staticmethod
    def _add_padding(resized_image: Image.Image, image_size: int) -> Image.Image:
        """Add some padding to the image if it is not a square
            - Padding will be added to the right if width < height
            - Padding will be added to the bottom if width > height
            - Unique color (114, 114, 144) is used
            - 114, 114, 144 won't work if its L mode

        Args:
            resized_image (Image.Image): image to add padding
            image_size (int): size of the image to resize to

        Returns:
            Image.Image: image with padding
        """
        width, height = resized_image.size
        if width == height:
            return resized_image
        else:
            color = (114, 114, 144) if resized_image.mode == "RGB" else 114
            result = Image.new(resized_image.mode, (image_size, image_size), color)
            result.paste(resized_image, (0, 0))
            return result

    def _save(self, image: Image.Image, image_path: str) -> None:
        """Save the image inside dataset folder inside a folder with the current date

        Args:
            image (Image.Image): the image to save
            image_path (str): the path to the image to save
        """
        image_name = image_path.split("/")[-1]
        image.save(f"dataset/{self.current_date}/{image_name}")

    def _create_output_images_folder(self) -> None:
        if not os.path.isdir("dataset"):
            os.mkdir("dataset")
        if not os.path.isdir(f"dataset/{self.current_date}"):
            os.mkdir(f"dataset/{self.current_date}")
