
# coding: utf-8

# # SVMによる学習と識別性能評価（生データ&特徴データ）

# ---
#
# 引数：raw_tap.csv/raw_rest.csv/TDAvec_autocor_tap.csv/TDAvec_autocor_rest.csvがあるディレクトリまでのパス
#
# ---
#
# 入力：
# * raw_tap.csv/raw_rest.csv
# * TDAvec_autocor_tap.csv/TDAvec_autocor_rest.csv
#
# ---
#
# 出力：ACCURACYts[loo][k_list].csv　識別性能評価結果一覧
# k_listはk-分割交差検証法で用いた分割数
#
# ---
#
# 生データ（生データ or 生データに移動平均線を適用したデータ）と特徴抽出したデータをSVMを用いて学習し，
# 交差検証法（k-分割交差検証，leave-one-out交差検証）を用いて識別性能評価を行う．
# ベクトル：あるボクセルのscan数分のデータ（時系列データ）
#

# In[1]:

import numpy as np
import pandas as pd
import sys

from sklearn import cross_validation
from sklearn import svm
from sklearn.model_selection import train_test_split


# コマンドライン引数でraw_tap.csv/raw_rest.csv/TDAvec_autocor_tap.csv/TDAvec_autocor_rest.csvがあるディレクトリまでのパスを取得

# In[2]:

args = sys.argv
PATH = args[1]

# jupyter notebookのときはここで指定
#PATH = '../Data_block/20170130ar/12ch/MAL5/'


# In[3]:

# RawDataディレクトリかMALディレクトリか識別用
DIRs = PATH.split("/")
DATA_NAME = DIRs[len(DIRs) - 2]

# k-分割交差検証用
k_list = [3, 5, 7]


# ## SVM_LOO関数

# 引数としてTrainingData関数で作成した教師データをX，ラベルをyで受け取る．
# 交差検証法の一つleave-one-out交差検証で識別精度評価を行う．
#
# * (1個をテストデータ，残りを教師データにして学習・評価) * すべてのデータ個
# * 得られたすべてのデータ個の評価結果（識別率）の平均を求めてパーセントに直す
# * 評価結果（識別率）をTrainingData関数に返す

# In[4]:

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
# * データとラベルをSVM_LOO関数，SVM_kCV関数に渡す
# * 帰ってきた識別率をまとめてmain関数に返す

# In[6]:

def TrainingData(file_rest, file_tap):

    # 読み込みたいファイルのパス
    PATH_rest = PATH + file_rest
    PATH_tap = PATH + file_tap

    # csvファイル読み込み
    rest = pd.read_csv(PATH_rest, header = 0)
    tap = pd.read_csv(PATH_tap, header = 0)

    # 時系列データをベクトル化したいので，生データの場合は転置をしておく
    #（元の生データ　横軸：ボクセル，縦軸：scan数（時系列データ）ー＞　転置後　横軸：scan数（時系列データ），縦軸：ボクセル）
    if file_rest == 'raw_rest.csv':
        rest = rest.T
        tap = tap.T


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
    results = pd.DataFrame({col_name : [result_LOO] })


    # 学習とk-分割交差検証

    print('k-hold Cross-Validation')

    # k_listに従って学習・評価
    for i in k_list:

        col_name = 'k = ' + str(i)

        #print(col_name)

        # SVM_CV関数
        result_CV = SVM_kCV(X, y, i)

        # 評価結果（識別率）をデータフレームに変換・格納
        result_CV = pd.DataFrame({col_name : [result_CV] })
        results = pd.concat([results, result_CV], axis = 1)

    return results




# ## main関数

# In[7]:

if __name__ == '__main__':

    # 生データの識別率

    print('--------- ' + DATA_NAME + ' ---------')
    raw_result = TrainingData('raw_rest.csv', 'raw_tap.csv')
    print('\n' + str(raw_result))

    # 特徴抽出データの識別率

    print('\n--------- Feature Extraction Data ---------')
    fe_result = TrainingData('TDAvec_autocor_rest.csv', 'TDAvec_autocor_tap.csv')
    print('\n' + str(fe_result))

    # 生データと特徴抽出データの識別率をまとめる
    result_cmp = pd.concat([raw_result, fe_result], axis = 0)

    # インデックス名をつける
    result_index = [DATA_NAME, 'TDAvec_autocor']
    result_cmp.index = result_index

    # csv書き出し
    PATH_RESULT = PATH + 'ACCURACYts[loo]' + str(k_list) + '_SVM.csv'
    result_cmp.to_csv(PATH_RESULT, index = True)


# In[ ]:




# In[ ]:
