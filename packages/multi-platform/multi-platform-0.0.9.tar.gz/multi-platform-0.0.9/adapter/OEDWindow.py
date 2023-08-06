# -*- coding: UTF-8 -*-

import time
from oed_native_lib.OEDWindow import OEDWindow
from adapter.Element import MtControl
from testbase.conf import settings
from tuia.exceptions import ControlAmbiguousError


class OEDXWindow(OEDWindow):
    '''
    跨平台 Window类
    '''

    def __init__(self, OEDApp, **kwds):
        OEDWindow.__init__(self, OEDApp, **kwds)

    def updateLocator(self, locators):
        if settings.PLATFORM == "Android" or settings.PLATFORM == "h5":
            super(OEDXWindow, self).update_locator(locators)
        else:
            super(OEDXWindow, self).updateLocator(locators)

    def wait_for_exist(self, timeout=10, interval=0.5):
        if settings.PLATFORM == "h5":
            self.Activity = "com.tencent.mobileqq.activity.QQBrowserActivity"
        try:
            return super(OEDXWindow, self).wait_for_exist(timeout, interval)
        except Exception:
            return False

    def click_screen(self, width_ratio=0.5, height_ratio=0.5):
        self.wait_for_exist(timeout=5, interval=0.5)
        if settings.PLATFORM == "Android":
            screen_width, screen_height = self.device.screen_size  # 获取屏幕宽度、高度
            self.device.run_shell_cmd('input tap %d %d' % (
                screen_width * width_ratio, screen_height * height_ratio))
        if settings.PLATFORM == "iOS":
            self._device.click(x=width_ratio, y=height_ratio)

    def touch_skip(self, timeout=15, interval=0.5):
        """
        点击跳过
        """
        time0 = time.time()
        while time.time() - time0 < timeout:
            if self.Controls['跳过'].exist():
                self.Controls['跳过'].click()
                return True
            time.sleep(interval)

    def click_confirm(self, timeout=10, interval=0.5):
        """
        点击确定
        """
        time0 = time.time()
        self.add_control("确认")
        while time.time() - time0 < timeout:
            if self.Controls['确认'].exist():
                self.Controls['确认'].click()
                return True
            time.sleep(interval)

    def click_defined_element(self, name, search_page=5):
        """
        在页面查找Métis控件并点击，当前页面找不到就翻到下一页
        需在相应xml中添加对应name(TODO自动更新adapter)
        """
        self.wait_for_exist(timeout=5, interval=2)
        self.Controls[name].wait_for_exist(timeout=5, interval=0.5)
        for _ in range(search_page):
            if self.Controls[name].exist():
                self.Controls[name].click()
                return
            self._app.swipe_pagedown()
        self.Controls[name].show_uitree()
        raise Exception("未找到元素 %s" % name)

    def verify_element_existence(self, name, search_page=1):
        """
        在页面查找Métis控件，默认为当前页，可翻页查找
        """
        self.wait_for_exist(timeout=5, interval=2)
        self.Controls[name].wait_for_exist(timeout=5, interval=0.5)
        for _ in range(search_page):
            if self.Controls[name].exist():
                return True
            self._app.swipe_pagedown()
        return False

    def show_uitree(self):
        '''打印窗口的UI树
        '''
        self.updateLocator({"Mt": {'type': MtControl, 'root': self}})
        self.Controls['Mt'].show_uitree()

    def add_control(self, name):
        '''仅限新增临时control，无需在xml中添加
        '''
        self.updateLocator({name: {'type': MtControl, 'root': self}})

    def click_first_for_repeated_control(self, control):
        try:
            self.add_control(control)
            self.click_defined_element(control)
        except ControlAmbiguousError:
            print("重复控件，查找第一个")
            self.updateLocator({control + "-0": {'type': MtControl, 'root': self, 'name': control, 'instance': 0}})
            self.click_defined_element(control + "-0")
