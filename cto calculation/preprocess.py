import os, re
import pandas as pd
from PIL import Image, ImageOps


class DataPreprocessor:

    def __init__(self, original_images_folder_path, default_output_images_folder_path):
        self.original_images_folder_path = original_images_folder_path
        self.default_output_images_folder_path = default_output_images_folder_path
        os.makedirs(self.default_output_images_folder_path, exist_ok=True)

    def get_image_paths(self, images_folder_path):
        # return [os.path.join(images_folder_path, filename) for filename in sorted(os.listdir(images_folder_path), key=lambda x: int(re.search(r'\((\d+)\)', x).group(1)))]
        return [os.path.join(images_folder_path, filename) for filename in os.listdir(images_folder_path)]
    
    def init_output_images_folder(self, output_images_folder_path):
        output_images_folder_path = output_images_folder_path or self.default_output_images_folder_path
        os.makedirs(output_images_folder_path, exist_ok=True)
        return output_images_folder_path

    def crop_images_to_square(self, input_images_folder_path=None, output_images_folder_path=None):
        input_images_folder_path = input_images_folder_path or self.original_images_folder_path
        output_images_folder_path = self.init_output_images_folder(output_images_folder_path)

        for image_path in self.get_image_paths(input_images_folder_path):
            with Image.open(image_path) as img:
                width, height = img.size
                min_dim = min(width, height)
                left, top = (width - min_dim) // 2, (height - min_dim) // 2
                right, bottom = left + min_dim, top + min_dim
                cropped_img = img.crop((left, top, right, bottom))
                cropped_img.save(os.path.join(output_images_folder_path, os.path.basename(image_path)))

    def pad_images_to_square(self, input_images_folder_path=None, output_images_folder_path=None):
        input_images_folder_path = input_images_folder_path or self.original_images_folder_path
        output_images_folder_path = self.init_output_images_folder(output_images_folder_path)

        for image_path in self.get_image_paths(input_images_folder_path):
            with Image.open(image_path) as img:
                max_dim = max(img.size)
                padded_img = ImageOps.pad(img, (max_dim, max_dim), color=(0), centering=(0.5,0.5))
                padded_img.save(os.path.join(output_images_folder_path, os.path.basename(image_path)))

    def resize_images(self, target_width, input_images_folder_path=None, output_images_folder_path=None):
        input_images_folder_path = input_images_folder_path or self.original_images_folder_path
        output_images_folder_path = self.init_output_images_folder(output_images_folder_path)

        for image_path in self.get_image_paths(input_images_folder_path):
            with Image.open(image_path) as img:
                resized_img = img.resize((target_width, target_width))
                resized_img.save(os.path.join(output_images_folder_path, os.path.basename(image_path)))


original_images_folder_path = "./data/teknofest/images/original"
default_output_images_folder_path = "./data/teknofest/images/processed"
data_file_path = "./data/teknofest/CTO_dataset.csv"

preprocessor = DataPreprocessor(original_images_folder_path, default_output_images_folder_path)
preprocessor.crop_images_to_square(output_images_folder_path="./data/teknofest/images/cropped")
preprocessor.resize_images(512, "./data/teknofest/images/cropped", "./data/teknofest/images/cropped-resized")
preprocessor.pad_images_to_square(output_images_folder_path="./data/teknofest/images/padded")
preprocessor.resize_images(512, "./data/teknofest/images/padded", "./data/teknofest/images/padded-resized")