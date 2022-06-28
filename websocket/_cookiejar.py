try:
    import Cookie
except:
    import http.cookies as Cookie


class SimpleCookieJar(object):
    def __init__(self):
        self.jar = {}

    def add(self, set_cookie):
        if not set_cookie:
            return
        try:
            simpleCookie = Cookie.SimpleCookie(set_cookie)
        except:
            simpleCookie = Cookie.SimpleCookie(set_cookie.encode('ascii', 'ignore'))

        for k, v in simpleCookie.items():
            if domain := v.get("domain"):
                if not domain.startswith("."):
                    domain = f".{domain}"
                cookie = self.jar.get(domain) or Cookie.SimpleCookie()
                cookie.update(simpleCookie)
                self.jar[domain.lower()] = cookie

    def set(self, set_cookie):
        if set_cookie:
            try:
                simpleCookie = Cookie.SimpleCookie(set_cookie)
            except:
                simpleCookie = Cookie.SimpleCookie(set_cookie.encode('ascii', 'ignore'))

            for k, v in simpleCookie.items():
                if domain := v.get("domain"):
                    if not domain.startswith("."):
                        domain = f".{domain}"
                    self.jar[domain.lower()] = simpleCookie

    def get(self, host):
        if not host:
            return ""

        cookies = []
        for domain, simpleCookie in self.jar.items():
            host = host.lower()
            if host.endswith(domain) or host == domain[1:]:
                cookies.append(self.jar.get(domain))

        return "; ".join(
            filter(
                None,
                [
                    f"{k}={v.value}"
                    for cookie in filter(None, sorted(cookies))
                    for k, v in sorted(cookie.items())
                ],
            )
        )
