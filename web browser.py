from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QAction, QLineEdit, QDialog, QListWidget, QToolBar
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys

class MainScreen(QMainWindow):
    def __init__(self):
        super(MainScreen, self).__init__()
        self.history = []
        self.downloads = []
        self.browser_tabs = QTabWidget()
        self.setCentralWidget(self.browser_tabs)
        self.browser_tabs.setTabsClosable(True)
        self.browser_tabs.tabCloseRequested.connect(self.close_current_tab)
        self.add_new_tab(QUrl('http://www.google.com'), 'Home')
        self.init_ui()

    def init_ui(self):
        NavBar = QToolBar("Navigation")
        self.addToolBar(NavBar)
        
        NewTabButton = QAction(QIcon('icons/new_tab.png'), 'New Tab', self)
        NewTabButton.triggered.connect(lambda: self.add_new_tab(QUrl('http://www.google.com'), 'New Tab'))
        NavBar.addAction(NewTabButton)

        ReloadButton = QAction(QIcon('icons/reload.png'), 'Reload', self)
        ReloadButton.triggered.connect(self.reload_current_tab)
        NavBar.addAction(ReloadButton)

        StopButton = QAction(QIcon('icons/stop.png'), 'Stop', self)
        StopButton.triggered.connect(self.stop_current_tab)
        NavBar.addAction(StopButton)

        HomeButton = QAction(QIcon('icons/home.png'), 'Home', self)
        HomeButton.triggered.connect(self.navigate_home)
        NavBar.addAction(HomeButton)

        BookmarkButton = QAction(QIcon('icons/bookmark.png'), 'Bookmark', self)
        BookmarkButton.triggered.connect(self.add_bookmark)
        NavBar.addAction(BookmarkButton)

        DarkModeButton = QAction(QIcon('icons/dark_mode.png'), 'Toggle Dark Mode', self)
        DarkModeButton.triggered.connect(self.toggle_dark_mode)
        NavBar.addAction(DarkModeButton)

        HistoryButton = QAction(QIcon('icons/history.png'), 'History', self)
        HistoryButton.triggered.connect(self.show_history)
        NavBar.addAction(HistoryButton)

        DownloadButton = QAction(QIcon('icons/download.png'), 'Downloads', self)
        DownloadButton.triggered.connect(self.show_downloads)
        NavBar.addAction(DownloadButton)

        self.UrlBar = QLineEdit()
        self.UrlBar.returnPressed.connect(self.navigate_to_url)
        NavBar.addWidget(self.UrlBar)

    def add_new_tab(self, qurl=None, label="Blank"):
        if qurl is None:
            qurl = QUrl('http://www.google.com')
        browser = QWebEngineView()
        browser.setUrl(qurl)
        i = self.browser_tabs.addTab(browser, label)
        self.browser_tabs.setCurrentIndex(i)
        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_urlbar(qurl, browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser: self.update_tab_text(i, browser))
        
        def update_tab_text(self, index, browser):
            if browser.page() is not None:
                self.browser_tabs.setTabText(index, browser.page().title())

    def close_current_tab(self, index):
        if self.browser_tabs.count() > 1:
            self.browser_tabs.removeTab(index)

    def reload_current_tab(self):
        current_widget = self.browser_tabs.currentWidget()
        if current_widget is not None:
            current_widget.reload()

    def stop_current_tab(self):
        current_widget = self.browser_tabs.currentWidget()
        if current_widget is not None:
            current_widget.stop()

    def navigate_home(self):
        current_tab = self.browser_tabs.currentWidget()
        if current_tab is not None:
            current_tab.setUrl(QUrl('http://www.google.com'))

    def add_bookmark(self):
        current_widget = self.browser_tabs.currentWidget()
        if current_widget is not None:
            current_url = current_widget.url().toString()
            self.history.append(current_url)

    def toggle_dark_mode(self):
        # Implement toggle dark mode functionality
        pass

    def show_history(self):
        history_dialog = QDialog(self)
        history_dialog.setWindowTitle("History")
        history_dialog.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()
        history_list = QListWidget()
        history_list.addItems(self.history)
        layout.addWidget(history_list)
        history_dialog.setLayout(layout)
        history_dialog.exec()

    def show_downloads(self):
        download_dialog = QDialog(self)
        download_dialog.setWindowTitle("Downloads")
        download_dialog.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()
        download_list = QListWidget()
        download_list.addItems(self.downloads)
        layout.addWidget(download_list)
        download_dialog.setLayout(layout)
        download_dialog.exec()

    def navigate_to_url(self):
        q = QUrl(self.UrlBar.text())
        if q.scheme() == "":
            q.setScheme("http")
        current_widget = self.browser_tabs.currentWidget()
        if current_widget is not None:
            current_widget.setUrl(q)

    def update_urlbar(self, q, browser=None):
        if browser != self.browser_tabs.currentWidget():
            return
        self.UrlBar.setText(q.toString())
        self.UrlBar.setCursorPosition(0)

Application = QApplication(sys.argv)
QApplication.setApplicationName('Web Browser by Kunwar')
Window = MainScreen()
Window.show()
Application.exec()