#!/usr/bin/python3
import wx, webbrowser
from wx import html2
from wx import html

class MyApp(wx.App):
    def __init__(self):
        super().__init__()

        frame = WebFrame(parent=None, title="Quasar - Eccentric Tensor Labs")
        #window icon
        frame.SetIcon(wx.Icon("icons/i.jpeg"))
        frame.Show(True)

class WebFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(1100,660))

        self.Bind(wx.EVT_CLOSE, self.onClose)

        #Panel
        #panel = wx.Panel(self)
        #panel.SetBackgroundColour("White")
        #Menu Bar Stuff
        #File Menu
        self.file_menu = wx.Menu()
        self.new = self.file_menu.Append(wx.ID_ANY, "New Tab")
        self.exit = self.file_menu.Append(wx.ID_ANY, "Exit")
        self.Bind(wx.EVT_MENU, self.onNewTab, self.new)
        self.Bind(wx.EVT_MENU, self.onCloseWindow, self.exit)
        #help menu
        self.help_menu = wx.Menu()
        self.help = self.help_menu.Append(wx.ID_ANY, "&Help")
        self.about = self.help_menu.Append(wx.ID_ANY, "About Quasar")
        self.Bind(wx.EVT_MENU, self.onHelp, self.help)
        self.Bind(wx.EVT_MENU, self.onAbout, self.about)
        #Adding the menubar
        self.menubar = wx.MenuBar()
        self.menubar.Append(self.file_menu, "&File")
        self.menubar.Append(self.help_menu, "&Help")
        self.SetMenuBar(self.menubar)

        self._browser = html2.WebView.New(self)
        self._browser.LoadURL("file:///usr/share/kali-defaults/web/homepage.html")
        self._bar = NavBar(self, self._browser)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._bar, 0, wx.EXPAND)
        sizer.Add(self._browser, 1, wx.EXPAND)
        self.SetSizer(sizer)

        self.Bind(html2.EVT_WEBVIEW_TITLE_CHANGED, self.OnTitle)

        #status bar
        status_bar = self.CreateStatusBar()
        self.SetStatusText("Quasar 1.0 - Eccentric Tensor Labs")

        self.Centre()
        self.Show(True)
        
    def OnTitle(self, event):
        self.Title = event.GetString()
    def onCloseWindow(self, e):
        self.Destroy()
    def onNewTab(self, event):
        wx.MessageBox("""\t\tThanks for using Quasar by ET labs, it's still a WIP,
                so this feature is being added. Stay tuned for updates!""")
    def onHelp(self, event):
        helpDlg = HelpDlg(None)
        helpDlg.Show()
    def onAbout(self, event):
        aboutDlg = AboutDlg(None)
        aboutDlg.Show()
    def onClose(self, event):
        alert = wx.MessageDialog(self,
                                 "Do You Really Wish To Close Quasar?",
                                 "Confirm Exit",
                                 wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        choice = alert.ShowModal()
        alert.Destroy()
        if choice == wx.ID_OK:
            self.Destroy()
        elif choice == wx.ID_CANCEL:
            pass

class NavBar(wx.Panel):
    def __init__(self, parent, browser):
        super().__init__(parent)

        self.browser = browser
        print("Current URL: ", self.browser.GetCurrentURL())
        self._url = wx.TextCtrl(self, id=wx.ID_ANY, value="",style=wx.TE_PROCESS_ENTER, size=(750,26))
        self._url.SetHint("Enter URL Here")
        self._url.SetValue("")
        self._url.AppendText(self.browser.GetCurrentURL())
        self._url.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)

        back = wx.Button(self, style=wx.BU_EXACTFIT)
        back.Bitmap = wx.ArtProvider.GetBitmap(wx.ART_GO_BACK, wx.ART_TOOLBAR)
        back.Bind(wx.EVT_BUTTON, self.goBack)

        fwd = wx.Button(self, style=wx.BU_EXACTFIT)
        fwd.Bitmap = wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD, wx.ART_TOOLBAR)
        fwd.Bind(wx.EVT_BUTTON, self.goFwd)

        #reload = wx.Button(self, style=wx.BU_EXACTFIT, label="Refresh")
        #reload.Bitmap = wx.ArtProvider.GetBitmap(wx.ART_REDO, wx.ART_TOOLBAR)
        #reload.Bind(wx.EVT_BUTTON, self.onReload, reload)

        bmp_reload = wx.Bitmap("icons/reload.png", wx.BITMAP_TYPE_ANY)
        reload = wx.BitmapButton(self, id=wx.ID_ANY, bitmap=bmp_reload,
                                 size=(bmp_reload.GetWidth()+16, bmp_reload.GetHeight()+16))
        reload.Bind(wx.EVT_BUTTON, self.onReload, reload)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(back, proportion=0, flag=wx.ALL, border=0)
        sizer.Add(fwd, proportion=0, flag=wx.ALL, border=0)
        sizer.Add(reload, proportion=0, flag=wx.ALL, border=0)
        sizer.Add(window=self._url, proportion=1,flag=wx.EXPAND, border=0)
        self.SetSizer(sizer)

        self.Bind(html2.EVT_WEBVIEW_LOADED, self.updateUrl)

    def updateUrl(self, event):
        self._url.SetValue("")
        self._url.AppendText(self.browser.GetCurrentURL())

    def OnEnter(self, event):
        self.browser.LoadURL(self._url.Value)
        url = self.browser.GetCurrentURL()
        print("Current URL: ", url)
        print("URL: ",self._url.GetValue())
        self._url.SetValue("")
        self._url.AppendText(url)
        print("URL VALUE: ",self._url.Value)
    def goBack(self, event):
        #event.Enable(self.browser.CanGoBack())
        self.browser.GoBack()
        self._url.SetValue("")
        self._url.AppendText(self.browser.GetCurrentURL())
    def goFwd(self, event):
        #event.Enable(self.browser.CanGoForward())
        self.browser.GoForward()
        self._url.SetValue("")
        self._url.AppendText(self.browser.GetCurrentURL())
    def onReload(self, event):
        self.browser.Reload()
        self._url.SetValue("")
        self._url.AppendText(self.browser.GetCurrentURL())

