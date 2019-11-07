try:
    import configparser as  ConfigParser
except:
    import ConfigParser
import codecs
path = './app.conf'


def getConfig(section, key):
    config = ConfigParser.ConfigParser()
    try:
        config.read_file(codecs.open(path, encoding='utf-8'))
    except:
        config.read(path)

    return config.get(section, key)