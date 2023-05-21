
import os
import sys
import numpy as np
import cv2
from tqdm import trange

os.environ["OMP_NUM_THREADS"] = "4"
os.environ["OMP_WAIT_POLICY"] = "PASSIVE"

import onnxruntime as ort # pylint: disable=import-error
ORT_TYPES_TO_NP_TYPES = {'tensor(float16)': np.float16, 'tensor(float)': np.float32, 'tensor(uint8)': np.uint8}

def non_max_suppression(boxes, scores, threshold):
  assert boxes.shape[0] == scores.shape[0]
  ys1 = boxes[:, 0]
  xs1 = boxes[:, 1]
  ys2 = boxes[:, 2]
  xs2 = boxes[:, 3]
  areas = (ys2 - ys1) * (xs2 - xs1)
  scores_indexes = scores.argsort().tolist()
  boxes_keep_index = []
  while len(scores_indexes):
    index = scores_indexes.pop()
    boxes_keep_index.append(index)
    if not len(scores_indexes):
      break
    ious = compute_iou(boxes[index], boxes[scores_indexes], areas[index],
            areas[scores_indexes])
    filtered_indexes = set((ious > threshold).nonzero()[0])
    scores_indexes = [
      v for (i, v) in enumerate(scores_indexes)
      if i not in filtered_indexes
    ]
  return np.array(boxes_keep_index)

def compute_iou(box, boxes, box_area, boxes_area):
  assert boxes.shape[0] == boxes_area.shape[0]
  ys1 = np.maximum(box[0], boxes[:, 0])
  xs1 = np.maximum(box[1], boxes[:, 1])
  ys2 = np.minimum(box[2], boxes[:, 2])
  xs2 = np.minimum(box[3], boxes[:, 3])
  intersections = np.maximum(ys2 - ys1, 0) * np.maximum(xs2 - xs1, 0)
  unions = box_area + boxes_area - intersections
  ious = intersections / unions
  return ious

def xywh2xyxy(x):
  y = x.copy()
  y[:, 0] = x[:, 0] - x[:, 2] / 2  # top left x
  y[:, 1] = x[:, 1] - x[:, 3] / 2  # top left y
  y[:, 2] = x[:, 0] + x[:, 2] / 2  # bottom right x
  y[:, 3] = x[:, 1] + x[:, 3] / 2  # bottom right y
  return y

def nms(prediction, conf_thres=0.3, iou_thres=0.45):
  prediction = prediction[prediction[...,4] > conf_thres]
  boxes = xywh2xyxy(prediction[:, :4])
  res = non_max_suppression(boxes,prediction[:,4],iou_thres)
  result_boxes = []
  result_scores = []
  result_classes = []
  for r in res:
    result_boxes.append(boxes[r])
    result_scores.append(prediction[r,4])
    result_classes.append(np.argmax(prediction[r,5:]))
  return np.c_[result_boxes, result_scores, result_classes]

print("Onnx available providers: ", ort.get_available_providers(), file=sys.stderr)
options = ort.SessionOptions()
options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_DISABLE_ALL
options.intra_op_num_threads = 2
options.inter_op_num_threads = 8
options.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
provider = 'CPUExecutionProvider'

# ort_session = ort.InferenceSession("test.onnx", options, providers=[provider])
ort_session = ort.InferenceSession("yolov5n.onnx", options, providers=[provider])
ishapes = [[1]+ii.shape[1:] for ii in ort_session.get_inputs()]
keys = [x.name for x in ort_session.get_inputs()]
itypes = [ORT_TYPES_TO_NP_TYPES[x.type] for x in ort_session.get_inputs()]


def get_crop(img):
  h, w = ishapes[0][-2:]
  img = img[::2, ::2, :]
  ih, iw = img.shape[:2]
  sub_img = img[int((ih - h)/2):int((ih + h)/2), int((iw - w)/2):int((iw + w)/2), :]
  return sub_img


CLASSES = ["person","bicycle","car","motorcycle","airplane","bus","train","truck","boat","traffic light","fire hydrant","stop sign","parking meter","bench","bird","cat","dog","horse","sheep","cow","elephant","bear","zebra","giraffe","backpack","umbrella","handbag","tie","suitcase","frisbee","skis","snowboard","sports ball","kite","baseball bat","baseball glove","skateboard","surfboard","tennis racket","bottle","wine glass","cup","fork","knife","spoon","bowl","banana","apple","sandwich","orange","broccoli","carrot","hot dog","pizza","donut","cake","chair","couch","potted plant","bed","dining table","toilet","tv","laptop","mouse","remote","keyboard","cell phone","microwave","oven","toaster","sink","refrigerator","book","clock","vase","scissors","teddy bear","hair drier","toothbrush"]
COLORS = [(231, 76, 60), (52, 152, 219), (241, 196, 15), (46, 204, 113)]
def run_inference(session, img):
  img = img.astype(itypes[0])
  img = np.swapaxes(img, 0, 2)
  img = np.swapaxes(img, 1, 2)
  img = np.expand_dims(img, 0)
  img/=255

  res = session.run(None, {'image': img})
  res = nms(res[0])
  return [{"pred_class": CLASSES[int(opt[-1])] , "prob": opt[-2], "pt_1": opt[:2].astype(int), "pt_2": opt[2:4].astype(int)} for opt in res]
  
def annotate_img(img, res):
  for i, opt in enumerate(res):
    color = COLORS[i%len(COLORS)]
    color = [color[2], color[1], color[0]]
    img = cv2.rectangle(np.array(img), opt['pt_1'], opt['pt_2'], color=color, thickness=1)
    img = cv2.putText(np.array(img), opt['pred_class'], opt['pt_1'], cv2.FONT_HERSHEY_SIMPLEX, 1, color, 1, cv2.LINE_AA)
  return img
