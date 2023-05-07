import numpy as np
import cv2
import math


def glViewportToInterParam(width, height):

    # Define fov and principle point
    fov = 45
    fx = width / (2 * np.tan(np.deg2rad(fov) / 2))
    fy = height / (2 * np.tan(np.deg2rad(fov) / 2))
    principal_point = np.array([width / 2.0, height / 2.0])

    # Put intrinsic parameter
    K = np.array([[fx, 0.0, principal_point[0]],
                  [0.0, fy, principal_point[1]],
                  [0.0, 0.0, 1.0]])

    return K

def glulookat2camext(eye, center, up):

    # Calculate z axis
    z = eye - center
    z /= np.linalg.norm(z)

    # Calculate x axis
    x = np.cross(up, z)
    x /= np.linalg.norm(x)

    # Calculate y axis
    y = np.cross(z, x)

    # Calculate rotation matrix
    R = np.identity(3)
    R[0, :] = x
    R[1, :] = y
    R[2, :] = z

    # Calculate translation matrix
    T = -np.dot(R, eye)

    # Combine them as extrinsic matrix
    M = np.identity(4)
    M[:3, :3] = R
    M[:3, 3] = T

    # Transform coordinate from opengl to opencv
    flip_yz = np.array([[1, 0, 0, 0],
                        [0, -1, 0, 0],
                        [0, 0, -1, 0],
                        [0, 0, 0, 1]])
    M = flip_yz @ M @ flip_yz

    return M

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

def pixel2world(interparam, Cam_ext, u, v, depth):

    K_inv = np.linalg.inv(interparam)
    t = Cam_ext[3:4, :]

    Zc = 1
    Xc = u
    Yc = v

    P_cam = (np.dot(K_inv, np.array([[Xc], [Yc], [Zc]])) * depth)
    P_cam = np.vstack((P_cam, 1))
    RT_inv = np.linalg.inv(Cam_ext)
    
    # Transform world coordinate from camera coordinate
    world_coords = np.dot(RT_inv, P_cam)

    return np.array([world_coords[0][0], world_coords[1][0], world_coords[2][0], 1.0])

def world2pixel(interparam, Cam_ext, world_coords):
    return np.dot(np.dot(interparam, Cam_ext), world_coords)

def process(Cam, Obs, Obj):
    Cam_img = cv2.imread('Cam.png')
    Obs_img = cv2.imread('Obs.png')

    # Get bbox
    width = height = 250
    box = np.where(Cam_img>0)
    min_x, min_y = min(box[1]), min(box[0])
    max_x, max_y = max(box[1]), max(box[0])
    # print(min_x, min_y, max_x, max_y)

    # Recieve extrinsic parameters from glulookat
    Cam_ext = glulookat2camext(np.array([Cam[0], Cam[1], Cam[2]]),
                               np.array([Cam[3], Cam[4], Cam[5]]), 
                               np.array([Cam[6], Cam[7], Cam[8]]))
    Obs_ext = glulookat2camext(np.array([Obs[0], Obs[1], Obs[2]]),
                               np.array([Obs[3], Obs[4], Obs[5]]), 
                               np.array([Obs[6], Obs[7], Obs[8]]))

    # Recieve intrinsic parameters from glviewport 
    Cam_interparam = glViewportToInterParam(width, height)
    Obs_interparam = glViewportToInterParam(width, height)

    # Transform world coordinate from pixel coordinate of camera
    P1_Cam2Wor = pixel2world(Cam_interparam, Cam_ext, min_x, min_y, np.abs(Obj[-1]))
    P2_Cam2Wor = pixel2world(Cam_interparam, Cam_ext, max_x, max_y, np.abs(Obj[-1]))

    # Transform pixel coordinate of observer from world coordinate
    P1_in_Obs = world2pixel(Obs_interparam, Obs_ext[:3,:], P1_Cam2Wor)
    P2_in_Obs = world2pixel(Obs_interparam, Obs_ext[:3,:], P2_Cam2Wor)

    P1_in_Obs /= P1_in_Obs[-1]
    P2_in_Obs /= P2_in_Obs[-1]

    # Draw Result
    ori_img = cv2.hconcat([Cam_img, Obs_img])
    cv2.putText(Cam_img, f"{Cam[0]}, {Cam[1]}, {Cam[2]}", (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(Obs_img, "%.1f, %.1f, %.1f" % (Obs[0], Obs[1], Obs[2]), (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(Obs_img, "%.1f, %.1f, %.1f" % (Obs[3], Obs[4], Obs[5]), (140, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1, cv2.LINE_AA)
    cv2.rectangle(Cam_img, (min_x, min_y), (max_x, max_y), (0,255,0), 1, cv2.LINE_AA)
    cv2.rectangle(Obs_img, (int(P1_in_Obs[0]), int(P1_in_Obs[1])), (int(P2_in_Obs[0]), int(P2_in_Obs[1])), (0,255,0), 1, cv2.LINE_AA)

    # Show Result
    img = cv2.hconcat([Cam_img, Obs_img])
    out_img = cv2.vconcat([ori_img, img])
    cv2.imwrite('Result.jpg', out_img)

    return P1_Cam2Wor, P2_Cam2Wor