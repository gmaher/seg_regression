print("imported svWrapper.py")

import os
import json

print("importing seg_reg modules")
from modules import io
from modules import sv_image
from modules import vascular_data

print("importing factories")
import factories.model_factory as model_factory
import factories.preprocessor_factory as preprocessor_factory
import factories.postprocessor_factory as postprocessor_factory

print("getting directories")
SRC_DIR    = os.path.dirname(os.path.realpath(__file__))
CONFIG_DIR = os.path.join(SRC_DIR,"config")

import tensorflow as tf
tf.set_random_seed(0)

import numpy as np
np.random.seed(0)

class SVWrapper(object):
    def __init__(self, network_type):
        print("SVWrapper init, {}".format(network_type))
        self.cfg_fn = os.path.join(CONFIG_DIR,"{}.yaml".format(network_type))
        print(self.cfg_fn)

        if not os.path.isfile(self.cfg_fn):
            raise RuntimeError("network type does not exist {}".format(self.cfg_fn))

        self.cfg = io.load_yaml(self.cfg_fn)

        self.cfg['MODEL_DIR'] = self.cfg['MODEL_DIR'].replace('./results',
            '{}/results'.format(SRC_DIR))

        print("Model dir ", self.cfg['MODEL_DIR'])

        self.model = model_factory.get(self.cfg)

        try:
            self.model.sample()
        except:
            print("using model without sample")

        print("loading model")
        self.model.load()
        print("model loaded")

        self.preprocessor  = preprocessor_factory.get(self.cfg)
        self.postprocessor = postprocessor_factory.get(self.cfg)

    def set_image(self, image_fn):
        print("setting image {}".format(image_fn))
        if not os.path.isfile(image_fn):
            raise RuntimeError("image file not found {}".format(image_fn))

        self.image = sv_image.Image(image_fn)
        self.image.set_reslice_ext(self.cfg['CROP_DIMS'])
        self.image.set_spacing(self.cfg['SPACING'])

        return "ok"

    def segment_normal(self, p,v,n):
        img = self.image.get_reslice(p,n,v)

        img     = self.preprocessor(img)
        pred    = self.model.predict(img)
        contour = self.postprocessor(pred)

        print(contour)

        scale = self.cfg['CROP_DIMS']*self.cfg['SPACING']/2

        # plt.figure()
        # plt.imshow(img[:,:,0],cmap='gray',extent=[-scale,scale,scale,-scale])
        # plt.colorbar()
        # plt.plot(contour[:,0], contour[:,1], color='r', marker='*')
        # plt.savefig('./images/{}.png'.format(seg['index']), dpi=300)
        # plt.close()

        contour[:,1] = contour[:,1]*-1
        contour_3d    = vascular_data.denormalizeContour(contour, p,n,v)

        return contour_3d

    def segment(self, point_string):
        print("test: point_string {}".format(point_string))

        try:
            data = json.loads(point_string)
            print(data)

            p     = data["p"]
            v     = data["n"]
            n     = data["tx"]

            contour_3d = self.segment_normal(p,v,n)

            seg = {}
            seg["points"] = contour_3d.tolist()

            return json.dumps(seg)
        except:
            print("error during sv_wrapper.segment")
            return ""

    def sample(self):
        self.model.sample()

    # def __del__(self):
    #     print("svWrapper destructor")
    #     self.model.sess.close()
    #     tf.reset_default_graph()
