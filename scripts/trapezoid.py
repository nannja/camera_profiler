#coding:utf-8
#descriptiton: 台形補正用のスクリプト。

import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys
import re

#[settings]
input_file = "../npydatam/differed/npy_BCD/12345_15.npy"
output_file = ""

#以下のパラメータで調整してスクリプトを動かしてうまい具合に補正
rx = 1200 # x方向の引き伸ばし
ry = 1200 # y方向の引き伸ばし
down = -200 # 出力画像を上下方向にずらす
right = 0 # 出力画像を左右方向にずらす



if input_file[-3:] == "npy":
    img = np.load(input_file)
else:
    img = cv2.imread(input_file, 1)

#サイズ
xsize = img.shape[1]
ysize = img.shape[0]
size = tuple(np.array([xsize, ysize]))

#perspective1は出力画像の大きさ
perspective1 = np.float32([[right, ysize+down],
                           [xsize+right, ysize+down],
                           [xsize+right, down],
                           [right, down]])

#persipective2はインプット画像のふちをリサイズ
perspective2 = np.float32([[0, ysize],
                           [xsize, ysize],
                           [xsize+rx , -ry],
                           [-rx, -ry]])
# 透視変換行列を生成
psp_matrix = cv2.getPerspectiveTransform(perspective1,perspective2)
# 透視変換を行い、出力
img_psp = cv2.warpPerspective(img, psp_matrix, size)

if input_file[-3:] == "npy":
    np.save(output_file, img_psp)
else:
    cv2.imwrite(output_file, img_psp)
