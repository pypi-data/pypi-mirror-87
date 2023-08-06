import concurrent.futures
import json
import typing

import settings


class ScraperManager:
    PRODUCT_URL_MIDDLEWARE = settings.MIDDLEWARES["PRODUCT_URL_MIDDLEWARE"]
    MESSENGER_FUNCTION = None
    REQUEST_MANAGER = None
    LOGGER = None
    PRODUCT_LIST_PAGE_URLS = []
    REQUIRED_KEYWORDS = None
    product_list_page_count = 0
    WEBSITE_BASE_URL = None

    USE_CONCURRENT_REQUESTS = False
    MAX_CONCURRENT_REQUESTS = None

    PRODUCT_DETAIL_PAGE_TEMPLATE = {
        "product_image": "",
        "product_price": "",
        "product_url": "",
        "product_brand": "",
        "product_name": "",
        "product_sizes": "",
        "product_colors": ""
    }

    def __init__(
            self, request_manger=None, logger=None,
            check_restock=False
    ):
        self.request_manager = request_manger or self.REQUEST_MANAGER
        self.logger = logger or self.LOGGER

        self.addons = []

        self.check_restock = check_restock
        self.product_data = {} if check_restock else set()
        self.current_product = None

    def get_product_urls(self) -> typing.Generator:
        """This must yield product urls scraped from the product list page."""
        raise ValueError("Override ``get_product_urls`` method to yield product detail page urls.")

    def get_product_detail(self, product_url: str) -> dict:
        """This must yield product detail data scraped from the product detail page.

        Must return dict with following keys
          * restock: bool = False,
          * product_image: (list, str) = None,
          * product_price: str = None,
          * product_url: str = None,
          * product_brand: str = None,
          * product_name: str = None,
          * product_sizes: (list, str) = None,
          * product_colors: (list, str) = None
        """
        raise ValueError("Override ``get_product_detail`` to return product details as mentioned above.")

    def get_absolute_url(self, url: str):
        if url.startswith("http://") or url.startswith("https://"):
            return url

        if self.WEBSITE_BASE_URL.endswith("/"):
            f"{self.WEBSITE_BASE_URL[0:-1]}{url}"

        return f"{self.WEBSITE_BASE_URL}{url}"

    def parse_json(self, data, default=None, *args, **kwargs):
        default = default or {}
        return self.handler(lambda: json.loads(data, *args, **kwargs), default=default)

    def quit(self):
        raise SystemExit

    def dump_json(self, data, default=None, *args, **kwargs):
        default = default or {}
        return self.handler(lambda: json.dumps(data, *args, **kwargs), default=default)

    def get_product_detail_template(self, **kwargs):
        return {**self.PRODUCT_DETAIL_PAGE_TEMPLATE, **kwargs}

    def handler(self, func, default="", *args, clean=False):
        try:
            if clean:
                return func().replace("\n", "").strip()
            else:
                return func()
        except (ValueError, KeyError, AttributeError, IndexError, *args) as e:
            self.logger(e)
            return default

    def get_product_list_page_urls(self):
        return self.PRODUCT_LIST_PAGE_URLS

    def get_messenger_function(self):
        messenger = getattr(self, self.MESSENGER_FUNCTION, None)
        assert messenger is not None, (
            "either provide messenger function name in ``MESSENGER_FUNCTION`` or override ``get_messenger_function``"
            "and return function object which contains required parameters for sending message."
        )
        return messenger

    def default_diff_checker(self):
        messenger = self.get_messenger_function()

        if self.check_restock:
            product_url = self.current_product.get("product_url")

            if product_url in self.product_data:
                if self.product_data[product_url] != self.current_product:
                    messenger(restock=True, **self.current_product)
                    return
            else:
                messenger(restock=False, **self.current_product)
                return
        else:
            if self.current_product not in self.product_data:
                messenger(restock=False, **self.get_product_detail(self.current_product))
                return

    def check_diff(self, checker="default"):
        diff_checker = getattr(self, f"{checker}_diff_checker")
        assert diff_checker is not None, f"``{checker}_diff_checker`` Function not found."
        diff_checker()

    def validate(self, data):
        if self.REQUIRED_KEYWORDS is None:
            return True

        for keyword in self.REQUIRED_KEYWORDS:
            if keyword.lower() in data.lower():
                return True

        return False

    def __run(self, first):
        def product_detail_manager(product_detail):
            # For validating keywords !!
            if not self.validate(product_detail.get("product_name")):
                return

            self.current_product = product_detail
            if not first:
                self.check_diff()

            self.product_data[product_detail["product_url"]] = product_detail

        self.product_list_page_count = 0
        product_urls = []

        for url in self.get_product_urls():
            if self.check_restock:
                if self.USE_CONCURRENT_REQUESTS:
                    product_urls.append(url)
                else:
                    product_detail_manager(self.get_product_detail(url))
            else:
                self.current_product = url
                if not first:
                    self.check_diff()
                self.product_data.add(url)

        if self.check_restock and self.USE_CONCURRENT_REQUESTS:
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.MAX_CONCURRENT_REQUESTS) as executor:
                for _product_detail in concurrent.futures.as_completed([
                    executor.submit(self.get_product_detail, url) for url in product_urls
                ]):
                    product_detail_manager(_product_detail.result())

    def run(self, infinite=True, iterations=99):
        first = True

        if infinite:
            while True:
                self.__run(first)
                first = False
        else:
            for i in range(iterations):
                self.__run(first)
                first = False

    def __call__(self, *args, **kwargs):
        self.run(*args, **kwargs)


class ThreadManager:
    def __init__(self, max_concurrent_requests=None):
        self.runner = []
        self.max_concurrent_requests = max_concurrent_requests

    def append(self, function):
        self.runner.append(function)

    def set_func(self, functions):
        self.runner = functions

    def run_async(self, on_success=None):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_concurrent_requests) as executor:
            for out in concurrent.futures.as_completed([executor.submit(func) for func in self.runner]):
                if on_success:
                    on_success(out.result())

    @staticmethod
    def concurrent_func_wrapper(func, *args, **kwargs):
        def __wrapper():
            return func(*args, **kwargs)

        return __wrapper
