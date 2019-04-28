# coding:utf-8
# author: Kawamata Yuya
# description: トムソン迷光対策解析用のプログラムです。
# 画像中心から半径幅ごとに輪切りにしてピクセル数を積算したものをプロットします。

import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys

#[settings]
#img_file = "../npydatam/differed/img/A/1_15.jpg" # 対象とする画像ファイル
#npyfile = "../npydatam/differed/npy_A/1_15.npy" # 画像ファイルの中間ファイルnpy
#rscanfile = "../npydatam/rscan/npy_A/rscan_1_15.npy" # アウトプットとなるrscanファイル
img_file = "../data/touhou/result/touhoum.jpg" # 対象とする画像ファイル
npyfile = "../data/touhou/result/touhoum.npy" # 画像ファイルの中間ファイルnpy
rscanfile = "../data/touhou/result/rscan_touhoum.npy" # アウトプットとなるrscanファイル
#hole
x_center = 1033 # 穴の中心x座標、デフォルト値1089で表示しずれていたら適宜調整。
y_center = 845 # 穴の中心y座標、デフォルト値600で表示しずれていたら適宜調整。
r_pixel = 64 # ピクセル数での穴の大きさ、デフォルト値70で表示しずれていたら適宜調整。
#ボードの穴を上の初期値による黒い円で合わせることで、ピクセルをcmに変換したり輪切りにしたりしています。
#必ず黒い円が合っているか確認してください。円周辺部が光っていることもあるので注意。
#plot
r_step = 1 # 輪切りにするstep幅です。cm指定です。
r_max = 20 # 輪切りにする最大の半径です。cm指定です。
#例えば2 cm~8 cmを出したい場合には、上からstepを8、maxを11以上で指定すれば良いです。
#二つ目の黒い円は2 cm+r_stepの半径の円なので、チェックしてみてください。

#[constant]
r_cm = 2.0 # ボード穴の半径が2 cm。
r_ratio = r_pixel/r_cm # ピクセルとcmを変換するための比率。



def cover_circle(img, x, y, r, color=0, fill = -1):
    """画像の(x, y)座標に半径r cmの黒い円を置く"""

    r = r * r_ratio
    r = int(r)
    img = cv2.circle(img, (x,y), r, color, fill)

    return img


def integrate_pix(img, x, y, r1, r2):
    """中心(x, y)で半径r1 cmからr2 cmの画像のピクセルをすべて積算し、密度を出します"""

    img1 = cover_circle(img, x, y, r1)
    sumpix1 = img1.sum()
    img2 = cover_circle(img, x, y, r2)
    sumpix2 = img2.sum()
    sumpix = sumpix1 - sumpix2

    #密度に変換
    r1 = r1 * r_ratio
    r2 = r2 * r_ratio
    area = r2*r2*np.pi - r1*r1*np.pi
    sumdensity = sumpix/area

    return sumdensity


def r_scan(img, x, y):
    """中心(x, y)からr_stepの感覚で半径2 cmからr_max cmを積算していきます"""

    r_steps = np.arange(2, r_max, r_step)
    r_scans = []
    for i in r_steps:
        r_scans.append(integrate_pix(img, x, y, i, i + r_step))
    r_scans = np.array(r_scans)

    return r_steps, r_scans


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


if __name__ == "__main__":
    """実行関数です。"""

    # オリジナル画像のプロット
    # 穴中心に半径2 cmの円と次ステップの円を置く
    img1 = cv2.imread(img_file) # カラーで画像ファイルからロード
    img1 = cover_circle(img1, x_center, y_center, 2.0, (250,0,0), 5)
    #img1 = cover_circle(img1, x_center, y_center, 15, (250,0,0), 5)
    #img1 = uint8_img(img1)
    plt.subplot(1,2,1)
    plt.imshow(img1, cmap="gray")
    plt.title('Original Image', fontsize=20)
    x = np.array(range(len(img1[0])))
    plt.xticks([0,20*r_ratio,40*r_ratio,60*r_ratio],[0,200,400,600], fontsize=14)
    plt.yticks([0,20*r_ratio,40*r_ratio],[0,200,400], fontsize=14)
    #plt.xticks([0,20*r_ratio,40*r_ratio],[0,200,400])
    #plt.yticks([0,20*r_ratio],[0,200])
    plt.xlabel('X [mm]', fontsize=20)
    plt.ylabel('Y [mm]', fontsize=20)

    # rscan
    plt.subplot(1,2,2)
    img2 = np.load(npyfile)
    scan_result = r_scan(img2, x_center, y_center)
    np.save(rscanfile,scan_result)

    # logplotのとき
    #for j in np.arange(len(scan_result[1])):
    #    if scan_result[1][j] > 1.1:
    #        scan_result[1][j] = np.log(scan_result[1][j])
    #    else:
    #        scan_result[1][j] = None
    #plt.yscale("log") # logplotのとき
    #ここまで

    plt.grid(which="both")
    plt.scatter(scan_result[0], scan_result[1])
    plt.plot(scan_result[0], scan_result[1])
    plt.title('Radius profile', fontsize=20)
    xticks = []

    for i in scan_result[0]:
        xticks.append(str(i*10+5))
    plt.xticks(scan_result[0],xticks, fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlim(2,19)
    #plt.gca().ticklabel_format(style="sci", scilimits=(0,0), axis="y")
    plt.xlabel("Radius of concentric area [mm]", fontsize=20)
    plt.ylabel('Intensity per area [a.u.]', fontsize=20)

    #plt.tight_layout()
    plt.show()
