import requests
import random
import time


class Logger:
    def __init__(self, std_log=True, file_log=False, file_name=f"{__name__}.log", log_format=None):
        # ``log_formats: [
        #           "messenger",
        #           "error",
        #           "scraper_api_request",
        #           "request",
        #           "",
        # ]
        # ``
        self.std_log = std_log
        self.file_log = file_log
        self.file_name = file_name
        self.log_format = set(log_format) if log_format else None

    def log_to_file(self, filename=None, log=True):
        if filename:
            self.file_name = filename
        self.file_log = log

    def __call__(self, log, log_type=None, *args, func=None, **kwargs):
        if self.std_log:
            if func:
                if func():
                    print(log, *args, **kwargs)
            else:
                if log_type is None or self.log_format is None or log_type in self.log_format:
                    print(log, *args, **kwargs)

        if self.file_log:
            with open(self.file_name, "a") as f:
                if func:
                    if func():
                        f.write(log)
                else:
                    f.write(log)


class RequestManager:
    RAW_HEADERS = """
accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
accept-encoding: gzip, deflate, br
accept-language: en-GB,en;q=0.9
cookie: _abck=044987E7364AE524549D7485C01B965B~-1~YAAQRC7fFxxPnnF1AQAAhfNmtgRf6puoOnZ0QqoVgo/qwddW5Wa1H5YdAwqctl7EcB+t0uhR1oToGXteqlur4ZQIimSjItYzppr7ji4XcRNqSGDBkikxYg1SiUqPalNnSfWMNDIqtR9XqgHfY8D0FMPo6wi9fdHEghQhxzyWtWRekudkCsuIBJvLX48Hud9WVXNk05kVsycTmtCs+N5uXPJ6MZclufEKLltFHswBum3sy3xPurGrNy9sBKcGAcaBzd/x559Y5UCZfiAC57QQfoF5gJydc5PgQhVAiS6d7eOg05AEkWJnRwI=~-1~-1~-1; bm_sz=4C37F1CAE16605D2A8A3E6788D6733C0~YAAQRC7fFx1PnnF1AQAAhfNmtgksLIFRs1s7pNe1l3vckuFLA/lo2GrRnqFX+TzhOsy7t7oGK781vL/S86vb314Zya2wVLe6EhCN9cGk3/9ZNhVqugOGsZUnNk/CeWz+eeqMhVepEaO3eIohD5p/UlvOzb8kp9NpvhHcBiURHSzQEhBkj1Rx6PgLyKpGPwks8LMIw6I0NwwNNbF6fG72S0YgLNkEBUKZhIEMC+ZeRVDlGXWMkSHhVMD/pe9rRw==; ak_bmsc=EEB3A46B0317A00C5DC04D25439E868D17DF2E445F6E0000799FAB5F5B2A172F~pl+Mk9aXmrQwg3eRZz1U5sPLEsBgpB+avE/kSC1CG5gUGxiD2TJ5/SdJppwJAHcxiM1osfpelDUWOvCsKrdFQ4tPRYXEYdOQw5FnDsnYOSki//0NHUTkrEsMQzVE1Vv+efEvRQ6vP18ZczzRvx0CLO1PZFdSr7uibAXR4l8e+nse0napT0WMXm4m32HNLuqefoyf8RoP+GaerQmwLnsUi294pxapJWGzkX9rOcwjh1oNU+LS+azQYU5M9WTu1BVu+F6QIZ9EVdB8tugEFmI4wRDiZULo+TChbVef8oFZkhu68=; _Context=en; CS_CONTEXT=en; PRICE_COUNTRY=-; _URLbefore=https%3A%2F%2Fwww.kickz.com%2Fen%2Fshoes%2Fc; _catalog_entry_url="https://www.kickz.com/en/shoes/c?selectedPage=2&ext=true"; _user_last_search_url="https://www.kickz.com/en/shoes/c?selectedPage=1&ext=true"
dnt: 1
sec-fetch-dest: document
sec-fetch-mode: navigate
sec-fetch-site: none
sec-fetch-user: ?1
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36
    """
    EXCLUDED_HEADERS = {"cookie"}
    HEADERS = {}

    def __init__(
            self, use_proxies=False, session=None, request_timeout=3, retry=3, logger=None,
            image_host_api_url=None, image_host_api_key=None,
            increment_sleep_time_after_request_fails=9,
            initial_sleep_time_on_error=100,
            sleep_time_after_each_request=3
    ):
        self.successful_request_count = 0
        self.unsuccessful_request_count = 0
        self.session = session or requests
        self.write = logger or Logger()

        self.image_host_api_url = image_host_api_url
        self.image_host_api_key = image_host_api_key

        self.use_proxies = use_proxies
        self.__proxies = []  # list of dict mapping the proxies !!

        self.request_timeout = request_timeout  # timeout of request !!
        self.retry = retry  # how many times to retry !!

        self.increment_sleep_time_after_request_fails = increment_sleep_time_after_request_fails
        self.initial_sleep_time_on_error = initial_sleep_time_on_error
        self.sleep_time_after_each_request = sleep_time_after_each_request

        if not self.HEADERS and self.RAW_HEADERS:
            self.parse_raw_header()

    @property
    def total_request_count(self):
        return self.successful_request_count + self.unsuccessful_request_count

    def get_headers(self):
        return self.HEADERS

    def parse_raw_header(self, raw_header=None, exclude=None):
        if self.HEADERS and raw_header is None:
            return self.HEADERS

        _header = {}
        exclude = exclude or self.EXCLUDED_HEADERS
        raw_header = raw_header or self.RAW_HEADERS

        for header in raw_header.strip().split("\n"):
            key, value = header.split(": ")

            if key not in exclude:
                _header[key] = value

        self.HEADERS = _header
        return _header

    def get_random_proxy(self) -> dict:
        """Returns random proxy from current list of proxies"""
        return random.choice(self.__proxies)

    def set_proxies(self, proxies):
        if type(proxies) != list:
            raise TypeError("Proxies must be of list of dict containing proxies.")

        self.__proxies = proxies

    def get_proxies(self):
        """Override this to get proxies from http request and run set_proxies."""

    def get_response(self, url, method="GET", *args, **kwargs):
        if self.use_proxies:
            kwargs.setdefault("proxies", self.get_random_proxy())

        for _ in range(self.retry):
            try:
                res = self.session.get(url, *args, **kwargs) if method == "GET" else requests.post(url, *args, **kwargs)
                self.write(
                    f"[+] Response For '{url}' => '{res.url}', STATUS: ``{res}``, METHOD: ``{method}``",
                    "request"
                )
                self.successful_request_count += 1
                time.sleep(self.sleep_time_after_each_request)
                return res
            except Exception as e:
                self.unsuccessful_request_count += 1
                self.write(e, "error")

                if self.initial_sleep_time_on_error:
                    time.sleep(self.initial_sleep_time_on_error)

                if self.increment_sleep_time_after_request_fails:
                    self.initial_sleep_time_on_error += self.increment_sleep_time_after_request_fails

    def get_image_url(self, image, use_self_request=False):
        image_kwargs = {
            "data": {
                "key": self.image_host_api_key
            },
            "files": {
                "img": image
            }
        }
        if use_self_request:
            resp = self.post(**image_kwargs)
        else:
            resp = requests.post(**image_kwargs)

        return resp.json().get("url")

    def get(self, url, *args, **kwargs):
        return self.get_response(url, method="GET", *args, **kwargs)

    def post(self, url, *args, **kwargs):
        return self.get_response(url, method="POST", *args, **kwargs)


