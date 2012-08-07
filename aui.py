# -*- coding: utf-8 -*-

import sys
import datetime

import wx
import wx.grid
import wx.html
import wx.aui

import cStringIO

import config

#    This is a Python open source project for migration of modules
#    and functions from GestionPyme and other ERP products from Sistemas
#    Ágiles.
#
#   Copyright (C) 2012 Sistemas Ágiles.
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

# This is a modified version of the wxPython AUI Notebook demo
# adapted for ERP Libre by Alan Etkin <spametki@gmail.com>

__author__ = "Mike Driscoll; Andrea Gavana"
__license__ = "AGPLv3 (the posted code was under LGPL)"

ID_CreateTree = wx.NewId()
ID_CreateGrid = wx.NewId()
ID_CreateText = wx.NewId()
ID_CreateHTML = wx.NewId()
ID_CreateSizeReport = wx.NewId()
ID_GridContent = wx.NewId()
ID_TextContent = wx.NewId()
ID_TreeContent = wx.NewId()
ID_HTMLContent = wx.NewId()
ID_SizeReportContent = wx.NewId()
ID_CreatePerspective = wx.NewId()
ID_CopyPerspective = wx.NewId()

ID_TransparentHint = wx.NewId()
ID_VenetianBlindsHint = wx.NewId()
ID_RectangleHint = wx.NewId()
ID_NoHint = wx.NewId()
ID_HintFade = wx.NewId()
ID_AllowFloating = wx.NewId()
ID_NoVenetianFade = wx.NewId()
ID_TransparentDrag = wx.NewId()
ID_AllowActivePane = wx.NewId()
ID_NoGradient = wx.NewId()
ID_VerticalGradient = wx.NewId()
ID_HorizontalGradient = wx.NewId()

ID_Settings = wx.NewId()
ID_About = wx.NewId()
ID_FirstPerspective = ID_CreatePerspective+1000



#----------------------------------------------------------------------
def GetMondrianData():
    return \
'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00 \x00\x00\x00 \x08\x06\x00\
\x00\x00szz\xf4\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\x00\x00qID\
ATX\x85\xed\xd6;\n\x800\x10E\xd1{\xc5\x8d\xb9r\x97\x16\x0b\xad$\x8a\x82:\x16\
o\xda\x84pB2\x1f\x81Fa\x8c\x9c\x08\x04Z{\xcf\xa72\xbcv\xfa\xc5\x08 \x80r\x80\
\xfc\xa2\x0e\x1c\xe4\xba\xfaX\x1d\xd0\xde]S\x07\x02\xd8>\xe1wa-`\x9fQ\xe9\
\x86\x01\x04\x10\x00\\(Dk\x1b-\x04\xdc\x1d\x07\x14\x98;\x0bS\x7f\x7f\xf9\x13\
\x04\x10@\xf9X\xbe\x00\xc9 \x14K\xc1<={\x00\x00\x00\x00IEND\xaeB`\x82' 


def GetMondrianBitmap():
    return wx.BitmapFromImage(GetMondrianImage())


def GetMondrianImage():
    stream = cStringIO.StringIO(GetMondrianData())
    return wx.ImageFromStream(stream)


def GetMondrianIcon():
    icon = wx.EmptyIcon()
    icon.CopyFromBitmap(GetMondrianBitmap())
    return icon


class PyAUIFrame(wx.Frame):
    
    def __init__(self, parent, id=-1, title="ERP Libre", pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE |
                                            wx.SUNKEN_BORDER |
                                            wx.CLIP_CHILDREN):
        wx.Frame.__init__(self, parent, id, title, pos, size, style)


    def start_manager(self):
        # tell FrameManager to manage this frame
        self._mgr = wx.aui.AuiManager()
        self._mgr.SetManagedWindow(self)

        # allow active pane
        self._mgr.SetFlags(\
        self._mgr.GetFlags() ^ wx.aui.AUI_MGR_ALLOW_ACTIVE_PANE)

        # post-init code
        # web2py internationalization support
        T = config.env["T"]

        self._perspectives = []
        self.n = 0
        self.x = 0

        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(wx.Bitmap("images/erplibre-iso-sa.png"))
        
        self.SetIcon(icon)

        # create menu
        self.starting_menubar = wx.MenuBar()

        self.view_menu = wx.Menu()
        self.view_menu.Append(ID_CreateText, "Create Text Control")
        self.view_menu.Append(ID_CreateHTML, "Create HTML Control")
        self.view_menu.Append(ID_CreateTree, "Create Tree")
        self.view_menu.Append(ID_CreateGrid, "Create Grid")
        self.view_menu.Append(ID_CreateSizeReport, "Create Size Reporter")
        self.view_menu.AppendSeparator()
        self.view_menu.Append(ID_GridContent, "Use a Grid for the Content Pane")
        self.view_menu.Append(ID_TextContent, "Use a Text Control for the Content Pane")
        self.view_menu.Append(ID_HTMLContent, "Use an HTML Control for the Content Pane")
        self.view_menu.Append(ID_TreeContent, "Use a Tree Control for the Content Pane")
        self.view_menu.Append(ID_SizeReportContent, "Use a Size Reporter for the Content Pane")

        self.options_menu = wx.Menu()
        self.options_menu.AppendRadioItem(ID_TransparentHint, T("Transparent Hint"))
        self.options_menu.AppendRadioItem(ID_VenetianBlindsHint, T("Venetian Blinds Hint"))
        self.options_menu.AppendRadioItem(ID_RectangleHint, T("Rectangle Hint"))
        self.options_menu.AppendRadioItem(ID_NoHint, T("No Hint"))
        self.options_menu.AppendSeparator();
        self.options_menu.AppendCheckItem(ID_HintFade, T("Hint Fade-in"))
        self.options_menu.AppendCheckItem(ID_AllowFloating, T("Allow Floating"))
        self.options_menu.AppendCheckItem(ID_NoVenetianFade, T("Disable Venetian Blinds Hint Fade-in"))
        self.options_menu.AppendCheckItem(ID_TransparentDrag, T("Transparent Drag"))
        self.options_menu.AppendCheckItem(ID_AllowActivePane, T("Allow Active Pane"))
        self.options_menu.AppendSeparator();
        self.options_menu.AppendRadioItem(ID_NoGradient, T("No Caption Gradient"))
        self.options_menu.AppendRadioItem(ID_VerticalGradient, T("Vertical Caption Gradient"))
        self.options_menu.AppendRadioItem(ID_HorizontalGradient, T("Horizontal Caption Gradient"))
        self.options_menu.AppendSeparator();
        self.options_menu.Append(ID_Settings, T("Settings Pane"))

        self._perspectives_menu = wx.Menu()
        self._perspectives_menu.Append(ID_CreatePerspective, T("Create Perspective"))
        self._perspectives_menu.Append(ID_CopyPerspective, T("Copy Perspective Data To Clipboard"))
        self._perspectives_menu.AppendSeparator()
        self._perspectives_menu.Append(ID_FirstPerspective+0, T("Default Startup"))
        self._perspectives_menu.Append(ID_FirstPerspective+1, T("All Panes"))
        self._perspectives_menu.Append(ID_FirstPerspective+2, T("Vertical Toolbar"))

        # self.SetMenuBar(self.starting_menubar)

        self.statusbar = self.CreateStatusBar(2, wx.ST_SIZEGRIP)
        self.statusbar.SetStatusWidths([-2, -3])
        self.statusbar.SetStatusText(T("Ready"), 0)
        self.statusbar.SetStatusText(T("Welcome To ERP Libre!"), 1)

        # min size for the frame itself isn't completely done.
        # see the end up FrameManager::Update() for the test
        # code. For now, just hard code a frame minimum size
        self.SetMinSize(wx.Size(400, 300))

        # create some toolbars

        self.tb2 = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                         wx.TB_FLAT | wx.TB_NODIVIDER)
        self.tb2.SetToolBitmapSize(wx.Size(16,16))
        self.tb2_bmp1 = wx.ArtProvider_GetBitmap(wx.ART_GO_BACK, wx.ART_OTHER, wx.Size(16, 16))
        self.tb2_bmp2 = wx.ArtProvider_GetBitmap(wx.ART_GO_FORWARD, wx.ART_OTHER, wx.Size(16, 16))
        self.tb2_bmp3 = wx.ArtProvider_GetBitmap(wx.ART_GO_HOME, wx.ART_OTHER, wx.Size(16, 16))
        
        # GestionLibre main shortcuts
        
        self.button_6 = self.tb2.AddLabelTool(10006, "Test", self.tb2_bmp1)
        self.button_7 = self.tb2.AddLabelTool(10007, "Test", self.tb2_bmp2)
        self.button_9 = self.tb2.AddLabelTool(10009, "Test", self.tb2_bmp3)

        # End of GestionLibre main shortcuts

        self.tb2.Realize()

        self.tb3 = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                         wx.TB_FLAT | wx.TB_NODIVIDER)
        self.tb3.SetToolBitmapSize(wx.Size(16,16))

        # Fugue Icons by Yusuke Kamiyamane

        # login
        self.tb3_bmp10 = wx.Bitmap("images/user.png")
        # logout
        self.tb3_bmp11 = wx.Bitmap("images/user--arrow.png")
        # register
        self.tb3_bmp12 = wx.Bitmap("images/user--plus.png")
        # specify firm's tin
        self.tb3_bmp13 = wx.Bitmap("images/address-book--pencil.png")
        # index
        self.tb3_bmp14 = wx.Bitmap("images/application-home.png")
        # setup
        self.tb3_bmp15 = wx.Bitmap("images/property.png")


        # Other ERP Libre shortcuts
        
        self.button_10 = self.tb3.AddLabelTool(10010, "Test", self.tb3_bmp10)
        self.button_11 = self.tb3.AddLabelTool(10011, "Test", self.tb3_bmp11)
        self.button_12 = self.tb3.AddLabelTool(10012, "Test", self.tb3_bmp12)
        self.button_13 = self.tb3.AddLabelTool(10013, "Test", self.tb3_bmp13)
        self.tb3.AddSeparator()
        self.button_14 = self.tb3.AddLabelTool(10014, "Test", self.tb3_bmp14)
        self.button_15 = self.tb3.AddLabelTool(10015, "Test", self.tb3_bmp15)

        # End of Other ERP Libre shortcuts
        
        self.tb3.Realize()

        self.tb4 = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                         wx.TB_FLAT | wx.TB_NODIVIDER | wx.TB_HORZ_TEXT)
        self.tb4.SetToolBitmapSize(wx.Size(16,16))
        
        self.tb4_bmp1 = wx.Bitmap("images/blue-documents-stack.png")
        self.tb4_bmp2 = wx.Bitmap("images/report.png")
        self.tb4_bmp3 = wx.Bitmap("images/arrow-skip.png")
        self.tb4_bmp4 = wx.Bitmap("images/box-search-result.png")
        self.tb4_bmp5 = wx.Bitmap("images/edit-rule.png")
        self.tb4_bmp8 = wx.Bitmap("images/document--pencil.png")
        
        # ERP Libre html window buttons (home, previous, next)

        self.button_1 = self.tb4.AddLabelTool(10001, str(T("Billing")), self.tb4_bmp1)
        self.button_2 = self.tb4.AddLabelTool(10002, str(T("CA")), self.tb4_bmp2)
        self.button_3 = self.tb4.AddLabelTool(10003, str(T("Movements")), self.tb4_bmp3)

        # End of ERP Libre html window buttons (home, previous, next)
        
        self.button_4 = self.tb4.AddLabelTool(10004, str(T("Articles")), self.tb4_bmp4)
        self.tb4.AddSeparator()
        self.button_5 = self.tb4.AddLabelTool(10005, str(T("Queries")), self.tb4_bmp5)
        self.button_8 = self.tb4.AddLabelTool(10008, str(T("Operations")), self.tb4_bmp8)
        self.tb4.Realize()

        self.text_pane = self.CreateTextCtrl(default_text = "")
        
        self.tree_pane = wx.TreeCtrl(self, -1, wx.Point(0, 0), wx.Size(160, 250), \
        wx.TR_DEFAULT_STYLE | wx.NO_BORDER)

        # add a bunch of panes
        self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().
                          Name("test1").Caption("Pane Caption").Top().
                          CloseButton(True).MaximizeButton(True))

        self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().
                          Name("test2").Caption("Client Size Reporter").
                          Bottom().Position(1).CloseButton(True).MaximizeButton(True))

        self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().
                          Name("test3").Caption("Client Size Reporter").
                          Bottom().CloseButton(True).MaximizeButton(True))
     
        self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().
                          Name("test4").Caption("Pane Caption").
                          Left().CloseButton(True).MaximizeButton(True))
                      
        self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().
                          Name("test5").Caption("Pane Caption").
                          Right().CloseButton(True).MaximizeButton(True))
                      
        self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().
                          Name("test6").Caption("Client Size Reporter").
                          Right().Row(1).CloseButton(True).MaximizeButton(True))

        self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().
                          Name("test7").Caption("Client Size Reporter").
                          Left().Layer(1).CloseButton(True).MaximizeButton(True))
                      
        self._mgr.AddPane(self.tree_pane, wx.aui.AuiPaneInfo().
                          Name("test8").Caption("Tree Pane").
                          Left().Layer(1).Position(1).CloseButton(True).MaximizeButton(True))
                      
        self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().
                          Name("test9").Caption("Min Size 200x100").
                          BestSize(wx.Size(200,100)).MinSize(wx.Size(200,100)).
                          Bottom().Layer(1).CloseButton(True).MaximizeButton(True))

        self._mgr.AddPane(self.text_pane, wx.aui.AuiPaneInfo().
                          Name("test10").Caption("Standard output").
                          Bottom().Layer(1).Position(1).CloseButton(True).MaximizeButton(True))


        # This output redirection code was taken from
        # Mouse vs. Python blog (Mike Driscoll)
        # The source Licence is L-GPL

        # redirect text here
        from gui import RedirectText
        self.redir=RedirectText(self.text_pane)
        sys.stdout=self.redir

        self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().
                          Name("test11").Caption("Fixed Pane").
                          Bottom().Layer(1).Position(2).Fixed().CloseButton(True).MaximizeButton(True))

        self._mgr.AddPane(SettingsPanel(self, self), wx.aui.AuiPaneInfo().
                          Name("settings").Caption("Dock Manager Settings").
                          Dockable(False).Float().Hide().CloseButton(True).MaximizeButton(True))

        # create some center panes

        self._mgr.AddPane(self.CreateGrid(), wx.aui.AuiPaneInfo().Name("grid_content").
                          CenterPane().Hide())

        self._mgr.AddPane(self.CreateTreeCtrl(), wx.aui.AuiPaneInfo().Name("tree_content").
                          CenterPane().Hide())
                      
        self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().Name("sizereport_content").
                          CenterPane().Hide())

        self._mgr.AddPane(self.CreateTextCtrl(), wx.aui.AuiPaneInfo().Name("text_content").
                          CenterPane().Hide())

        # changed to non-center for sharing workspace with the rest of the windows
        self._mgr.AddPane(self.CreateHTMLCtrl(),
                          wx.aui.AuiPaneInfo().Name("html_content").Caption("Work space").CloseButton(True).MaximizeButton(True))

        # add the toolbars to the manager

        self._mgr.AddPane(self.tb2, wx.aui.AuiPaneInfo().
                          Name("tb2").Caption("Toolbar 2").
                          ToolbarPane().Top().Row(0).Position(0).
                          LeftDockable(False).RightDockable(False))
                      
        self._mgr.AddPane(self.tb3, wx.aui.AuiPaneInfo().
                          Name("tb3").Caption("Toolbar 3").
                          ToolbarPane().Top().Row(0).Position(1).
                          LeftDockable(False).RightDockable(False))
                      
        self._mgr.AddPane(self.tb4, wx.aui.AuiPaneInfo().
                          Name("tb4").Caption("Sample Bookmark Toolbar").
                          ToolbarPane().Top().Row(2).Position(0).
                          LeftDockable(False).RightDockable(False))

        # make some default perspectives

        perspective_all = self._mgr.SavePerspective()
        all_panes = self._mgr.GetAllPanes()
        
        for ii in xrange(len(all_panes)):
            if not all_panes[ii].IsToolbar():
                all_panes[ii].Hide()
                
        self._mgr.GetPane("test8").Show().Left().Layer(0).Row(0).Position(0)
        self._mgr.GetPane("test10").Show().Bottom().Layer(0).Row(0).Position(0)
        self._mgr.GetPane("html_content").Show().Center().Layer(0).Row(0).Position(0)

        perspective_default = self._mgr.SavePerspective()

        for ii in xrange(len(all_panes)):
            if not all_panes[ii].IsToolbar():
                all_panes[ii].Hide()

        self._mgr.GetPane("grid_content").Show()
        self._mgr.GetPane("test8").Show().Left().Layer(0).Row(0).Position(0)
        self._mgr.GetPane("test10").Show().Bottom().Layer(0).Row(0).Position(0)
        self._mgr.GetPane("html_content").Show().Center().Layer(0).Row(0).Position(0)

        perspective_vert = self._mgr.SavePerspective()
        
        self._perspectives.append(perspective_default)
        self._perspectives.append(perspective_all)
        self._perspectives.append(perspective_vert)

        self._mgr.GetPane("grid_content").Hide()

        # "commit" all changes made to FrameManager   
        self._mgr.Update()

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # Show How To Use The Closing Panes Event
        self.Bind(wx.aui.EVT_AUI_PANE_CLOSE, self.OnPaneClose)
        
        self.Bind(wx.EVT_MENU, self.OnCreateTree, id=ID_CreateTree)
        self.Bind(wx.EVT_MENU, self.OnCreateGrid, id=ID_CreateGrid)
        self.Bind(wx.EVT_MENU, self.OnCreateText, id=ID_CreateText)
        self.Bind(wx.EVT_MENU, self.OnCreateHTML, id=ID_CreateHTML)
        self.Bind(wx.EVT_MENU, self.OnCreateSizeReport, id=ID_CreateSizeReport)
        self.Bind(wx.EVT_MENU, self.OnCreatePerspective, id=ID_CreatePerspective)
        self.Bind(wx.EVT_MENU, self.OnCopyPerspective, id=ID_CopyPerspective)

        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_AllowFloating)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_TransparentHint)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_VenetianBlindsHint)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_RectangleHint)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_NoHint)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_HintFade)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_NoVenetianFade)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_TransparentDrag)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_AllowActivePane)
        
        self.Bind(wx.EVT_MENU, self.OnGradient, id=ID_NoGradient)
        self.Bind(wx.EVT_MENU, self.OnGradient, id=ID_VerticalGradient)
        self.Bind(wx.EVT_MENU, self.OnGradient, id=ID_HorizontalGradient)
        self.Bind(wx.EVT_MENU, self.OnSettings, id=ID_Settings)
        self.Bind(wx.EVT_MENU, self.OnChangeContentPane, id=ID_GridContent)
        self.Bind(wx.EVT_MENU, self.OnChangeContentPane, id=ID_TreeContent)
        self.Bind(wx.EVT_MENU, self.OnChangeContentPane, id=ID_TextContent)
        self.Bind(wx.EVT_MENU, self.OnChangeContentPane, id=ID_SizeReportContent)
        self.Bind(wx.EVT_MENU, self.OnChangeContentPane, id=ID_HTMLContent)
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=ID_About)

        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_TransparentHint)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_VenetianBlindsHint)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_RectangleHint)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_NoHint)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_HintFade)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_AllowFloating)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_NoVenetianFade)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_TransparentDrag)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_AllowActivePane)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_NoGradient)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_VerticalGradient)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_HorizontalGradient)

    
        self.Bind(wx.EVT_MENU_RANGE, self.OnRestorePerspective, id=ID_FirstPerspective,
                  id2=ID_FirstPerspective+1000)

        # end of post-init code

    def OnPaneClose(self, event):

        caption = event.GetPane().caption

        if caption in ["Tree Pane", "Dock Manager Settings", "Fixed Pane"]:
            msg = "Are You Sure You Want To Close This Pane?"
            dlg = wx.MessageDialog(self, msg, "AUI Question",
                                   wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)

            if dlg.ShowModal() in [wx.ID_NO, wx.ID_CANCEL]:
                event.Veto()
            dlg.Destroy()
        

    def OnClose(self, event):
        self._mgr.UnInit()
        del self._mgr
        self.Destroy()


    def OnExit(self, event):
        self.Close()

    def OnAbout(self, event):

        msg = "wx.aui Demo\n" + \
              "An advanced window management library for wxWidgets\n" + \
              "(c) Copyright 2005-2006, Kirix Corporation"
        dlg = wx.MessageDialog(self, msg, "About wx.aui Demo",
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()        


    def GetDockArt(self):

        return self._mgr.GetArtProvider()


    def DoUpdate(self):

        self._mgr.Update()


    def OnEraseBackground(self, event):

        event.Skip()


    def OnSize(self, event):

        event.Skip()


    def OnSettings(self, event):

        # show the settings pane, and float it
        floating_pane = self._mgr.GetPane("settings").Float().Show()

        if floating_pane.floating_pos == wx.DefaultPosition:
            floating_pane.FloatingPosition(self.GetStartPosition())

        self._mgr.Update()


    def OnGradient(self, event):

        gradient = 0

        if event.GetId() == ID_NoGradient:
            gradient = wx.aui.AUI_GRADIENT_NONE
        elif event.GetId() == ID_VerticalGradient:
            gradient = wx.aui.AUI_GRADIENT_VERTICAL
        elif event.GetId() == ID_HorizontalGradient:
            gradient = wx.aui.AUI_GRADIENT_HORIZONTAL

        self._mgr.GetArtProvider().SetMetric(wx.aui.AUI_DOCKART_GRADIENT_TYPE, gradient)
        self._mgr.Update()


    def OnManagerFlag(self, event):

        flag = 0
        eid = event.GetId()

        if eid in [ ID_TransparentHint, ID_VenetianBlindsHint, ID_RectangleHint, ID_NoHint ]:
            flags = self._mgr.GetFlags()
            flags &= ~wx.aui.AUI_MGR_TRANSPARENT_HINT
            flags &= ~wx.aui.AUI_MGR_VENETIAN_BLINDS_HINT
            flags &= ~wx.aui.AUI_MGR_RECTANGLE_HINT
            self._mgr.SetFlags(flags)

        if eid == ID_AllowFloating:
            flag = wx.aui.AUI_MGR_ALLOW_FLOATING
        elif eid == ID_TransparentDrag:
            flag = wx.aui.AUI_MGR_TRANSPARENT_DRAG
        elif eid == ID_HintFade:
            flag = wx.aui.AUI_MGR_HINT_FADE
        elif eid == ID_NoVenetianFade:
            flag = wx.aui.AUI_MGR_NO_VENETIAN_BLINDS_FADE
        elif eid == ID_AllowActivePane:
            flag = wx.aui.AUI_MGR_ALLOW_ACTIVE_PANE
        elif eid == ID_TransparentHint:
            flag = wx.aui.AUI_MGR_TRANSPARENT_HINT
        elif eid == ID_VenetianBlindsHint:
            flag = wx.aui.AUI_MGR_VENETIAN_BLINDS_HINT
        elif eid == ID_RectangleHint:
            flag = wx.aui.AUI_MGR_RECTANGLE_HINT
        
        self._mgr.SetFlags(self._mgr.GetFlags() ^ flag)


    def OnUpdateUI(self, event):

        flags = self._mgr.GetFlags()
        eid = event.GetId()
        
        if eid == ID_NoGradient:
            event.Check(self._mgr.GetArtProvider().GetMetric(wx.aui.AUI_DOCKART_GRADIENT_TYPE) == wx.aui.AUI_GRADIENT_NONE)

        elif eid == ID_VerticalGradient:
            event.Check(self._mgr.GetArtProvider().GetMetric(wx.aui.AUI_DOCKART_GRADIENT_TYPE) == wx.aui.AUI_GRADIENT_VERTICAL)

        elif eid == ID_HorizontalGradient:
            event.Check(self._mgr.GetArtProvider().GetMetric(wx.aui.AUI_DOCKART_GRADIENT_TYPE) == wx.aui.AUI_GRADIENT_HORIZONTAL)

        elif eid == ID_AllowFloating:
            event.Check((flags & wx.aui.AUI_MGR_ALLOW_FLOATING) != 0)

        elif eid == ID_TransparentDrag:
            event.Check((flags & wx.aui.AUI_MGR_TRANSPARENT_DRAG) != 0)

        elif eid == ID_TransparentHint:
            event.Check((flags & wx.aui.AUI_MGR_TRANSPARENT_HINT) != 0)

        elif eid == ID_VenetianBlindsHint:
            event.Check((flags & wx.aui.AUI_MGR_VENETIAN_BLINDS_HINT) != 0)

        elif eid == ID_RectangleHint:
            event.Check((flags & wx.aui.AUI_MGR_RECTANGLE_HINT) != 0)

        elif eid == ID_NoHint:
            event.Check(((wx.aui.AUI_MGR_TRANSPARENT_HINT |
                          wx.aui.AUI_MGR_VENETIAN_BLINDS_HINT |
                          wx.aui.AUI_MGR_RECTANGLE_HINT) & flags) == 0)

        elif eid == ID_HintFade:
            event.Check((flags & wx.aui.AUI_MGR_HINT_FADE) != 0);

        elif eid == ID_NoVenetianFade:
            event.Check((flags & wx.aui.AUI_MGR_NO_VENETIAN_BLINDS_FADE) != 0);


    def SetActionTools(self, links):
        # erease and re-complete the action tools pane
        # links to other actions
        
        # auto completed action toolbar

        # This method is disabled
        # It has issues on toolbar render on ms windows
        
        # auto completed action toolbar
        """
        self.tb5 = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                         wx.TB_FLAT | wx.TB_NODIVIDER | wx.TB_HORZ_TEXT)
        self.tb5.SetToolBitmapSize(wx.Size(16, 16))

        self.tb5_bmp16 = wx.ArtProvider_GetBitmap(wx.ART_LIST_VIEW, wx.ART_OTHER, wx.Size(16, 16))
        
        self.button_16 = self.tb5.AddLabelTool(10016, "Actions", self.tb5_bmp16)
        self.tb5.Realize()

        self._mgr.AddPane(self.tb5, wx.aui.AuiPaneInfo().
                          Name("tb5").Caption("Action toolbar").
                          ToolbarPane().Top().Row(2).Position(1).
                          LeftDockable(False).RightDockable(False))
        """
        return

        if not type(links) in (list, set, tuple):
            print T("Liks object is not a sequence.")
            return
            
        elif len(links) == 0:
            print "SetActionTools: no links"
            self.tb5.ClearTools()
            return

        if hasattr(self, "tb5"):
            if self.tb5 is not None:
                # remove old action buttons
                self.tb5.ClearTools()
        else:
            print "Action tool bar not found"
            return

        for link in links:
            # search bitmap in directory or assign a default icon
            if ("_href" in link.attributes) and (link.attributes["_href"].find(config.APP_NAME) in (0, 1)):
                link_list = [l for l in link.attributes["_href"].split("/") if l != ""]
                try:
                    the_bitmap = wx.Bitmap(config.address[link_list[0]][link_list[1]]["__icon"])
                except KeyError:
                    # default icon bitmap
                    the_bitmap = wx.ArtProvider_GetBitmap(wx.ART_MISSING_IMAGE)

                # create new action with label from link data and the icon
                the_action_tool = self.tb5.AddLabelTool(wx.NewId(), str(link.flatten()), the_bitmap)

                # append url reference to the tool
                the_action_tool.SetClientData(link.attributes["_href"])

                # bind tool activation with the event handler
                self.Bind(wx.EVT_TOOL, self.OnActionToolLink, the_action_tool)

        # update the AUI manager and widget
        self._mgr.Update()
        return


    def OnActionToolLink(self, evt):
        # retrieve url from event data
        action_tool_id = evt.GetId()
        self.window.OnLinkClicked(self.tb5.GetToolClientData(action_tool_id))
        return

    def OnCreatePerspective(self, event):

        dlg = wx.TextEntryDialog(self, "Enter a name for the new perspective:", "AUI Test")
        
        dlg.SetValue(("Perspective %d")%(len(self._perspectives)+1))
        if dlg.ShowModal() != wx.ID_OK:
            return
        
        if len(self._perspectives) == 0:
            self._perspectives_menu.AppendSeparator()
        
        self._perspectives_menu.Append(ID_FirstPerspective + len(self._perspectives), dlg.GetValue())
        self._perspectives.append(self._mgr.SavePerspective())


    def OnCopyPerspective(self, event):

        s = self._mgr.SavePerspective()
        
        if wx.TheClipboard.Open():
        
            wx.TheClipboard.SetData(wx.TextDataObject(s))
            wx.TheClipboard.Close()
        
    def OnRestorePerspective(self, event):

        self._mgr.LoadPerspective(self._perspectives[event.GetId() - ID_FirstPerspective])


    def GetStartPosition(self):

        self.x = self.x + 20
        x = self.x
        pt = self.ClientToScreen(wx.Point(0, 0))
        
        return wx.Point(pt.x + x, pt.y + x)


    def OnCreateTree(self, event):
        self._mgr.AddPane(self.CreateTreeCtrl(), wx.aui.AuiPaneInfo().
                          Caption("Tree Control").
                          Float().FloatingPosition(self.GetStartPosition()).
                          FloatingSize(wx.Size(150, 300)).CloseButton(True).MaximizeButton(True))
        self._mgr.Update()


    def OnCreateGrid(self, event):
        self._mgr.AddPane(self.CreateGrid(), wx.aui.AuiPaneInfo().
                          Caption("Grid").
                          Float().FloatingPosition(self.GetStartPosition()).
                          FloatingSize(wx.Size(300, 200)).CloseButton(True).MaximizeButton(True))
        self._mgr.Update()


    def OnCreateHTML(self, event):
        self._mgr.AddPane(self.CreateHTMLCtrl(), wx.aui.AuiPaneInfo().
                          Caption("HTML Content").
                          Float().FloatingPosition(self.GetStartPosition()).
                          FloatingSize(wx.Size(300, 200)).CloseButton(True).MaximizeButton(True))
        self._mgr.Update()


    def OnCreateText(self, event):
        self._mgr.AddPane(self.CreateTextCtrl(), wx.aui.AuiPaneInfo().
                          Caption("Text Control").
                          Float().FloatingPosition(self.GetStartPosition()).
                          CloseButton(True).MaximizeButton(True))
        self._mgr.Update()


    def OnCreateSizeReport(self, event):
        self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().
                          Caption("Client Size Reporter").
                          Float().FloatingPosition(self.GetStartPosition()).
                          CloseButton(True).MaximizeButton(True))
        self._mgr.Update()


    def OnChangeContentPane(self, event):

        self._mgr.GetPane("grid_content").Show(event.GetId() == ID_GridContent)
        self._mgr.GetPane("text_content").Show(event.GetId() == ID_TextContent)
        self._mgr.GetPane("tree_content").Show(event.GetId() == ID_TreeContent)
        self._mgr.GetPane("sizereport_content").Show(event.GetId() == ID_SizeReportContent)
        self._mgr.GetPane("html_content").Show(event.GetId() == ID_HTMLContent)
        self._mgr.Update()


    def CreateTextCtrl(self, default_text = None):
        if default_text == None:
            text = ("This is text box %d")%(self.n + 1)
        else:
            text = default_text

        return wx.TextCtrl(self,-1, text, wx.Point(0, 0), wx.Size(150, 90),
                           wx.NO_BORDER | wx.TE_MULTILINE)



    def CreateGrid(self):

        grid = wx.grid.Grid(self, -1, wx.Point(0, 0), wx.Size(150, 250),
                            wx.NO_BORDER | wx.WANTS_CHARS)
        
        grid.CreateGrid(50, 20)

        return grid


    def CreateTreeCtrl(self):

        tree = wx.TreeCtrl(self, -1, wx.Point(0, 0), wx.Size(160, 250),
                           wx.TR_DEFAULT_STYLE | wx.NO_BORDER)
        
        root = tree.AddRoot("Actions")
        items = []

        imglist = wx.ImageList(16, 16, True, 2)
        imglist.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, wx.Size(16,16)))
        imglist.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, wx.Size(16,16)))
        
        tree.AssignImageList(imglist)

        items.append(tree.AppendItem(root, "Item 1", 0))
        items.append(tree.AppendItem(root, "Item 2", 0))
        items.append(tree.AppendItem(root, "Item 3", 0))
        items.append(tree.AppendItem(root, "Item 4", 0))
        items.append(tree.AppendItem(root, "Item 5", 0))

        for ii in xrange(len(items)):
        
            id = items[ii]
            tree.AppendItem(id, "Subitem 1", 1)
            tree.AppendItem(id, "Subitem 2", 1)
            tree.AppendItem(id, "Subitem 3", 1)
            tree.AppendItem(id, "Subitem 4", 1)
            tree.AppendItem(id, "Subitem 5", 1)
        
        tree.Expand(root)

        return tree


    def CreateSizeReportCtrl(self, width=80, height=80):

        ctrl = SizeReportCtrl(self, -1, wx.DefaultPosition,
                              wx.Size(width, height), self._mgr)
        return ctrl


    def CreateHTMLCtrl(self):
        from gui import NewHtmlWindow
        self.window = NewHtmlWindow(self, -1, wx.DefaultPosition, wx.Size(400, 300), style = config.WX_HTML_STYLE)
        if "gtk2" in wx.PlatformInfo:
            self.window.SetStandardFonts()
        # self.window.SetPage(self.GetIntroText())
        return self.window


    def GetIntroText(self):
        return overview


