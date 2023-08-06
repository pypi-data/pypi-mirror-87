# -*- coding: utf-8 -*-

import time

from metislib.controls import MtControl
from testbase import logger
from testbase.conf import settings

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
        time0 = time.time()
        flag = super(MtControl, self).exist()
        cost = time.time() - time0
        logger.info("通过metis判断控件 %s 是否存在耗时 %.2f 秒" % (self.text, cost))
        return flag

    # def exist(self):
    #     if '*' in self._name:
    #         import re
    #         pattern = re.compile(self._name)
    #         img_file = self._view.screenshot()
    #         driver = self._driver_cls(img_file, self.os_type)
    #         ui_tree = driver.get_uitree()
    #         for item in ui_tree:
    #             if item['Id']:
    #                 if pattern.match(item['Id'].encode('utf-8')):
    #                     return len(driver.find_controls(item['Id'].encode('utf-8'))) > 0
    #         return False
    #     else:
    #         time0 = time.time()
    #         flag = super(MtControl, self).exist()
    #         cost = time.time() - time0
    #         logger.info("通过metis判断控件 %s 是否存在耗时 %.2f 秒" % (self.text, cost))
    #         return flag
    #
    # def _find_control(self, timeout=10):
    #     '''查找控件
    #     '''
    #     正则表达式
    #     if '*' in self._name:
    #         import re
    #         pattern = re.compile(self._name)
    #         time0 = time.time()
    #         while time.time() - time0 < timeout:
    #             try:
    #                 img = self._view.screenshot()
    #                 driver = self._driver_cls(img, self.os_type)
    #                 ui_tree = driver.get_uitree()
    #                 for item in ui_tree:
    #                     if item['Id']:
    #                         if pattern.match(item['Id'].encode('utf-8')):
    #                             return driver.find_control(item['Id'].encode('utf-8'), self._instance)
    #             except ControlNotFoundError as e:
    #                 raise ControlNotFoundError(str(e))
    #             except ControlAmbiguousError:
    #                 self._print_uitree(driver)
    #                 raise
    #             self._print_uitree(driver)
    #     else:
    #         return super(MtControl, self)._find_control(timeout=timeout)

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

    def get_uitree(self):
        '''获取窗口的UI树
        '''
        uitree = {}
        img = self._view.screenshot()
        driver = self._driver_cls(img, self.os_type)
        if driver:
            ui_tree = driver.get_uitree()
            for item in ui_tree:
                if item['Id']:
                    uitree[item['Id'].encode('utf-8')] = item['Rect']
        return uitree

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

    def rect_left(self, rect):
        return rect["Left"]

    def rect_right(self, rect):
        return rect["Left"] + rect["Width"]

    def rect_bottom(self, rect):
        return rect["Top"] + rect["Height"]

    def rect_top(self, rect):
        return rect["Top"]

    def get_relative_name(self, direction):
        x, y, w, h = self.rect
        left = x
        right = x + w
        top = y
        bottom = y + h
        uitree = self.get_uitree()
        minValue = 10000
        target_name = ""
        if direction == 'right':
            for name, rect in uitree.items():
                # 在右面
                if self.rect_left(rect) > right:
                    if (top < self.rect_top(rect) < bottom) or (top < self.rect_bottom(rect) < bottom):
                        value = self.rect_left(rect) - right
                        if value < minValue:
                            minValue = value
                            target_name = name
            return target_name
        elif direction == 'left':
            for name, rect in uitree.items():
                # 在左面
                if self.rect_right(rect) < left:
                    if (top < self.rect_top(rect) < bottom) or (top < self.rect_bottom(rect) < bottom):
                        value = left - self.rect_right(rect)
                        if value < minValue:
                            minValue = value
                            target_name = name
            return target_name
        elif direction == 'top':
            for name, rect in uitree.items():
                # 在上面
                if self.rect_bottom(rect) < top:
                    if (left < self.rect_left(rect) < right) or (left < self.rect_right(rect) < right):
                        value = top - self.rect_bottom(rect)
                        if value < minValue:
                            minValue = value
                            target_name = name
            return target_name
        elif direction == 'bottom':
            for name, rect in uitree.items():
                # 在下面
                if self.rect_top(rect) > bottom:
                    if (left < self.rect_left(rect) < right) or (left < self.rect_right(rect) < right):
                        value = self.rect_top(rect) - bottom
                        if value < minValue:
                            minValue = value
                            target_name = name
            return target_name
        else:
            raise RuntimeError('不支持的方向：%s' % direction)

    def show_elements_around(self):
        for direction in ['left', 'right', 'top', 'bottom']:
            print("%s: %s" % (direction, self.get_relative_name(direction)))
