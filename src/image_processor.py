from typing import Final
import os
from PIL import Image
from datetime import datetime


IMAGE_SIZE: Final[int] = 640
DATASET_FOLDER: Final = "dataset"


class ImageProcessor:

    def __init__(self, path_to_images_folder: str, image_size: int = IMAGE_SIZE) -> None:
        if not os.path.isdir(path_to_images_folder):
            raise ValueError(f"This folder {path_to_images_folder} doesnt exist")
        self.path_to_images_folder = path_to_images_folder
        self.image_size = image_size
        self.current_date = datetime.now().strftime("%Y%m%d%H%M%S")
        self.output_folder = os.path.join(DATASET_FOLDER, self.current_date)

    def process_folder(self) -> None:
        """Create an output folder, loop inside the images folder and process them"""
        os.makedirs(self.output_folder, exist_ok=True)
        for image in os.listdir(self.path_to_images_folder):
            path_to_image = f"{self.path_to_images_folder}/{image}"
            self._process_image(path_to_image)

    def _process_image(self, image_path: str) -> None:
        """Process image like so :
            - Open it
            - Resize it to a square format
            - Add some padding if it is not a square
            - Save the image in a new folder 'dataset'

        Args:
            image_path (str): path to the image to process
        """
        image = Image.open(image_path)
        resized_image = self._image_resizing(image)
        padded_image = self._add_padding(resized_image)
        self._save(padded_image, image_path)

    def _image_resizing(self, image: Image.Image) -> Image.Image:
        """Resize the image to a square format, using a specific size
            - Used with resize() from pillow
            - Handle case where width is greater, smaller or equal to height
            - Keep the aspect ratio

        Args:
            image (Image.Image): image to resize

        Returns:
            Image.Image: resized image
        """
        width, height = image.size
        if width > height:
            new_width = self.image_size
            new_height = int(height * (self.image_size / width))
        elif width < height:
            new_width = int(width * (self.image_size / height))
            new_height = self.image_size
        else:
            new_width = new_height = self.image_size

        return image.resize((new_width, new_height))

    def _add_padding(self, resized_image: Image.Image) -> Image.Image:
        """Add some padding to the image if it is not a square
            - Padding will be added to the right if width < height
            - Padding will be added to the bottom if width > height
            - Unique color (114, 114, 144) is used for RGV mode, 114 for L mode

        Args:
            resized_image (Image.Image): image to add padding

        Returns:
            Image.Image: image with padding
        """
        width, height = resized_image.size
        if width == height:
            return resized_image
        else:
            color = (114, 114, 144) if resized_image.mode == "RGB" else 114
            result = Image.new(
                resized_image.mode, (self.image_size, self.image_size), color
            )
            result.paste(resized_image, (0, 0))
            return result

    def _save(self, image: Image.Image, image_path: str) -> None:
        """Save the image inside dataset folder inside a folder with the current date

        Args:
            image (Image.Image): the image to save
            image_path (str): the path to the image to save
        """
        image_name = image_path.split("/")[-1]
        output_path = os.path.join(self.output_folder, image_name)
        image.save(output_path)
