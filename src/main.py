import cv2
import numpy as np
import argparse
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from utils import *
from sim import *


def main(Cam, Obs, Obj, args):
	glutInit()
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
	glutInitWindowSize(500, 250)
	glutCreateWindow("Two Cameras")
	sim = Sim(Cam, Obs, Obj, args)
	glutKeyboardFunc(sim.keyboard)
	glutDisplayFunc(sim.display)
	glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_CONTINUE_EXECUTION);
	glutMainLoop()


if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Simulation of Coordinate transformation')
	parser.add_argument('--Cam_img', default='../result/Cam.png', type=str, help='Camera image')
	parser.add_argument('--Obs_img', default='../result/Obs.png', type=str, help='Obeserver image')
	parser.add_argument('--result', default='../result/Result.png', type=str, help='Result')
	parser.add_argument('--Cam_par', default=(0.0, 0.0, 0.0, 0.0, 0.0, -100.0, 0.0, 1.0, 0.0), type=tuple, help='Camera parameters')
	parser.add_argument('--Obs_par', default=(4.0, 7.0, 0.0, 4.0, 7.0, -100.0, 0.0, 1.0, 0.0), type=tuple, help='Observer parameters')
	parser.add_argument('--Obj_par', default=(-1, -1, -40.0), type=tuple, help='Object parameters')

	args = parser.parse_args()

	main(args.Cam_par, args.Obs_par, args.Obj_par, args)
