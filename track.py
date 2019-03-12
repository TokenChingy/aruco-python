#!/usr/bin/env python3

import cv2
import numpy


def main():
    camera = cv2.VideoCapture(0)
    camera.set(3, 640)
    camera.set(4, 480)

    calibration_file = cv2.FileStorage(
        './calibration/calibration.yaml', cv2.FILE_STORAGE_READ)
    camera_matrix = calibration_file.getNode('camera_matrix').mat()
    camera_distortion_coefficients = calibration_file.getNode(
        'dist_coeff').mat()
    calibration_file.release()

    while True:
        try:
            frame_status, frame = camera.read()
            composite_frame = frame.copy()
            filtered_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            aruco_dictionary = cv2.aruco.Dictionary_get(
                cv2.aruco.DICT_5X5_1000)
            aruco_parameters = cv2.aruco.DetectorParameters_create()
            corners, ids, rejected_points = cv2.aruco.detectMarkers(
                filtered_frame, aruco_dictionary, parameters=aruco_parameters)

            if numpy.all(ids != None):
                rotation_vector, translation_vecotor, _ = cv2.aruco.estimatePoseSingleMarkers(
                    corners[0], 0.05, camera_matrix, camera_distortion_coefficients)
                cv2.aruco.drawAxis(composite_frame, camera_matrix, camera_distortion_coefficients,
                                   rotation_vector[0], translation_vecotor[0], 0.1)
                cv2.aruco.drawDetectedMarkers(
                    composite_frame, corners, ids)

            cv2.imshow('Aruco Markers: Q to quit.', composite_frame)

            keyboard_event = cv2.waitKey(0)
            if keyboard_event == 27:
                cv2.destroyAllWindows()
                break

        except:
            raise

    camera.release()
    cv2.destroyAllWindows()
    return


if __name__ == '__main__':
    main()
