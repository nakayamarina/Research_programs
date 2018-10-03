
# coding: utf-8

# # SVMによる学習と識別性能評価（生データ+SPM（パターン））

# ---
#
# 引数：raw_rest.csv/raw_tap.csvファイルがあるディレクトリまでのパス
#
# ---
#
# 入力：raw_rest.csv/raw_tap.csv
#
# ---
#
# 出力：ACCURACY[k_cv]_SVM_SVM.csv　識別性能評価
#
# ---
#
# 各ボクセルの値をベクトルとしてSVMを用いて学習，交差検証法（kー分割交差検証）を用いて識別性能評価を行う．
#

# In[3]:

import numpy as np
import pandas as pd
import sys

from sklearn import cross_validation
from sklearn import svm
from sklearn.model_selection import train_test_split


# コマンドライン引数でraw_rest.csv/raw_tap.csvファイルがあるディレクトリまでのパスを取得

# In[4]:

args = sys.argv
PATH = args[1]

# jupyter notebookのときはここで指定
# PATH = '../Data_tappingState-2fe_Active/analysis_by_programs/20171020rn/12ch/RawData/'

# 機械学習するデータ（提案手法でベクトル化したcsvファイル）
ML_restData = 'raw_rest.csv'
ML_tapData = 'raw_tap.csv'

# 出力するデータの行名，ファイル名
outputIndex = 'SPM + SVM'
outputFile = 'SPM'


# ## SVM_kCV関数

# 引数としてTrainingData関数で作成した教師データをX，ラベルをy，データ分割数をkで受け取る．
# 交差検証法の一つk-分割交差検証で識別精度評価を行う．
#
# * 学習
# * (k分割し，1グループをテストデータ，残りグループを教師データにして評価) * k
# * 得られたk個の評価結果（識別率）の平均を求めてパーセントに直す
# * 評価結果（識別率）をTrainingData関数に返す

# In[5]:

def SVM_kCV(X, y, k):

    # 線形SVMのインスタンスを生成
    model = svm.SVC(kernel = 'linear', C = 1)

    # k分割し，1グループをテストデータ，残りグループを教師データにして評価
    # すべてのグループに対して行う
    # 評価結果（識別率）を格納
    CVscore = cross_validation.cross_val_score(model, X, y, cv = k)

    # 評価結果（識別率）の平均を求める
    result = CVscore.mean()

    # パーセントに直す
    result = round(result * 100, 1)

    print('k = ' + str(k) + '：' + str(CVscore))

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

    # ラベル作成用
    label_rest = np.zeros(len(rest.index))
    label_tap = np.ones(len(tap.index))


    # ベクトル化＆ラベル作成

    for i in range(rest.shape[1]):

        # RestとTappingのデータをまとめる
        if(i == 0):

            rest_df = pd.DataFrame(rest.iloc[:,i])
            tap_df = pd.DataFrame(tap.iloc[:,i])

            all_data = pd.concat([rest_df, tap_df], axis = 0)

            all_data.columns = ['Voxel']

            #ラベル
            y = np.r_[label_rest, label_tap]

        else:

            rest_df = pd.DataFrame(rest.iloc[:,i])
            tap_df = pd.DataFrame(tap.iloc[:,i])

            new_data = pd.concat([rest_df, tap_df], axis = 0)
            new_data.columns = ['Voxel']

            all_data = pd.concat([all_data, new_data], axis = 0)

            #ラベル
            y = np.r_[y, label_rest]
            y = np.r_[y, label_tap]

    # ベクトル化
    X = all_data.as_matrix()

    cv_k = rest.shape[0] * 2


    print('k-hold Cross-Validation')

    col_name = 'k = ' + str(cv_k)

    #print(col_name)

    # SVM_CV関数
    result_CV = SVM_kCV(X, y, cv_k)

    # 評価結果（識別率）をデータフレームに変換・格納
    ac = pd.DataFrame({col_name : [result_CV] })

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
    PATH_RESULT = PATH + 'ACCURACY[k_cv]_' + outputFile + '_SVM.csv'
    PS_result.to_csv(PATH_RESULT, index = True)


# In[ ]:




# In[ ]:
