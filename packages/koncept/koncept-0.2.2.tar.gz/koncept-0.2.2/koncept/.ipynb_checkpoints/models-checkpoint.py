from kuti import model_helper as mh
from kuti import applications as apps
from kuti import tensor_ops as ops
from kuti import generic as gen
from kuti import image_utils as iu

import pandas as pd, numpy as np, os, urllib

class Koncept512:
    def __init__(self, data_root='~/.koncept/', verbose=1):
        super().__init__()        
        self.data_root = data_root
        self.verbose = verbose
        self.create_model()
        self.load_weights()
        
    def create_model(self):
        if self.verbose:
            print('Creating the Koncept512 model')
        base_model = apps.InceptionResNetV2(weights     = None, 
                                            include_top = False,
                                            input_shape = None)
        gap = apps.GlobalAveragePooling2D(name="final_gap")\
                             (base_model.layers[-1].output)
        self.base_model = apps.Model(inputs=base_model.input, outputs=gap)        
        self.preprocess_fn = apps.process_input[apps.InceptionResNetV2]
        
        head = apps.fc_layers(self.base_model.output, name='fc',
                              fc_sizes      = [2048, 1024, 256, 1],
                              dropout_rates = [0.25, 0.25, 0.5, 0],
                              batch_norm    = 2)
        
        self.model = apps.Model(inputs = self.base_model.inputs, outputs = head)

    def load_weights(self, model_file_name = 'koncep512-trained-model.h5'):        
        model_path = os.path.join(self.data_root, model_file_name)
        model_url = 'http://datasets.vqa.mmsp-kn.de/archives/' + model_file_name
        if not os.path.exists(model_path):
            if self.verbose:
                print(f'Downloading model weights to: {model_path}')
            gen.make_dirs(self.data_root)
            urllib.request.urlretrieve(model_url, model_path)            
        self.model.load_weights(model_path)

    def assess(self, images):
        if isinstance(images, np.ndarray):
            ims = images.copy()
        elif isinstance(images, list):
            ims = np.stack(images)
        else:
            raise ValueError("`images` is not `np.ndarray` or a list thereof")

        if len(ims.shape)<4:
            ims = np.expand_dims(ims, 0)
        
        for i in range(ims.shape[0]):
            ims[i,...] = self.preprocess_fn(ims[i,...])

        # Predict quality score
        y_pred = self.model.predict(ims).squeeze()
        return y_pred