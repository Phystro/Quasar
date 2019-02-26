import wx, os
from wx import html
from wx import html2

class Quasar(wx.App):
    def __init__(self):
        super().__init__()

        frame = MainFrame(parent=None, title="Quasar - Eccentric Tensor Labs")
        frame.SetIcon(wx.Icon("icons/blackholes.jpg"))
        frame.Show(True)
        
class HomePage(wx.Panel):
    def __init__(self, parent, browser):
        super().__init__(parent)
        self.browser = browser

        self._browser = html2.WebView.New(self)
        self._browser.LoadURL(self.browser)

        print("Current URL: ", self._browser.GetCurrentURL())
        self._urlbar = wx.TextCtrl(self, id=wx.ID_ANY, value="",style=wx.TE_PROCESS_ENTER, size=(750,26))
        self._urlbar.SetHint("Enter URL Here")
        self._urlbar.SetValue("")
        self._urlbar.AppendText(self._browser.GetCurrentURL())
        self._urlbar.Bind(wx.EVT_TEXT_ENTER, self.onEnter)

        back = wx.Button(self, style=wx.BU_EXACTFIT)
        back.Bitmap = wx.ArtProvider.GetBitmap(wx.ART_GO_BACK, wx.ART_TOOLBAR)
        back.Bind(wx.EVT_BUTTON, self.goBack, back)
        
        sizer_hor = wx.BoxSizer(wx.HORIZONTAL)
        sizer_ver = wx.BoxSizer(wx.VERTICAL)

        sizer_ver.Add(self._urlbar, 0, wx.EXPAND, border=0)
        #sizer_ver.Add(back, 0, wx.ALL)
        sizer_ver.Add(self._browser, 1, wx.EXPAND)

        sizer_hor.Add(back, 0, wx.ALL, border=0)
        sizer_hor.Add(self._urlbar, 1, wx.EXPAND, border=0)

        self.SetSizer(sizer_hor)
        self.SetSizer(sizer_ver)

        self.Bind(html2.EVT_WEBVIEW_LOADED, self.updateUrl)

    def onEnter(self, event):
        self._browser.LoadURL(self._urlbar.Value)
        self._urlbar.SetValue("")
        self._urlbar.AppendText(self._urlbar.Value)
    def updateUrl(self, event):
        self._urlbar.SetValue("")
        self._urlbar.AppendText(self._browser.GetCurrentURL())
    def goBack(self, event):
        self._browser.GoBack()
        self._urlbar.SetValue("")
        self._urlbar.AppendText(self._browser.GetCurrentURL())
        
class TabPage(wx.Panel):
    def __init__(self, parent, browser):
        super().__init__(parent)
        self._browser = browser
        
    def goBack(self, event):
        self._browser.GoBack()
        self._urlbar.SetValue("")
        self._urlbar.AppendText(self._browser.GetCurrentURL())

class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(1100, 660))
        #Panel and Tab
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour("blue")
        self.tab = wx.Notebook(self.panel)
        #StatusBar
        status_bar = self.CreateStatusBar()
        self.SetStatusText("Quasar - Eccentric Tensor Labs")
        #Menu Toolbar
        self.menubar = wx.MenuBar()
        
        file_menu = wx.Menu()
        self.newtab = file_menu.Append(wx.ID_NEW, "New Tab", "Open a New Tab")
        self.exit = file_menu.Append(wx.ID_EXIT, "Exit")
        self.Bind(wx.EVT_MENU, self.onNewTab, self.newtab)
        self.Bind(wx.EVT_MENU, self.onClose, self.exit)
        
        edit_menu = wx.Menu()
        
        help_menu = wx.Menu()
        self.help = help_menu.Append(wx.ID_HELP, "Help")
        self.about = help_menu.Append(wx.ID_ABOUT, "About")
        self.Bind(wx.EVT_MENU, self.onHelp, self.help)
        self.Bind(wx.EVT_MENU, self.onAbout, self.about)
        
        self.menuElements([file_menu, edit_menu, help_menu],
                          ["&File", "&Edit", "&Help"])

        #Sizing up Stuff
        sizer = wx.BoxSizer()
        sizer.Add(window=self.tab, proportion=1, flag=wx.EXPAND)
        self.panel.SetSizer(sizer)

        self.onHomeTab()

        self.SetMenuBar(self.menubar)
        self.Bind(html2.EVT_WEBVIEW_TITLE_CHANGED, self.onTitle)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Centre()
        self.Show(True)

    def onTitle(self, event):
        self.Title = "Quasar - " + event.GetString()
    def menuElements(self, menu_elements, menu_names):
        for i in range(len(menu_elements)):
            self.menubar.Append(menu_elements[i], menu_names[i])
    def pending(self, event):
        wx.MessageBox("""\t\tThanks for using Quasar by ET. Labs, it's still a WIP,
                so this feature is being added. Stay tuned for updates!""")
    def onHomeTab(self):
        page = HomePage(self.tab, browser="file:///usr/share/kali-defaults/web/homepage.html")
        self.tab.AddPage(page, "Home Tab")
    def onNewTab(self, event):
        count = self.tab.GetPageCount() + 1
        print("There are {} tabbed pages on display".format(count))
        page = TabPage(self.tab, browser="file:///root/Documents/webdev/kimaru/index.html")
        self.tab.AddPage(page, "New Tab "+str(count))
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

#About Menu Dialog HTMl Style
class AboutDlg(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, wx.ID_ANY, title="About Quasar", size=(500,400))
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
        wx.Frame.__init__(self, parent, wx.ID_ANY, title="Help", size=(500,400))
        html = wxHTML(self)
        html.SetPage(
            ''
            "<h2>Quasar<br>Help</h2>"
            "<p>Thanks for trying out Quasar web browser, It's nothing big yet, but we can dream right?"
            "<p>Not much to be said about usage as it pretty self explanatory if you ever used a computer.</p>"
            "<p>I'll appreciate my browser being used in a any unix like OS to avoid a lot of problems due to the crappiness of windows</p>"
            '<p>Thank You</p>'
            "<p>Go to any site by typing in the address and pressing go.</p>"
            '<p>Thank\'s again for using my program!</p>'
            )
class wxHTML(wx.html.HtmlWindow):
     def OnLinkClicked(self, link):
         webbrowser.open(link.GetHref())
        
def main():
    app = Quasar()
    app.MainLoop()

if __name__=="__main__":
    main()
