#!/usr/bin/env python3

import glob
import os
import sys

import cv2
import numpy

def main():
    horizontal_cells = int(sys.argv[1])
    vertical_cells = int(sys.argv[2])

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    object_points = numpy.zeros((horizontal_cells * vertical_cells, 3), dtype=numpy.float32)
    object_points[:, :2] = numpy.mgrid[0:vertical_cells, 0:horizontal_cells].T.reshape(-1, 2)

    world_points = []
    image_points = []

    if not os.path.exists('./calibration'):
        os.mkdir('./calibration')

    images = glob.glob('calibration/*.jpg')

    if len(images) == 0:
        print('The directory "calibration" does not contain any images (.jpg).')

        return

    for image in images:
        frame = cv2.imread(image)
        composite_frame = frame.copy()
        frame_filtered = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        return_status, corners = cv2.findChessboardCorners(frame_filtered, (vertical_cells, horizontal_cells), None)

        if return_status == True:
            world_points.append(object_points)
            sub_corners = cv2.cornerSubPix(frame_filtered, corners, (11, 11), (-1, -1), criteria)
            image_points.append(sub_corners)

            composite_frame = cv2.drawChessboardCorners(composite_frame, (vertical_cells, horizontal_cells), sub_corners, return_status)

            cv2.imshow('Calibrated Image: Esc to quit.', composite_frame)

            keyboard_event = cv2.waitKey(0)

            if keyboard_event == 27:
                cv2.destroyAllWindows()
                break

    calibration_status, camera_matrix, distortion_coefficient, rotation_vectors, translation_vectors = cv2.calibrateCamera(world_points, image_points, frame_filtered.shape[::-1], None, None)

    calibration_file = cv2.FileStorage('calibration/calibration.yaml', cv2.FILE_STORAGE_WRITE)
    calibration_file.write("camera_shape", frame_filtered.shape[::-1])
    calibration_file.write("camera_matrix", camera_matrix)
    calibration_file.write("distortion_coefficients ", distortion_coefficient)
    calibration_file.release()

    return


if __name__ == '__main__':
    if len(sys.argv) == 3:
        main()
    else:
        print(f'Usage: {sys.argv[0]} <horizontal_cells: Integer> <vertical_cells: Integer>')
