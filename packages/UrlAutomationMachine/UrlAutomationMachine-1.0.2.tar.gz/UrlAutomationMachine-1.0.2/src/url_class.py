import re
import json
import urllib3
from colorama import Fore, init


class urlAutomationMachine:
    def __init__(self, file_input=None, isJson=False, ignore=None):
        self.file_input = file_input
        self.listOfUrls = []
        self.isJson = isJson
        self.http = urllib3.PoolManager()
        self.response_status = None
        self.ignore_list = []
        if ignore is not None:
            ignore_file = open(ignore, "r")

            self.ignore_list = re.findall(
                r"https?:[a-zA-Z0-9_.+-/#~]+", ignore_file.read()
            )

    def processUrl(self):
        if self.file_input is not None:
            if isinstance(self.file_input, str):
                try:
                    if (self.checkUrl()) is not None:
                        self.makeRequest(self.file_input)
                except ValueError as error_exe:
                    raise ValueError("Input was not a valid URL") from error_exe
        else:
            raise AttributeError("Function requires a url that's a string")

    def processFile(self):
        if self.file_input is not None:
            if isinstance(self.file_input, str):
                fileToCheck = open(self.file_input, "r")
                self.listOfUrls = re.findall(
                    r"https?:[a-zA-Z0-9_.+-/#~]+", fileToCheck.read()
                )

                if self.listOfUrls == []:
                    pass

                for line in self.listOfUrls:
                    line = line.strip()
                    if line not in self.ignore_list:
                        self.makeRequest(line)

                fileToCheck.close()
            else:
                raise ValueError("Function requires a file to be inserted")
        else:
            raise AttributeError("A parameter is required")

    def makeRequest(self, url):
        init()
        try:
            r = self.http.request("HEAD", url)
            self.response_status = r
            self.printOutput(r, url)
        except urllib3.exceptions.MaxRetryError as e:  # At this point, the connection attempt timed out and therfore, the url cannot be reached, so in this case, we skip the url entirely.
            print("Url does not load fast enough")
            print(str(e))

    def printOutput(self, r, url):
        if self.isJson:
            jsonURL = {"url": url, "status_code": r.status}
            if r.status == 200:
                print(
                    Fore.GREEN
                    + f"[SUCCESS]: {jsonURL} passes automation. This url is working properly!"
                )
            elif r.status == 400 or r.status == 404:
                print(
                    Fore.RED
                    + f"[FAILURE]: {jsonURL} fails automation. This url is broken unfortunately!"
                )
            else:
                print(
                    Fore.WHITE
                    + f"[UNKNOWN] {jsonURL} gives off a warning. This url is fishy!"
                )
        else:
            if r.status == 200:
                print(
                    Fore.GREEN
                    + f"[SUCCESS]: {url} passes automation. This url is working properly!"
                )
            elif r.status == 400 or r.status == 404:
                print(
                    Fore.RED
                    + f"[FAILURE]: {url} fails automation. This url is broken unfortunately!"
                )
            else:
                print(
                    Fore.WHITE
                    + f"[UNKNOWN] {url} gives off a warning. This url is fishy!"
                )

    def getStatus(self) -> int:
        return self.response_status.status

    def processTelescope(self):
        telescopeURL = "http://localhost:3000/posts"
        try:
            posts = self.http.request("GET", telescopeURL)
            posts = json.loads(posts.data)
            for post in posts:
                self.makeRequest(f"{telescopeURL}/{post['id']}")
        except urllib3.exceptions.MaxRetryError as e:
            print(str(e))

    def checkUrl(self) -> str or None:
        valid_search = re.search(r"https?:[a-zA-Z0-9_.+-/#~]+", self.file_input)

        if valid_search is not None:
            return valid_search.string
        return None
