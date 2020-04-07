#! /usr/bin/env python
# -*- coding:utf-8 -*-
# Author: kenny.bai
# Date: 2020/4/1 11:23
# File: main.py

from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import os

chrome_driver = './chromedriver.exe'
auth_config_path = './configs/auth.txt'


class MyTest():
    def __init__(self):
        self.__driver = webdriver.Chrome(executable_path=chrome_driver)
        self.__account = ''
        self.__password = ''
        self.__plugin_path = ''

    # 测试本地html文件
    def test_local_url(self):
        file_path = 'file:///' + os.path.abspath('drop_down.html')
        self.__driver.get(file_path)

    # 测试url地址
    def test_url(self):
        self.parse_config()
        self.__driver.get('http://www.baidu.com')
        cookies = self.__driver.get_cookies()
        print('cookies:', cookies)
        self.__driver.find_element_by_id('username').clear()
        self.__driver.find_element_by_id('username').send_keys(self.__account)
        self.__driver.find_element_by_id('password').clear()
        self.__driver.find_element_by_id('password').send_keys(self.__password)
        self.__driver.find_element_by_xpath("//input[@class='button']").click()
        cookies1 = self.__driver.get_cookies()
        time.sleep(3)
        self.__driver.find_element_by_id("d_wsSwitchBtnMonitor").click()

    # 解析配置文件
    def parse_config(self):
        with open(auth_config_path, mode='r+', encoding='utf8') as config_file:
            lines = config_file.readlines()
            self.__account = lines[0].split(':')[1].strip().rstrip()
            self.__password = lines[1].split(':')[1].strip().rstrip()
            self.__plugin_path = lines[2].split(':')[1].strip().rstrip()
            print('self.account:', self.__account, 'self.password:', self.__password, 'self.pluginpath:',
                  self.__plugin_path)

    # xpath定位
    def find_element_by_xpath(self):
        # 直接匹配
        self.__driver.find_element_by_xpath("//input[@class='button']")
        # 使用contains定位元素 匹配href属性字符串中包含logout的元素
        self.__driver.find_element_by_xpath("//a[contains(@href,'logout')]")
        # starts-with定位元素 匹配rel属性值字符串以nofo为开头的元素
        self.__driver.find_element_by_xpath("//a[starts-with(@rel,'nofo')]")
        # ends-with定位元素 匹配id属性值字符串以__userName为结尾的元素
        self.__driver.find_element_by_xpath("//a[ends-with(@id,'_userName')]")
        # 注:ends-with是xpath2.0的语法，可能浏览器只支持1.0语法，会有兼容的问题，可以使用substring代替
        # //input[substring( @ id, string - length( @ id) - string - length('多测师') + 1) = '多测师']
        pass

    # actions chains类
    def test_actions_chains(self):
        sel = self.__driver.find_element_by_xpath("//select[@id='status']")
        actions = ActionChains(self.__driver)

        # click(on_element) 鼠标单击
        actions.click(sel)

        # click_and_hold(on_element) 鼠标单击并且按住不放
        actions.click_and_hold(sel)

        # context_click(on_element) 鼠标右击
        actions.context_click(sel)

        # double_click(on_element) 鼠标双击
        actions.double_click(sel)

        # drag_and_drop(source, target) 从source拖拽到target
        actions.drag_and_drop(sel, target=None)

        # drag_and_drop_by_offset(source, xoffset, yoffset) 将source拖动到指定的位置
        actions.drag_and_drop_by_offset(sel, 100, 100)

        # key_down(value, element) 按住某个键,使用这个方法可以实现某些快捷键，比如Ctrl+c键
        actions.key_down(Keys.CONTROL).send_keys('c').perform()

        # key_up(value, element) 按住Ctrl+c键，然后松开
        actions.key_up(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()

        # move_by_offset(x_off_set, y_off_set) 鼠标移动到某个位置
        actions.move_by_offset(100, 100)

        # move_to_element(to_element) 鼠标移动到某个元素的位置, 该方法可以用于代替滚动条滚动到指定的位置
        actions.move_to_element(sel)

        # move_to_element_with_offset(to_element, x_off_set, y_off_set) 移动鼠标到某个元素位置的偏移位置
        actions.move_to_element_with_offset(sel, 100, 100)

        # perform(to_element, x_off_set, y_off_set) 将之前的一系列的ActionChains执行
        actions.move_to_element_with_offset(sel, 100, 100).perform()

        # release() 释放按下的鼠标
        actions.move_to_element_with_offset(sel, 100, 100).release()

        # send_keys(val) 向某个元素输入值
        sel.send_keys('mmmm')

        # send_keys_to_element(to_element, val) 向指定元素输入数据
        actions.send_keys_to_element(sel, 'nnn')

    # 获取property和attribute
    def test_get_property_or_attr(self):
        # 获取dom固有属性
        self.__driver.find_element_by_id('password').get_property("value")
        # 获取dom自定义属性
        self.__driver.find_element_by_xpath('password').get_attribute("value")

    # 操作原生 html select组件
    def test_operate_select(self):
        # 使用Select, 选取option标签的value值
        sel = self.__driver.find_element_by_xpath("//select[@id='status']")
        sel.selectByValue("0")

    # 多frames情况的快速定位
    def test_frames_locations(self):
        self.__driver.implicitly_wait(30)
        # 使用frame的index来定位，定位第一个frame, index下标从0开始
        self.__driver.switch_to.frame(0)
        # 使用id值来定位
        self.__driver.switch_to.frame('frame1')
        # 使用name来定位
        self.__driver.switch_to.frame('myframe')
        # 使用find_element系列方法获取对象
        self.__driver.switch_to.frame(self.__driver.find_element_by_tag_name("iframe"))

        # 从子frame切回到父frame
        self.__driver.switch_to.parent_frame()
        # 切换到默认frame
        self.__driver.switch_to.default_content()

    # 多window情况的快速定位
    def test_windows_locations(self):
        # 传参和frames一致
        self.__driver.switch_to.window(0)

    # 同步调用js
    def test_call_javascript(self):
        '''
            执行js一般有两种场景:
            1.直接在页面上执行js
            2.另一种在某个已经定位的元素上执行js
        '''
        # case 1
        js = 'var dom = document.getElementById(\"test-wrap\"); dom.style.border=\"1px solid red\"'
        self.__driver.execute_script(js)

        # case 2
        button = self.__driver.find_element_by_tag_name('btn')
        self.__driver.execute_script('$(arguments[0]).fadeOut()', button)

        js1 = "var q=document.documentElement.scrollTop=0"
        self.__driver.execute_script(js1)

    # 处理下拉框
    def test_drop_down(self):
        # 其实就是设置寻找范围
        father = self.__driver.find_element_by_id("ShippingMethod")
        father.find_element_by_xpath("//option[@value='1.0']").click()

    # cookie
    def test_operate_cookie(self):
        # 获取cookie
        self.__driver.get_cookies()
        # 添加cookie
        self.__driver.add_cookie({'name': 'key-aaaa'})
        # 删除一个cookie
        self.__driver.delete_cookie('value')
        # 删除所有cookie
        self.__driver.delete_all_cookies()


myTest = MyTest()
myTest.test_url()
