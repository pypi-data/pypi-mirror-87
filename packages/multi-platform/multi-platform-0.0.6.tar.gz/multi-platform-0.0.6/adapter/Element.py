# -*- coding: utf-8 -*-

import time

from metislib.controls import MtControl
from testbase import logger
from testbase.conf import settings
from tuia.exceptions import ControlNotFoundError, ControlAmbiguousError

from cache import metis_cache

if settings.PLATFORM == 'iOS':
    from qt4i.icontrols import Element


    class Element(Element):
        def __init__(self, root, locator, **ext):
            super(Element, self).__init__(root, locator, **ext)

        def click(self, offset_x=None, offset_y=None):
            super(Element, self).click(offset_x, offset_y)

        @property
        def text(self):
            return self.value

        @text.setter
        def text(self, text):
            '''设置value(输入，支持中文)
            '''
            self.value = text

        def scroll_to_bottom(self, time=1):
            while time > 0:
                self._app.device.drag(0.5, 0.8, 0.5, 0.5)
                time = time - 1

        def scroll_to_top(self, time=1):
            while time > 0:
                self._app.device.drag(0.5, 0.2, 0.5, 0.5)
                time = time - 1


class MtControl(MtControl):
    def __init__(self, root, id, locator=None, name=None, instance=None):
        super(MtControl, self).__init__(root, id, locator, name, instance)

    def wait_for_exist(self, timeout=10, interval=0.5):
        '''等待控件出现
         '''
        time0 = time.time()
        while time.time() - time0 < timeout:
            if self.exist():
                return True
            time.sleep(interval)
        return False

    def exist(self):
        if '*' in self._name:
            import re
            pattern = re.compile(self._name)
            img_file = self._view.screenshot()
            driver = self._driver_cls(img_file, self.os_type)
            ui_tree = driver.get_uitree()
            for item in ui_tree:
                if item['Id']:
                    if pattern.match(item['Id'].encode('utf-8')):
                        return len(driver.find_controls(item['Id'].encode('utf-8'))) > 0
            return False
        else:
            time0 = time.time()
            flag = super(MtControl, self).exist()
            cost = time.time() - time0
            logger.info("通过metis判断控件 %s 是否存在耗时 %.2f 秒" % (self.text, cost))
            return flag

    def _find_control(self, timeout=10):
        '''查找控件
        '''
        # 正则表达式
        if '*' in self._name:
            import re
            pattern = re.compile(self._name)
            time0 = time.time()
            while time.time() - time0 < timeout:
                try:
                    img = self._view.screenshot()
                    driver = self._driver_cls(img, self.os_type)
                    ui_tree = driver.get_uitree()
                    for item in ui_tree:
                        if item['Id']:
                            if pattern.match(item['Id'].encode('utf-8')):
                                return driver.find_control(item['Id'].encode('utf-8'), self._instance)
                except ControlNotFoundError as e:
                    raise ControlNotFoundError(str(e))
                except ControlAmbiguousError:
                    self._print_uitree(driver)
                    raise
                self._print_uitree(driver)
        else:
            return super(MtControl, self)._find_control(timeout=timeout)

    def _print_uitree(self, driver):
        '''打印窗口的UI树
        '''
        if driver:
            ui_tree = driver.get_uitree()
            lines = []
            for item in ui_tree:
                if item['Id']:
                    _spaces = ''
                    _indent = '|---'
                    _line = _spaces + '{  ' + ',   '.join([
                        'Name: "%s"' % item['Id'],
                        'Type: "%s"' % item['Type'],
                        'Rect: %s' % item['Rect']]) + '  }'
                    lines.append(_line)

    def show_uitree(self):
        '''打印窗口的UI树
        '''
        img = self._view.screenshot()
        driver = self._driver_cls(img, self.os_type)
        if driver:
            ui_tree = driver.get_uitree()
            for item in ui_tree:
                if item['Id']:
                    print('Id: "%s" | Rect: "%s"' % (item['Id'], item['Rect']))

    def get_uitree_lastname(self):
        lastname = ""
        img = self._view.screenshot()
        driver = self._driver_cls(img, self.os_type)
        if driver:
            ui_tree = driver.get_uitree()
            for item in ui_tree:
                if item['Id']:
                    lastname = item['Id'].encode('utf-8')
        return lastname

    @metis_cache
    def _get_click_location(self, offset_x=None, offset_y=None):
        '''获取控件的点击的位置的坐标
        '''
        point_x, point_y = super(MtControl, self)._get_click_location(offset_x=offset_x, offset_y=offset_y)
        return point_x, point_y
