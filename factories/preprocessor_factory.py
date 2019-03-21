from components.common import BasePreProcessor
#from components.seg import SegPreProcessor

def get(config):
    if config.get('PREPROCESSOR') == 'SEG':
        return SegPreProcessor(config)

    return BasePreProcessor(config)
