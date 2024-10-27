# insightface
# 스탭 1 : import modules 
import argparse
import cv2
import sys
import numpy as np
import insightface
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image

# 스탭 2 : create inference object(instance)
app = FaceAnalysis()
app.prepare(ctx_id=0, det_size=(640, 640))
# parser.add_argument('--ctx', default=0
# parser.add_argument('--det-size', default=640

# 스탭 3 : load data
# img = ins_get_image('t1')
img1 = cv2.imread('iu1.jpg')
# 작동 순서
# file open 
# decode img
img2 = cv2.imread('iu2.jpg')

# 스탭 4 : inference
faces1 = app.get(img1)
assert len(faces1)==1

faces2 = app.get(img2)
assert len(faces2)==1

# 스탭 5 : Post processing (application)
# rimg = app.draw_on(img, faces)
# cv2.imwrite("./t1_output.jpg", rimg)

# then print all-to-all face similarity
emb1 = faces1[0].normed_embedding
emb2 = faces2[0].normed_embedding

np_emb1 = np.array(emb1, dtype=np.float32)
np_emb2 = np.array(emb2, dtype=np.float32)

sims = np.dot(np_emb1, np_emb2.T)
# np_emb2.T : .T 행렬을 수직으로 변환한다.
# np.dot : 코사인 유사도
print(sims)
# 0.4 이상이면 거의 동일 인물로 본다.
