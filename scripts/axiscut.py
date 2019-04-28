# coding:utf-8
# description: トムソン迷光対策解析用のプログラムです。
# 円の中心でx方向y方向に切って分布を表示する画像解析を行います。
# how to use: python axiscut.py

import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob
import sys

#[settings]
img_file = "../data/touhou/touhoum.jpg" # 解析する画像です。
img_npy = "../npydata/etc/touhou.npy" # 解析する画像の中間ファイル(npy)です。本来は負の値もちゃんと表示するためにnpyを使いますが、もし中間ファイルがなく画像をそのまま解析する場合は0を指定してください。

#[hole]
# 何回かスクリプトを動かして画像を見ながら穴の中心に設定します。
x_center = 1033   # 穴の中心x座標、デフォルト値1095で表示しずれていたら適宜調整
y_center = 573   # 穴の中心y座標、デフォルト値618で表示しずれていたら適宜調整
r_pixel = 55 # ピクセルでの穴の大きさの設定

#[constant]
r_cm = 2 # 穴の大きさ
r_ratio = r_pixel/r_cm # ピクセルに変換


if __name__ == "__main__":
    """実行関数です。"""

    # 読み込み。画像そのままの場合の条件分岐あり。
    img = cv2.imread(img_file)
    if img_npy == 0:
        img_npy = img
    else:
        img_npy = np.load(img_npy)

    # オリジナル画像のプロット
    plt.subplot(2,2,2)
    plt.xticks([0,20*r_ratio,40*r_ratio,60*r_ratio,80*r_ratio],[0,200,400,600,800])
    plt.yticks([0,20*r_ratio,40*r_ratio,60*r_ratio,80*r_ratio],[0,200,400,600,800])
    img = cv2.circle(img, (x_center, y_center), int(2*r_ratio), (250,0,0), 3)
    plt.imshow(img, cmap="gray")
    #plt.scatter(x_center, y_center, s=10, marker="o")
    plt.title('Original Image')
    plt.xlabel('X [mm]')
    plt.ylabel('Y [mm]')

    #x軸の画像の中心の列を抽出して表示
    plt.subplot(2,2,1)
    plt.xticks([0,20*r_ratio,40*r_ratio,60*r_ratio,80*r_ratio],[0,200,400,600,800])
    y = img_npy[:,x_center]
    plt.plot(y)
    #plt.plot(y_ave)
    plt.ylim([-30,250])
    plt.xlim([1535,0])
    plt.xlabel('Y [mm]')
    plt.ylabel('Intensity [a.u.]')
    plt.title('Y distribution')

    #y軸の画像の中心の行を抽出して表示
    plt.subplot(2,2,4)
    plt.xticks([0,20*r_ratio,40*r_ratio,60*r_ratio,80*r_ratio],[0,200,400,600,800])
    x = img_npy[y_center,:]
    plt.plot(x)
    plt.ylim([-30,250])
    plt.xlabel('X [mm]')
    plt.ylabel('Intensity')
    plt.title('X distribution')

    plt.tight_layout()
    plt.show()
