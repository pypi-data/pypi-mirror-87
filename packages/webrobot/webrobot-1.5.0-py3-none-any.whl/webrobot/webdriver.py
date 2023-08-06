from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from webrobot.element import Element


class create:
    driver = None

    def __init__(self, wait_time=30, driver_path=None, display=True):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        if not driver_path and display:
            self.driver = webdriver.Chrome()
        elif driver_path and display:
            self.driver = webdriver.Chrome(executable_path="webrobot/chromedriver.exe")
        elif not driver_path and not display:
            self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="chromedriver.exe")
        else:
            self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="webrobot/chromedriver.exe")
        self.driver.implicitly_wait(wait_time)
        self.max()

    def select(self, element_id=None, element_text=None, element_class=None, element_tag=None, element_xpath=None,
               element_css=None, element_name=None, element_partial_text=None, wait_time=5):
        try:
            element = None
            if element_id:
                element = WebDriverWait(self.driver, wait_time).until(lambda s: s.find_element_by_id(element_id))
            elif element_text:
                element = WebDriverWait(self.driver, wait_time).until(
                    lambda s: s.find_element_by_link_text(element_text))
            elif element_class:
                element = WebDriverWait(self.driver, wait_time).until(
                    lambda s: s.find_element_by_class_name(element_class))
            elif element_tag:
                element = WebDriverWait(self.driver, wait_time).until(
                    lambda s: s.find_element_by_tag_name(element_tag))
            elif element_xpath:
                element = WebDriverWait(self.driver, wait_time).until(
                    lambda s: s.find_element_by_xpath(element_xpath))
            elif element_css:
                element = WebDriverWait(self.driver, wait_time).until(
                    lambda s: s.find_element_by_css_selector(element_css))
            elif element_name:
                element = WebDriverWait(self.driver, wait_time).until(
                    lambda s: s.find_element_by_name(element_name))
            elif element_partial_text:
                element = WebDriverWait(self.driver, wait_time).until(
                    lambda s: s.find_element_by_partial_link_text(element_partial_text))
            return Element(element)
        except Exception as e:
            print(e.__traceback__.tb_lineno)
            return None

    # 获取元素对象

    def selects(self, element_id=None, element_text=None, element_class=None, element_tag=None, element_xpath=None,
                element_css=None, element_name=None, element_partial_text=None, wait_time=5):
        try:
            elements = []
            element_list = []
            if element_id:
                elements = WebDriverWait(self.driver, wait_time).until(
                    lambda s: s.find_elements_by_id(element_id))
            elif element_text:
                elements = WebDriverWait(self.driver, wait_time).until(
                    lambda s: s.find_elements_by_link_text(element_text))
            elif element_class:
                elements = WebDriverWait(self.driver, wait_time).until(
                    lambda s: s.find_elements_by_class_name(element_class))
            elif element_tag:
                elements = WebDriverWait(self.driver, wait_time).until(
                    lambda s: s.find_elements_by_tag_name(element_tag))
            elif element_xpath:
                elements = WebDriverWait(self.driver, wait_time).until(
                    lambda s: s.find_elements_by_xpath(element_xpath))
            elif element_css:
                elements = WebDriverWait(self.driver, wait_time).until(
                    lambda s: s.find_elements_by_css_selector(element_css))
            elif element_name:
                elements = WebDriverWait(self.driver, wait_time).until(
                    lambda s: s.find_elements_by_name(element_name))
            elif element_partial_text:
                elements = WebDriverWait(self.driver, wait_time).until(
                    lambda s: s.find_elements_by_partial_link_text(element_partial_text))
            for element in elements:
                element_list.append(Element(element))
            return element_list
        except Exception as e:
            print(e.__traceback__.tb_lineno)
            return None

    # 获取元素对象列表

    def back(self):
        try:
            self.driver.back()
            return True
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return False

    # 后退到当前浏览器会话的浏览器历史记录中后一步操作后的页面

    def close(self):
        try:
            self.driver.close()
            return True
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return False

    # 关闭当前浏览器窗口

    def forward(self):
        try:
            self.driver.forward()
            return True
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return False

    # 前进一步到当前浏览器会话的浏览器历史记录中前一步操作后的页面

    def get(self, url):
        try:
            self.driver.get(url)
            return True
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return False

    # 跳转到指定URL

    def max(self):
        try:
            self.driver.maximize_window()
            return True
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return False

    # 窗口最大化

    def quit(self):
        try:
            self.driver.quit()
            return True
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return False

    # 推出当前Driver并关闭所有页面

    def refresh(self):
        try:
            self.driver.refresh()
            return True
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return False

    # 刷新当前页面

    def switch_alert(self):
        try:
            self.driver.switch_to_alert()
            return True
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return False

    # 将焦点切换至弹出警告

    def switch_default_content(self):
        try:
            self.driver.switch_to_default_content()
            return True
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return False

    # 将焦点切换至默认框架内

    def switch_frame(self, name):
        try:
            self.driver.switch_to_frame(name)
            return True
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return False

    # 将焦点切换至指定的框架

    def switch_window(self, name):
        try:
            self.driver.switch_to_window(name)
            return True
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return False

    # 将焦点切换至指定的窗口

    # implicitly_wait?!

    @property
    def cookies(self):
        try:
            return self.driver.get_cookies()
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @cookies.setter
    def cookies(self, cookie_dict):
        try:
            for cookie in cookie_dict:
                self.driver.add_cookie({"name": cookie, "value": cookie_dict[cookie]})
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)

    @property
    def load_wait_time(self):
        return None

    @load_wait_time.setter
    def load_wait_time(self, second: int):
        try:
            self.driver.set_page_load_timeout(second)
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)

    @property
    def execute_wait_time(self):
        return None

    @execute_wait_time.setter
    def execute_wait_time(self, second: int):
        try:
            self.driver.set_script_timeout(second)
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)

    @property
    def url(self):
        try:
            return self.driver.current_url
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def handle(self):
        try:
            return self.driver.current_window_handle
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def handles(self):
        try:
            return self.driver.window_handles
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def name(self):
        try:
            return self.driver.name
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def orientation(self):
        try:
            return self.driver.orientation
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def source(self):
        try:
            return self.driver.page_source
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def title(self):
        try:
            return self.driver.title
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def active_element(self):
        try:
            return Element(self.driver.switch_to_active_element())
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None
