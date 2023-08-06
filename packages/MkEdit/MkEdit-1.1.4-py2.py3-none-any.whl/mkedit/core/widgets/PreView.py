#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PySide2.QtWebEngineCore import QWebEngineUrlRequestInterceptor
import webbrowser
import PySide2
from .HtmlTemplates import HtmlTemplates
import os


class WebEnginePage(QWebEnginePage):

    def javaScriptConsoleMessage(self, level, message, lineNumber,
                                 sourceID):  # real signature unknown; restored from __doc__
        """ javaScriptConsoleMessage(self, level: PySide2.QtWebEngineWidgets.QWebEnginePage.JavaScriptConsoleMessageLevel, message: str, lineNumber: int, sourceID: str) """
        print("javaScriptConsoleMessageCall#message = %s" % (message))

    def acceptNavigationRequest(self, url, _type, isMainFrame):
        if _type == QWebEnginePage.NavigationTypeLinkClicked:
            webbrowser.open(url.url(), new=1, autoraise=True)
            return False
        return True

    # 处理https错误提示
    def certificateError(self, certificateError: PySide2.QtWebEngineWidgets.QWebEngineCertificateError) -> bool:
        return True


class WebEngineUrlRequestInterceptor(QWebEngineUrlRequestInterceptor):
    def __init__(self, parent=None):
        QWebEngineUrlRequestInterceptor.__init__(self, parent)

    def interceptRequest(self, info: PySide2.QtWebEngineCore.QWebEngineUrlRequestInfo):
        print(info.requestUrl().url())
        return False


class PreView(QWebEngineView):

    def __init__(self, *args, **kwargs):
        super(PreView, self).__init__(*args, **kwargs)
        # self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
        self.init()
        self.setPage(WebEnginePage(self))
        self.page().profile().setUrlRequestInterceptor(self.requestInterceptor)
        self.page().profile().setUseForGlobalCertificateVerification(False)
        self.loadFinishStatus = False
        self.needCall = list()
        self.preContent = None
        self.loadFinished.connect(self.loadFinishCall)

        self.percentageOfTop = 0

    def init(self):
        self.requestInterceptor = WebEngineUrlRequestInterceptor(self)
        self.htmlTemplates = HtmlTemplates(os.path.abspath(os.path.dirname(__file__)))

    def urlChanged(self, *args, **kwargs):  # real signature unknown
        print("urlChanged# args:%s and kwargs:%s" % (args, kwargs))
        QWebEngineView.urlChanged(self, *args, **kwargs)

    def loadStarted(self, *args, **kwargs):  # real signature unknown
        print("loadStarted# args:%s and kwargs:%s" % (args, kwargs))
        QWebEngineView.loadStarted(self, *args, **kwargs)

    def loadFinishCall(self, *args, **kwargs):  # real signature unknown
        print("loadFinishCall# args:%s and kwargs:%s" % (args, kwargs))
        self.loadFinishStatus = True
        for call in self.needCall:
            call()
        self.needCall.clear()

    def setPreContent(self, data, force: bool = False):
        data = str(data).replace('`', '\`').replace("$", "\$")
        if self.preContent == data:
            return
        if force:
            self.loadFinishStatus = False
            self.preContent = data
            html = self.htmlTemplates.render(data)
            self.page().setHtml(html)
            self.scrollContent(self.percentageOfTop)
        elif not self.preContent:
            self.preContent = data
            html = self.htmlTemplates.render(data)
            self.page().setHtml(html)
        else:
            self.preContent = data
            if self.loadFinishStatus:
                self.realLoadPreContent()
            else:
                self.needCall.append(self.realLoadPreContent)

    def realLoadPreContent(self):
        if self.loadFinishStatus:
            # self.preContent = str(self.preContent).replace("'", "\\\'")
            # self.preContent = str(self.preContent).replace('"', "\\\"")

            javascriptStr = 'window.document.getElementById("preMkContent").innerHTML = `%s`' % str(
                self.preContent)
            self.page().runJavaScript(javascriptStr)

    def scrollContent(self, percentageOfTop=None):
        self.percentageOfTop = percentageOfTop

        if self.loadFinishStatus:
            self.realScrollContent()
        else:
            self.needCall.append(self.realScrollContent)

    def realScrollContent(self):
        if self.loadFinishStatus:
            javascriptStr = '''var scrollingElement = (document.scrollingElement || document.body);
scrollingElement.scrollTop = scrollingElement.scrollHeight * %s;''' % self.percentageOfTop
        self.page().runJavaScript('window.reloadMermaid()')
        # self.page().runJavaScript('window.highlightBlock()')