class ScraperAPIRequestManager(RequestManager):
    def __init__(
            self, scraper_api_key=None,
            custom_api_key=None, request_new_api_key_after_n_requests=10, custom_api_key_request_url=None,
            *args, **kwargs
    ):
        self.scraper_api_key = scraper_api_key
        self.custom_api_key = custom_api_key
        self.custom_api_key_request_url = custom_api_key_request_url
        self.request_new_api_key_after_n_requests = request_new_api_key_after_n_requests

        if custom_api_key:
            self.set_custom_api_key()

        super(ScraperAPIRequestManager, self).__init__(*args, **kwargs)

    def set_custom_api_key(self):
        res = requests.get(self.custom_api_key_request_url, params={
            "key": self.custom_api_key
        })

        if res.ok:
            self.scraper_api_key = res.json().get("key")
        else:
            self.write(f"[!] Error when grabbing custom API key in `ScraperAPIRequestManager -> set_custom_api_key`",
                       "scraper_api_request")
            self.write(f"[!] Using Last key Instead.", "scraper_api_request")

    def get_response(self, url, method="GET", *args, **kwargs):
        if self.custom_api_key and (self.total_request_count % self.request_new_api_key_after_n_requests) == 0:
            self.set_custom_api_key()

        url = f"http://api.scraperapi.com?api_key={self.scraper_api_key}&url={url}"
        return super(ScraperAPIRequestManager, self).get_response(url, method, *args, **kwargs)


class AbstractAPIRequestManager(RequestManager):
    def __init__(self, api_key=None, *args, **kwargs):
        self.api_key = api_key
        super(AbstractAPIRequestManager, self).__init__(*args, **kwargs)

    def get_response(self, url, method="GET", *args, **kwargs):
        url = f"https://scrape.abstractapi.com?url={url}&api_key={self.api_key}"
        return super(AbstractAPIRequestManager, self).get_response(url, method, *args, **kwargs)
