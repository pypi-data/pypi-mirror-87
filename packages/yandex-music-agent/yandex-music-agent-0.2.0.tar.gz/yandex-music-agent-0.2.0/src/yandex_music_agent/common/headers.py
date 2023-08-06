from urllib import parse


class Headers:
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) " \
                 "AppleWebKit/537.36 (KHTML, like Gecko) " \
                 "Chrome/83.0.4103.122 " \
                 "Safari/537.36 "

    def __init__(self, host: str, cookie: str):
        self.host = host
        self.cookie = cookie

    def build(self, page: str, values: dict = None, cross_site: bool = False) -> dict:
        referer = f"https://{self.host}/{page}"
        result = {}
        if values:
            result.update(values)
        result.update({
            "Accept": "application/json; q=1.0, text/*; q=0.8, */*; q=0.1",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7",
            "Connection": "keep-alive",
            "Origin": f"https://{self.host}",
            "Referer": referer,
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site" if cross_site else "same-origin",
            "User-Agent": self.user_agent,
            # "X-Current-UID": "1130000014799604",
            "X-Requested-With": "XMLHttpRequest",
            "X-Retpath-Y": parse.quote(referer),
        })
        if not cross_site:
            result["Cookie"] = self.cookie
            result["Host"] = self.host
        return result
