from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def get_text_content(file):
    with open(file.content.path, encoding='utf-8') as stream:
        data = load(stream, Loader=Loader)
        return data
