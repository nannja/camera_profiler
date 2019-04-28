#coding:utf-8
#descriptiton: rscanのプロット用プログラムです。
#あるディレクトリ以下のrsan結果をオーバープロットします。

import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys
import re
import glob

#[settings]
rscanfile = "../npydatam/rscan/npy_BCD/*" # rscan結果のディレクトリ。/*で指定。
#rscanfile = "../npydatam/rscan/npy_A/*" # rscan結果のディレクトリ。/*で指定。
r_step = 1 # 整数のみ

if __name__ == "__main__":
    """実行関数です。"""

    rscanfiles = glob.glob(rscanfile)
    #linenames = ["#4","#3", "#2", "#1" ]
    linenames = ["#10", "#9", "#7", "#8", "#6","#5"]
    #linenames = ["A φ10","A φ15", "A φ20", "No aperture" ]
    #linenames = ["A φ15, B φ15, C φ15, D φ15, E φ15", "A φ15, B φ15, C φ15, D φ15", "A φ15, B φ15, C φ15", "A φ15, B φ15, D φ15", "A φ15, B φ15","A φ15, B φ20"]
    k = 0

    for i in rscanfiles:
        scan_result = np.load(i)
        # logplotのとき
        for j in np.arange(len(scan_result[1])):
            if scan_result[1][j] > 1.1:
                scan_result[1][j] = np.log(scan_result[1][j])
            else:
                scan_result[1][j] = None
        #ここまで
        plt.scatter(scan_result[0], scan_result[1])
        plt.plot(scan_result[0], scan_result[1], label=linenames[k])
        k = k+1
    #plt.title('Radial profile at the position A',fontsize=14)
    plt.title('Radial profile at the positions from A to E',fontsize=14)
    xticks = []
    for i in scan_result[0]:
        xticks.append(str(int(i*10+5)))
    plt.xticks(scan_result[0],xticks)
    #plt.gca().ticklabel_format(style="sci", scilimits=(0,0), axis="y") # log plotのとき
    plt.xlabel("Radius of concentric area [mm]", fontsize=14)
    plt.ylabel('Intensity per area [a.u.]', fontsize=14)
    plt.yscale("log") # logplotのとき
    plt.grid(which="both")
    plt.tight_layout()
    plt.xlim([2,15])
    plt.legend(fontsize=11).get_frame().set_alpha(1)
    plt.show()
