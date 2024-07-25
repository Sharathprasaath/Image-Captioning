from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import torch
from PIL import Image
import tensorflow
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Model
import keras
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input

class Image_captioning():

    def __init__(self):
        self.feature_extractor= VGG16()
        self.tokenizer = pd.read_pickle(r"C:\Users\Sharath Prasaath\App\tokenizer7.pkl")

        self.device = '/gpu:0' if tensorflow.config.list_physical_devices('GPU') else '/cpu:0'
        with tensorflow.device(self.device):
            self.model = tensorflow.keras.models.load_model(r'C:\Users\Sharath Prasaath\App\best_model7.h5')
    def idx_to_word(self,integer, tokenizer):
        for word, index in tokenizer.word_index.items():
            if index == integer:
                return word
        return None
    def predict_caption(self,model, image, tokenizer, max_length):
    # add start tag for generation process
        in_text = 'startseq'
        # iterate over the max length of sequence
        for i in range(max_length):
            # encode input sequence
            sequence = tokenizer.texts_to_sequences([in_text])[0]
            # pad the sequence
            sequence = pad_sequences([sequence], max_length)
            # predict next word
            yhat = model.predict([image, sequence], verbose=0)
            # get index with high probability
            yhat = np.argmax(yhat)
            # convert index to word
            word = self.idx_to_word(yhat, tokenizer)
            # stop if word not found
            if word is None:
                break
            # append word as input for generating next word
            in_text += " " + word
            # stop if we reach end tag
            if word == 'endseq':
                break
        
        return in_text
    def generate_caption(self,image_id):
        
        y_pred = self.predict_caption(self.model, image_id, self.tokenizer, max_length=74)
        return y_pred
    def caption(self,img):
        i_image=load_img(img, target_size=(224, 224))
        layer_name = self.feature_extractor.layers[-2].name
        modelf = Model(inputs=self.feature_extractor.input, outputs=self.feature_extractor.get_layer(layer_name).output)
        i_image = img_to_array(i_image)
        i_image = i_image.reshape((1, i_image.shape[0], i_image.shape[1], i_image.shape[2]))
        i_image = preprocess_input(i_image)
        feature = modelf.predict(i_image, verbose=0)
        cap=self.generate_caption(feature)
        return cap
    