# -- wx.SizeReportCtrl --
# (a utility control that always reports it's client size)

class SizeReportCtrl(wx.PyControl):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, mgr=None):

        wx.PyControl.__init__(self, parent, id, pos, size, wx.NO_BORDER)
            
        self._mgr = mgr

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)


    def OnPaint(self, event):

        dc = wx.PaintDC(self)
        
        size = self.GetClientSize()
        s = ("Size: %d x %d")%(size.x, size.y)

        dc.SetFont(wx.NORMAL_FONT)
        w, height = dc.GetTextExtent(s)
        height = height + 3
        dc.SetBrush(wx.WHITE_BRUSH)
        dc.SetPen(wx.WHITE_PEN)
        dc.DrawRectangle(0, 0, size.x, size.y)
        dc.SetPen(wx.LIGHT_GREY_PEN)
        dc.DrawLine(0, 0, size.x, size.y)
        dc.DrawLine(0, size.y, size.x, 0)
        dc.DrawText(s, (size.x-w)/2, ((size.y-(height*5))/2))
        
        if self._mgr:
        
            pi = self._mgr.GetPane(self)
            
            s = ("Layer: %d")%pi.dock_layer
            w, h = dc.GetTextExtent(s)
            dc.DrawText(s, (size.x-w)/2, ((size.y-(height*5))/2)+(height*1))
           
            s = ("Dock: %d Row: %d")%(pi.dock_direction, pi.dock_row)
            w, h = dc.GetTextExtent(s)
            dc.DrawText(s, (size.x-w)/2, ((size.y-(height*5))/2)+(height*2))
            
            s = ("Position: %d")%pi.dock_pos
            w, h = dc.GetTextExtent(s)
            dc.DrawText(s, (size.x-w)/2, ((size.y-(height*5))/2)+(height*3))
            
            s = ("Proportion: %d")%pi.dock_proportion
            w, h = dc.GetTextExtent(s)
            dc.DrawText(s, (size.x-w)/2, ((size.y-(height*5))/2)+(height*4))
        

    def OnEraseBackground(self, event):
        # intentionally empty
        pass        
    

    def OnSize(self, event):
    
        self.Refresh()
        event.Skip()
    

