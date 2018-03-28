import sys
import numpy as np
from scipy import misc


# function that takes in [R,G,B] values of a pixel
# and returns a single transformed Black and white value
def transform_to_black_and_white(rgb):
    return rgb[0] * 0.3 + rgb[1] * .59 + rgb[2] * .11


def bw_filename_for(color_file_name):
    temp = color_file_name.split('.')
    temp[-2] = temp[-2] + "_black_and_white"
    return '.'.join(temp)


def main(color_file_name):
    image_array = misc.imread(color_file_name)
    black_and_white_image = np.empty((image_array.shape[0], image_array.shape[1]), dtype='uint8')
    for row in range(0, len(image_array)):
        for col in range(0, len(image_array[row])):
            black_and_white_image[row][col] = transform_to_black_and_white(image_array[row][col])
    misc.imsave(bw_filename_for(color_file_name), black_and_white_image)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        main(color_file_name = '..//test_images//manathil_uruthi_vendum.gif')
    else:
        main(sys.argv[1])

