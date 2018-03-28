import sys
import numpy as np
from scipy import misc


# function that takes in [R,G,B] values of a pixel
# and returns a single transformed Black and white value
# read here more about the formula used : https://www.tutorialspoint.com/dip/grayscale_to_rgb_conversion.htm
def transform_to_black_and_white(rgb):
    return rgb[0] * 0.3 + rgb[1] * .59 + rgb[2] * .11


def bw_filename_for(color_file_name):
    temp = color_file_name.split('.')
    temp[-2] = temp[-2] + "_black_and_white"
    return '.'.join(temp)


def black_and_white_copy_of(color_file_name):
    image_array = misc.imread(color_file_name)
    black_and_white_image = np.empty((image_array.shape[0], image_array.shape[1]), dtype='uint8')
    for row in range(0, len(image_array)):
        for col in range(0, len(image_array[row])):
            black_and_white_image[row][col] = transform_to_black_and_white(image_array[row][col])
    return black_and_white_image


# Any line that has > 220 ( considered white for the current test image)
# this logic will have to improve a lot, and also possibly include neural networks in the future.
def find_lines_to_skip(black_and_white_image):
    lines_to_skip = []
    for row in range(0, black_and_white_image.shape[0]):
        should_skip = False
        for col in range(0, black_and_white_image.shape[1]):
            if black_and_white_image[row][col] != 255 and black_and_white_image[row][col] != 226:
                should_skip = True
                break
        if should_skip:
            lines_to_skip.append(row)
    return lines_to_skip


def inverse(lines_to_skip, max_rows):
    all_rows = range(0, max_rows)
    return [x for x in all_rows if x not in lines_to_skip]


def ranges(data):
    list_of_ranges = []
    start = 0
    prev = 0
    for index, x in enumerate(data):
        if index == 0:
            start = data[0]
            prev = data[0]
        else:
            if x > prev+1:
                list_of_ranges.append((start,data[index-1]))
                start = x
            prev = x
    return list_of_ranges


def main(color_file_name):
    black_and_white_image = black_and_white_copy_of(color_file_name)
    misc.imsave(bw_filename_for(color_file_name), black_and_white_image)
    lines_to_skip = find_lines_to_skip(black_and_white_image)
    ranges_to_scan = ranges(inverse(lines_to_skip, black_and_white_image.shape[0]))
    print(lines_to_skip)
    print(ranges_to_scan)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        main(color_file_name = '..//test_images//manathil_uruthi_vendum.gif')
    else:
        main(sys.argv[1])