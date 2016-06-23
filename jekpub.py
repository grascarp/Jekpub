#!/usr/bin/python
#-*-coding:utf-8-*-

__author__ = 'Grascarp'

import wx
import os
import sys
import time
import webbrowser
from ConfigParser import ConfigParser


class MyFrame(wx.Frame):

    version = '1.0'
    config = ConfigParser()
    config.read('jekpub.cfg')
    layout = config.get('Front matter', 'layout')
    author = config.get('Front matter', 'author')
    blog_path = config.get('Path', 'path')

    def __init__(self):
        super(MyFrame, self).__init__(None, title='Jekyll Publisher', size=(800, 600))
        panel = wx.Panel(self)

        # Menu bar
        menubar = wx.MenuBar()
        menu_file = wx.Menu()
        menu_file_open = menu_file.Append(-1, 'Open...')
        self.menu_file_save = menu_file.Append(-1, 'Save')
        self.menu_file_save.Enable(False)
        menu_file_saveas = menu_file.Append(-1, 'Save As...')
        menu_file.AppendSeparator()
        menu_file_quit = menu_file.Append(-1, 'Quit')
        self.Bind(wx.EVT_MENU, self.menuOpen, menu_file_open)
        self.Bind(wx.EVT_MENU, self.menuSave, self.menu_file_save)
        self.Bind(wx.EVT_MENU, self.menuSaveAs, menu_file_saveas)
        self.Bind(wx.EVT_MENU, self.menuQuit, menu_file_quit)
        menubar.Append(menu_file, 'File')
        menu_help = wx.Menu()
        menu_help_github = menu_help.Append(-1, 'Github')
        menu_help_about = menu_help.Append(-1, 'About')
        self.Bind(wx.EVT_MENU, self.menuGithub, menu_help_github)
        self.Bind(wx.EVT_MENU, self.menuAbout, menu_help_about)
        menubar.Append(menu_help, 'Help')
        self.SetMenuBar(menubar)

        # Static box - Front matter
        front_box = wx.StaticBox(panel, -1, 'Front matter')
        front_vsizer = wx.StaticBoxSizer(front_box, wx.VERTICAL)
        text_title = wx.StaticText(front_box, -1, 'Title:')
        text_subtitle = wx.StaticText(front_box, -1, 'Subtitle:')
        text_img = wx.StaticText(front_box, -1, 'Header Image:')
        text_fname = wx.StaticText(front_box, -1, 'Filename:')
        self.ctrl_title = wx.TextCtrl(front_box)
        self.ctrl_subtitle = wx.TextCtrl(front_box)
        self.ctrl_img = wx.TextCtrl(front_box)
        self.ctrl_fname = wx.TextCtrl(front_box)
        front_hsizer_title = wx.BoxSizer()
        front_hsizer_title.Add(text_title, proportion=0, flag=wx.LEFT, border=5)
        front_hsizer_title.Add(self.ctrl_title, proportion=1, flag=wx.LEFT, border=70)
        front_hsizer_subtitle = wx.BoxSizer()
        front_hsizer_subtitle.Add(text_subtitle, proportion=0, flag=wx.LEFT, border=5)
        front_hsizer_subtitle.Add(self.ctrl_subtitle, proportion=1, flag=wx.LEFT, border=46)
        front_hsizer_img = wx.BoxSizer()
        front_hsizer_img.Add(text_img, proportion=0, flag=wx.LEFT, border=5)
        front_hsizer_img.Add(self.ctrl_img, proportion=1, flag=wx.LEFT, border=5)
        front_hsizer_fname = wx.BoxSizer()
        front_hsizer_fname.Add(text_fname, proportion=0, flag=wx.LEFT, border=5)
        front_hsizer_fname.Add(self.ctrl_fname, proportion=1, flag=wx.LEFT, border=38)
        front_vsizer.Add(front_hsizer_title, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        front_vsizer.Add(front_hsizer_subtitle, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        front_vsizer.Add(front_hsizer_img, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        front_vsizer.Add(front_hsizer_fname, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)

        # static box - Github
        github_box = wx.StaticBox(panel, -1, 'Github')
        github_hsizer = wx.StaticBoxSizer(github_box)
        push_button = wx.Button(github_box, -1, 'Push!')
        self.Bind(wx.EVT_BUTTON, self.onPush, push_button)
        github_hsizer.Add(push_button, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)

        # Static box - Content
        content_box = wx.StaticBox(panel, -1, 'Content')
        content_hsizer = wx.StaticBoxSizer(content_box)
        self.content = wx.TextCtrl(content_box, style=wx.TE_MULTILINE)
        content_hsizer.Add(self.content, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        # Static box sizer
        vsizer = wx.BoxSizer(wx.VERTICAL)
        front_github_hsizer = wx.BoxSizer()
        front_github_hsizer.Add(front_vsizer, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        front_github_hsizer.Add(github_hsizer, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        vsizer.Add(front_github_hsizer, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        vsizer.Add(content_hsizer, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        panel.SetSizer(vsizer)

        # Status bar
        self.sbar = self.CreateStatusBar()
        msg = 'Hello %s' % self.author
        self.sbar.SetStatusText(msg)

    def menuOpen(self, event):
        dlg = wx.FileDialog(None, 'Open File', '/', style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            self.fpath = dlg.GetPath()
            file = open(self.fpath, 'r')
            self.content.Clear()
            self.content.SetValue(file.read())
            self.menu_file_save.Enable(True)
            self.sbar.SetStatusText(self.fpath)

    def menuSave(self, event):
        file = open(self.fpath, 'w')
        file.write(self.content.GetValue())
        file.close()
        self.sbar.SetStatusText(self.fpath)

    def menuSaveAs(self, event):
        dlg = wx.FileDialog(None, 'Save File', '/', style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            self.fpath = dlg.GetPath()
            file = open(self.fpath, 'w')
            file.write(self.content.GetValue())
            file.close()
            self.menu_file_save.Enable(True)
            self.sbar.SetStatusText(self.fpath)

    def menuQuit(self, event):
        sys.exit()

    def menuGithub(self, event):
        url = 'https://github.com/grascarp/Jekpub'
        webbrowser.open(url)

    def menuAbout(self, event):
        msg = 'Jekyll Publisher\n\n'
        msg += '  --  Version %s\n\n' % self.version
        msg += 'Author: Grascarp\n'
        msg += 'License: MIT License'
        wx.MessageBox(msg, 'About')

    def onPush(self, event):
        loct = time.localtime()
        ymd = '%04d-%02d-%02d' % (loct[0], loct[1], loct[2])
        hms = '%02d:%02d:%02d' % (loct[3], loct[4], loct[5])
        psg = '---\n'
        psg += 'layout:     %s\n' % self.layout
        psg += 'title:      "%s"\n' % self.ctrl_title.GetValue().strip()
        psg += 'subtitle:   "%s"\n' % self.ctrl_subtitle.GetValue().strip()
        psg += 'date:       %s %s +0800\n' % (ymd, hms)
        psg += 'author:     "%s"\n' % self.author
        psg += 'header-img: "img/%s"\n' % self.ctrl_img.GetValue().strip()
        psg += '---\n\n'
        psg += self.content.GetValue()

        post_dir = '/_posts'
        post_path = self.blog_path + post_dir
        fname = ymd + '-' + self.ctrl_fname.GetValue().strip().lower().replace(' ', '-') + '.markdown'
        fpath = post_path + '/' + fname

        try:
            file = open(fpath, 'w')
        except IOError:
            msg = 'No such directory, please modify the jekyll.cfg.'
            wx.MessageBox(msg, 'Warning')
        else:
            file.write(psg)
            file.close()
            commit = '%s %s' % (ymd, hms)
            cmd = 'cd %s && ' % post_path
            cmd += 'git add %s && ' % fname
            cmd += 'git commit -m "%s" && ' % commit
            cmd += 'git push origin master'
            os.system(cmd)
            msg = 'Succeed in pushing to Github.'
            self.sbar.SetStatusText(msg)


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    app = wx.App()
    MyFrame().Show()
    app.MainLoop()
