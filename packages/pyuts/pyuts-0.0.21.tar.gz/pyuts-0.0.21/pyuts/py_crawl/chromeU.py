# -*- coding: UTF-8 -*-
from ..py_api_b import PyApiB
import os
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from typing import List


class ChromeU(PyApiB):
    """
    网页浏览器模拟工具
    """
    def __init__(self):
        self.driver: WebDriver = None
        self._windowSize = [1080, 720]
        self._imagesEnable = False
        self._isHide = True

    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def setConfig(self, windowSize=None, imagesEnable=None, isHide=True):
        """
        设置浏览器格式\n 
        @Args: \n 
        windowSize:窗口大小，例如：[1920.1080]\n 
        imagesEnable: 是否加载图片\n 
        isHide: 是否为后台执行
        """
        if windowSize == None:
            windowSize = self._windowSize
        else:
            self._windowSize = windowSize
        if imagesEnable == None:
            imagesEnable = self._imagesEnable
        else:
            self._imagesEnable = imagesEnable
        if isHide == None:
            isHide = self._isHide
        else:
            self._isHide = isHide
        from selenium import webdriver
        options = webdriver.ChromeOptions()
        # options.add_argument('--kiosk')
        if isHide:
            options.add_argument('headless')
        options.add_argument(f'window-size={windowSize[0]}x{windowSize[1]}')
        options.add_argument(
            f'blink-settings=imagesEnabled={str(imagesEnable).lower()}')
        # options.add_argument('user-data-dir=./chrome_tmp')
        if "webdriver_hub" in os.environ:
            self.driver = webdriver.Remote(
                command_executor=os.environ["webdriver_hub"],
                desired_capabilities=options.to_capabilities())
        else:
            self.driver = webdriver.Chrome(chrome_options=options)
        return self

    def loadUrl(self, url) -> WebDriver:
        """
        加载地址
        """
        if not self.driver:
            self.setConfig()
        self.driver.get(url)
        return self.driver

    def getDriver(self) -> WebDriver:
        return self.driver

    def toHTML(self):
        return self.driver.find_element_by_xpath("//*").get_attribute(
            "outerHTML")

    def wait_for_fun(self, fun, *parms):
        import time
        for i in range(0, 60):
            if not self.__can_do(fun, *parms):
                time.sleep(1)
            else:
                return True
        return False

    def __can_do(self, fun, *parms):
        try:
            fun(*parms)
            return True
        except BaseException as e:
            return False

    def find_element_by_css_selector(self, value) -> WebElement:
        return self.driver.find_element_by_css_selector(value)

    def find_elements_by_css_selector(self, value) -> List[WebElement]:
        return self.driver.find_elements_by_css_selector(value)

    def find_element_by_id(self, value) -> WebElement:
        return self.driver.find_element_by_id(value)

    def find_elements_by_id(self, value) -> List[WebElement]:
        return self.driver.find_elements_by_id(value)

    def find_element_by_class_name(self, value) -> WebElement:
        return self.driver.find_element_by_class_name(value)

    def find_elemenst_by_class_name(self, value) -> List[WebElement]:
        return self.driver.find_elements_by_class_name(value)

    def find_element_by_tag_name(self, value) -> WebElement:
        return self.driver.find_element_by_tag_name(value)

    def find_elements_by_tag_name(self, value) -> List[WebElement]:
        return self.driver.find_elements_by_tag_name(value)

    def find_element_by_xpath(self, value) -> WebElement:
        return self.driver.find_element_by_xpath(value)

    def find_elements_by_xpath(self, value) -> List[WebElement]:
        return self.driver.find_elements_by_xpath(value)

    def find_element_by_name(self, value) -> WebElement:
        return self.driver.find_element_by_name(value)

    def find_elements_by_name(self, value) -> List[WebElement]:
        return self.driver.find_elements_by_name(value)

    def find_element_by_link_text(self, value) -> WebElement:
        return self.driver.find_element_by_link_text(value)

    def find_elements_by_link_text(self, value) -> List[WebElement]:
        return self.driver.find_elements_by_link_text(value)

    def set_attribute(self, element, attr_key, attr_value):
        self.driver.execute_script(
            f"arguments[0].{attr_key} = `{attr_value}`;", element)

    def get_attribute(self, element, attr_key):
        """
        获取元素内的属性值\n
        @Args:\n
        element:元素\n
        attr_key: 属性的键，例如：href\n
        """
        return element.get_attribute(attr_key)

    def shot(self, element, path=''):
        if path.strip() == '':
            return path
        element.screenshot(path)
        return path

    def downloadFile(self, url, savePath):
        import requests
        import shutil
        r = requests.get(url, stream=True)
        r.raw.decode_content = True
        if r.status_code == 404:
            return
        with open(savePath, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    def execute(self, js, view):
        return self.driver.execute_script(js, view)

    def quit(self):
        self.driver.close()
        self.driver.quit()
        self.driver = None

    def click(self, on_element=None):
        """
        单击鼠标左键
        """
        from selenium.webdriver.common.action_chains import ActionChains
        ActionChains(self.driver).click(on_element).perform()

    def click_and_hold(self, on_element=None):
        """
        点击鼠标左键，不松开
        """
        from selenium.webdriver.common.action_chains import ActionChains
        ActionChains(self.driver).click_and_hold(on_element).perform()

    def context_click(self, on_element=None):
        """
        点击鼠标右键
        """
        from selenium.webdriver.common.action_chains import ActionChains
        ActionChains(self.driver).context_click(on_element).perform()

    def double_click(self, on_element=None):
        """
        双击鼠标左键
        """
        from selenium.webdriver.common.action_chains import ActionChains
        ActionChains(self.driver).double_click(on_element).perform()

    def drag_and_drop(self, from_element, target_element):
        """
        拖拽到某个元素然后松开
        """
        from selenium.webdriver.common.action_chains import ActionChains
        ActionChains(self.driver).drag_and_drop(from_element,
                                                target_element).perform()

    def drag_and_drop_by_offset(self, from_element, xoffset, yoffset):
        """
        拖拽到某个坐标然后松开
        """
        from selenium.webdriver.common.action_chains import ActionChains
        ActionChains(self.driver).drag_and_drop_by_offset(
            from_element, xoffset, yoffset).perform()

    def key_down(self, value, element=None):
        """
        按下某个键盘上的键
        """
        from selenium.webdriver.common.action_chains import ActionChains
        ActionChains(self.driver).key_down(value, element).perform()

    def key_up(self, value, element=None):
        """
        松开某个键
        """
        from selenium.webdriver.common.action_chains import ActionChains
        ActionChains(self.driver).key_up(value, element).perform()

    def move_by_offset(self, xoffset, yoffset):
        """
        鼠标从当前位置移动到某个坐标
        """
        from selenium.webdriver.common.action_chains import ActionChains
        ActionChains(self.driver).move_by_offset(xoffset, yoffset).perform()

    def move_to_element(self, to_element):
        """
        鼠标移动到某个元素
        """
        from selenium.webdriver.common.action_chains import ActionChains
        ActionChains(self.driver).move_to_element(to_element).perform()

    def move_to_element_with_offset(self, to_element, xoffset, yoffset):
        """
        移动到距某个元素（左上角坐标）多少距离的位置
        """
        from selenium.webdriver.common.action_chains import ActionChains
        ActionChains(self.driver).move_to_element_with_offset(
            to_element, xoffset, yoffset).perform()

    def release(self, on_element=None):
        """
        在某个元素位置松开鼠标左键
        """
        from selenium.webdriver.common.action_chains import ActionChains
        ActionChains(self.driver).release(on_element).perform()

    def send_keys(self, keys_to_send):
        """
        发送某个键到当前焦点的元素
        """
        from selenium.webdriver.common.action_chains import ActionChains
        ActionChains(self.driver).send_keys(*keys_to_send).perform()

    def send_keys_to_element(self, element, keys_to_send):
        """
        发送某个键到指定元素
        """
        from selenium.webdriver.common.action_chains import ActionChains
        ActionChains(self.driver).send_keys_to_element(
            element, *keys_to_send).perform()
