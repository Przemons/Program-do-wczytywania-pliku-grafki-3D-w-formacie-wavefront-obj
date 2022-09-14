import sys
from data.pygame import run_pygame
from wx_obj_canvas import GLCanvas
sys.path.append('..')
import wx
from objloader import *


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.CreateStatusBar()
        file_menu = wx.Menu()
        file_open_menu_item = file_menu.Append(wx.ID_FILE, '&Otwórz',
                                               'Otwiera plik .obj')
        file_menu.AppendSeparator()
        info_menu_item = file_menu.Append(wx.ID_ABOUT, 'O program&ie',
                                          'Informacje o aplikacji')
        file_menu.AppendSeparator()
        exit_menu_item = file_menu.Append(wx.ID_EXIT, '&Wyjdź', 'Zamyka aplikację')
        self.Bind(wx.EVT_MENU, self.on_open, file_open_menu_item)
        self.Bind(wx.EVT_MENU, self.on_info, info_menu_item)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_menu_item)
        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, '&Plik')
        self.SetMenuBar(menu_bar)
        self.panel_os = wx.Panel(self, wx.ID_ANY, style=wx.SUNKEN_BORDER | wx.TAB_TRAVERSAL)
        self.slider_os = wx.Slider(self.panel_os, wx.ID_ANY, 0, 0, 10, style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS)
        self.sizer_os = wx.StaticBox(self.panel_os, wx.ID_ANY, "Oświetlenie otoczenia")
        self.panel_poz = wx.Panel(self, wx.ID_ANY, style=wx.SUNKEN_BORDER | wx.TAB_TRAVERSAL)
        self.slider_poz = wx.Slider(self.panel_poz, wx.ID_ANY, 0, -5, 5, style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS)
        self.sizer_poz = wx.StaticBox(self.panel_poz, wx.ID_ANY, "Pozycja oświetlenia")
        self.panel_roz = wx.Panel(self, wx.ID_ANY, style=wx.SUNKEN_BORDER | wx.TAB_TRAVERSAL)
        self.slider_roz = wx.Slider(self.panel_roz, wx.ID_ANY, 0, 0, 10, style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS)
        self.sizer_roz = wx.StaticBox(self.panel_roz, wx.ID_ANY, "Rozproszenie oświetlenia")
        self.canvas = GLCanvas(self)
        self.__set_properties()
        self.__do_layout()
        self.Bind(wx.EVT_COMMAND_SCROLL, self.slider_1_event, self.slider_os)
        self.Bind(wx.EVT_COMMAND_SCROLL, self.slider_2_event, self.slider_poz)
        self.Bind(wx.EVT_COMMAND_SCROLL, self.slider_3_event, self.slider_roz)
        self.filepath = ""
        self.v1 = -40
        self.v2 = 0.2
        self.v3 = 0.5

    def __set_properties(self):
        self.SetTitle("3D viewer")
        self.SetSize(500, 300)
        self.SetBackgroundColour(wx.Colour(192, 192, 192))
        self.slider_os.SetMinSize((1000, 35))
        self.slider_poz.SetMinSize((1000, 35))
        self.slider_roz.SetMinSize((1000, 35))
    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        self.sizer_roz.Lower()
        sizer_4 = wx.StaticBoxSizer(self.sizer_roz, wx.HORIZONTAL)
        self.sizer_poz.Lower()
        sizer_6 = wx.StaticBoxSizer(self.sizer_poz, wx.HORIZONTAL)
        self.sizer_os.Lower()
        sizer_5 = wx.StaticBoxSizer(self.sizer_os, wx.HORIZONTAL)
        sizer_1.Add(self.canvas, 6, wx.ALL | wx.EXPAND, 5)
        sizer_5.Add(self.slider_os, 0, 0, 0)
        self.panel_os.SetSizer(sizer_5)
        sizer_1.Add(self.panel_os, 0, wx.ALL | wx.EXPAND, 5)
        sizer_6.Add(self.slider_poz, 0, 0, 0)
        self.panel_poz.SetSizer(sizer_6)
        sizer_1.Add(self.panel_poz, 0, wx.ALL | wx.EXPAND, 5)
        sizer_4.Add(self.slider_roz, 0, 0, 0)
        self.panel_roz.SetSizer(sizer_4)
        sizer_1.Add(self.panel_roz, 0, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(sizer_1)
        self.Layout()
    def slider_1_event(self, event):
        self.v1 = self.slider_os.Value / 10.0
        run_pygame(self.filepath,self.v1,self.v2,self.v3)
        event.Skip()
    def slider_2_event(self, event):
        self.v2 = self.slider_poz.Value / 10.0
        run_pygame(self.filepath,self.v1,self.v2,self.v3)
        event.Skip()
    def slider_3_event(self, event):
        self.v3 = self.slider_roz.Value / 10.0
        run_pygame(self.filepath,self.v1,self.v2,self.v3)
        event.Skip()
    def on_open(self, event):
        "Open an Obj file, set title if successful"
        filters = 'Obj files (*.obj;*.OBJ;*.Obj)|*.obj;*.OBJ;*.Obj'
        dlg = wx.FileDialog(self, message="Open an Image...", defaultDir=os.getcwd() + "\objects",
                            defaultFile="", wildcard=filters, style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetFilename()
            self.filepath = os.path.join(os.path.dirname(__file__), filename)
            run_pygame(self.filepath,123,0,0)

        dlg.Destroy()
    def on_info(self, event):
        dlg = wx.MessageDialog(self, "Wersja programu: 1.0\nAutorzy: Przemysław Głód & Adrian Derdaś"
                                     "\nInternal use only\n©2022", "O programie", wx.OK)
        dlg.ShowModal()
    def on_exit(self, event):
        self.Close()

if __name__ == "__main__":
    app = wx.App()
    wx.InitAllImageHandlers()
    frame = MyFrame(None, title="3D viewer")
    app.SetTopWindow(frame)
    frame.Show()
    app.MainLoop()