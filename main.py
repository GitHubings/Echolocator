# author: Somsubhra Bairi (201101056)

# Draw sphere with QUAD_STRIP
# Controls: UP/DOWN - scale up/down
#           LEFT/RIGHT - rotate left/right
#           F1 - Toggle surface as SMOOTH or FLAT

# Python imports
from math import *
from objloader import *

# OpenGL imports for python
try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GLUT import *
except:
    print("OpenGL wrapper for python not found")

# Last time when sphere was re-displayed
last_time = 0
rotating = False
scaling  = False
scale = 1.

def screen2space(x, y):
    width, height = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
    radius = min(width, height)*scale
    return (2.*x-width)/radius, -(2.*y-height)/radius

# The sphere class
class Sphere:

    def mouse(bla, button, state, x, y):
        #print "starting mouse"
        #print button
        #print state
        #print x
        #print y
        #print bla
        global rotating, scaling, x0, y0
        if button == GLUT_LEFT_BUTTON:
            rotating = (state == GLUT_DOWN)
        elif button == GLUT_RIGHT_BUTTON:
            scaling = (state == GLUT_DOWN)
        x0, y0 = x, y

    def motion(bla, x1, y1):
        #print "starting motion"
        #print x1
        #print y1
        #print bla
        global x0, y0, rotation, scale
        if rotating:
            p0 = screen2space(x0, y0)
            p1 = screen2space(x1, y1)
        if scaling:
            scale *= exp(((x1-x0)-(y1-y0))*.01)
            x0, y0 = x1, y1
            glutPostRedisplay()

    def onKeyUp(*args):
        print(args[1])
        if (args[1] == b'd'):
            width = glutGet(GLUT_WINDOW_WIDTH)
            height = glutGet(GLUT_WINDOW_HEIGHT)
            depth = glReadPixelsub(0,0, width, height, GL_DEPTH_COMPONENT, GL_FLOAT)
            f = open("depthframe.txt", "w");
            print("saving depth frame")
            for i in range(len(depth)):
                for j in range(len(depth[i])):
                    f.write(str(depth[i][j]))
                    f.write(" ")
                f.write("\n")
        return
    # Constructor for the sphere class
    def __init__(self, radius, objname):
        print(objname)
        self.object3d = OBJ(objname, swapyz=False)
        glutKeyboardUpFunc(self.onKeyUp)
        glutMouseFunc(self.mouse)
        glutMotionFunc(self.motion)

        # Radius of sphere
        self.radius = radius

        # Number of latitudes in sphere
        self.lats = 100

        # Number of longitudes in sphere
        self.longs = 100

        self.user_theta = 0
        self.user_height = 0

        # Direction of light
        self.direction = [0.0, 2.0, -1.0, 1.0]

        # Intensity of light
        self.intensity = [0.7, 0.7, 0.7, 1.0]

        # Intensity of ambient light
        self.ambient_intensity = [0.3, 0.3, 0.3, 1.0]

        # The surface type(Flat or Smooth)
        self.surface = GL_FLAT

    # Initialize
    def init(self):

        # Set background color to black
        glClearColor(0.0, 0.0, 0.0, 0.0)

        self.compute_location()

        # Set OpenGL parameters
        glEnable(GL_DEPTH_TEST)

        # Enable lighting
        glEnable(GL_LIGHTING)

        # Set light model
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, self.ambient_intensity)

        # Enable light number 0
        glEnable(GL_LIGHT0)

        # Set position and intensity of light
        glLightfv(GL_LIGHT0, GL_POSITION, self.direction)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.intensity)

        # Setup the material
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

    # Compute location
    def compute_location(self):
        x = 2 * cos(self.user_theta)
        y = 2 * sin(self.user_theta)
        z = self.user_height
        d = sqrt(x * x + y * y + z * z)

        # Set matrix mode
        glMatrixMode(GL_PROJECTION)

        # Reset matrix
        glLoadIdentity()
        glFrustum(-d * 0.5, d * 0.5, -d * 0.5, d * 0.5, d - 1.1, d + 1.1)

        # Set camera
        gluLookAt(x, y, z, 0, 0, 0, 0, 0, 1)

    # Display the sphere
    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Set color to white
        glColor3f(1.0, 1.0, 1.0)

        # Set shade model
        glShadeModel(self.surface)

        self.draw()
        glutSwapBuffers() 

    # Draw the sphere
    def draw(self):
        #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        #glLoadIdentity()
        glCallList(self.object3d.gl_list)

    # Keyboard controller for sphere
    def special(self, key, x, y):

        # Scale the sphere up or down
        if key == GLUT_KEY_UP:
            self.user_height += 0.1
        if key == GLUT_KEY_DOWN:
            self.user_height -= 0.1

        # Rotate the cube
        if key == GLUT_KEY_LEFT:
            self.user_theta += 0.1
        if key == GLUT_KEY_RIGHT:
            self.user_theta -= 0.1

        # Toggle the surface
        if key == GLUT_KEY_F1:
            if self.surface == GL_FLAT:
                self.surface = GL_SMOOTH
            else:
                self.surface = GL_FLAT

        self.compute_location()
        glutPostRedisplay()

    # The idle callback
    def idle(self):
        global last_time
        time = glutGet(GLUT_ELAPSED_TIME)

        if last_time == 0 or time >= last_time + 40:
            last_time = time
            glutPostRedisplay()

    # The visibility callback
    def visible(self, vis):
        if vis == GLUT_VISIBLE:
            glutIdleFunc(self.idle)
        else:
            glutIdleFunc(None)


# The main function
def main():

    # Initialize the OpenGL pipeline
    glutInit(sys.argv)

    # Set OpenGL display mode
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)

    # Set the Window size and position
    glutInitWindowSize(300, 300)
    glutInitWindowPosition(50, 100)

    # Create the window with given title
    glutCreateWindow(b'Sphere')

    # Instantiate the sphere object
    s = Sphere(1.0, 'obj.obj')

    s.init()

    # Set the callback function for display
    glutDisplayFunc(s.display)

    # Set the callback function for the visibility
    glutVisibilityFunc(s.visible)

    # Set the callback for special function
    glutSpecialFunc(s.special)

    # Run the OpenGL main loop
    glutMainLoop()


# Call the main function
if __name__ == '__main__':
    main()