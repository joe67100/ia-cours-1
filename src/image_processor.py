from typing import Final
import os
from PIL import Image
from datetime import datetime


class ImageProcessor:
    """Class to process images (resize, add padding, save) using Pillow

    Attributes:
        IMAGE_SIZE (int): size to resize the image to. Default is 640
        DATASET_FOLDER (str): name of the folder where to save the images. Default is 'dataset'
        DATETIME_FORMAT (str): format to use for the folder name. Default is '%Y%m%d%H%M%S'
        input_folder (str): path to the folder containing the images to process
        image_size (int): size to resize the image to. Default is IMAGE_SIZE

    Methods:
        process_folder():
            Create an output folder, loop inside the images folder and process them

        process_image(image_path: str, output_folder: str):
            Process an image (resize, add padding, save)

        resize_image(image: Image.Image, size_to_resize: int = 0):
            Resize the image to a square format if possible

        add_padding(resized_image: Image.Image, background_color: tuple[int, ...] = (114,) * 3):
            Add padding to the image if it is not a square

        save_image(image: Image.Image, original_image_path: str, output_folder: str):
            Save the image

        output_dataset_folder_name():
            Return the name of the output folder

        set_input_folder(path: str):
            Set the path to the images folder
    """

    IMAGE_SIZE: Final[int] = 640
    DATASET_FOLDER: Final = "dataset"
    DATETIME_FORMAT: Final = "%Y%m%d%H%M%S"

    def __init__(self, input_folder: str = "", image_size: int = IMAGE_SIZE) -> None:
        self.input_folder = input_folder
        self.image_size = image_size

    def process_folder(self) -> None:
        """Create an output folder, loop inside the images folder and process them

        Raises:
            ValueError: no input folder was provided. set_input_folder() to set the input folder
        """
        if not os.path.isdir(self.input_folder):
            raise ValueError("No input folder was provided")
        output_folder = self.output_dataset_folder_name
        os.makedirs(output_folder, exist_ok=True)
        for image in os.listdir(self.input_folder):
            path_to_image = f"{self.input_folder}/{image}"
            self.process_image(path_to_image, output_folder)

    def process_image(self, image_path: str, output_folder: str) -> None:
        """Process image like so :
            - Open it
            - Resize it to a square format
            - Add some padding if it is not a square
            - Save the image in a new folder 'dataset'

        Args:
            output_folder (str): the folder where to save the image.
            image_path (str): path to the image to process
        """
        image = Image.open(image_path)
        resized_image = self.resize_image(image)
        padded_image = self.add_padding(resized_image)
        self.save_image(padded_image, image_path, output_folder)

    def resize_image(self, image: Image.Image, size_to_resize: int = 0) -> Image.Image:
        """Resize the image to a square format, using a specific size
            - Used with resize() from pillow
            - Handle case where width is greater, smaller or equal to height
            - Keep the aspect ratio

        Args:
            size_to_resize (int, optional):
                size to resize the image to. self.image_size is used by default
            image (Image.Image): image to resize

        Returns:
            Image.Image: resized image
        """
        target_size = size_to_resize or self.image_size
        width, height = image.size
        if width > height:
            new_width = target_size
            new_height = int(height * (target_size / width))
        elif width < height:
            new_width = int(width * (target_size / height))
            new_height = target_size
        else:
            new_width = new_height = target_size

        return image.resize((new_width, new_height))

    def add_padding(
        self,
        resized_image: Image.Image,
        background_color: tuple[int, ...] = (114,) * 3,
    ) -> Image.Image:
        """Add some padding to the image if it is not a square
            - Padding will be added to the right if width < height
            - Padding will be added to the bottom if width > height

        Args:
            background_color (tuple) : color to use for padding. Default is (114, 114, 114)
            resized_image (Image.Image): image to add padding

        Returns:
            Image.Image: image with padding
        """
        width, height = resized_image.size
        if width == height:
            return resized_image
        else:
            color = background_color if resized_image.mode == "RGB" else (114,)
            result = Image.new(resized_image.mode, (self.image_size, self.image_size), color)
            result.paste(resized_image, (0, 0))
            return result

    @staticmethod
    def save_image(image: Image.Image, original_image_path: str, output_folder: str) -> None:
        """Save the image inside dataset folder inside a folder with the current date

        Args:
            output_folder (str): the path to save the image.
            image (Image.Image): the image to save
            original_image_path (str): the path to the image to save
        """
        if not os.path.isdir(output_folder):
            os.makedirs(output_folder, exist_ok=True)
        image_name = original_image_path.split("/")[-1]
        output_path = os.path.join(output_folder, image_name)
        image.save(output_path)

    @property
    def output_dataset_folder_name(self) -> str:
        return os.path.join(self.DATASET_FOLDER, datetime.now().strftime(self.DATETIME_FORMAT))

    def set_input_folder(self, path: str) -> None:
        self.input_folder = path
