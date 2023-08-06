"""
@author: JiXuan Xu, Jun Wang
@date: 20201023
@contact: jun21wangustc@gmail.com 
"""
import sys

import logging.config
logging.config.fileConfig("config/logging.conf")
logger = logging.getLogger('api')

import yaml
import cv2
import numpy as np
from core.model_loader.face_landmark.FaceLmsModelLoader import FaceLmsModelLoader
from core.model_handler.face_landmark.FaceLmsModelHandler import FaceLmsModelHandler

with open('config/model_conf.yaml') as f:
    model_conf = yaml.load(f)

if __name__ == '__main__':
    # common setting for all model, need not modify.
    model_path = 'models'

    # model setting, modified along with model
    model_category = 'face_landmark'
    model_name =  model_conf[model_category]['face_landmk_s']

    logger.info('Start to load the face landmark model...')
    # load model
    try:
        facelmsModelLoader = FaceLmsModelLoader(model_path, model_category, model_name)
    except Exception as e:
        logger.info('Failed to parse model configuration file!')
        sys.exit(-1)
    else:
        logger.info('Successfully parsed the model configuration file meta.json!')

    try:
        model, cfg = facelmsModelLoader.load_model()
    except Exception as e:
        logger.error('Model loading failed!')
        sys.exit(-1)
    else:
        logger.info('Successfully loaded the face landmark model!')

    faceLmsModelHandler = FaceLmsModelHandler(model, 'cuda:0', cfg)

    # read image
    image_path = 'sample_api/test_image/ori_faces/test1.jpg'
    image_det_txt_path = 'sample_api/temp/test1_detect.txt'
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    with open(image_det_txt_path, 'r') as f:
        lines = f.readlines()
    try:
        for i, line in enumerate(lines):
            line = line.strip().split()
            det = np.asarray(list(map(int, line[0:4])), dtype=np.int32)
            landmarks = faceLmsModelHandler.inference_on_image(image, det)

            save_path_img = 'sample_api/temp/test1_' + 'landmark_' + str(i) + '.jpg'
            save_path_txt = 'sample_api/temp/test1_' + 'landmark_' + str(i) + '.txt'
            image_show = image.copy()
            with open(save_path_txt, "w") as fd:
                for (x, y) in landmarks.astype(np.int32):
                    cv2.circle(image_show, (x, y), 2, (255, 0, 0),-1)
                    line = str(x) + ' ' + str(y) + ' '
                    fd.write(line)
            cv2.imwrite(save_path_img, image_show)
    except Exception as e:
        logger.error('Face landmark failed!')
        sys.exit(-1)
    else:
        logger.info('Successful face landmark!')
