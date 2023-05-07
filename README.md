# Coordinate Transformation
Coordinate system is critical in the fields of robot and autonomous vehicle. Coordinate transfomration is required for connecting view of cameras. This repo simulates coordinate transformation from pixel to world and world to pixel between two cameras. To simulate it, this repo create two cameras (Cam, Obs) and a object using OpenGL. The intrinsic and extrinsic parameters are transformed from the parameters of glviewport and glulookat. Firstly, the bounding box of object in pixel coordinate of Cam is transformed to world coordinate. Afterward, we transformed it from world coordinate to pixel coordinate of Obs. We can verify the result by comparing transformed coordinate and coordinate in image of Obs.

<img src="https://github.com/Rayhchs/Coordinate_Transformation/blob/main/img/flow.png">

## World2Pixel
Transformation from world to pixel coordinate is shown as follow:

$$\begin{bmatrix}
u\\
v\\
1\\
\end{bmatrix}=
\begin{bmatrix}
fx&0&u0&0\\
0&fy&v0&0\\
0&0&1&0\\
\end{bmatrix}
\begin{bmatrix}
R&T\\
0&1\\
\end{bmatrix}
\begin{bmatrix}
Xw\\
Yw\\
Zw\\
1\\
\end{bmatrix}$$

## Pixel2World
Transformation from pixel to camera coordinate is shown as follow:

$$\begin{bmatrix}
Xc\\
Yc\\
Zc\\
\end{bmatrix}=
\begin{bmatrix}
fx&0&u0\\
0&fy&v0\\
0&0&1\\
\end{bmatrix}^{-1}
\begin{bmatrix}
u\\
v\\
1\\
\end{bmatrix}*depth$$

Transformation from camera to world coordinate is shown as follow:

$$\begin{bmatrix}
Xw\\
Yw\\
Zw\\
\end{bmatrix}=
\begin{bmatrix}
R&T\\
0&1\\
\end{bmatrix}^{-1}
\begin{bmatrix}
Xc\\
Yc\\
Zc\\
1\\
\end{bmatrix}$$

## Simulation
* Requisite
1. OpenGL
2. OpenCV
3. Numpy

* Clone this repo

    ```shell script
    git clone https://github.com/Rayhchs/Coordinate_Transformation.git
    ```

* Arguments

|    Argument    |    Explanation    |
|:--------------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
|      Cam_img      | Path to save camera image |
|    Obs_img   | Path to save observer image |
|    result   | Path to save result |
|    Cam_par   | Glulookat parameters of camera |
|    Obs_par   | Glulookat parameters of observer |
|    Obj_par   | x, y, z coordinate of object |

* How to use

    ```shell script
    python main.py
    ```

1. press 'c' to draw a cube object.
2. press 'd' to calculate the transformation of coordinate of bounding box.

## Result
The result of simulation is shown as follow:
The top-left image is captured by Cam. The top-right image is captured by Obs. The bottom-left image shows the bbox of object in Cam image. (0.0, 0.0, 0.0) indicates the coordinate of Cam. The bottom-right image shows the transformed coordinate of bbox. (4.0, 7.0, 0.0) indicates the coordinate of Obs and (4.0, 7.0, -100) means where the Obs looking at. The object of this simulation is at (-1.0, -1.0, -40.0)

<img src="https://github.com/Rayhchs/Coordinate_Transformation/blob/main/result/Result.png">