from src.image_processor import ImageProcessor
import os


def main():
    path_to_images_folder = f"{os.getcwd()}/input_images"
    image_processor = ImageProcessor(path_to_images_folder)
    image_processor.process_folder()


if __name__ == "__main__":
    main()
