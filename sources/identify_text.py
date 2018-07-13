import sys
import numpy as np
from scipy import misc


# This would be the eventual public method, when this is rewritten as a class
def get_character_coordinates(color_file_name):
    black_and_white_image = bw_converted_img_data(color_file_name)
    return get_character_coordinates_for_image(black_and_white_image)


def get_character_coordinates_for_image(black_and_white_image):
    char_co_ordinates = {}
    row_slices = ranges(find_rows_with_chars(black_and_white_image))
    for row, row_slice in enumerate(row_slices):
        col_slices = ranges(find_cols_with_chars(black_and_white_image, row_slice))
        char_co_ordinates[row] = {'row_slice': row_slice, 'col_slices': col_slices}
    return char_co_ordinates


# function that takes in [R,G,B] values of a pixel
# and returns a single transformed Black and white value
# read here more about the formula used :
# https://www.tutorialspoint.com/dip/grayscale_to_rgb_conversion.htm
def transform_to_black_and_white(rgb):
    return rgb[0] * 0.3 + rgb[1] * .59 + rgb[2] * .11


# We are making a few assumptions here. These may have to change as as we progress.
# We are going to make this black and white image into a binary black and white image.
# I mean, we either have a DARK pixel = 0; or a BRIGHT pixel = 255, nothing in the middle.
def bw_converted_img_data(color_file_name):
    image_array = misc.imread(color_file_name)
    return bw_copy_img_data(image_array)


def bw_copy_img_data(image_array):
    black_and_white_image = np.empty((image_array.shape[0], image_array.shape[1]), dtype='uint8')
    for row in range(0, len(image_array)):
        for col in range(0, len(image_array[row])):
            bw_value = transform_to_black_and_white(image_array[row][col])
            black_and_white_image[row][col] = 0 if bw_value < 200 else 255
    return black_and_white_image


# We are making a few assumptions here. These may have to change as as we progress.
# Any row which has at-least one dark pixel is assumed to have a character
# All other rows which contains only bright pixel are considered to be very bright and no character in them.
def find_rows_with_chars(black_and_white_image):
    rows_with_chars = []
    for row in range(0, black_and_white_image.shape[0]):
        contains_chars = False
        for col in range(0, black_and_white_image.shape[1]):
            if black_and_white_image[row][col] < 175:
                contains_chars = True
                break
        if contains_chars:
            rows_with_chars.append(row)
    return rows_with_chars


# We are making a few assumptions here. These may have to change as as we progress.
# Any row which has at-least one dark pixel is assumed to have a character
# All other rows which contains only bright pixel are considered to be very bright and no character in them.
def find_cols_with_chars(black_and_white_image, row_slice):
    cols_with_chars = []
    for col in range(0, black_and_white_image.shape[1]):
        contains_chars = False
        for row in range(row_slice[0], row_slice[1]):
            if black_and_white_image[row][col] < 175:
                contains_chars = True
                break
        if contains_chars:
            cols_with_chars.append(col)
    return cols_with_chars


def ranges(data):
    list_of_ranges = []
    start = 0
    prev = 0
    for index, x in enumerate(data):
        if index == 0:
            start = data[0]
            prev = data[0]
        else:
            if x > prev + 1:
                list_of_ranges.append((start, data[index - 1]))
                start = x
            prev = x
    return list_of_ranges


def strip_row_and_save(black_and_white_image, ranges_to_scan):
    for top, bottom in ranges_to_scan:
        misc.imsave("..//test_images//tmp//stripped_{1}.gif".format(top), black_and_white_image[top:bottom + 1])



# simple function to create B&W filename
def bw_filename_for(color_file_name):
    temp = color_file_name.split('.')
    temp[-2] = temp[-2] + "_black_and_white"
    return '.'.join(temp)


# This is just a fun method to demonstrate that we have actually found the character coordinates
# and we are ready for the next step. Would be removed in the log run
def mark_for_fun(color_file_name, coordinates):
    black_and_white_image = bw_converted_img_data(color_file_name)
    for row in coordinates:
        row_slice = coordinates[row]['row_slice']
        for left, right in coordinates[row]['col_slices']:
            top, bottom = row_slice
            black_and_white_image[top][left] = 0
            black_and_white_image[top][right + 1] = 0
            black_and_white_image[bottom + 1][left] = 0
            black_and_white_image[bottom + 1][right + 1] = 0
    misc.imsave("..//test_images//tmp//marked.gif", black_and_white_image)


def main(color_file_name):
    coordinates = get_character_coordinates(color_file_name)
    print(coordinates)
    mark_for_fun(color_file_name, coordinates)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        main(color_file_name='..//test_images//pilayar_vanakkam.jpg')
    else:
        main(sys.argv[1])