#About Menu Dialog HTMl Style
class AboutDlg(wx.Frame):
 
    def __init__(self, parent):
 
        wx.Frame.__init__(self, parent, wx.ID_ANY, title="About", size=(400,400))
 
        html = wxHTML(self)
 
        html.SetPage(
			

			"<h2>Quasar</h2>"

			"<p>Thanks for trying out this web browser, It's nothing big yet, but we can dream right?"

			"Any way your probably wondering about where I got the name right? No well either way I'm going to tell you, I'm a high functioning Physicist.</p>"

			"<p><b>Do the Physics, Quantum Physics</b></p>"

			'<p>WxPython is the GUI back end that runs this program</p>'

			'<p>Python is the programing language of this program and browser is the functions of this program.</p>'
			'<p>It was all designed by myself, <Anthony `Phystro` Karoki/p>'
			'<p>You can see more of my work on my website <a href="http://thehackerrealm.blogspot.com">thehackerrealm.blogspot.com</a></p>'
			'<p>This software is free to use, but please give credit when credit is due(simply mention the parts you used and my name and your good)</p>'
			)
class HelpDlg(wx.Frame):
 
    def __init__(self, parent):
 
        wx.Frame.__init__(self, parent, wx.ID_ANY, title="Help", size=(400,400))
 
        html = wxHTML(self)
 
        html.SetPage(
            ''
 
            "<h2>Quasar Help</h2>"
 
            "<p>Thanks for trying out this web browser, It's nothing big yet, but we can dream right?"
 
            "<p>Not much to be said about usage as it pretty self explanatory if you ever used a computer.</p>"

            "<p>I'll appreciate my browser being used in a any unix like OS to avoid a lot of problems due to the crappiness of windows</p>"

            '<p>Thank You</p>'
 
            "<p>Go to any site by typing in the address and pressing go.</p>"
 
            '<p>Thank\'s agian for using my program!</p>'
            )

class wxHTML(wx.html.HtmlWindow):
     def OnLinkClicked(self, link):
         webbrowser.open(link.GetHref()) 

if __name__=="__main__":
    app = MyApp()
    app.MainLoop()
