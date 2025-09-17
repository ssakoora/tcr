try:
    from scipy import misc
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False

try:
    import imageio.v2 as imageio
    IMAGEIO_AVAILABLE = True
except ImportError:
    try:
        import imageio
        IMAGEIO_AVAILABLE = True
    except ImportError:
        IMAGEIO_AVAILABLE = False

try:
    from PIL import Image
    import numpy as np
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

import os
from sources.identify_text import bw_converted_img_data, get_character_coordinates_for_image, bw_copy_img_data


class ImageWithText(object):
    def __init__(self, image_file_location):
        self._image_file_location = image_file_location
        self._image_array = self._load_image(image_file_location)
        self._bw_copy = bw_copy_img_data(self._image_array)
        self._char_coordinates = get_character_coordinates_for_image(self._bw_copy)
    
    def _load_image(self, image_file_location):
        if IMAGEIO_AVAILABLE:
            return imageio.imread(image_file_location)
        elif PIL_AVAILABLE:
            img = Image.open(image_file_location)
            return np.array(img)
        elif SCIPY_AVAILABLE:
            return misc.imread(image_file_location)
        else:
            raise ImportError("No image reading library available. Please install imageio or Pillow.")

    def print_characters(self):
        coordinates = self._char_coordinates
        image_array = self._image_array
        i=0
        for row in coordinates:
            row_slice = coordinates[row]['row_slice']
            for left, right in coordinates[row]['col_slices']:
                i=i+1
                top, bottom = row_slice
                image_array[top][left] = 0
                image_array[top][right + 1] = 0
                image_array[bottom + 1][left] = 0
                image_array[bottom + 1][right + 1] = 0
        self._save_image("..//test_images//tmp//marked_{0}.gif".format(i), image_array)

    def strip_char_and_save(self):
        coordinates = self._char_coordinates
        i=0
        for row in coordinates:
            top, bottom = coordinates[row]['row_slice']
            for left, right in coordinates[row]['col_slices']:
                self._save_image("..//test_images//tmp//char_{0}.gif".format(i),
                            self._bw_copy[top:bottom + 1, left:right + 1])
                i = i+1
    
    def extract_characters_to_directory(self, output_dir):
        coordinates = self._char_coordinates
        character_files = []
        i = 0
        
        for row in coordinates:
            top, bottom = coordinates[row]['row_slice']
            for left, right in coordinates[row]['col_slices']:
                filename = f"char_{i}.gif"
                filepath = os.path.join(output_dir, filename)
                self._save_image(filepath, self._bw_copy[top:bottom + 1, left:right + 1])
                character_files.append(filename)
                i += 1
        
        return character_files
    
    def _save_image(self, filepath, image_array):
        import os
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        if IMAGEIO_AVAILABLE:
            imageio.imwrite(filepath, image_array)
        elif PIL_AVAILABLE:
            img = Image.fromarray(image_array)
            img.save(filepath)
        elif SCIPY_AVAILABLE:
            misc.imsave(filepath, image_array)
        else:
            raise ImportError("No image writing library available. Please install imageio or Pillow.")
