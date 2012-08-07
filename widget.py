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


"""
This module is intended to store custom widget classes
to handle user input and wx widgets inside the application
work space (wx.HTMLWindow instance), trough the HTML
object tag
"""

import datetime
import os
import wx
import wx.html
import wx.lib.masked.timectrl
import gui2py.input
import aui

FORMATS = {"date": "%Y-%m-%d", "datetime": "%Y-%m-%d %H:%M:%S", "time": "%H:%M:%S"}

class MyTextInput(gui2py.input.TextInput):
    """
    gui2py form input class overriding
    subclasses gui2py.input.TextInput
    """
    # This statement is required to override gui2py tag handling
    __metaclass__ = gui2py.input.TypeHandler("TEXT")
    def __init__(self, parent, form, tag, parser, *args, **kwargs):
        # call the parent class __init__ method to initialize
        # common input properties
        gui2py.input.TextInput.__init__(self, parent, form, tag, parser, *args, **kwargs)


        # Widget's output on dialog accept
        self.value = None

        # input events
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_LEFT_UP, self.OnClick)
        self.Bind(wx.EVT_KEY_UP, self.OnKeyUp)

    def OnClick(self, event):
        if self.FindFocus() == self:
            self.StartDialog(event)
        event.Skip()

    def OnKeyUp(self, event):
        """ Handles the wx.EVT_KEY_UP event for the widget. """
        if event.GetKeyCode() == wx.WXK_F2:
            self.StartDialog(event)
        event.Skip()

    def StartDialog(self, event):
        self.mydialog = None
        if self._attributes.get("_class") == "date":
            self.mydialog = aui.MyDialog(self, size=(150, 50), title=self._attributes.get("_name").capitalize())
            self.mydatewidget = wx.DatePickerCtrl(self.mydialog, size=(150, 50))
            self.mydatewidget.Bind(wx.EVT_DATE_CHANGED, self.OnDateChanged)

            value = self.GetDate(self._attributes.get("_value"))
            if value is not None:
                wdt = wx.DateTime()
                wdt.Set(value.day, month=int(value.month) - 1, year=value.year)
                self.mydatewidget.SetValue(wdt)

            self.mydatewidget.Bind(wx.EVT_KEY_UP, self.DateOnKeyUp)
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(self.mydatewidget, 0, 0, 0)
            self.mydialog.SetSizer(sizer)
            sizer.Fit(self.mydialog)

            self.mydialog.Layout()
            self.mydialog.Show()
            self.mydialog.SetFocus()

        elif self._attributes.get("_class") == "datetime":
            self.mydialog = aui.MyDialog(self, size=(150, 100), title=self._attributes.get("_name").capitalize())
            self.mydatewidget = wx.DatePickerCtrl(self.mydialog, size=(150, 50))
            self.mydatewidget.Bind(wx.EVT_DATE_CHANGED, self.OnDateChanged)
            self.mytimewidget = wx.lib.masked.timectrl.TimeCtrl(self.mydialog, size=(150, 50))

            value = self.GetDate(self._attributes.get("_value"))
            if value is not None:
                wdt = wx.DateTime()
                wdt.Set(value.day, month=int(value.month) -1, year=value.year, hour=value.hour, minute=value.minute, second=value.second)
                self.mydatewidget.SetValue(wdt)
                self.mytimewidget.SetValue(wdt)

            self.mydatewidget.Bind(wx.EVT_KEY_UP, self.DateOnKeyUp)
            self.mytimewidget.Bind(wx.EVT_KEY_UP, self.DateOnKeyUp)
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(self.mytimewidget, 0, 0, 0)
            sizer.Add(self.mydatewidget, 0, 0, 0)
            self.mydialog.SetSizer(sizer)
            sizer.Fit(self.mydialog)

            self.mydialog.Layout()
            self.mydialog.Show()
            self.mydialog.SetFocus()

        elif self._attributes.get("_class") == "path":
            # path dialog
            default = self._attributes.get("_value", os.getcwd())
            message=self._attributes.get("_name").capitalize()
            if default is not None:
                self.path_dialog = wx.DirDialog(self, message=message,
                                                defaultPath=default)
            else:
                self.path_dialog = wx.DirDialog(self, message=message)

            if self.path_dialog.ShowModal() == wx.ID_OK:
                self.SetValue(self.path_dialog.GetPath())

        elif self._attributes.get("_class") == "file":
            # file dialog
            default = self._attributes.get("_value")
            default_file = ""
            default_dir = os.getcwd()
            message = self._attributes.get("_name").capitalize()
            if default is not None:
                default_file = os.path.basename(default)
                default_dir = os.path.dirname(default)
                self.file_dialog = wx.FileDialog(self, message=message,
                                                    defaultDir=default_dir,
                                                    defaultFile=default_file,
                                                    wildcard="*.*", style=0)
            else:
                self.file_dialog = wx.FileDialog(self, message=message, wildcard="*.*", style=0)

            if self.file_dialog.ShowModal() == wx.ID_OK:
                self.SetValue(os.path.basename(self.file_dialog.GetPath()))

        elif self._attributes.get("_class") == "color":
            # color picker
            # set default color (read from cell)
            default = self._attributes.get("_value")
            if default is not None and len(default) == 7:
                data = wx.ColourData()
                red = int("0x" + default[1:3], 0)
                blue =  int("0x" + default[3:5], 0)
                green = int("0x" + default[5:], 0)
                default_color = wx.Colour(red, blue, green)
                data.SetColour(default_color)
                self.color_dialog = wx.ColourDialog(self, data)
            else:
                self.color_dialog = wx.ColourDialog(self)

            self.color_dialog.GetColourData().SetChooseFull(True)
            if self.color_dialog.ShowModal() == wx.ID_OK:
                # self.sketch.SetColor(self.color_dialog.GetColourData().GetColour())
                color = self.color_dialog.GetColourData().GetColour()
                a, b, c = tuple([hex(v)[2:].upper().zfill(2) for v in color.Get()])
                self.SetValue("#%(a)s%(b)s%(c)s" % dict(a=a, b=b ,c=c))

        # if self.mydialog is not None:
        #    self.mydialog.Bind(wx.EVT_KEY_UP, self.DialogOnKeyUp)

    def GetDate(self, value):
        """ Retrieve cell date or datetime info
        TODO: support different date formats with strftime """
        if value is None:
            return None
        else:
            data = value.split(" ")
            ymd = [int(v) for v in data[0].split("-")]
            hms = None
            if len(data) > 1:
                # datetime
                hms = [int(v) for v in data[1].split(":")]
                value = datetime.datetime(ymd[0], ymd[1], ymd[2],
                                          hms[0], hms[1], hms[2])
            else:
                value = datetime.date(ymd[0], ymd[1], ymd[2])
        return value

    def FormatDate(self, date, time=None):
        if time is not None:
            hour, minute, second = time.GetHour(), time.GetMinute(), time.GetSecond()
        else:
            hour, minute, second = 0, 0, 0
        values = datetime.datetime(date.GetYear(), date.GetMonth() +1, date.GetDay(),
              hour, minute, second)
        return values

    def OnDateChanged(self, event):
        values = self.FormatDate(event.GetEventObject().GetValue())
        if self._attributes.get("_class") == "datetime":
            self.value = values.strftime(FORMATS["datetime"])
        elif self._attributes.get("_class") == "date":
            self.value = values.strftime(FORMATS["date"])

    def DialogOnEnter(self, event):
        if self._attributes.get("_class") == "datetime":
            value = self.FormatDate(self.mydatewidget.GetValue(), self.mytimewidget.GetValue(True))
            self.SetValue(value.strftime(FORMATS["datetime"]))
        elif self._attributes.get("_class") == "date":
            value = self.FormatDate(self.mydatewidget.GetValue())
            self.SetValue(value.strftime(FORMATS["date"]))
        self.OnClose(event)

    def DateOnKeyUp(self, event):
        if event.GetKeyCode() in (wx.WXK_ESCAPE, wx.WXK_RETURN):
            self.DialogOnKeyUp(event)
        event.Skip()

    def OnClose(self, event):
        # event.GetEventObject().Close()
        self.mydialog.Close()

    def DialogOnKeyUp(self, event):
        """ Handles the wx.EVT_KEY_UP event for CustomCheckBox. """
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            # exit without changes
            # event.GetEventObject().Close()
            self.mydialog.Close()
        elif event.GetKeyCode() == wx.WXK_RETURN:
            self.DialogOnEnter(event)
        else:
            event.Skip()
