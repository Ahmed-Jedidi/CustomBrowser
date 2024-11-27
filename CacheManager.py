class CacheManager:
    def __init__(self):
        self.cache = {}

    def get_cache_headers(self, url):
        headers = {}
        if url in self.cache:
            cached_data = self.cache[url]
            # Utiliser If-Modified-Since basé sur la dernière date de modification
            if 'last_modified' in cached_data:
                headers['If-Modified-Since'] = cached_data['last_modified']
        return headers

    def update_cache(self, url, response):
        # Sauvegarder d'autres en-têtes utiles pour la gestion du cache
        self.cache[url] = {
            'content': response.text,
            'last_modified': response.headers.get('Last-Modified'),
            'cache_control': response.headers.get('Cache-Control'),
            'expires': response.headers.get('Expires')
        }

    def get_cached_content(self, url):
        if url in self.cache:
            return self.cache[url]['content']
        return None
