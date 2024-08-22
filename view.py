import sys
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Function to load the image as a texture
def load_texture(image_path):
    texture_surface = pygame.image.load(image_path)
    texture_data = pygame.image.tostring(texture_surface, "RGB", 1)
    width, height = texture_surface.get_rect().size
    print ("wid,hei ",width,height)
    #print ("tex_dat",texture_data)

    glEnable(GL_TEXTURE_2D)
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
    
    return texture

# Function to draw the cylinder with the texture
def draw_cylinder(texture, radius, height, sides):
    glBindTexture(GL_TEXTURE_2D, texture)
    
    # Draw the sides of the cylinder
    glBegin(GL_QUAD_STRIP)
    for i in range(sides + 1 ):
        angle = 2 * np.pi * i / sides
        x = np.cos(angle) * radius
        y = np.sin(angle) * radius
        glTexCoord2f(0, 1-i / sides)
        glVertex3f(x, y, -height / 2)
        glTexCoord2f(1, 1-i / sides)
        glVertex3f(x, y, +height / 2)
    glEnd()

    ## # Draw the top and bottom of the cylinder
    ## for z in [-height / 2, height / 2]:
    ##     glBegin(GL_TRIANGLE_FAN)
    ##     glTexCoord2f(0.5, 0.5)
    ##     glVertex3f(0, 0, z)
    ##     for i in range(sides + 1):
    ##         angle = 2 * np.pi * i / sides
    ##         x = np.cos(angle) * radius
    ##         y = np.sin(angle) * radius
    ##         glTexCoord2f((np.cos(angle) + 1) / 2, (np.sin(angle) + 1) / 2)
    ##         glVertex3f(x, y, z)
    ##     glEnd()

# Initialize the Pygame and OpenGL context
def main(image_path):
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    texture = load_texture(image_path)
    radius = 1.0
    height = 2.0
    sides = 32  
    rotate_x, rotate_y = 0, 0
    mouse_down = False
    last_pos = (0, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_down = True
                    last_pos = event.pos
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_down = False
            elif event.type == MOUSEMOTION:
                if mouse_down:
                    dx, dy = event.pos[0] - last_pos[0], event.pos[1] - last_pos[1]
                    rotate_x += dy
                    rotate_y += dx
                    last_pos = event.pos

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glRotatef(rotate_x, 1, 0, 0)
        glRotatef(rotate_y, 0, 1, 0)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        draw_cylinder(texture, radius, height, sides)
        glCullFace(GL_FRONT)
        draw_cylinder(texture, radius, height, sides)
        glPopMatrix()
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    image_path = "image2.jpg"
    image_path = "image.png"
    main(image_path)

