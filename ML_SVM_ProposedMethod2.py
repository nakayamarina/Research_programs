
# coding: utf-8

# # SVMによる学習と識別性能評価（提案手法）

# ---
#
# 引数：提案手法でベクトル化したcsvファイルがあるディレクトリまでのパス
#
# ---
#
# 入力： 提案手法でベクトル化したcsvファイル
#
# ---
#
# 出力：ACCURACY[loo]_(ファイル名)_SVM.csv　識別性能評価
#
# ---
#
# 提案手法でベクトル化したデータをSVMを用いて学習，交差検証法（leave-one-out交差検証）を用いて識別性能評価を行う．
#

# In[1]:

import numpy as np
import pandas as pd
import sys

from sklearn import cross_validation
from sklearn import svm
from sklearn.model_selection import train_test_split


# コマンドライン引数で提案手法でベクトル化したcsvファイルがあるディレクトリまでのパスを取得

# In[6]:

args = sys.argv
PATH = args[1]

# jupyter notebookのときはここで指定
# PATH = '../Data_block/analysis_by_programs/20170130ar/12ch/RawData/'

# 機械学習するデータ（提案手法でベクトル化したcsvファイル）
ML_restData = 'TDAvec_autocor_rest_custom_300_012dim.csv'
ML_tapData = 'TDAvec_autocor_tap_custom_300_012dim.csv'

# 出力するデータの行名，ファイル名
outputIndex = 'TDAvec_autocor(300, 012dim) + SVM'
outputFile = 'TDAvecAutocor012dim300'


# ## SVM_LOO関数

# 引数としてTrainingData関数で作成した教師データをX，ラベルをyで受け取る．
# 交差検証法の一つleave-one-out交差検証で識別精度評価を行う．
#
# * (1個をテストデータ，残りを教師データにして学習・評価) * すべてのデータ個
# * 得られたすべてのデータ個の評価結果（識別率）の平均を求めてパーセントに直す
# * 評価結果（識別率）をTrainingData関数に返す

# In[7]:

def SVM_LOO(X, y):

    LOOscore = np.zeros(len(X))

    # 1個をテストデータ，残りを教師データにして学習・評価
    # すべてのデータに対して行う
    for i in range(len(X)):

        print('------ ' + str(i) + ' / ' + str(len(X)) + '回 -----')

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

# In[8]:

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

# In[9]:

if __name__ == '__main__':

    # 識別率を算出

    print('\n--------- ' + outputIndex + ' Data ---------')
    PS_result = TrainingData(ML_restData, ML_tapData)
    print('\n' + str(PS_result))


    # インデックス名をつける
    result_index = [outputIndex]
    PS_result.index = result_index

    # csv書き出し
    PATH_RESULT = PATH + 'ACCURACY[loo]_' + outputFile + '_SVM.csv'
    PS_result.to_csv(PATH_RESULT, index = True)


# In[ ]:




# In[ ]:
