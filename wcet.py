import os
import glob
import cv2
import caffe
import lmdb
import numpy as np
import time
import matplotlib.pyplot as plt
from caffe.proto import caffe_pb2
from resizing import *
from operator import add
#caffe.set_mode_gpu()

os.system('export OMP_NUM_THREADS=1')

#Size of images
IMAGE_WIDTH = 227
IMAGE_HEIGHT = 227

exec_time = 0
preds = []
exec_list = []

def transform_img(img, img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT):

    #Histogram Equalization
    img[:, :, 0] = cv2.equalizeHist(img[:, :, 0])
    img[:, :, 1] = cv2.equalizeHist(img[:, :, 1])
    img[:, :, 2] = cv2.equalizeHist(img[:, :, 2])

    #Image Resizing
    img = cv2.resize(img, (img_width, img_height), interpolation = cv2.INTER_CUBIC)
    return img

#Read mean image
mean_blob = caffe_pb2.BlobProto()
with open('/home/raam/WCET/model1/deeplearning-cats-dogs-tutorial/input/mean.binaryproto') as f:
    mean_blob.ParseFromString(f.read())
mean_array = np.asarray(mean_blob.data, dtype=np.float32).reshape(
(mean_blob.channels, mean_blob.height, mean_blob.width))


#Read model architecture and trained model's weights
net = caffe.Net('/home/raam/WCET/model1/deeplearning-cats-dogs-tutorial/caffe_models/caffe_model_1/caffenet_deploy_1.prototxt',
            '/home/raam/WCET/model1/deeplearning-cats-dogs-tutorial/caffe_models/caffe_model_1/models/caffe_model_1_iter_10000.caffemodel',
            caffe.TEST)

#Define image transformers
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_mean('data', mean_array)
transformer.set_transpose('data', (2,0,1))   
resizing_time = []
re_time = []

for i in range(1,2):
    start_resizingTime = time.time()
    path = resize_time("/home/raam/WCET/model1/deeplearning-cats-dogs-tutorial/input/estimation/"+ str(i) + ".jpg")
    end_resizingTime = time.time()
    resize = end_resizingTime - start_resizingTime
    test_img_paths = [img_path for img_path in glob.glob("/home/raam/WCET/model1/deeplearning-cats-dogs-tutorial/input/estimation/"+ str(i) + ".jpg")]    
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)    
    img_hist = transform_img(img,img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT)
    exact_startTime = time.time()
    net.blobs['data'].data[...] = transformer.preprocess('data', img_hist)
    out = net.forward()	
    pred_probas = out['prob']
    preds = preds + [pred_probas.argmax()]
    exact_endTime = time.time()
    exec_time = (exact_endTime - exact_startTime)
    exec_list.append(exec_time)		
    #resizing_time.append(path)
    #re_time.append(resize)

#inference_time =map(add, exec_list,resizing_time)
#inference = map(add, exec_list, re_time)
   
#with open("/home/raam/WCET/model1/deeplearning-cats-dogs-tutorial/WCET/resize1000.txt","a") as f:           
#    f.write('Overall inference time considering resizing time from code c++ = {}'.format(inference_time)+'\n')
#    f.write('Overall inference time  = {}'.format(inference)+'\n')
#    f.write('actual resizing time  = {}'.format(resizing_time)+'\n')
#    f.write('resizing time  = {}'.format(re_time)+'\n')

#f.close()

 

