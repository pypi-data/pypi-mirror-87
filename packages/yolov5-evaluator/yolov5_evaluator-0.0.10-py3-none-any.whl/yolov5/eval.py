import argparse
import os
import platform
import shutil
import time
from pathlib import Path

import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random
import numpy as np

from models.experimental import attempt_load
from utils.datasets import LoadImages,letterbox
from utils.general import (
    check_img_size, non_max_suppression, apply_classifier, scale_coords,
    xyxy2xywh, plot_one_box, strip_optimizer, set_logging)
from utils.torch_utils import select_device, load_classifier, time_synchronized


def detectByImgWithModel(img0,model,imgsz,iou_thres=0.4,conf_thres=0.5,classes=None,agnostic_nms=False,augment=False):
    # Initialize
    device = torch.device('cpu')
    # Load model
    # model = attempt_load(weight, map_location=device)  # load FP32 model
    imgsz = check_img_size(imgsz, s=model.stride.max())  # check img_size

    img = letterbox(img0,imgsz)[0]
    img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
    img = np.ascontiguousarray(img)
    img = torch.from_numpy(img).to(device)
    img = img.float()  # uint8 to fp16/32
    img /= 255.0  # 0 - 255 to 0.0 - 1.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)

    # Get names and colors
    names = model.module.names if hasattr(model, 'module') else model.names

    # Inference
    pred = model(img, augment=augment)[0]

    # Apply NMS
    pred = non_max_suppression(pred, conf_thres, iou_thres, classes=classes, agnostic=agnostic_nms)

    # Process detections
    for i, det in enumerate(pred):  # detections per image
        if det is not None and len(det):

            # Rescale boxes from img_size to img0 size
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], img0.shape).round()

            # Write results
            result=list()
            for *xyxy, conf, cls in reversed(det):                
                xywh = xyxy2xywh(torch.tensor(xyxy).view(1, 4)).view(-1).tolist()  # normalized xywh
                result.append([int(cls),*xywh])

            return result

def detectByImg(img0,weight,imgsz,iou_thres=0.4,conf_thres=0.5,classes=None,agnostic_nms=False,augment=False):
    # Initialize
    device = torch.device('cpu')
    # Load model
    model = torch.load(weight, map_location=device)['model'].float().fuse().eval()   # load FP32 model
    results = detectByImgWithModel(img0,model,imgsz,iou_thres,conf_thres,classes,agnostic_nms,augment)
    return results

def detectByPath(source,weight,imgsz,iou_thres=0.4,conf_thres=0.5,classes=None,agnostic_nms=False,augment=False):
    img0 = cv2.imread(source)
    return detectByImg(img0,weight,imgsz,iou_thres,conf_thres,classes,agnostic_nms,augment)
    
def detectByUnint8Array(image,weight,imgsz,iou_thres=0.4,conf_thres=0.5,classes=None,agnostic_nms=False,augment=False):
    arr =  np.asarray(bytearray(image), dtype="uint8")
    img0 = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return detectByImg(img0,weight,imgsz,iou_thres,conf_thres,classes,agnostic_nms,augment)
    
def detectByPathWithModel(source,model,imgsz,iou_thres=0.4,conf_thres=0.5,classes=None,agnostic_nms=False,augment=False):
    img0 = cv2.imread(source)
    return detectByImgWithModel(img0,model,imgsz,iou_thres,conf_thres,classes,agnostic_nms,augment)
    
def detectByUnint8ArrayWithModel(image,model,imgsz,iou_thres=0.4,conf_thres=0.5,classes=None,agnostic_nms=False,augment=False):
    arr =  np.asarray(bytearray(image), dtype="uint8")
    img0 = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return detectByImgWithModel(img0,model,imgsz,iou_thres,conf_thres,classes,agnostic_nms,augment)
