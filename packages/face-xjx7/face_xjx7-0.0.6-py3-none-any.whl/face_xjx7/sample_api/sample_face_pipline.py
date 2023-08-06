"""
@author: JiXuan Xu, Jun Wang
@date: 20201024
@contact: jun21wangustc@gmail.com 
"""
import sys

import logging.config
logging.config.fileConfig("config/logging.conf")
logger = logging.getLogger('api')

import yaml
import cv2
import numpy as np
from core.model_loader.face_detection.FaceDetModelLoader import FaceDetModelLoader
from core.model_handler.face_detection.FaceDetModelHandler import FaceDetModelHandler
from core.model_loader.face_landmark.FaceLmsModelLoader import FaceLmsModelLoader
from core.model_handler.face_landmark.FaceLmsModelHandler import FaceLmsModelHandler
from core.image_cropper.arcface_face_recognition.FaceRecImageCropper import FaceRecImageCropper
from core.model_loader.face_recognition.FaceRecModelLoader import FaceRecModelLoader
from core.model_handler.face_recognition.FaceRecModelHandler import FaceRecModelHandler

with open('config/model_conf.yaml') as f:
    model_conf = yaml.load(f)

if __name__ == '__main__':
    # common setting for all model, need not modify.
    model_path = 'models'

    # model setting, modified along with model
    model_category = 'face_detection'
    model_name =  model_conf[model_category]['face_det_s']

    logger.info('Start to load the face detection model...')
    # load model
    try:
        faceDetModelLoader = FaceDetModelLoader(model_path, model_category, model_name)
    except Exception as e:
        logger.info('Failed to parse model configuration file!')
        sys.exit(-1)
    else:
        logger.info('Successfully parsed the model configuration file meta.json!')

    try:
        model, cfg = faceDetModelLoader.load_model()
    except Exception as e:
        logger.error('Model loading failed!')
        sys.exit(-1)
    else:
        logger.info('Successfully loaded the face detection model!')
    faceDetModelHandler = FaceDetModelHandler(model, 'cuda:0', cfg)

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

    # model setting, modified along with model
    model_category = 'face_recognition'
    model_name =  model_conf[model_category]['face_feat_w']

    logger.info('Start to load the face recognition model...')
    # load model
    try:
        faceRecModelLoader = FaceRecModelLoader(model_path, model_category, model_name)
    except Exception as e:
        logger.info('Failed to parse model configuration file!')
        sys.exit(-1)
    else:
        logger.info('Successfully parsed the model configuration file meta.json!')
        
    try:
        model, cfg = faceRecModelLoader.load_model()
    except Exception as e:
        logger.error('Model loading failed!')
        sys.exit(-1)
    else:
        logger.info('Successfully loaded the face recognition model!')
    faceRecModelHandler = FaceRecModelHandler(model, 'cuda:0', cfg)

    # read image
    image_path = 'sample_api/test_image/ori_faces/'
    image_name = 'test2'
    image = cv2.imread(image_path + image_name + '.jpg', cv2.IMREAD_COLOR)

    try:
        dets = faceDetModelHandler.inference_on_image(image)
    except Exception as e:
       logger.error('Face detection failed!')
       sys.exit(-1)
    else:
       logger.info('Successful face detection!')
    face_det_num = dets.shape[0]

    face_cropper = FaceRecImageCropper()
    feature_list = []
    try:
        for i in range(face_det_num):
            landmarks = faceLmsModelHandler.inference_on_image(image, dets[i])
            landmarks_list = []
            image_show = image.copy()
            for (x, y) in landmarks.astype(np.int32):
                landmarks_list.extend((x, y))
                cv2.circle(image_show, (x, y), 2, (255, 0, 0),-1)
            cv2.imwrite('sample_api/temp/'+ image_name + '_landmark_' + str(i) + '.jpg', image_show)
            cropped_image = face_cropper.crop_image_by_mat(image, landmarks_list)
            cv2.imwrite('sample_api/temp/'+ image_name + '_arcface_cropped_' + str(i) + '.jpg', cropped_image)
            feature = faceRecModelHandler.inference_on_image(cropped_image)
            feature_list.append(feature)
    except Exception as e:
        logger.error('Face landmark failed!')
        logger.error('Face crop failed!')
        logger.error('Failed to extract facial features!')
        sys.exit(-1)
    else:
        logger.info('Successful face landmark!')
        logger.info('Crop image successful!')
        logger.info('Successfully extracted facial features!')

    score = np.dot(feature_list[0], feature_list[1])
    print(score)





    
    

