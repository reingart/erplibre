#! /usr/bin/python
# -*- coding: utf-8 -*-

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

__author__ = "Alan Etkin <spametki@gmail.com>"
__copyright__ = "Copyright (C) 2012 Sistemas Ágiles"
__license__ = "AGPLv3"

import wx

# wxGlade pre-made setup frame
class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        self.starting_frame_statusbar = \
        self.CreateStatusBar(1, 0)
        self.bitmap_1 = wx.StaticBitmap(self, \
        -1, wx.Bitmap("images/erplibre-setup-background.png", wx.BITMAP_TYPE_ANY))
        self.button_start = wx.Button(self, -1, "Install")
        self.panel = wx.Panel(self, -1)
        self.count = 0
        self.gauge = wx.Gauge(self.panel, -1, 50, \
        (0, 0), (480, 25))
        self.gauge.SetBezelFace(3)
        self.gauge.SetShadowWidth(3)
        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle(u"ERP Libre Setup")
        self.starting_frame_statusbar.SetStatusWidths( \
        [-1])
        # statusbar fields
        starting_frame_statusbar_fields = ["Status bar text"]
        for i in range(len(starting_frame_statusbar_fields)):
            self.starting_frame_statusbar.SetStatusText( \
            starting_frame_statusbar_fields[i], i)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)

        sizer_1.Add(self.bitmap_1, 0, 0, 0)
        sizer_1.Add((20, 20))
        sizer_2.Add((20, 20), 0, 0, 0)
        sizer_2.Add(self.button_start, 0, 0, 0)
        sizer_2.Add((20, 20), 0, 0, 0)
        sizer_2.Add(self.panel, 0, 0, 0)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        sizer_1.Add((20, 20))

        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade

