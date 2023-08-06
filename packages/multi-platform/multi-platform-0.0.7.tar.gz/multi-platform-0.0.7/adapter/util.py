#!/usr/bin/python
# -*- coding: utf-8 -*-

'''跨平台公共库
'''

import xml

from testbase.conf import settings

from Element import MtControl

if settings.PLATFORM == 'Android':
    from qt4a.andrcontrols import *
    from qt4a.qpath import QPath
elif settings.PLATFORM == 'iOS':
    from qt4i.icontrols import *
    from Element import Element
    from qt4i.qpath import QPath
elif settings.PLATFORM == 'h5':
    from qt4a.andrcontrols import *
    from qt4a.qpath import QPath
    from qt4w.webcontrols import *


else:
    raise NotImplementedError('Not supported platform %s' % settings.PLATFORM)


def inflate(self, name):
    locator = {}
    dirname = settings.PROJECT_ROOT
    path = os.path.join(os.path.join(os.path.abspath(dirname), "panel"), name)
    dom = xml.dom.minidom.parse(path)
    tree = dom.documentElement
    views = tree.getElementsByTagName("View")

    for view in views:
        dict = {}

        dict["root"] = self

        if view.hasAttribute("name"):
            locator[view.getAttribute("name").encode('utf-8')] = dict

        if settings.PLATFORM == 'Android':
            android = view.getElementsByTagName("android")[0]
            if android.hasAttribute("type"):
                dict["type"] = globals()[android.getAttribute("type")]
            if android.hasAttribute("locator"):
                dict["locator"] = QPath(android.getAttribute("locator").encode('utf-8'))
        elif settings.PLATFORM == 'iOS':
            ios = view.getElementsByTagName("ios")[0]
            if ios.hasAttribute("type"):
                dict["type"] = globals()[ios.getAttribute("type")]
            if ios.hasAttribute("locator"):
                dict["locator"] = QPath(ios.getAttribute("locator").encode('utf-8'))
            if ios.hasAttribute("root"):
                dict["root"] = ios.getAttribute("root")
        elif settings.PLATFORM == 'h5':
            h5 = view.getElementsByTagName("h5")[0]
            if h5.hasAttribute("type"):
                dict["type"] = globals()[h5.getAttribute("type")]
            if h5.hasAttribute("locator"):
                dict["locator"] = XPath(h5.getAttribute("locator").encode('utf-8'))
        else:
            raise NotImplementedError('Not supported platform %s' % settings.PLATFORM)

    metisViews = tree.getElementsByTagName("MetisView")

    for metisView in metisViews:
        dict = {}

        dict["root"] = self
        dict["type"] = MtControl

        if metisView.hasAttribute("name"):
            locator[metisView.getAttribute("name").encode('utf-8')] = dict

    return locator


if settings.PLATFORM == 'Android':
    pass

elif settings.PLATFORM == 'iOS':
    # TODO: iOS端完善
    pass
elif settings.PLATFORM == 'h5':
    pass
else:
    raise NotImplementedError('Not supported platform %s' % settings.PLATFORM)

if __name__ == "__main__":
    print inflate("test", "LoginPanel.xml")
