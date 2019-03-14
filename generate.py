#!/usr/bin/env python3

import os
import sys

import cv2


def mm_to_pixel(mm):
    return int((mm * 72) / 25.4)


def main():
    dictionary_bits = int(sys.argv[1])
    dictionary_length = int(sys.argv[2])
    marker_size_in_mm = int(sys.argv[3])

    if not os.path.exists(f'./DICT_{dictionary_bits}X{dictionary_bits}_{dictionary_length}'):
        os.mkdir(f'./DICT_{dictionary_bits}X{dictionary_bits}_{dictionary_length}')

    aruco_dictionary = cv2.aruco.Dictionary_get(getattr(cv2.aruco, f'DICT_{dictionary_bits}X{dictionary_bits}_{dictionary_length}'))

    for i in range(0, dictionary_length):
        aruco_marker = cv2.aruco.drawMarker(aruco_dictionary, i, mm_to_pixel(marker_size_in_mm))
        cv2.imwrite(f'./DICT_{dictionary_bits}X{dictionary_bits}_{dictionary_length}/{i}.png', aruco_marker)

    return


if __name__ == '__main__':
    if len(sys.argv) == 4:
        main()
    else:
        print(f'Usage: {sys.argv[0]} <dictionary_bits: Integer: 4, 5, 6, 7> <dictionary_length: Integer: 50, 100, 250, 1000> <marker_size_in_mm: Integer>')
