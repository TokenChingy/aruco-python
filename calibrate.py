#!/usr/bin/env python3

import cv2
import glob
import numpy
import os


def main():
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    object_points = numpy.zeros((6*7, 3), dtype=numpy.float32)
    object_points[:, :2] = numpy.mgrid[0:7, 0:6].T.reshape(-1, 2)

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

        return_status, corners = cv2.findChessboardCorners(
            frame_filtered, (7, 6), None)

        if return_status == True:
            world_points.append(object_points)
            sub_corners = cv2.cornerSubPix(
                frame_filtered, corners, (11, 11), (-1, -1), criteria)
            image_points.append(sub_corners)

            composite_frame = cv2.drawChessboardCorners(
                composite_frame, (7, 6), sub_corners, return_status)
            cv2.imshow('Calibrated Image', composite_frame)

            keyboard_event = cv2.waitKey(0)
            if keyboard_event == 27:
                cv2.destroyAllWindows()
                break

    calibration_status, camera_matrix, distortion_coefficient, rotation_vectors, translation_vectors = cv2.calibrateCamera(
        world_points, image_points, frame_filtered.shape[::-1], None, None)

    calibration_file = cv2.FileStorage(
        'calibration/calibration.yaml', cv2.FILE_STORAGE_WRITE)
    calibration_file.write("camera_matrix", camera_matrix)
    calibration_file.write("dist_coeff", distortion_coefficient)
    calibration_file.release()

    return


if __name__ == '__main__':
    main()
