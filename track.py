#!/usr/bin/env python3

import cv2
import numpy

import math
import sys
import time

def main():
    dictionary_bits = int(sys.argv[1])
    dictionary_length = int(sys.argv[2])
    marker_size_in_mm = int(sys.argv[3])

    camera = cv2.VideoCapture(0, cv2.CAP_ANY)

    try:
        calibration_file = cv2.FileStorage('./calibration/calibration.yaml', cv2.FILE_STORAGE_READ)
        camera_shape = calibration_file.getNode('camera_shape').mat()
        camera_matrix = calibration_file.getNode('camera_matrix').mat()
        camera_distortion_coefficients = calibration_file.getNode('distortion_coefficients').mat()
        calibration_file.release()

        camera.set(3, int(camera_shape[0]))
        camera.set(4, int(camera_shape[1]))
    except:
        raise

    while True:
        start_time = time.time()

        try:
            frame_status, frame = camera.read()
            composite_frame = frame.copy()
            filtered_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            aruco_dictionary = cv2.aruco.Dictionary_get(getattr(cv2.aruco, f'DICT_{dictionary_bits}X{dictionary_bits}_{dictionary_length}'))
            aruco_parameters = cv2.aruco.DetectorParameters_create()
            corners, ids, rejected_points = cv2.aruco.detectMarkers(filtered_frame, aruco_dictionary, parameters=aruco_parameters)

            if numpy.all(ids != None):
                rotation_vector, translation_vector, _ = cv2.aruco.estimatePoseSingleMarkers(corners[0], marker_size_in_mm / 1000, camera_matrix, camera_distortion_coefficients)
                cv2.aruco.drawAxis(composite_frame, camera_matrix, camera_distortion_coefficients,rotation_vector[0], translation_vector[0], 0.1)
                cv2.aruco.drawDetectedMarkers(composite_frame, corners, ids)

            cv2.putText(composite_frame, f'FPS: {math.floor(1.0 / (time.time() - start_time))}', (8, 16), cv2.FONT_HERSHEY_PLAIN, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.imshow('Aruco Markers: Esc to quit.', composite_frame)

            keyboard_event = cv2.waitKey(1)

            if keyboard_event == 27:
                cv2.destroyAllWindows()
                break

        except:
            raise

    cv2.destroyAllWindows()
    camera.release()

    return


if __name__ == '__main__':
    if len(sys.argv) == 4:
        main()
    else:
        print(f'Usage: {sys.argv[0]} <dictionary_bits: Integer: 4, 5, 6, 7> <dictionary_length: Integer: 50, 100, 250, 1000> <marker_size_in_mm: Integer>')
