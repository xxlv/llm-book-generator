import json

# -1 means no limit 
DEFAULT_CONFIG = {
    "minLevel": -1,
    "maxLevel": -1,
    "minChapter": -1,
    "maxChapter": -1,
    "minSize": -1,
    "maxSize": -1
}

class BuildConfig:
    """
    BuildConfig class for representing book building configuration.

    Attributes:
        min_level (int): The minimum level of the generated book.
        max_level (int): The maximum level of the generated book.
        min_chapter (int): The minimum number of chapters in the generated book.
        max_chapter (int): The maximum number of chapters in the generated book.
        min_size (int): The minimum size of the generated book.
        max_size (int): The maximum size of the generated book.
    """
    def __init__(self, min_level=None, max_level=None,
                 min_chapter=None, max_chapter=None, min_size=None, max_size=None):
        self.min_level = min_level
        self.max_level = max_level
        self.min_chapter = min_chapter
        self.max_chapter = max_chapter
        self.min_size = min_size
        self.max_size = max_size

    def generate_config(self):
        config = {
            "minLevel": self.min_level if self.min_level is not None else DEFAULT_CONFIG["minLevel"],
            "maxLevel": self.max_level if self.max_level is not None else DEFAULT_CONFIG["maxLevel"],
            "minChapter": self.min_chapter if self.min_chapter is not None else DEFAULT_CONFIG["minChapter"],
            "maxChapter": self.max_chapter if self.max_chapter is not None else DEFAULT_CONFIG["maxChapter"],
            "minSize": self.min_size if self.min_size is not None else DEFAULT_CONFIG["minSize"],
            "maxSize": self.max_size if self.max_size is not None else DEFAULT_CONFIG["maxSize"],
        }
        return config

    @classmethod
    def from_file(cls, filename="buildbook.json"):
        with open(filename, 'r') as file:
            data = json.load(file)
        return cls(min_level=data.get("minLevel", None),
                   max_level=data.get("maxLevel", None),
                   min_chapter=data.get("minChapter", None),
                   max_chapter=data.get("maxChapter", None),
                   min_size=data.get("minSize", None),
                   max_size=data.get("maxSize", None))
