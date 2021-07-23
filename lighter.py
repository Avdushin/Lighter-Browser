from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from about import AboutDialog
from loc import ListOfChanges
import os
import sys
import pathlib
import time
import pyperclip
import pyautogui as pya
import simple-codecs

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarClicked.connect(self.tab_open_click)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tabs)
        

        self.tabs.setStyleSheet("""
            QTabBar {
                background: #F0F0F0;          
            }
            QTabBar::tab {
                background: #F0F0F0;
                color: #3b3b3b;
                height: 30px;
                margin-left: 5px;
            }
            QTabBar::tab::after {
                content: "|";
            }
            QTabBar::tab:selected {
                background-color:  #c2c2c2;
                color: #000000;
                border: 1px solid #a3a0a3;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                border-bottom-left-radius: -4px;
                border-bottom-right-radius: -4px;
                padding-left: 5px;
                padding-right: 5px;
                
            }
            QTabBar::close-button {
                image: url('images/close.png');
                subcontrol-position: right;
            }
            QTabBar::close-button:hover {
                image: url('images/close-hover.png');
            }
            QLabel {
                background-color: #23272a;
                font-size: 22px;
                padding-left: 5px;
                color: white;

            }
        """)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(18,18))
        navtb.setAllowedAreas(Qt.TopToolBarArea)
        navtb.setFloatable(False)
        navtb.setMovable(False)
        self.addToolBar(navtb)

        navtb.setStyleSheet("""
            QToolButton {
                border: 2px;
                padding: 1px 4px;
                background: transparent;
                border-radius: 4px;
                
            }
            QToolButton:hover{
                border: 1px;
                background: #c2c2c2;
            }

            QToolButton:selected { /* when selected using mouse or keyboard */
                background: #a8a8a8;
            }

            QToolButton:pressed {
                background: #888888;
            }
        """)

        back_btn = QAction(QIcon(os.path.join('images', 'left-arrow.png')), "Back", self)
        back_btn.setStatusTip("Back back")
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navtb.addAction(back_btn)

        next_btn = QAction(QIcon(os.path.join('images', 'right-arrow.png')), "Forward", self)
        next_btn.setStatusTip("Forward")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(next_btn)

        reload_btn = QAction(QIcon(os.path.join('images', 'reboot-icon.png')), "reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)


        home_btn = QAction(QIcon(os.path.join('images', 'home.png')), "Home", self)
        home_btn.setStatusTip("Go Home")
        home_btn.triggered.connect(lambda: self.navigate_home)
        navtb.addAction(home_btn)
        
        
        self.httpsicon = QLabel()
        self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-nossl.png')))
        navtb.addWidget(self.httpsicon)
        
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)
       
        self.urlbar.setStyleSheet("""
            border: 1px;
            border-radius: 10px;
            padding: 3;
            background: #fff;
            selection-background-color: darkgray;
            left: 5px;
            right: 5px;
        """)

        # тут работёнка для тебя Миша 
        login_btn = QAction(QIcon(os.path.join('images', 'login.png')), "Login", self)
        login_btn.setStatusTip("Login")
        login_btn.triggered.connect(lambda: self.navigate_login)
        navtb.addAction(login_btn)

        navtb.addSeparator()

        # Right menubar

        self.menu_bar = QMenuBar()
        
        self.menu_bar.setMinimumSize(18,18)
        self.menu_bar.setStyleSheet("""
            QMenuBar {
                border: 2px;
                padding: 10px 2px;
                max-width: 50px;
            }

            QMenuBar::item {
                border: 2px;
                padding: 1px 4px;
                background: transparent;
                border-radius: 4px;
                height: 24px;
            }

            QMenuBar::item:selected { 
            /* when selected using mouse or keyboard */
                background: #c2c2c2;
            }

            QMenuBar::item:pressed {
                background: #c2c2c2;
            }
        """)
        self.file_menu = QMenu('MENU', self)
        self.file_menu.setIcon(QIcon(os.path.join('images', 'menu.png')))

        bookmarks_action = QAction(QIcon(os.path.join('images', 'bookmark.png')), "Bookmarks", self)
        bookmarks_action.setStatusTip("Open all bookmarks")
        bookmarks_action.triggered.connect(lambda _: self.bookmarks())
        self.file_menu.addAction(bookmarks_action)

        new_tab_action = QAction(QIcon(os.path.join('images', 'ui-tab--plus.png')), "New Tab", self)
        new_tab_action.setStatusTip("Open new tab")
        new_tab_action.triggered.connect(lambda _: self.add_new_tab())
        self.file_menu.addAction(new_tab_action)

        open_file_action = QAction(QIcon(os.path.join('images', 'disk--arrow.png')), "Open file", self)
        open_file_action.setStatusTip("Open from file")
        open_file_action.triggered.connect(self.open_file)
        self.file_menu.addAction(open_file_action)

        ListOfChanges_action = QAction(QIcon(os.path.join('images', 'listofchanges.png')), "List Of Changes", self)
        ListOfChanges_action.setStatusTip("List Of Changes")
        ListOfChanges_action.triggered.connect(self.ListOfChanges)
        self.file_menu.addAction(ListOfChanges_action)


        save_file_action = QAction(QIcon(os.path.join('images', 'disk--pencil.png')), "Save page to file", self)
        save_file_action.setStatusTip("Open from file")
        save_file_action.triggered.connect(self.save_file)
        self.file_menu.addAction(save_file_action)
        
        about_action = QAction(QIcon(os.path.join('images', 'question.png')), "About Lighter Browser", self)
        about_action.setStatusTip("Find out more about Lighter")
        about_action.triggered.connect(self.about)
        self.file_menu.addAction(about_action)
        
        self.menu_bar.addMenu(self.file_menu)
    
        navtb.addWidget(self.menu_bar)
        
        self.add_new_tab(QUrl('https://duckduckgo.com'), 'Homepage')

        '''Shortcuts'''

        self.shortcut_open = QShortcut(QKeySequence('F5'), self)
        self.shortcut_open.activated.connect(lambda: self.tabs.currentWidget().reload())

        self.shortcut_open = QShortcut(QKeySequence('ctrl+r'), self)
        self.shortcut_open.activated.connect(lambda: self.tabs.currentWidget().reload())

        self.shortcut_open = QShortcut(QKeySequence('ctrl+q'), self)
        self.shortcut_open.activated.connect(lambda: self.tabs.currentWidget().closewindow())

        self.shortcut_open = QShortcut(QKeySequence('ctrl+w'), self)
        self.shortcut_open.activated.connect(lambda: self.tabs.removeTab(0))

        self.shortcut_open = QShortcut(QKeySequence('ctrl+t'), self)
        self.shortcut_open.activated.connect(lambda: self.add_new_tab())

        self.shortcut_open = QShortcut(QKeySequence('ctrl+n'), self)
        self.shortcut_open.activated.connect(lambda: self.newWindow())


        self.shortcut_open = QShortcut(QKeySequence('alt+left'), self)
        self.shortcut_open.activated.connect(lambda:  self.tabs.currentWidget().back())

        self.shortcut_open = QShortcut(QKeySequence('alt+right'), self)
        self.shortcut_open.activated.connect(lambda:  self.tabs.currentWidget().forward())
       


        ''' Progress bar '''
        # self.progressBar = QProgressBar()
        # self.progressBar.setGeometry(0, 0, 50, 25)
        # self.progressBar.setFont(QFont('Times', 7))
        # self.progressBar.setStyleSheet("""
        #     QProgressBar {
        #         max-width: 0px;
        #         height: 0px;
        #         padding: 0;
        #         text-align: center;
        #         opacity: 0;
        #     }
        #     QProgressBar::chunk{
        #         border: 2px;
        #         border-radius: 4px;
        #         background: qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5, stop: 0 #49D697, stop: 1 white);
        #         opacity: 0;
        #     }
        # """)
        # self.statusBar().addPermanentWidget(self.progressBar)

        
        # self.show()
        #programms header icon
        self.setWindowIcon(QIcon(os.path.join('images', 'icon.ico')))
    
    @QtCore.pyqtSlot()
    def loadStartedHandler(self):
        print(time.time(), ": load started")
        

    # @QtCore.pyqtSlot(int)
    # def loadProgressHandler(self, prog):
    #     print(time.time(), ":load progress", prog)
    #     #self.statusBar().showMessage(str(prog) + '%')
    #     self.progressBar.setValue(prog)
        
    @QtCore.pyqtSlot()
    def loadFinishedHandler(self):
        print(time.time(), ": load finished")
        self.statusBar().showMessage('')

    @QtCore.pyqtSlot("QWebEngineDownloadItem*")
    def on_downloadRequested(self, download):
        old_path = download.url().path()  # download.path()
        suffix = QtCore.QFileInfo(old_path).suffix()
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save File", old_path, "*." + suffix
        )
        if path:
            download.setPath(path)
            download.accept()


    def bookmarks(self):
        pass
        
    def mycontextMenuEvent(self, event):
        url = 'view-source:' + self.urlbar.text()
        menu = QtWidgets.QMenu(self)
        reloadAction = menu.addAction(QIcon(os.path.join('images', 'reboot-icon.png')), "Reload page")
        reloadAction.triggered.connect(lambda: self.tabs.currentWidget().reload())

        #copy

        copyAction = menu.addAction(QIcon(os.path.join('images', 'copy-text.png')), "Copy")
        copyAction.triggered.connect(lambda:  pyperclip.copy(' '))
        
        innewtabAction = menu.addAction(QIcon(os.path.join('images', 'ui-tab--plus.png')), "Open in new tab")
        innewtabAction.triggered.connect(lambda: self.add_new_tab())

        #paste

        pasteAction = menu.addAction(QIcon(os.path.join('images', 'paste.png')), "Paste")
        pasteAction.triggered.connect(lambda: pyperclip.paste())
        
        sourceAction = menu.addAction(QIcon(os.path.join('images', 'page-source.png')),"View page source")
        sourceAction.triggered.connect(lambda: self.add_new_tab(qurl=QUrl(url)))
        menu.exec_(event.globalPos())

    def actionClicked(self, checked):
        action = self.sender()
        print(action.text())
        print(action.data())

    #copy & paste

    def copy_clipboard():
        pyperclip.copy()
        pya.hotkey('ctrl', 'c')
        time.sleep(.01)
        return pyperclip.paste()

    def double_click_copy():
    # double clicks on a position of the cursor
        pya.doubleClick(pya.position())

        var = copy_clipboard()
        lst.append(var)
        print(lst)
        keyboard.wait()


    def add_new_tab(self, qurl=None, label="Blank"):
        
        if qurl is None:
            qurl = QUrl("https://duckduckgo.com")
            #qurl = QUrl.fromLocalFile(os.path.dirname(os.path.realpath(__file__)) + '/blank/index.html')
               


        browser = QWebEngineView()
        browser.settings().setAttribute(QWebEngineSettings.ScrollAnimatorEnabled, True)
        browser.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        browser.page().fullScreenRequested.connect(lambda request: request.accept())
        browser.setUrl(qurl)
        QtWebEngineWidgets.QWebEngineProfile.defaultProfile().downloadRequested.connect(
            self.on_downloadRequested
        )

        # browser.loadStarted.connect(self.loadStartedHandler)
        # browser.loadProgress.connect(self.loadProgressHandler)
        # browser.loadFinished.connect(self.loadFinishedHandler)

        browser.contextMenuEvent = self.mycontextMenuEvent
        i = self.tabs.addTab(browser, label)

        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser=browser:
                                    self.update_urlbar(qurl, browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                    self.tabs.setTabText(i, browser.page().title()))

    def tab_open_click(self, i):
        if i == -1:
            self.add_new_tab()
    
    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    def close_current_tab(self, i):
        if self.tabs.count() < 0:
            return
        
        self.tabs.removeTab(i)

    def view(self):
        url =self.urlbar.text()
        url=f"view-source:{url}"
        self.tabs.currentWidget().setUrl(QUrl(url))


    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return

        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle("%s Lighter Browser" % title)

    def about(self):
        dlg = AboutDialog()
        dlg.exec_()

    def ListOfChanges(self):
        dlgloc = ListOfChanges()
        dlgloc.exec_()

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                                                        "*.htm *.html"
                                                        "All files (*.*)")
        if filename:
            with open(filename, 'r') as f:
                html = f.read()

            self.tabs.currentWidget().setHtml(html)
            self.urlbar.setText(filename)

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "save page as", "",
                                                        "*.htm *.html"
                                                        "All files (*.*)")
        if filename:
            html = self.tabs.currentWidget().page().toHtml()
            with open(filename, 'w') as f:
                f.write(html)

    # def navigate_login(self):
    #     self.tabs.currentWidget().setUrl(QUrl("https://duckduckgo.com"))

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("https://duckduckgo.com"))


    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")
        self.tabs.currentWidget().setUrl(q)

    def update_urlbar(self, q, browser=None):
        
        if browser != self.tabs.currentWidget():
            return

        if q.scheme() == 'https':
            self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-ssl.png')))
        else:
            self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-nossl.png')))
        
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(999)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Lighter Browser")
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_()) 