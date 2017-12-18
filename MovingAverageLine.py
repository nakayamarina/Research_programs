
# coding: utf-8

# # ノイズ除去のための移動平均線
# ---
#
# 引数：raw_tap.csv/raw_rest.csvがあるディレクトリまでのパス
#
# ---
#
# 入力：raw_tap.csv/raw_rest.csv
#
# ---
#
# 出力：
# * MAL[区間]/raw_tap.csv：Tapping時のデータに移動平均線を用いることでノイズ除去をしたもの
# * MAL[区間]/raw_rest.csv：Rest時のデータに移動平均線を用いることでノイズ除去をしたもの
# * MAL[区間]/MAL_image/voxel[ボクセル番号]_Tapping.png：Tapping時の各ボクセルの元データと移動平均線を重ねてプロットしたもの
# * MAL[区間]/MAL_image/voxel[ボクセル番号]_Rest.png：Rest時の各ボクセルの元データと移動平均線を重ねてプロットしたもの
#
# [区間]には移動平均線を求める際の区間数 変数section
# [ボクセル番号]には列名にもあるボクセルの数
#
# ---
#
# Preprocessing_block.pyでまとめた，
#
# * Tapping時の複数ボクセル（raw_tap.csv）
# * Rest時の複数ボクセル（raw_rest.csv）
#
# において，ノイズ除去をしたいものに対しては移動平均線（MAL : Moving Average Line）を用いる．

# In[131]:

print('########## MovingAverageLine.py program excution ############')


# In[132]:

import numpy as np
import pandas as pd
import sys
import os
import matplotlib.pyplot as plt

# jupyter notebook以外はコメントアウト
#get_ipython().magic('matplotlib inline')


# コマンドライン引数でtap_raw.csv/rest_raw.csvがあるディレクトリまでのパスを取得

# In[133]:

args = sys.argv
PATH = args[1]

# jupyter notebookのときはここで指定
#PATH = '../tameshi/20170130ar/mb/RawData/'

# 移動平均線で用いる区間
section = 5


# 後で出力するcsvファイルを保存するディレクトリ（MAL[区間]）、pngファイルを保存するディレクトリ（MAL_image）を作成

# In[139]:

# MAL[区間]のディレクトリ名・パス
DIR_MAL = PATH + '../MAL' + str(section)
PATH_MAL = DIR_MAL + '/'

# すでに存在する場合は何もせず，存在していない場合はディレクトリ作成
if not os.path.exists(DIR_MAL):
    os.mkdir(DIR_MAL)

# MAL_imageのディレクトリ名・パス
DIR_image = PATH_MAL + 'MAL_image'
PATH_image = DIR_image + '/'

# すでに存在する場合は何もせず，存在していない場合はディレクトリ作成
if not os.path.exists(DIR_image):
    os.mkdir(DIR_image)


# ## MAL関数
# 引数としてmain関数で読み込んだデータをdata、移動平均線を用いる際の区間をsection，出力画像保存先のディレクトリ名をDIR_NAMEで受け取る．
# * 出力ファイル保存用のディレクトリを作成（ディレクトリ名：AveraveMovingLine + 区間数）
# * Rest, Tappingの各ボクセルごとの移動平均線を求めて元データとの比較用にplot --> pngで出力，上記ディレクトリに保存
# * Rest, Tappingの各ボクセルごとの移動平均線を求めて返す

# In[135]:

def MAL(data, task):

    # 求めた移動平均線を格納するためのデータフレームを準備する
    # =だけではコピー元の値も変わってしまうので、copy()を使う
    MAL_data = data.copy()

    # ボクセル（列）の数だけ繰り返す
    for i in range(len(data.columns)):

        # i番目のボクセルデータ抽出
        voxel = MAL_data.iloc[:, i]

        # 移動平均線を求める
        mal = pd.rolling_mean(voxel, section)

        # 求めた移動平均線を格納
        MAL_data.iloc[:, i] = mal



        # この後に出力するpngファイル名
        FILE_NAME = DIR_image + '/voxel' + str(i+1) + '_' + task + '.png'

        # 元データをplot
        plt.plot(data.iloc[:, i], label = 'fMRIdata')

        # 移動平均線のグラフのラベル
        label_MAL = 'Moving Average Line (' + str(section) + ')'

        # 移動平均線を重ねて点線でplot
        plt.plot(mal, linestyle="dashed", label = label_MAL)

        # グラフのタイトル
        graph_name = 'fMRIdata : ' + task + '-voxel' + str(i+1)
        plt.title(graph_name)

        # グラフの凡例
        plt.legend()


        # ファイル名をつけて保存，終了
        plt.savefig(FILE_NAME)
        plt.close()

        print(FILE_NAME)

    # 移動平均線を用いるとNaNが発生するので除去
    MAL_data = MAL_data.dropna()

    return MAL_data


# ## main関数
# * tap_raw.csv/rest_raw.csv読み込み

# In[136]:

if __name__ == '__main__':


    # 読み込みたいファイルのパス
    PATH_rest = PATH + 'raw_rest.csv'
    PATH_tap = PATH + 'raw_tap.csv'

    # csvファイル読み込み
    rest = pd.read_csv(PATH_rest, header = 0)
    tap = pd.read_csv(PATH_tap, header = 0)


# In[137]:

MAL_rest = MAL(rest, 'Rest')

MAL_tap = MAL(tap, 'Tapping')


# In[138]:

# csv書き出し
PATH_REST = PATH_MAL + 'raw_rest.csv'
MAL_rest.to_csv(PATH_REST, index = False)
PATH_TAP = PATH_MAL + 'raw_tap.csv'
MAL_tap.to_csv(PATH_TAP, index = False)


# In[ ]:
