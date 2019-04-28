# coding: utf-8
# description: 画像を積算するpythonプログラムです。
# 任意のディレクトリ以下の画像すべてを積算し一つの画像を生成します。
# how to use: python integrate.py

import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob
import sys

#[settings]
dir = "../data/touhou/off/*"     # インプットする画像全てが入ったディレクトリ（末尾が/*と書く必要がある）
outimg = "../data/touhou/off_inte.jpg"    # 画像のアウトプット先

def integrated_img(dir):
    """
    指定のディレクトリ直下の画像を積算して、積算画像の配列を返します。すべて同じピクセル数(=同じカメラで同じ条件)である必要があります。
    """

    files = glob.glob(dir)
    img1 = cv2.imread(files[0], 0)
    img = np.zeros((img1.shape[0], img1.shape[1]))

    for file in files:
        img_load = cv2.imread(file, 0)
        img = img_load + img
    img = img / ( len(files))

    return img


if __name__ == "__main__":
    """実行関数"""
    img = integrated_img(dir)
    cv2.imwrite(outimg, img)
