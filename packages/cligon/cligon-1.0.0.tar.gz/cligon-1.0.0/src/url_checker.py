"""
This function is used to get any URLs in a file.
Written in Python 3.8.2
"""
import re
from itertools import repeat
from multiprocessing.dummy import Pool as ThreadPool
import requests

try:
    from src import url_status
except ModuleNotFoundError:
    import url_status

UrlStatus = url_status.UrlStatus


class UrlChecker:
    """contains methods to help check url"""

    def remove_html_tags(self, text):
        """Remove any html tags, return as string"""
        new_text = re.compile(r"<.*?>")
        return new_text.sub("", text)

    def parse_urls_from_file(self, file_name):
        """Get URLs using regex, return as an array of strings"""
        regex = r"(?P<url>https?://[^\s]+)"
        file = open(file_name)
        contents = file.read()
        return re.findall(regex, self.remove_html_tags(contents))

    def get_url_status_code(self, link, time_out):
        """Get the status code of the URLs, and outputs a list of url_status obj"""
        try:
            status_code = requests.head(link, timeout=time_out).status_code
        except requests.exceptions.Timeout:
            status_code = None
        except requests.exceptions.TooManyRedirects:
            status_code = None
        except requests.exceptions.RequestException:
            status_code = None

        if status_code in (400, 404):
            result_name = "BAD"
        elif status_code == 200:
            result_name = "GOOD"
        else:
            result_name = "UNKNOWN"

        return UrlStatus(link, result_name, status_code)

    def check_urls_thread(self, urls, time_out):
        """Check urls by starting threads"""
        pool = ThreadPool(10)
        url_status_list = pool.starmap(
            self.get_url_status_code, zip(urls, repeat(time_out))
        )
        pool.close()
        pool.join()

        return url_status_list

    def output_urls_and_status(self, url_status_list, args):
        """Outputs a list of websites and the result of the website"""
        output_list = []

        for url_status in url_status_list:
            if args.good and url_status.get_result_name() == "GOOD":
                output_list.append(url_status)
            elif args.bad and url_status.get_result_name() == "BAD":
                output_list.append(url_status)
            elif not args.bad and not args.good:
                output_list.append(url_status)

        if args.json:
            print("[")
            for i, url_status in enumerate(output_list):
                if i:  # print comma if not 0
                    print(",")
                print(url_status.output(args), end="")
            print("\n]")
        else:
            for url_status in output_list:
                print(url_status.output(args))
