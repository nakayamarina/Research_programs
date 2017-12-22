# TDAによる特徴抽出とベクトル化

# ---

# 引数：raw_tap.csv/raw_rest.csv, 時間遅れτのcsvファイルがあるディレクトリまでのパス

# ---

# 入力：raw_tap.csv/raw_rest.csv, 時間遅れτのcsvファイル(TAUautocre.csv)

# ---

# 出力：
# * TDAvec_autocor_tap.csv：前処理をしたTapping時のデータの特徴抽出を行ったもの
# * TDAvec_autocor_rest.csv：前処理をしたRest時のデータの特徴抽出を行ったもの
# * TDAvec_autocor_attractor/voxel[ボクセル番号]_Tapping.png
# * TDAvec_autocor_attractor/voxel[ボクセル番号]_Rest.png
# * TDAvec_autocor_barcode/voxel[ボクセル番号]_Tapping.png
# * TDAvec_autocor_barcode/voxel[ボクセル番号]_Rest.png

# [ボクセル番号]には列名にもあるボクセルの数

# ---

# 前処理（Preprocessing_block.py, MovingAverageLine.py）をした

# * Tapping時のデータ（raw_tap.csv or MAL区間_tap.csv）
# * Rest時のデータ（raw_rest.csv or MAL区間_rest.csv）

# の特徴抽出をTDAを用いて行う．

# (1) 3次元空間への写像
# Tapping時とRest時の各ボクセルの時間遅れτを用いて
# 各ボクセルの時系列データにおいてある時刻tの値，t+τの値，t+2*τの値で3次元データとする

# (2) TDA適用
# 3次元データに対してTDAのPersistent Homology適用しバーコードダイアグラムを得る

# (3) ベクトル化
# 穴の数をkizamiNumber(TDAvec関数の変数)回数えることでベクトル化する

if (!require(package = "TDA")) {
  install.packages(pkgs = "TDA")
}

if (!require(package = "scatterplot3d")) {
  install.packages(pkgs = "scatterplot3d")
}

library(TDA)
library(scatterplot3d)

print('################ TDAvec_autocor.r excution ###################')

# コマンドライン引数でraw_tap.csv/raw_rest.csv, TAUautocor.csvがあるディレクトリまでのパスを取得

#PATH <- '../tameshi/20170130ar/mb/MAL5/'
PATH = commandArgs(trailingOnly=TRUE)[1]

# TDAvec関数で使うripsDiagのmaxsxaleの値設定
ms <- 3

# TDAvec_autocor_attractorのディレクトリ名・パス
DIR_attractor <- paste(PATH, 'TDAvec_autocor_attractor', sep="")
PATH_attractor <- paste(DIR_attractor, '/', sep="")

# すでに存在する場合は何もせず，存在していない場合はディレクトリ作成
if(!file.exists(PATH_attractor)) {
  dir.create(DIR_attractor)
}

# TDAvec_autocor_barcodeのディレクトリ名・パス
DIR_tda <- paste(PATH, 'TDAvec_autocor_barcode', sep="")
PATH_tda <- paste(DIR_tda, '/', sep="")

# すでに存在する場合は何もせず，存在していない場合はディレクトリ作成
if(!file.exists(PATH_tda)) {
  dir.create(DIR_tda)
}


# main関数

# * raw_tap.csv/raw_reset.csv読み込み
# * TDAvec_autocor_tap.csv/TDAvec_autocor_rest.csv書き出し

main <- function(){

  # 読み込みたいファイルのパス
  PATH_rest <- paste(PATH, 'raw_rest.csv', sep = "")
  PATH_tap <- paste(PATH, 'raw_tap.csv', sep = "")
  PATH_tau <- paste(PATH, 'TAUautocor.csv', sep = "")

  # csvファイルの読み込み
  rest <- read.csv(PATH_rest)
  tap <- read.csv(PATH_tap)
  taus <- read.csv(PATH_tau)

  # ベクトル化したデータを格納する配列
  restVec <- c()
  tapVec <- c()

  # ボクセルの数だけ繰り返す
  for(i in 1:nrow(taus)){

    # i番目のボクセルデータ
    voxel_rest <- rest[i]
    voxel_tap <- tap[i]

    # i番目のボクセルの時間遅れτ
    tau_rest <- taus[i, 1]
    tau_tap <- taus[i, 2]

    attractor_rest <- Attractor(voxel_rest, tau_rest, i, "Rest")
    attractor_tap <- Attractor(voxel_tap, tau_tap, i, "Tapping")

    restVec <- rbind(restVec, TDAvec(attractor_rest, i, "Rest"))
    tapVec <- rbind(tapVec, TDAvec(attractor_tap, i, "Tapping"))

  }

  # csv書き出し
  PATH_restVec <- paste(PATH, 'TDAvec_autocor_rest.csv', sep = "")
  write.csv(as.data.frame(restVec), PATH_restVec, quote = FALSE, row.names = FALSE)

  PATH_tapVec <- paste(PATH, 'TDAvec_autocor_tap.csv', sep = "")
  write.csv(as.data.frame(tapVec), PATH_tapVec, quote = FALSE, row.names = FALSE)

}


