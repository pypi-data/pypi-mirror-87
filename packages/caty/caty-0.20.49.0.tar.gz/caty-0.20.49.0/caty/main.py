from caty.plugins import Plugins


def main(path, ext):
    handlers = {
        ext : Plugin()
        for Plugin in Plugins
        for ext in Plugin.ext
    }
    handler = handlers.get(ext,  handlers['hex'])
    try:
        data = handler.read(path)
        handler.dump(data)
    except Exception as x:
        print(x)
