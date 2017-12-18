
# coding: utf-8

# # 実験（ブロックデザイン）から得られたfMRIデータの前処理
# ----
#
# 引数：Y01.csv, Y02.csv,... があるディレクトリまでのパス
#
# ---
#
# 入力：Y01.csv, Y02.csv,...
#
# ---
#
# 出力：
# * RawData/raw_all.csv : すべてのボクセルのZ-scoreをまとめたもの
# * RawData/raw_rest.csv : Rest時のZ-scoreだけをまとめたもの
# * RawData/raw_tap.csv : Tapping時のZ-scoreだけをまとめたもの
# * RawData/Raw_image/voxel[ボクセル番号]_Tapping.png：Tapping時の各ボクセルのデータをプロットしたもの
# * RawData/Raw_image/voxel[ボクセル番号]_Rest.png：Rest時の各ボクセルのデータをプロットしたもの
#
# [ボクセル番号]には列名にもあるボクセルの数
#
# ----
#
#
# /VoxelディレクトリのY01.csv, Y02.csv, ... のデータには，指のタッピング運動時に賦活しているとされる上位10ボクセルそれぞれのZ-score（賦活度合いみたいなもの）が記録されている．
#
# 実験デザインは以下のようになっており，（撮像方法は12ch, 32ch Head coil, Multi-bandの3種類）
#
# [12ch or 32ch Head coil]
#
# 120 scan（360s）
# TR 3s / 1scan
#
# 1-10:	Rest
# 11-20:  Tapping
# 21-30:	Rest
# 31-40:  Tapping
# 41-50:	Rest
# 51-60:  Tapping
# 61-70:	Rest
# 71-80:  Tapping
# 81-90:	Rest
# 91-100:  Tapping
# 101-110: Rest
# 111-120:  Tapping
#
# [32ch Multi-band]
#
# 360 scan（360s）
# TR 1s / 1scan
#
# 1-30:	Rest
# 31-60:  Tapping
# 61-90:	Rest
# 91-120:  Tapping
# 121-150: Rest
# 151-180: Tapping
# 181-210: Rest
# 211-240: Tapping
# 241-270: Rest
# 271-300: Tapping
# 301-330: Rest
# 331-360: Tapping
#
#
# Z-scoreはこの実験デザインに従って記録されている．
# ここでは，Rest時とTapping時を分別して順番に並べることで時系列データを得る．
#
#

# In[169]:

print('########## Preprocessing.py program excution ############')


# In[170]:

import glob
import sys
import pandas as pd
import matplotlib.pyplot as plt
import os


# コマンドライン引数で/Voxelディレクトリまでのパスを取得

# In[171]:

args = sys.argv
PATH = args[1]

# jupyter notebookのときはここで指定
#PATH = '../tameshi/20170130ar/12ch/Voxel/'


# 後で出力するcsvファイルを保存するディレクトリ（RawData）、pngファイルを保存するディレクトリ（Raw_image）を作成

# In[172]:

# RawDataのディレクトリ名・パス
DIR_RAW = PATH + '../RawData'
PATH_RAW = DIR_RAW + '/'

# すでに存在する場合は何もせず，存在していない場合はディレクトリ作成
if not os.path.exists(DIR_RAW):
    os.mkdir(DIR_RAW)

# Raw_imageのディレクトリ名・パス
DIR_image = PATH_RAW + 'Raw_image'
PATH_image = DIR_image + '/'

# すでに存在する場合は何もせず，存在していない場合はディレクトリ作成
if not os.path.exists(DIR_image):
    os.mkdir(DIR_image)


# ## splitRT関数
#
# 引数に１ブロックのscan数を受け取り，Rest時とTapping時のデータを分けてcsvファイルで書き出し

# In[173]:

def splitRT(brain, number_scan):

    # Rest，Tappingのデータ抽出用maskを作成
    # （行数 // number_scan）% 2　で割り切れる（0）ならRest，割り切れない（1）のであればTapping
    # （除算は '//' としないと小数まで計算される）

    mask_R = (brain.index // number_scan) % 2 == 0
    mask_T = (brain.index // number_scan) % 2 == 1

    # mask適用
    data_rest = brain[mask_R]
    data_tap = brain[mask_T]

    # csv書き出し
    PATH_REST = PATH_RAW + 'raw_rest.csv'
    data_rest.to_csv(PATH_REST, index = False)
    PATH_TAP = PATH_RAW + 'raw_tap.csv'
    data_tap.to_csv(PATH_TAP, index = False)

    plotIMAGE(data_rest, 'Rest')
    plotIMAGE(data_tap, 'Tapping')


# ## plotIMAGE関数
#

# In[174]:

def plotIMAGE(data, task):

    # indexが連番になっていないのでreset_indexで番号を振り直す
    # drop=Trueにしなければ古いindexが新しい列として追加されてしまう
    data = data.reset_index(drop = True)

    # ボクセル（列）の数だけ繰り返す
    for i in range(len(data.columns)):

        # この後に出力するpngファイル名
        FILE_NAME = DIR_image + '/voxel' + str(i+1) + '_' + task + '.png'

        # データをplot
        plt.plot(data.iloc[:, i], label = 'fMRIdata')

        # グラフのタイトル
        graph_name = 'fMRIdata : ' + task + '-voxel' + str(i+1)
        plt.title(graph_name)

        # グラフの凡例
        plt.legend()

        # ファイル名をつけて保存，終了
        plt.savefig(FILE_NAME)
        plt.close()

        print(FILE_NAME)


# ## main関数

# * fMRIデータ読み込み
# * 全ボクセルデータ連結
# * 全ボクセルデータをcsvで書き出し

# In[175]:

if __name__ == '__main__':
    # /Voxelディレクトリ内のcsvファイルのパスを取得
    csv_file = PATH + '*.csv'
    files = []
    files = glob.glob(csv_file)


# In[176]:

# 1つ目のファイルを読み込む

# 列名
row_name = "Voxel1"

# 列名をつけてデータフレームとして読み込み（row_nameの後に','をつけることで1列だけ名前をつけることができる）
brain = pd.read_csv(files[0], names=(row_name,))


# In[177]:

# 同様に2つ目以降のファイルをデータフレームとして読み込み，1つ目のデータフレームに横連結
for i in range(1, len(files)):

    row_name = "Voxel" + str(i+1)
    data = pd.read_csv(files[i], names=(row_name,))

    brain = pd.concat([brain, data], axis = 1)


# In[178]:

# 全ボクセルデータをcsv書き出し
PATH_BRAIN = PATH_RAW + 'all_raw.csv'
brain.to_csv(PATH_BRAIN, index = False)


# In[179]:

# 12ch or 32ch Head coil の場合
if len(brain) == 120:

    splitRT(brain, 10)


# In[180]:

# 32ch Milti-band の場合
if len(brain) == 360:
    splitRT(brain, 30)


# In[ ]:
