class CookiesManager:
    def __init__(self):
        # Store cookies as a dictionary of dictionaries {url: {cookie_name: cookie_value}}
        self.cookies = {}
#2
    def add_cookie(self, url, cookie_name, cookie_value):
        """Add a cookie for a specific URL."""
        if url not in self.cookies:
            self.cookies[url] = {}
        self.cookies[url][cookie_name] = cookie_value
#2
    def get_cookies(self, url):
        """Get cookies for a specific URL."""
        if url in self.cookies:
            return self.cookies[url]
        return {}
    
# Comment cookies
#    def get_cookies_1(self, url):
#        """
#        Retrieve cookies for a given URL's domain.
#        """
#        from urllib.parse import urlparse
#        domain = urlparse(url).netloc
#        return self.cookies.get(domain, {})
#
#    def update_cookies(self, url, response):
#        """
#        Update cookies based on the 'Set-Cookie' header in the response.
#        """
#        from urllib.parse import urlparse
#        domain = urlparse(url).netloc
#
#        if 'Set-Cookie' in response.headers:
#            cookie_headers = response.headers.get('Set-Cookie')
#            domain_cookies = self.cookies.get(domain, {})
#
#            for cookie in cookie_headers.split(', '):  # Handle multiple cookies
#                parts = cookie.split(';')[0]  # Only process the main cookie part
#                if '=' in parts:
#                    key, value = parts.split('=', 1)
#                    domain_cookies[key] = value
#
#            self.cookies[domain] = domain_cookies
#
#    def attach_cookies(self, url, headers):
#        """
#        Attach cookies to the headers for a request.
#        """
#        from urllib.parse import urlparse
#        domain = urlparse(url).netloc
#        domain_cookies = self.cookies.get(domain, {})
#
#        if domain_cookies:
#            cookie_string = "; ".join([f"{key}={value}" for key, value in domain_cookies.items()])
#            headers['Cookie'] = cookie_string
#
#        return headers

#2
    def delete_cookie(self, url, cookie_name):
        """Delete a specific cookie for a URL."""
        if url in self.cookies and cookie_name in self.cookies[url]:
            del self.cookies[url][cookie_name]
            if not self.cookies[url]:  # Remove URL if no cookies remain
                del self.cookies[url]
#2
    def clear_cookies(self, url=None):
        """Clear all cookies or cookies for a specific URL."""
        if url:
            self.cookies.pop(url, None)
        else:
            self.cookies.clear()

#3 view
def view_cookies(self):
    cookies_text = self.get_cookies_text()
    
    # Create a dialog to display cookies
    text_dialog = QDialog(self)
    text_dialog.setWindowTitle("Cookies")
    text_dialog.setMinimumWidth(400)
    
    layout = QVBoxLayout(text_dialog)
    text_edit = QTextEdit()
    text_edit.setPlainText(cookies_text)
    text_edit.setReadOnly(True)  # Make it read-only
    
    layout.addWidget(text_edit)
    text_dialog.exec_()


def get_cookies_text(self):
    cookies_text = ""
    for url, cookies in self.cookies_manager.cookies.items():
        cookies_text += f"URL: {url}\n"
        for cookie_name, cookie_value in cookies.items():
            cookies_text += f"  {cookie_name}: {cookie_value}\n"
        cookies_text += "\n"
    return cookies_text