# Attractor関数
# 引数としてi番目のボクセルデータをVoxel，時間遅れτをtau，何番目のボクセルかをvoxel_no，RestかTappingかをtaskで受けとる
# * 時間遅れτを使って，ある時刻tの値，t+τの値，t+2*τの値で3次元データを作る・plot --> pngで出力，TDAvec_autocor_attractorディレクトリに保存
# * 3次元データを返す

Attractor <- function(voxel, tau, voxel_no, task){

  # データをずらすことで長さが変わるので注意！

  # 元データ
  x <- voxel[1:(nrow(voxel) - (2*tau)), 1]
  # 元データからτ分ずらしたデータ
  y <- voxel[(1 + tau):(nrow(voxel) - (tau)), 1]
  # 元データから2*τ分ずらしたデータ
  z <- voxel[(1 + (2*tau)):nrow(voxel), 1]

  # 3次元データとして結合
  xyz <- cbind(x, y, z)

  # この後にplotする図形のタイトル
  graph_name <- paste("Mapping to 3dim space : ", task, "-voxel", voxel_no, sep="")

  # この後に出力するpngファイル名
  PATH_graph <- paste(PATH_attractor, "voxel", voxel_no, '_', task, '.png', sep="")

  # 3次元データをplot，出力
  png(PATH_graph)
  scatterplot3d(xyz, xlab = "x = t", ylab = "y = t + τ", zlab = "z = t + 2*τ", pch = 16, type="o", main = graph_name)
  dev.off()

  print(PATH_graph)

  return (xyz)

}

# TDAvec関数
# 引数としてi番目のボクセルデータを3次元データにしたものをattractor，何番目のボクセルかをvoxel_no，RestかTappingかをtaskで受けとる
# * ripsDiagで3次元データにTDAのPersistent Homologyを適用・バーコードplot --> png出力、TDAvec_autocor_barcodeに保存
# * 0次，1次，2次の穴情報それぞれに対してBattiNumberCount関数を使って穴の数を数え，横結合することでベクトル化
# * ベクトル化したデータを返す

TDAvec <- function(attractor, voxel_no, task){

  # TDAのPersistent Homologyを適用
  tda <- ripsDiag(X = attractor, maxdimension = 2, maxscale = ms)

  # この後でplotするバーコードのタイトル
  barcode_name <- paste("Barcode Diagram (TDA) : ", task, "-voxel", voxel_no, sep="")

  # この後で出力するpngファイル名
  PATH_barcode <- paste(PATH_tda, "voxel", voxel_no, '_', task, '.png', sep="")

  # バーコードをplot，出力
  png(PATH_barcode)
  plot(tda$diagram, barcode = TRUE, main = barcode_name)
  dev.off()

  # 穴情報を抽出
  df_tda <- as.data.frame(tda$diagram[, 1:3])

  # 各次の穴情報を分割
  zeroDim <- subset(df_tda, df_tda$dimension == 0)
  oneDim <- subset(df_tda, df_tda$dimension == 1)
  twoDim <- subset(df_tda, df_tda$dimension == 2)

  # 各次の穴の数を数え横結合することでベクトル化
  tdaVec <- c(BettiNumberCount(zeroDim), BettiNumberCount(oneDim), BettiNumberCount(twoDim))

  print(PATH_barcode)

  return(tdaVec)

}

# BettiNumberCount関数
# 引数として各次の穴情報をholeで受け取る
# * 穴を数える回数（kizamiNumber）などのパラメータを決める
# * 穴情報はそれぞれの穴発生時の直径（Birth），穴消滅時の直径（Death）が記録されており，ある時刻timeの時の穴の数を数える
# * 1×kizamiNumberのデータを返す

BettiNumberCount <- function(hole){

  # 穴を数える回数
  kizamiNumber <- 300

  # 穴をkizamiNumber回数えるために時間幅を求める
  # もともとの時間はms，kizamiNumberで割ることでどれぐらいずつ時刻timeをずらせばいいかわかる
  kizamiWidth <- ms/kizamiNumber

  # 時刻
  time <- 0

  # 穴を数えた回数
  k <- 0

  # kizamiNumber回数えた結果を格納する配列
  bettiNumbers <- c()

  # 穴が発生していればTrue
  if(nrow(hole) >= 1){

    # kizamiNumber回穴の数を数えるまでループ
    while(k != kizamiNumber){

      # 時刻timeの時の穴の数
      bettiCount <- 0

      # 発生したそれぞれの穴に対して調べる
      for(j in 1:nrow(hole)){

        # 時刻timeがある穴の発生時間中（Birth <= time <= Death）であればbettiCountに1足す
        if((hole$Birth[j] <= time) && (time <= hole$Death[j])){

          bettiCount = bettiCount + 1

        }

      }

      # bettiCountを配列に格納
      bettiNumbers <- c(bettiNumbers, bettiCount)

      # 時刻timeをずらす
      time = time + kizamiWidth

      # 穴の数を数えたのでkに1足す
      k = k + 1

    }

  } else {

    # そもそも穴が発生していなければ0をkizamiNumber個格納
    bettiNumbers <- numeric(kizamiNumber)

  }

  return(bettiNumbers)

}

# Execute main function
main()
