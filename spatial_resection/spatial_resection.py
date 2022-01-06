import cv2
import numpy as np
from aruco_module import object_dictionary, find_aruco_markers, plot_aruco_markers, load_coefficients

def pair_coordinates(image, object_dictionary, plot=False):
    bboxs, ids = find_aruco_markers(image, marker_size=5, total_markers=250, draw=True)

    if plot:
        plot_aruco_markers(image, bboxs, ids)

    ids = np.squeeze(ids)
    img_pts = []
    obj_pts = []

    for idx, (id, bbox) in enumerate(zip(ids, bboxs)):
        img_pts.append([bbox[0][0][0], bbox[0][0][1]])
        obj_pts.append(object_dictionary[int(id)])

    return ids, np.array(img_pts, dtype=np.float32), np.array(obj_pts, dtype=np.float32)

def spatial_resection(camera_properties, image_points, object_points):    
    camera_matrix, dist_coeffs, _, _ = load_coefficients(camera_properties)

    success, rotation_vector, translation_vector = cv2.solvePnP(object_points, image_points, camera_matrix, dist_coeffs, cv2.SOLVEPNP_ITERATIVE)

    print(f"Rotation Vector:\n {rotation_vector}")
    print(f"Translation Vector:\n {translation_vector}")
    return rotation_vector, translation_vector


if __name__ == "__main__":

    aruco_obj_dict = object_dictionary("./aruco_object_coordinates.txt")

    image_path = "./2021-12-02-1504.jpg"
    image = cv2.imread(image_path)

    ids, image_points, object_points = pair_coordinates(image, aruco_obj_dict, plot=False)

    if len(ids) >= 6:
        camera_properties = "./camera_config.yml"
        spatial_resection(camera_properties, image_points, object_points)