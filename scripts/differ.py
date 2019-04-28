# coding:utf-8
# descriptiton: トムソン迷光対策解析用のプログラムです。
# 画像からバックグラウンドを引いて出力します。
# how to use: python differ.py

import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob
import sys

#[settings]
img_file = "../data/touhou/on_inte.jpg" # 差し引かれるレーザー画像
img_back_file = "../data/touhou/off_inte.jpg" # 差し引くバックグラウンド画像
img_outfile = "../data/touhou/touhou.jpg" # 画像ファイルのアウトプット先
npyfile = "../npydata/etc/touhou.npy" # 中間ファイルのアウトプット先、負の値を扱うので必要


def float_img(img):
    """
    指定の画像の配列の値をfloat型にします。複数の画像の配列を計算処理する場合には必須です。
    """

    img_zeros = np.zeros((img.shape[0], img.shape[1]))
    img_float = img_zeros + img

    return img_float


def uint8_img(img):
    """
    指定の画像の配列の値をfloat型からuint8型にします。
    10以下は0に、250以上は250にします。
    """
    #img_clip = np.clip(img, 0, 250)
    img_clip = np.where(img < 10, 0, img)
    img_clip = np.where(img > 255, 255, img_clip)
    img_uint8 = img_clip.astype(np.uint8)

    return img_uint8


def differ_img(img1, img2):
    """
    画像の配列を差し引きます。
    """

    img1 = float_img(img1)
    img2 = float_img(img2)
    img = img1 - img2

    return img


if __name__ == "__main__":
    """実行関数です。"""
    # 差し引き
    img = cv2.imread(img_file, 0)
    img_back = cv2.imread(img_back_file, 0)
    imgd = differ_img(img, img_back)

    np.save(npyfile, imgd)
    imgu8 = uint8_img(imgd)
#    imgu8 = cv2.GaussianBlur(imgu8,(5,5),0)
    cv2.imwrite(img_outfile, imgu8)

    # 差し引き画像のプロット
    plt.subplot(1,1,1)
    plt.imshow(imgu8, cmap="gray")
    plt.title('Differed Image')
    plt.xlabel('X pixel')
    plt.ylabel('Y pixel')

    plt.show()
