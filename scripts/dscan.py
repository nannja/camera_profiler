# coding:utf-8
# description:トムソン迷光対策解析用のプログラムです。角度スキャンをします。
# ピザ状に分割して強度分布の軸方向依存性を算出します。

import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys

#[files]
img_file = "../data/touhou/touhou.jpg" # 対象とする画像ファイル
npyfile = "../npydata/etc/touhou.npy"
dscanfile = "../npydata/etc/dscan_touhou.npy"

#[hole]
# 何回かスクリプトを動かして穴の中心に合わせる
x_center = 1030 # 穴の中心x座標、デフォルト値1095で表示しずれていたら適宜調整。
y_center = 570 # 穴の中心y座標、デフォルト値618で表示しずれていたら適宜調整。
r_pixel = 55 # ピクセル数での穴の大きさ、デフォルト値70で表示しずれていたら適宜調整。

#[plot]
d_step = 6 # ピザにする数です。8で45度ずつの8分割です。
d_r = 13 # ピザにする半径です。cm指定です。

#[constant]
r_cm = 2.0 # ボード穴の半径が2 cm。
r_ratio = r_pixel/r_cm # ピクセルとcmを変換するための比率。


def d_scan(img, x, y, r, step):
    r = r * r_ratio
    r = int(r)

    # ピザの和を出力
    sum_pi = []
    sum_img = img.sum()
    d = np.arange(0, 360, 360/step)
    for i in d:
        img1 = np.copy(img) # ellipeを呼び出しただけで上書きされることに注意
        img_pi = cv2.ellipse(img1, (x, y), (r, r), 0, -i, -i-d[1] , 0, -1)
        sum_pi.append(sum_img - img_pi.sum())
        del img1
        del img_pi

    # 密度に変換
    area_pi = r*r*np.pi*d[1]/360
    sum_pi = np.array(sum_pi)
    sum_pi = sum_pi/area_pi

    return sum_pi


if __name__ == "__main__":
    """実行関数です。"""

    # オリジナル画像のプロット
    # 穴中心に半径2 cmの円
    img1 = cv2.imread(img_file) # カラーで画像ファイルからロード
    img1 = cv2.circle(img1, (x_center, y_center), r_pixel, (250,0,0), 5)
    plt.subplot(1,2,1)
    plt.imshow(img1, cmap="gray")
    plt.title('Original Image')
    x = np.array(range(len(img1[0])))
    plt.xticks([0,20*r_ratio,40*r_ratio,60*r_ratio,80*r_ratio],[0,20,40,60,80])
    plt.yticks([0,20*r_ratio,40*r_ratio,60*r_ratio],[0,20,40,60])
    plt.xlabel('X [cm]')
    plt.ylabel('Y [cm]')

    # dscan
    img2 = np.load(npyfile)
    scan_result = d_scan(img2, x_center, y_center, d_r, d_step)
    scan_result = scan_result*0.3 # 調整用
    plt.subplot(1,2,2)
    d = np.arange(0, 360, 360/d_step)
    np.save(dscanfile,np.array([d,scan_result]))
    plt.scatter(d, scan_result)
    plt.plot(d, scan_result)
    plt.title('D scan')
    xticks = []
    for i in d:
        xticks.append(str(i) + " to " + str(d[1] + i))
    plt.xticks(d, xticks)
    plt.xlabel("D to " + "D + " + str(d[1]) + " degree")
    plt.ylabel('Intensity per Area')

    plt.show()
