'''
Built on top of Neural style transfer example with Keras.
# References
    - [A Neural Algorithm of Artistic Style](http://arxiv.org/abs/1508.06576)
'''

from __future__ import print_function
import sys
sys.path.insert(0, '../keras/')
from keras import backend as K
from img_processing import preprocess_image
from model import model
from loss import calc_loss_grad
from evaluator import Evaluator
from optimization import optimizer
import os
import shutil


def main(weights_path, base_path, base_file, style_path, style_file, img_width, img_height):
    result_prefix = base_file[:-4] + '_' + style_file[:-4]
    base_img_path = base_path + base_file
    style_img_path = style_path + style_file
    # get tensor representations of images
    base_img = K.variable(preprocess_image(base_img_path,
                                           img_width,
                                           img_height))
    style_img = K.variable(preprocess_image(style_img_path,
                                            img_width,
                                            img_height))
    combo_img = K.placeholder((1, 3, img_width, img_height))
    # combine the 3 images into a single Keras tensor
    input_tensor = K.concatenate([base_img, style_img, combo_img],
                                 axis=0)

    print('Creating painting of {} in the style of {}'.format(base_file[:-4],
                                                              style_file[:-4]))
    print('Loading model with VGG16 network weights...')
    nn = model(weights_path, input_tensor, img_width, img_height)
    loss, grads = calc_loss_grad(nn, combo_img, img_width, img_height)
    evaluate = Evaluator(loss, grads, combo_img, img_width, img_height)
    optimizer(evaluate, img_width, img_height, result_prefix)


if __name__ == '__main__':
    base_path = '../base/'
    style_path = '../style/'
    weights_path = '../vgg16_weights.h5'
    base_files = os.listdir(base_path)
    style_files = os.listdir(style_path)

    # dimensions of the generated picture
    img_width = 128
    img_height = 128
    assert img_height == img_width, \
           'Due to the use of the Gram matrix, width and height must match.'

    for base_file in base_files:
        for style_file in style_files:
            main(weights_path,
                base_path, base_file,
                style_path, style_file,
                img_width, img_height)
