# TDAによる特徴抽出とベクトル化

# ---

# 引数：raw_tap.csv/raw_rest.csv, 時間遅れτのcsvファイルがあるディレクトリまでのパス

# ---

# 入力：raw_tap.csv/raw_rest.csv, 時間遅れτのcsvファイル(TAUautocre.csv)

# ---

# 出力：
# * TDAvec_autocor_tap.csv：前処理をしたTapping時のデータの特徴抽出を行ったもの
# * TDAvec_autocor_rest.csv：前処理をしたRest時のデータの特徴抽出を行ったもの

# [時間遅れτの求め方] autocor

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
# 穴の数をn回数えることでベクトル化する

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
# PATH = commandArgs(trailingOnly=TRUE)[1]

PATH <- '../tameshi/20170130ar/mb/'
ms <- 3


DIR_attractor <- paste(PATH, 'TDAvec_autocor_attractor', sep="")
PATH_attractor <- paste(DIR_attractor, '/', sep="")

if(!file.exists(PATH_attractor)) {
  dir.create(DIR_attractor)
}




Attractor <- function(voxel, tau, voxel_no, task){

  x <- voxel[1:(nrow(voxel) - (2*tau)), 1]
  y <- voxel[(1 + tau):(nrow(voxel) - (tau)), 1]
  z <- voxel[(1 + (2*tau)):nrow(voxel), 1]

  xyz <- cbind(x, y, z)

  graph_name <- paste("Mapping to 3dim space : ", task, "-voxel", voxel_no, sep="")
  PATH_graph <- paste(PATH_attractor, "voxel", voxel_no, '_', task, '.png', sep="")

  png(PATH_graph)
  scatterplot3d(xyz, xlab = "x = t", ylab = "y = t + τ", zlab = "z = t + 2*τ", pch = 16, type="o", main = graph_name)
  dev.off()

  print(graph_name)

  return (xyz)

}

TDAvec <- function(attractor, voxel_no){

  tda <- ripsDiag(X = attractor, maxdimension = 2, maxscale = ms)



}


PATH_rest <- paste(PATH, 'raw_rest.csv', sep = "")
PATH_tap <- paste(PATH, 'raw_tap.csv', sep = "")
PATH_tau <- paste(PATH, 'TAUautocor.csv', sep = "")

rest <- read.csv(PATH_rest)
tap <- read.csv(PATH_tap)
taus <- read.csv(PATH_tau)




for(i in 1:nrow(taus)){

  voxel_rest <- rest[i]
  voxel_tap <- tap[i]

  tau_rest <- taus[i, 1]
  tau_tap <- taus[i, 2]

  attractor_rest <- Attractor(voxel_rest, tau_rest, i, "Rest")
  attractor_tap <- Attractor(voxel_tap, tau_tap, i, "Tapping")

  #TDAvec(attractor_rest, i)
  #TDAvec(attractor_tap, i)

}
