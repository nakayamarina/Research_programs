
# coding: utf-8

# # SVMによる学習と識別性能評価（生データ&特徴データ）

# ---
#
# 引数：RAWvec_SPMts_tap.csv/RAWvec_SPMts_rest.csvがあるディレクトリまでのパス
#
# ---
#
# 入力：
# * RAWvec_SPMts_tap.csv/RAWvec_SPMts_rest.csv
#
# ---
#
# 出力：ACCURACY[loo]_SVM_SPMts.csv　識別性能評価結果一覧
#
# ---
#
# SPMと時系列性を踏まえてベクトル化したデータをSVMを用いて学習し，
# 交差検証法（leave-one-out交差検証）を用いて識別性能評価を行う．
# ※ 生データや従来手法の(Raw_pt, Raw_ts)は以前算出したため今回は出力しないので，result0901.xlsxなどを参照
#

# In[6]:

import numpy as np
import pandas as pd
import sys

from sklearn import cross_validation
from sklearn import svm
from sklearn.model_selection import train_test_split


# コマンドライン引数でRAWvec_SPMts_tap.csv/RAWvec_SPMts_rest.csvがあるディレクトリまでのパスを取得

# In[11]:

args = sys.argv
PATH = args[1]

# jupyter notebookのときはここで指定
# PATH = '../Data_block/analysis_by_programs/20170130ar/12ch/RawData/'


# ## SVM_LOO関数

# 引数としてTrainingData関数で作成した教師データをX，ラベルをyで受け取る．
# 交差検証法の一つleave-one-out交差検証で識別精度評価を行う．
#
# * (1個をテストデータ，残りを教師データにして学習・評価) * すべてのデータ個
# * 得られたすべてのデータ個の評価結果（識別率）の平均を求めてパーセントに直す
# * 評価結果（識別率）をTrainingData関数に返す

# In[12]:

def SVM_LOO(X, y):

    LOOscore = np.zeros(len(X))

    # 1個をテストデータ，残りを教師データにして学習・評価
    # すべてのデータに対して行う
    for i in range(len(X)):

        # テストデータ
        X_test = X[i].reshape(1, -1)
        y_test = y[i].reshape(1, -1)

        # テストデータとして使用するデータを除いた教師データを作成
        X_train = np.delete(X, i, 0)
        y_train = np.delete(y, i, 0)

        # 線形SVMのインスタンスを生成
        model = svm.SVC(kernel = 'linear', C = 1)

        # モデルの学習
        model.fit(X_train, y_train)

        # 評価結果（識別率）を格納
        LOOscore[i] = model.score(X_test, y_test)


    # 評価結果（識別率）の平均を求める
    result = LOOscore.mean()

    # パーセントに直す
    result = round(result * 100, 1)

    print(str(LOOscore) + '\n')

    return result


# ## TrainingData関数
# 引数として読み込みたいTapping/Restのそれぞれのファイル名をfile_tap/file_restで受け取る．
# * 機械学習にかけれるようにデータのベクトル化とラベルを作成
# * データとラベルをSVM_LOO関数に渡す
# * 帰ってきた識別率をmain関数に返す

# In[13]:

def TrainingData(file_rest, file_tap):

    # 読み込みたいファイルのパス
    PATH_rest = PATH + file_rest
    PATH_tap = PATH + file_tap

    # csvファイル読み込み
    rest = pd.read_csv(PATH_rest, header = 0)
    tap = pd.read_csv(PATH_tap, header = 0)

    # RestとTappingのデータをまとめる
    all_data = pd.concat([rest, tap], axis = 0)

    # ベクトル化
    X = all_data.as_matrix()

    # ラベル作成
    label_rest = np.zeros(len(rest.index))
    label_tap = np.ones(len(tap.index))

    y = np.r_[label_rest, label_tap]


    # 学習とleave-one-out交差検証

    print('leave-one-out')

    col_name = 'leave-one-out'

    #print(col_name)

    # SVM_LOO関数
    result_LOO = SVM_LOO(X, y)

    # 評価結果（識別率）をデータフレームに変換・格納
    ac = pd.DataFrame({col_name : [result_LOO] })

    return ac




# ## main関数

# In[16]:

if __name__ == '__main__':

    # 識別率

    print('\n--------- SPM + TimeSeries Data ---------')
    SPMts_result = TrainingData('RAWvec_SPMts_rest.csv', 'RAWvec_SPMts_tap.csv')
    print('\n' + str(SPMts_result))


    # インデックス名をつける
    result_index = ['SPM + TimeSeries']
    SPMts_result.index = result_index

    # csv書き出し
    PATH_RESULT = PATH + 'ACCURACY[loo]_RAWvecSPMts_SVM.csv'
    SPMts_result.to_csv(PATH_RESULT, index = True)


# In[ ]:




# In[ ]:
