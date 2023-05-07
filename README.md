# Coordinate Transformation
Coordinate system is critical in the fields of robot and autonomous vehicle. Coordinate transfomration is required for connecting view of cameras. This repo simulates coordinate transformation from pixel to world and world to pixel between two cameras. To simulate it, this repo create two cameras (Cam, Obs) and a object using OpenGL. The intrinsic and extrinsic parameters are transformed from the parameters of glviewport and glulookat. Firstly, the bounding box of object in pixel coordinate of Cam is transformed to world coordinate. Afterward, we transformed it from world coordinate to pixel coordinate of Obs. We can verify the result by comparing transformed coordinate and coordinate in image of Obs.

## Simulation
* Requisite
1. OpenGL
2. OpenCV
3. Numpy

* Clone this repo

    ```shell script
    git clone https://github.com/Rayhchs/AugTheFace.git
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
Here shows the result of simulation:
<img src="https://github.com/Rayhchs/Coordinate_Transformation/blob/main/result/Result.png">