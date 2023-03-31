from pathlib import Path

class PoormansLocalFileCache:
    def __init__(self, cache_dir: str):
        self.cache_dir = cache_dir
        if cache_dir is not None:
            Path(cache_dir).mkdir(parents=True, exist_ok=True)

    def __cache_path(self, name: str):
        if self.cache_dir is None:
            return None
        return f"{self.cache_dir}/{name}"

    def get(self, name: str):
        if self.cache_dir is None:
            return None
        cache_path = self.__cache_path(name)
        if not Path(cache_path).is_file():
            return None
        with open(cache_path, "rb") as f:
            return f.read()

    def put(self, name: str, data: str):
        if self.cache_dir is None:
            return
        cache_path = self.__cache_path(name)
        with open(cache_path, "wb") as f:
            f.write(data)