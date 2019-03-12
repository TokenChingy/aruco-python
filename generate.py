#!/usr/bin/env python3

import cv2
import numpy
import os


def main():
    if not os.path.exists('./markers'):
        os.mkdir('./markers')

    aruco_dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_1000)

    for i in range(0, 1000):
        aruco_marker = cv2.aruco.drawMarker(aruco_dictionary, i, 100)
        cv2.imwrite(f'./markers/{i}.png', aruco_marker)

    return


if __name__ == '__main__':
    main()
