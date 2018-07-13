from scipy import misc

from sources.identify_text import bw_converted_img_data, get_character_coordinates_for_image, bw_copy_img_data


class ImageWithText(object):
    def __init__(self, image_file_location):
        self._image_file_location = image_file_location
        self._image_array = misc.imread(self._image_file_location)
        self._bw_copy = bw_copy_img_data(self._image_array)
        self._char_coordinates = get_character_coordinates_for_image(self._bw_copy)

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
        misc.imsave("..//test_images//tmp//marked_{0}.gif".format(i), image_array)

    def strip_char_and_save(self):
        coordinates = self._char_coordinates
        i=0
        for row in coordinates:
            top, bottom = coordinates[row]['row_slice']
            for left, right in coordinates[row]['col_slices']:
                misc.imsave("..//test_images//tmp//char_{0}.gif".format(i),
                            self._bw_copy[top:bottom + 1, left:right + 1])
                i = i+1
