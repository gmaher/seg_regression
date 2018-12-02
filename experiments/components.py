class AbstractModel(object):
    def __init__(self, config):
        self.config=config
        self.setup()
    def setup(self):
        pass
    def predict(self,x):
        pass
    def save(self):
        pass
    def load(self):
        pass
    def train(self):
        pass

class AbstractExperiment(object):
    def __init__(self, config):
        self.config = config
        self.setup()
    def setup(self):
        pass
    def set_data(self,data):
        pass
    def set_model(self,model):
        self.model = model
    def setup_directories(self):
        pass
    def predict(self):
        pass
    def train(self):
        pass
    def save(self):
        pass
    def load(self):
        pass
