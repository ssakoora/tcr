import sys

from sources.TextWithImage import ImageWithText


def main(color_file_name):
    f = ImageWithText(color_file_name)
    f.print_characters()
    f.strip_char_and_save()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        main(color_file_name='..//test_images//pilayar_vanakkam.jpg')
    else:
        main(sys.argv[1])
