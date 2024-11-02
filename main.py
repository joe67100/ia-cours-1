from src.image_processor import ImageProcessor
import os


def main():
    image_processor = ImageProcessor(f"{os.getcwd()}/input_images")
    image_processor.process_folder()


if __name__ == "__main__":
    main()
