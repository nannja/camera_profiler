# coding:utf-8
# description:トムソン迷光対策解析用のプログラムです。
# 任意のディレクトリ以下にある角度スキャンデータをプロットします。

import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys
import re
import glob

#[settings]
rscanfile = "./dscan_npy/*"

if __name__ == "__main__":
    """実行関数です。"""

    rscanfiles = glob.glob(rscanfile)
    for i in rscanfiles:
        scan_result = np.load(i)
        #scan_result[1] = np.log(scan_result[1]) # logplotのとき
        plt.scatter(scan_result[0], scan_result[1])
        plt.plot(scan_result[0], scan_result[1], label=i)
    d = scan_result[0]
    plt.title('D scan')
    xticks = []
    for i in scan_result[0]:
        xticks.append(str(int(i)) + " to " + str(int(d[1] + i)))
    plt.xticks(scan_result[0],xticks)
    #plt.gca().ticklabel_format(style="sci", scilimits=(0,0), axis="y") # log plotのとき
    plt.xlabel("D to " + "D + " + str(d[1]) + " [degree]")
    plt.ylabel('Intensity per Area')
    #plt.yscale("log") # logplotのとき
    plt.tight_layout()
    #plt.legend()
    plt.show()
