import wx
from OpenGL.GL import *
from OpenGL.GLU import *
from objloader import OBJ
from wx import glcanvas


class MyCanvasBase(glcanvas.GLCanvas):

    def __init__(self, parent):

        glcanvas.GLCanvas.__init__(self, parent, -1)
        self.init = False
        # initial mouse position
        self.rx, self.ry = self.last_rx, self.last_ry = (0, 0)
        self.tx, self.ty = self.last_tx, self.last_ty = (0, 0)
        self.size = None
        self.zpos = -3
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.on_erase_background)
        self.Bind(wx.EVT_SIZE, self.on_size)
        #self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_l_mouse_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_l_mouse_up)
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_r_mouse_down)
        self.Bind(wx.EVT_RIGHT_UP, self.on_r_mouse_up)
        self.Bind(wx.EVT_MOTION, self.on_mouse_motion)
        self.Bind(wx.EVT_MOUSEWHEEL, self.on_scroll)

    def on_erase_background(self, event):
        pass  # Do nothing, to avoid flashing on MSW.

    def on_scroll(self, event):
        if event.GetWheelRotation() > 0:
            self.zpos += 1
        else:
            self.zpos -= 1
        self.Refresh(True)

    def on_size(self, event):
        size = self.size = self.GetClientSize()
        '''
        if self.GetContext():
            self.SetCurrent()
        '''
        if self.init:
            glViewport(0, 0, size.width, size.height)
        event.Skip()

    def on_paint(self, event):
        dc = wx.PaintDC(self)
        self.SetCurrent(event)
        if not self.init:
            self.InitGL()
            self.init = True
        self.OnDraw()

    def on_l_mouse_down(self, evt):
        self.SetFocus()
        self.CaptureMouse()
        self.last_rx, self.last_ry = evt.GetPosition()

    def on_l_mouse_up(self, evt):
        self.Refresh(True)
        if self.HasCapture():
            self.ReleaseMouse()

    def on_r_mouse_down(self, evt):
        self.SetFocus()
        self.CaptureMouse()
        self.last_tx, self.last_ty = evt.GetPosition()

    def on_r_mouse_up(self, evt):
        self.Refresh(True)
        if self.HasCapture():
            self.ReleaseMouse()

    def on_mouse_motion(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            i, j = evt.GetPosition()
            self.rx += i - self.last_rx
            self.ry += j - self.last_ry
            self.last_rx, self.last_ry = (i, j)
            self.Refresh(False)
        elif evt.Dragging() and evt.RightIsDown():
            i, j = evt.GetPosition()
            self.tx += i - self.last_tx
            self.ty -= j - self.last_ty
            self.last_tx, self.last_ty = (i, j)
            self.Refresh(False)


class GLCanvas(MyCanvasBase):
    def __init__(self, parent):
        super().__init__(parent)
        self.obj = None

    def init_gl(self):
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2))
        glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0))
        glLightfv(GL_LIGHT0, GL_POSITION, (3, 3, 0.0))
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)  # most obj files expect to be smooth-shaded

        self.obj = OBJ("small_sphere.obj", swapyz=True)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        gluPerspective(90, 800.0 / 600.0, 1, 100.0)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_MODELVIEW)

    def load_obj(self, obj_file):
        obj_file = "C:\\Users\\acer\\Desktop\\PyWavefront-master\\examples\\data\\earth.obj"
        self.obj = OBJ(obj_file, swapyz=True)
        self.Refresh(True)

    def adj_amb_light(self, v):
        glLightfv(GL_LIGHT0, GL_AMBIENT, (v, v, v))
        self.Refresh(True)

    def adj_light_pos(self, v):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glLightfv(GL_LIGHT0, GL_POSITION, (3, 3, -v))
        self.Refresh(True)

    def adj_dif_light(self, v):
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (v, v, v))
        self.Refresh(True)

    def on_draw(self):
        # clear color and depth buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        if self.size is None:
            self.size = self.GetClientSize()
        w, h = self.size
        w = max(w, 1.0)
        h = max(h, 1.0)
        x_scale = 180.0 / w
        y_scale = 180.0 / h

        glTranslate(float(self.tx * x_scale) / 20.0, float(self.ty * y_scale) / 20.0, self.zpos)
        glRotatef(float(self.rx * x_scale), 0.0, 1.0, 0.0)
        glRotatef(float(self.ry * y_scale), 1.0, 0.0, 0.0)

        glCallList(self.obj.gl_list)
        self.SwapBuffers()