ID_PaneBorderSize = wx.ID_HIGHEST + 1
ID_SashSize = ID_PaneBorderSize + 1
ID_CaptionSize = ID_PaneBorderSize + 2
ID_BackgroundColor = ID_PaneBorderSize + 3
ID_SashColor = ID_PaneBorderSize + 4
ID_InactiveCaptionColor =  ID_PaneBorderSize + 5
ID_InactiveCaptionGradientColor = ID_PaneBorderSize + 6
ID_InactiveCaptionTextColor = ID_PaneBorderSize + 7
ID_ActiveCaptionColor = ID_PaneBorderSize + 8
ID_ActiveCaptionGradientColor = ID_PaneBorderSize + 9
ID_ActiveCaptionTextColor = ID_PaneBorderSize + 10
ID_BorderColor = ID_PaneBorderSize + 11
ID_GripperColor = ID_PaneBorderSize + 12
    
class SettingsPanel(wx.Panel):
    
    def __init__(self, parent, frame):

        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                          wx.DefaultSize)

        T = config.env["T"]
        self._frame = frame

        vert = wx.BoxSizer(wx.VERTICAL)

        s1 = wx.BoxSizer(wx.HORIZONTAL)
        self._border_size = wx.SpinCtrl(self, ID_PaneBorderSize, "", wx.DefaultPosition, wx.Size(50,20))
        s1.Add((1, 1), 1, wx.EXPAND)
        s1.Add(wx.StaticText(self, -1, T("Pane Border Size:")))
        s1.Add(self._border_size)
        s1.Add((1, 1), 1, wx.EXPAND)
        s1.SetItemMinSize(1, (180, 20))
        #vert.Add(s1, 0, wx.EXPAND | wxLEFT | wxBOTTOM, 5)

        s2 = wx.BoxSizer(wx.HORIZONTAL)
        self._sash_size = wx.SpinCtrl(self, ID_SashSize, "", wx.DefaultPosition, wx.Size(50,20))
        s2.Add((1, 1), 1, wx.EXPAND)
        s2.Add(wx.StaticText(self, -1, T("Sash Size:")))
        s2.Add(self._sash_size)
        s2.Add((1, 1), 1, wx.EXPAND)
        s2.SetItemMinSize(1, (180, 20))
        #vert.Add(s2, 0, wx.EXPAND | wxLEFT | wxBOTTOM, 5)

        s3 = wx.BoxSizer(wx.HORIZONTAL)
        self._caption_size = wx.SpinCtrl(self, ID_CaptionSize, "", wx.DefaultPosition, wx.Size(50,20))
        s3.Add((1, 1), 1, wx.EXPAND)
        s3.Add(wx.StaticText(self, -1, T("Caption Size:")))
        s3.Add(self._caption_size)
        s3.Add((1, 1), 1, wx.EXPAND)
        s3.SetItemMinSize(1, (180, 20))
        #vert.Add(s3, 0, wx.EXPAND | wxLEFT | wxBOTTOM, 5)

        #vert.Add(1, 1, 1, wx.EXPAND)

        b = self.CreateColorBitmap(wx.BLACK)

        s4 = wx.BoxSizer(wx.HORIZONTAL)
        self._background_color = wx.BitmapButton(self, ID_BackgroundColor, b, wx.DefaultPosition, wx.Size(50,25))
        s4.Add((1, 1), 1, wx.EXPAND)
        s4.Add(wx.StaticText(self, -1, T("Background Color:")))
        s4.Add(self._background_color)
        s4.Add((1, 1), 1, wx.EXPAND)
        s4.SetItemMinSize(1, (180, 20))

        s5 = wx.BoxSizer(wx.HORIZONTAL)
        self._sash_color = wx.BitmapButton(self, ID_SashColor, b, wx.DefaultPosition, wx.Size(50,25))
        s5.Add((1, 1), 1, wx.EXPAND)
        s5.Add(wx.StaticText(self, -1, T("Sash Color:")))
        s5.Add(self._sash_color)
        s5.Add((1, 1), 1, wx.EXPAND)
        s5.SetItemMinSize(1, (180, 20))

        s6 = wx.BoxSizer(wx.HORIZONTAL)
        self._inactive_caption_color = wx.BitmapButton(self, ID_InactiveCaptionColor, b,
                                                       wx.DefaultPosition, wx.Size(50,25))
        s6.Add((1, 1), 1, wx.EXPAND)
        s6.Add(wx.StaticText(self, -1, T("Normal Caption:")))
        s6.Add(self._inactive_caption_color)
        s6.Add((1, 1), 1, wx.EXPAND)
        s6.SetItemMinSize(1, (180, 20))

        s7 = wx.BoxSizer(wx.HORIZONTAL)
        self._inactive_caption_gradient_color = wx.BitmapButton(self, ID_InactiveCaptionGradientColor,
                                                                b, wx.DefaultPosition, wx.Size(50,25))
        s7.Add((1, 1), 1, wx.EXPAND)
        s7.Add(wx.StaticText(self, -1, T("Normal Caption Gradient:")))
        s7.Add(self._inactive_caption_gradient_color)
        s7.Add((1, 1), 1, wx.EXPAND)
        s7.SetItemMinSize(1, (180, 20))

        s8 = wx.BoxSizer(wx.HORIZONTAL)
        self._inactive_caption_text_color = wx.BitmapButton(self, ID_InactiveCaptionTextColor, b,
                                                            wx.DefaultPosition, wx.Size(50,25))
        s8.Add((1, 1), 1, wx.EXPAND)
        s8.Add(wx.StaticText(self, -1, T("Normal Caption Text:")))
        s8.Add(self._inactive_caption_text_color)
        s8.Add((1, 1), 1, wx.EXPAND)
        s8.SetItemMinSize(1, (180, 20))

        s9 = wx.BoxSizer(wx.HORIZONTAL)
        self._active_caption_color = wx.BitmapButton(self, ID_ActiveCaptionColor, b,
                                                     wx.DefaultPosition, wx.Size(50,25))
        s9.Add((1, 1), 1, wx.EXPAND)
        s9.Add(wx.StaticText(self, -1, T("Active Caption:")))
        s9.Add(self._active_caption_color)
        s9.Add((1, 1), 1, wx.EXPAND)
        s9.SetItemMinSize(1, (180, 20))

        s10 = wx.BoxSizer(wx.HORIZONTAL)
        self._active_caption_gradient_color = wx.BitmapButton(self, ID_ActiveCaptionGradientColor,
                                                              b, wx.DefaultPosition, wx.Size(50,25))
        s10.Add((1, 1), 1, wx.EXPAND)
        s10.Add(wx.StaticText(self, -1, T("Active Caption Gradient:")))
        s10.Add(self._active_caption_gradient_color)
        s10.Add((1, 1), 1, wx.EXPAND)
        s10.SetItemMinSize(1, (180, 20))

        s11 = wx.BoxSizer(wx.HORIZONTAL)
        self._active_caption_text_color = wx.BitmapButton(self, ID_ActiveCaptionTextColor,
                                                          b, wx.DefaultPosition, wx.Size(50,25))
        s11.Add((1, 1), 1, wx.EXPAND)
        s11.Add(wx.StaticText(self, -1, T("Active Caption Text:")))
        s11.Add(self._active_caption_text_color)
        s11.Add((1, 1), 1, wx.EXPAND)
        s11.SetItemMinSize(1, (180, 20))

        s12 = wx.BoxSizer(wx.HORIZONTAL)
        self._border_color = wx.BitmapButton(self, ID_BorderColor, b, wx.DefaultPosition,
                                             wx.Size(50,25))
        s12.Add((1, 1), 1, wx.EXPAND)
        s12.Add(wx.StaticText(self, -1, T("Border Color:")))
        s12.Add(self._border_color)
        s12.Add((1, 1), 1, wx.EXPAND)
        s12.SetItemMinSize(1, (180, 20))

        s13 = wx.BoxSizer(wx.HORIZONTAL)
        self._gripper_color = wx.BitmapButton(self, ID_GripperColor, b, wx.DefaultPosition,
                                              wx.Size(50,25))
        s13.Add((1, 1), 1, wx.EXPAND)
        s13.Add(wx.StaticText(self, -1, T("Gripper Color:")))
        s13.Add(self._gripper_color)
        s13.Add((1, 1), 1, wx.EXPAND)
        s13.SetItemMinSize(1, (180, 20))
        
        grid_sizer = wx.GridSizer(0, 2)
        grid_sizer.SetHGap(5)
        grid_sizer.Add(s1)
        grid_sizer.Add(s4)
        grid_sizer.Add(s2)
        grid_sizer.Add(s5)
        grid_sizer.Add(s3)
        grid_sizer.Add(s13)
        grid_sizer.Add((1, 1))
        grid_sizer.Add(s12)
        grid_sizer.Add(s6)
        grid_sizer.Add(s9)
        grid_sizer.Add(s7)
        grid_sizer.Add(s10)
        grid_sizer.Add(s8)
        grid_sizer.Add(s11)
         
        cont_sizer = wx.BoxSizer(wx.VERTICAL)
        cont_sizer.Add(grid_sizer, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(cont_sizer)
        self.GetSizer().SetSizeHints(self)

        self._border_size.SetValue(frame.GetDockArt().GetMetric(wx.aui.AUI_DOCKART_PANE_BORDER_SIZE))
        self._sash_size.SetValue(frame.GetDockArt().GetMetric(wx.aui.AUI_DOCKART_SASH_SIZE))
        self._caption_size.SetValue(frame.GetDockArt().GetMetric(wx.aui.AUI_DOCKART_CAPTION_SIZE))
        
        self.UpdateColors()

        self.Bind(wx.EVT_SPINCTRL, self.OnPaneBorderSize, id=ID_PaneBorderSize)
        self.Bind(wx.EVT_SPINCTRL, self.OnSashSize, id=ID_SashSize)
        self.Bind(wx.EVT_SPINCTRL, self.OnCaptionSize, id=ID_CaptionSize)
        self.Bind(wx.EVT_BUTTON, self.OnSetColor, id=ID_BackgroundColor)
        self.Bind(wx.EVT_BUTTON, self.OnSetColor, id=ID_SashColor)
        self.Bind(wx.EVT_BUTTON, self.OnSetColor, id=ID_InactiveCaptionColor)
        self.Bind(wx.EVT_BUTTON, self.OnSetColor, id=ID_InactiveCaptionGradientColor)
        self.Bind(wx.EVT_BUTTON, self.OnSetColor, id=ID_InactiveCaptionTextColor)
        self.Bind(wx.EVT_BUTTON, self.OnSetColor, id=ID_ActiveCaptionColor)
        self.Bind(wx.EVT_BUTTON, self.OnSetColor, id=ID_ActiveCaptionGradientColor)
        self.Bind(wx.EVT_BUTTON, self.OnSetColor, id=ID_ActiveCaptionTextColor)
        self.Bind(wx.EVT_BUTTON, self.OnSetColor, id=ID_BorderColor)
        self.Bind(wx.EVT_BUTTON, self.OnSetColor, id=ID_GripperColor)
    
    
    def CreateColorBitmap(self, c):
        image = wx.EmptyImage(25, 14)
        
        for x in xrange(25):
            for y in xrange(14):
                pixcol = c
                if x == 0 or x == 24 or y == 0 or y == 13:
                    pixcol = wx.BLACK
                    
                image.SetRGB(x, y, pixcol.Red(), pixcol.Green(), pixcol.Blue())
            
        return image.ConvertToBitmap()
    
    
    def UpdateColors(self):
    
        bk = self._frame.GetDockArt().GetColour(wx.aui.AUI_DOCKART_BACKGROUND_COLOUR)
        self._background_color.SetBitmapLabel(self.CreateColorBitmap(bk))
        
        cap = self._frame.GetDockArt().GetColour(wx.aui.AUI_DOCKART_INACTIVE_CAPTION_COLOUR)
        self._inactive_caption_color.SetBitmapLabel(self.CreateColorBitmap(cap))
        
        capgrad = self._frame.GetDockArt().GetColour(wx.aui.AUI_DOCKART_INACTIVE_CAPTION_GRADIENT_COLOUR)
        self._inactive_caption_gradient_color.SetBitmapLabel(self.CreateColorBitmap(capgrad))
        
        captxt = self._frame.GetDockArt().GetColour(wx.aui.AUI_DOCKART_INACTIVE_CAPTION_TEXT_COLOUR)
        self._inactive_caption_text_color.SetBitmapLabel(self.CreateColorBitmap(captxt))
        
        acap = self._frame.GetDockArt().GetColour(wx.aui.AUI_DOCKART_ACTIVE_CAPTION_COLOUR)
        self._active_caption_color.SetBitmapLabel(self.CreateColorBitmap(acap))
        
        acapgrad = self._frame.GetDockArt().GetColour(wx.aui.AUI_DOCKART_ACTIVE_CAPTION_GRADIENT_COLOUR)
        self._active_caption_gradient_color.SetBitmapLabel(self.CreateColorBitmap(acapgrad))
        
        acaptxt = self._frame.GetDockArt().GetColour(wx.aui.AUI_DOCKART_ACTIVE_CAPTION_TEXT_COLOUR)
        self._active_caption_text_color.SetBitmapLabel(self.CreateColorBitmap(acaptxt))
        
        sash = self._frame.GetDockArt().GetColour(wx.aui.AUI_DOCKART_SASH_COLOUR)
        self._sash_color.SetBitmapLabel(self.CreateColorBitmap(sash))
        
        border = self._frame.GetDockArt().GetColour(wx.aui.AUI_DOCKART_BORDER_COLOUR)
        self._border_color.SetBitmapLabel(self.CreateColorBitmap(border))
        
        gripper = self._frame.GetDockArt().GetColour(wx.aui.AUI_DOCKART_GRIPPER_COLOUR)
        self._gripper_color.SetBitmapLabel(self.CreateColorBitmap(gripper))
    
    
    def OnPaneBorderSize(self, event):
    
        self._frame.GetDockArt().SetMetric(wx.aui.AUI_DOCKART_PANE_BORDER_SIZE,
                                           event.GetInt())
        self._frame.DoUpdate()


    def OnSashSize(self, event):

        self._frame.GetDockArt().SetMetric(wx.aui.AUI_DOCKART_SASH_SIZE,
                                           event.GetInt())
        self._frame.DoUpdate()
    

    def OnCaptionSize(self, event):
    
        self._frame.GetDockArt().SetMetric(wx.aui.AUI_DOCKART_CAPTION_SIZE,
                                           event.GetInt())
        self._frame.DoUpdate()
    

    def OnSetColor(self, event):
    
        dlg = wx.ColourDialog(self._frame)
        
        dlg.SetTitle("Color Picker")
        
        if dlg.ShowModal() != wx.ID_OK:
            return
        
        var = 0
        if event.GetId() == ID_BackgroundColor:
            var = wx.aui.AUI_DOCKART_BACKGROUND_COLOUR
        elif event.GetId() == ID_SashColor:
            var = wx.aui.AUI_DOCKART_SASH_COLOUR
        elif event.GetId() == ID_InactiveCaptionColor:
            var = wx.aui.AUI_DOCKART_INACTIVE_CAPTION_COLOUR
        elif event.GetId() == ID_InactiveCaptionGradientColor:
            var = wx.aui.AUI_DOCKART_INACTIVE_CAPTION_GRADIENT_COLOUR
        elif event.GetId() == ID_InactiveCaptionTextColor:
            var = wx.aui.AUI_DOCKART_INACTIVE_CAPTION_TEXT_COLOUR
        elif event.GetId() == ID_ActiveCaptionColor:
            var = wx.aui.AUI_DOCKART_ACTIVE_CAPTION_COLOUR
        elif event.GetId() == ID_ActiveCaptionGradientColor:
            var = wx.aui.AUI_DOCKART_ACTIVE_CAPTION_GRADIENT_COLOUR
        elif event.GetId() == ID_ActiveCaptionTextColor:
            var = wx.aui.AUI_DOCKART_ACTIVE_CAPTION_TEXT_COLOUR
        elif event.GetId() == ID_BorderColor:
            var = wx.aui.AUI_DOCKART_BORDER_COLOUR
        elif event.GetId() == ID_GripperColor:
            var = wx.aui.AUI_DOCKART_GRIPPER_COLOUR
        else:
            return        
        
        self._frame.GetDockArt().SetColor(var, dlg.GetColourData().GetColour())
        self._frame.DoUpdate()
        self.UpdateColors()



#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)
        b = wx.Button(self, -1, "Show the wx.aui Demo Frame", (50,50))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)

    def OnButton(self, evt):
        frame = PyAUIFrame(self, wx.ID_ANY, "wx.aui wxPython Demo", size=(750, 590))
        frame.Show()

