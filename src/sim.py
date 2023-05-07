from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import cv2
from utils import *


def save_image(filename1, filename2):

    # recieve view height, width
    viewport = glGetIntegerv(GL_VIEWPORT)
    width, height = viewport[2], viewport[3]

    # load pixel value
    pixels = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)
    image = np.frombuffer(pixels, dtype=np.uint8).reshape(height, width, 3)
    pixels2 = glReadPixels(250, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)
    image2 = np.frombuffer(pixels2, dtype=np.uint8).reshape(height, width, 3)

    image = cv2.flip(cv2.cvtColor(image, cv2.COLOR_RGB2BGR), 0)
    image2 = cv2.flip(cv2.cvtColor(image2, cv2.COLOR_RGB2BGR), 0)

    cv2.imwrite(filename1, image)
    cv2.imwrite(filename2, image2)

def draw_cube(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(1.0, 0, 0)
    glutWireCube(4.0)
    glPopMatrix()


def draw_rect(P1, P2):

    glColor3f(1.0, 1.0, 0.0)
    glBegin(GL_LINES)

    glVertex3f(P1[0], -P2[1], -P1[2])  # bottom-left
    glVertex3f(P2[0], -P2[1], -P1[2])  # bottom-right

    glVertex3f(P2[0], -P2[1], -P1[2])  # bottom-right
    glVertex3f(P2[0], -P1[1], -P1[2])  # top-right

    glVertex3f(P2[0], -P1[1], -P1[2])  # top-right
    glVertex3f(P1[0], -P1[1], -P1[2])  # top-left

    glVertex3f(P1[0], -P1[1], -P1[2])  # top-left
    glVertex3f(P1[0], -P2[1], -P1[2])  # bottom-left
    glEnd()


class Sim():
    def __init__(self, Cam, Obs, Obj=None, args=None):
        self.Cam = Cam
        self.Obs = Obs
        self.Obj = Obj
        self.draw_rectangle = False
        self.draw_cube = False
        self.args = args

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Camera 1
        glViewport(0, 0, 250, 250)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, 1.0, 0.1, 500.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(self.Cam[0], self.Cam[1], self.Cam[2],
                  self.Cam[3], self.Cam[4], self.Cam[5], 
                  self.Cam[6], self.Cam[7], self.Cam[8])

        if self.draw_cube and self.Obj is not None:
            draw_cube(self.Obj[0], self.Obj[1], self.Obj[2])

        # Observer
        glViewport(250, 0, 250, 250)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, 1.0, 0.1, 500.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(self.Obs[0], self.Obs[1], self.Obs[2], 
                  self.Obs[3], self.Obs[4], self.Obs[5], 
                  self.Obs[6], self.Obs[7], self.Obs[8])

        if self.draw_cube and self.Obj is not None:
            draw_cube(self.Obj[0], self.Obj[1], self.Obj[2])

        if self.draw_rectangle:
            draw_rect(self.P1_proj_sheld, self.P2_proj_sheld)

        glutSwapBuffers()

    def keyboard(self, key, x, y):
        if key == b'd' or key == b'D':
            save_image(self.args.Cam_img, self.args.Obs_img)
            self.P1_proj_sheld, self.P2_proj_sheld = process(self.Cam, self.Obs, self.Obj, self.args)
            self.draw_rectangle = not self.draw_rectangle
            glutPostRedisplay()
        if key == b'c' or key == b'C':
            self.draw_cube = not self.draw_cube
            glutPostRedisplay()
        if key == b'q' or key == b'Q':
            glutLeaveMainLoop()