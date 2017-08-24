import pygame
from pygame.locals import *
 
from OpenGL.GL import *
from OpenGL.GLU import *

verticies = (
	(1, -1, -1),
	(1, 1, -1),
	(-1, 1, -1),
	(-1, -1, -1),
	(1, -1, 1),
	(1, 1, 1),
	(-1, -1, 1),
	(-1, 1, 1),
	)


edges = (
	(0,1),
	(0,3),
	(0,4),
	(2,1),
	(2,3),
	(2,7),
	(6,3),
	(6,4),
	(6,7),
	(5,1),
	(5,4),
	(5,7),
	)

surfaces = (
	(0,1,2,3),
	(3,2,7,6),
	(6,7,5,4),
	(4,5,1,0),
	(1,5,7,2),
	(4,0,3,6),
	)

def Cube():

	glBegin(GL_QUADS)
	for surface in surfaces:
		glColor3fv((0,0,1))
		#for vertex in surface:
		#	glVertex3fv(verticies[vertex])
		
	glEnd()
	glBegin(GL_LINES)
	for edge in edges:
		for vertex in edge:
			glVertex3fv(verticies[vertex])
	glEnd()






def main():
	flag = 0
	pygame.init()
	display = (800,600)
	pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
	
	gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
	
	glTranslate(0.0, 0.0, -5)
	
	glRotatef(0, 0, 0, 0)
	
	#glUniform3f(1.0 , 1.0, 0.0, 0.0)
	
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quite()
				
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		glRotatef(1, 2, 1, 3)
		Cube()
		#width, height = getViewPort()
		width, height = pygame.display.get_surface().get_size()

		depth = glReadPixelsub(0,0, width, height, GL_DEPTH_COMPONENT, GL_FLOAT )
		
		if flag == 0:
			flag = 0
			f = open("C:/Development/Test.txt", "w");
			for i in range(len(depth)):
				for j in range(len(depth[i])):
						f.write(str(depth[i][j]))
						f.write(" ")
				f.write("\n")

	
		pygame.display.flip()
		pygame.time.wait(10)

main()