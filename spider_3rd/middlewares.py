# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from .settings import driver_path, chrome_path
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

import time
import undetected_chromedriver as uc
from scrapy.http.response.html import HtmlResponse
import os

import subprocess

class Spider3RdSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class Spider3RdDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    def __init__(self):

        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument('--blink-settings=imagesEnabled=false')
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--disable-dev-shm-usage")
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument(f"--proxy-server=http://192.168.100.24:60021")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--profile-directory=Default")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--disable-plugins-discovery")
        chrome_options.add_argument('--no-first-run')
        chrome_options.add_argument('--no-service-autorun')
        chrome_options.add_argument('--no-default-browser-check')
        chrome_options.add_argument('--password-store=basic')
        chrome_options.add_argument('--no-sandbox')

        # os.system("start C://Program Files//Google//Chrome//Application//chrome.exe --remote-debugging-port=9222")
        # subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="F:\MyChromeDevUserData"')
        # time.sleep(4)
        # chrome_options=Options()
        # chrome_options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
        # driver_path = r'F:\dependency\chromedriver_win32 (109.0.5414.74)\chromedriver.exe'           #把浏览器驱动器放在任意位置都可以
        # browser_executable_path = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
        browser_executable_path = None
        if chrome_path != '':
            browser_executable_path = chrome_path  # 这里是你指定浏览器的路径
        # if chrome_path != '':
        #     options.binary_location = chrome_path  # 这里是你指定浏览器的路径
        print(driver_path, browser_executable_path)
        self.driver = uc.Chrome(driver_executable_path=driver_path, options=chrome_options, browser_executable_path=browser_executable_path)
        # self.driver = webdriver.Chrome(executable_path=driver_path)
        # self.driver = webdriver.Chrome(executable_path=driver_path,options=chrome_options);

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        
        # 我们需要拦截请求，由selenium发起请求，将获取的数据封装成一个response对象。
        self.driver.get(request.url)

        if 'conforama' in request.url:
            print("休眠了3秒======================")
            time.sleep(3)
        #
        time.sleep(1)
        js1 = "window.scrollTo(0, 1000)"
        self.driver.execute_script(js1)
        time.sleep(1)
        js1 = "window.scrollTo(0, 3000)"
        self.driver.execute_script(js1)
        time.sleep(1)
        js1 = "window.scrollTo(0, 5000)"
        self.driver.execute_script(js1)
        time.sleep(1)
        js1 = "window.scrollTo(0, 8000)"
        self.driver.execute_script(js1)
        time.sleep(1)
        time.sleep(2)
        if 'conforama' in request.url:
            time.sleep(3)

        if 'CAPTCHA' in self.driver.page_source:
            time.sleep(360)

        response = HtmlResponse(request.url, body=self.driver.page_source, request=request, encoding='utf-8')

        return response

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def spider_closed(self):
        self.driver.quit()
        pass
        
    def __del__(self):
        self.driver.quit()

from scrapy.http.response.html import HtmlResponse
from scrapy.exceptions import IgnoreRequest
from queue import Queue
from scrapy.utils.project import get_project_settings
import time

class Spider3RdDownloaderMiddlewareMuti(object):
    def __init__(self):
        # Initialize browser
        chrome_options = uc.ChromeOptions()
        # chrome_options.add_argument('--blink-settings=imagesEnabled=false')
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--disable-dev-shm-usage")
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument(f"--proxy-server=http://192.168.100.24:60021")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--profile-directory=Default")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--disable-plugins-discovery")
        chrome_options.add_argument('--no-first-run')
        chrome_options.add_argument('--no-service-autorun')
        chrome_options.add_argument('--no-default-browser-check')
        chrome_options.add_argument('--password-store=basic')
        chrome_options.add_argument('--no-sandbox')

        # os.system("start C://Program Files//Google//Chrome//Application//chrome.exe --remote-debugging-port=9222")
        # subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="F:\MyChromeDevUserData"')
        # time.sleep(4)
        # chrome_options=Options()
        # chrome_options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
        # driver_path = r'F:\zhangcrworkspace\23年1月\spider_3rd\spider_3rd\chromedriver'            #把浏览器驱动器放在任意位置都可以
        self.browser = uc.Chrome(driver_executable_path=driver_path,options = chrome_options)
        # self.driver = webdriver.Chrome(executable_path=driver_path)
        # self.driver = webdriver.Chrome(executable_path=driver_path,options=chrome_options);
        # get project settings
        settings=get_project_settings()
        concurrent_requests=settings.get('CONCURRENT_REQUESTS')

        # Initialize tabs
        while len(self.browser.window_handles) < concurrent_requests:
            self.browser.execute_script('''window.open("","_blank");''')

        # Initialize window handles queue
        self.handle_queue=Queue(maxsize=concurrent_requests)
        for handle in self.browser.window_handles:
            self.handle_queue.put(handle)

        time.sleep(1)

        # Initialize requests dict
        self.requests={}

    def process_request(self, request, spider):
        result=self.requests.get(request.url)
        if result is None:
            # get a free window_handle from queue
            if self.handle_queue.empty():
                return HtmlResponse(url=request.url,request=request, encoding='utf-8', status=202)
            handle = self.handle_queue.get()

            # open url by js
            self.browser.switch_to.window(handle)
            js = r"location.href='%s';" % request.url

            try:
                self.browser.get(request.url)
                js1 = "window.scrollTo(0, document.body.scrollHeight)"
                self.browser.execute_script(js1)
            except:
                try:
                    time.sleep(4)
                    self.browser.get(request.url)
                    js1 = "window.scrollTo(0, document.body.scrollHeight)"
                    self.browser.execute_script(js1)
                except:
                    time.sleep(4)
                    self.browser.get(request.url)
                    js1 = "window.scrollTo(0, document.body.scrollHeight)"
                    self.browser.execute_script(js1)

            time.sleep(1)
            # wait for 1s to avoid some bug ("document.readyState" will return a "complete" at the first)
            if 'CAPTCHA' in self.browser.page_source:
                print('触发反爬')
                time.sleep(30)
            # mark url
            self.requests[request.url]={'status':'waiting','handle':handle}

            return HtmlResponse(url=request.url,request=request, encoding='utf-8', status=202)

        elif result['status']=='waiting':

            # switch to the tab to check page status using javascript
            handle = result['handle']
            self.browser.switch_to.window(handle)
            document_status=self.browser.execute_script("return document.readyState;")

            if document_status=='complete':
                self.requests[request.url]['status'] = 'done'
                self.handle_queue.put(handle)
                return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',
                                    status=200)
            else:
                return HtmlResponse(url=request.url, request=request, encoding='utf-8', status=202)

        elif result['status']=="done":
            # Filter repeat URL
            raise IgnoreRequest

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        # crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def spider_closed(self, spider):
        self.browser.quit()

    def __del__(self):
        self.browser.quit()
