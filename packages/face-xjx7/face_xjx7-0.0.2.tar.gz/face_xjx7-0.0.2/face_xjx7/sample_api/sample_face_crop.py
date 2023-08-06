"""
@author: JiXuan Xu, Jun Wang
@date: 20201015
@contact: jun21wangustc@gmail.com 
"""
import logging.config
logging.config.fileConfig("config/logging.conf")
logger = logging.getLogger('api')

import cv2

from core.image_cropper.arcface_face_recognition.FaceRecImageCropper import FaceRecImageCropper

if __name__ == '__main__':
    image_path = 'sample_api/test_image/ori_faces/test1.jpg'
    image_info_file = 'sample_api/temp/test1_' + 'landmark_0' + '.txt'
    line = open(image_info_file).readline().strip()
    landmarks_str = line.split(' ')
    landmarks = [float(num) for num in landmarks_str]
    
    face_cropper = FaceRecImageCropper()
    image = cv2.imread(image_path)
    cropped_image = face_cropper.crop_image_by_mat(image, landmarks)
    cv2.imwrite('sample_api/temp/test1_arcface_cropped_0.jpg', cropped_image)
    logger.info('Crop image successful!')