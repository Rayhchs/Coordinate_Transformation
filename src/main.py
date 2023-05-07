import cv2
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from utils import *
from sim import *


def main(Cam, Obs, Obj):
	glutInit()
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
	glutInitWindowSize(500, 250)
	glutCreateWindow("Two Cameras")
	sim = Sim(Cam, Obs, Obj)
	glutKeyboardFunc(sim.keyboard)
	glutDisplayFunc(sim.display)
	glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_CONTINUE_EXECUTION);
	glutMainLoop()


if __name__ == '__main__':

	# Camera, Observer, Object
	Cam = (-1.0, -1.0, -1.0, -1.0, 1.0, -100.0, 0.0, 1.0, 0.0)
	Obs = (4, 7, 0.0, 4, 7, -100.0, 0.0, 1.0, 0.0)
	Obj = (-1, -1, -40.0)

	main(Cam, Obs, Obj)
