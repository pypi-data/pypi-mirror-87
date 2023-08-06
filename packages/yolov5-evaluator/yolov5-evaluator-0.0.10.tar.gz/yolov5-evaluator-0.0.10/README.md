# `yolov5-evaluator`

>  Wrapper for the detection program for ease of use yolov5.

## Install

```
pip install yolov5-evaluator
```

## Use
```
from yolov5 import eval

result=eval.detectByPath('./inference/images/01.jpg','./weights/v5-2/last.pt',640)
print(result)


image=cv2.imread('./inference/images/01.jpg')
result=eval.detectByImg(image,'./weights/v5-2/last.pt',640)
print(result)
```

## params
```

eval.detectByPath(source,weight,imgsz)

eval.detectByImage(image,weight,imgsz)

```