#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------


# wx Glade auto objects

class MyHTMLFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyHTMLFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.button_6 = wx.Button(self, -1, "Previous")
        self.button_9 = wx.Button(self, -1, "Home")
        self.button_7 = wx.Button(self, -1, "Next")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyHTMLFrame.__set_properties
        self.SetTitle("Work space")
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyHTMLFrame.__do_layout
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4.Add(self.button_6, 0, 0, 0)
        sizer_4.Add(self.button_9, 0, 0, 0)
        sizer_4.Add(self.button_7, 0, 0, 0)
        sizer_3.Add(sizer_4, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_3)
        sizer_3.Fit(self)
        self.Layout()
        # end wxGlade

# end of class MyHTMLFrame


class MyDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyDialog.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        
        self.title = kwds.get("title", "Feedback")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyDialog.__set_properties
        self.SetTitle(self.title)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyDialog.__do_layout
        self.Layout()
        # end wxGlade

# end of class MyDialog


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        # Menu Bar
        self.starting_menubar = wx.MenuBar()
        self.SetMenuBar(self.starting_menubar)
        # Menu Bar end
        self.starting_frame_statusbar = self.CreateStatusBar(1, 0)
        self.bitmap_1 = wx.StaticBitmap(self, -1, wx.Bitmap("images/logo.png", wx.BITMAP_TYPE_ANY))
        self.button_1 = wx.Button(self, -1, "Billing")
        self.button_2 = wx.Button(self, -1, "Current Accounts")
        self.button_3 = wx.Button(self, -1, "Customers")
        self.button_4 = wx.Button(self, -1, "Articles")
        self.button_5 = wx.Button(self, -1, "Queries")
        self.button_8 = wx.Button(self, -1, "Movements")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle(u"ERP Libre")
        self.starting_frame_statusbar.SetStatusWidths([-1])
        # statusbar fields
        starting_frame_statusbar_fields = ["Status bar text"]
        for i in range(len(starting_frame_statusbar_fields)):
            self.starting_frame_statusbar.SetStatusText(starting_frame_statusbar_fields[i], i)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(self.bitmap_1, 0, 0, 0)
        sizer_2.Add((20, 20), 0, 0, 0)
        sizer_2.Add(self.button_1, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_2.Add(self.button_2, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_2.Add(self.button_3, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_2.Add(self.button_4, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_2.Add(self.button_5, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_2.Add(self.button_8, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_2.Add((20, 20), 0, 0, 0)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade

# end of class MyFrame


class MyLoginDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyLoginDialog.__init__
        wx.Dialog.__init__(self, *args, **kwds)
        self.bitmap_2 = wx.StaticBitmap(self, -1, wx.Bitmap("images/erplibre-logo-100.png", wx.BITMAP_TYPE_ANY))
        self.label_1 = wx.StaticText(self, -1, "label_1")
        self.label_3 = wx.StaticText(self, -1, "label_3")
        self.text_ctrl_1 = wx.TextCtrl(self, -1, "")
        self.label_2 = wx.StaticText(self, -1, "label_2")
        self.text_ctrl_2 = wx.TextCtrl(self, -1, "", style=wx.TE_PASSWORD)
        self.button_10 = wx.Button(self, wx.ID_OK, "")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyLoginDialog.__set_properties
        self.SetTitle("Access control")
        self.label_3.SetMinSize((80, 17))
        self.text_ctrl_1.SetMinSize((160, 25))
        self.label_2.SetMinSize((80, 17))
        self.text_ctrl_2.SetMinSize((160, 25))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyLoginDialog.__do_layout
        sizer_5 = wx.BoxSizer(wx.VERTICAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_9 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5.Add((20, 20), 0, 0, 0)
        sizer_7.Add((20, 20), 0, 0, 0)
        sizer_7.Add(self.bitmap_2, 0, 0, 0)
        sizer_5.Add(sizer_7, 1, wx.EXPAND, 0)
        sizer_5.Add((20, 20), 0, 0, 0)
        sizer_9.Add((20, 20), 0, 0, 0)
        sizer_9.Add(self.label_1, 0, 0, 0)
        sizer_9.Add((20, 20), 0, 0, 0)
        sizer_5.Add(sizer_9, 1, wx.EXPAND, 0)
        sizer_10.Add((20, 20), 0, 0, 0)
        sizer_10.Add(self.label_3, 0, 0, 0)
        sizer_10.Add((20, 20), 0, 0, 0)
        sizer_10.Add(self.text_ctrl_1, 0, 0, 0)
        sizer_10.Add((20, 20), 0, 0, 0)
        sizer_5.Add(sizer_10, 1, wx.EXPAND, 0)
        sizer_8.Add((20, 20), 0, 0, 0)
        sizer_8.Add(self.label_2, 0, 0, 0)
        sizer_8.Add((20, 20), 0, 0, 0)
        sizer_8.Add(self.text_ctrl_2, 0, 0, 0)
        sizer_8.Add((20, 20), 0, 0, 0)
        sizer_5.Add(sizer_8, 1, wx.EXPAND, 0)
        sizer_5.Add((20, 20), 0, 0, 0)
        sizer_6.Add((120, 20), 0, 0, 0)
        sizer_6.Add(self.button_10, 0, 0, 0)
        sizer_6.Add((20, 20), 0, 0, 0)
        sizer_5.Add(sizer_6, 1, 0, 0)
        sizer_5.Add((20, 20), 0, 0, 0)
        self.SetSizer(sizer_5)
        sizer_5.Fit(self)
        self.Layout()
        # end wxGlade

# end of class MyLoginDialog


# end of wx Glade auto objects


overview = """\
<html><body>
</body></html>
"""

if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

