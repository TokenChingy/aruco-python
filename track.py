#!/usr/bin/env python3

import cv2
import numpy

import math
import sys
import time

def inverse_pose(rotation_vector, translation_vector):
    rotation_matrix, jacobian = cv2.Rodrigues(rotation_vector)
    rotation_matrix = numpy.matrix(rotation_matrix).T

    inverse_rotation_vector, jacobian = cv2.Rodrigues(rotation_matrix)
    inverse_translation_vector = numpy.dot(-rotation_matrix, numpy.matrix(translation_vector))

    return inverse_rotation_vector, inverse_translation_vector


def relative_pose(rotation_vector_parent, translation_vector_parent, rotation_vector_child, translation_vector_child):
    rotation_vector_parent, translation_vector_parent = rotation_vector_parent.reshape((3, 1)), translation_vector_parent.reshape((3, 1))
    rotation_vector_child, translation_vector_child = rotation_vector_child.reshape((3, 1)), translation_vector_child.reshape((3, 1))

    inverse_rotation_vector_child, inverse_translation_vector_child = inverse_pose(rotation_vector_child, translation_vector_child)

    composed_matrix = cv2.composeRT(rotation_vector_parent, translation_vector_parent, inverse_rotation_vector_child, inverse_translation_vector_child)
    composed_rotation_vector = composed_matrix[0]
    composed_translation_vector = composed_matrix[1]

    composed_rotation_vector.reshape((3, 1))
    composed_translation_vector. reshape((3, 1))

    return composed_rotation_vector, composed_translation_vector


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
