PATH_DATA="../Data_block/"

DIRs=`ls -F ${PATH_DATA} | grep /`

for dir in $DIRs
do

  for image_method in 12ch 32ch mb
  do

    PATH_voxel="${PATH_DATA}${dir}${image_method}/"

    echo "------------ ${PATH_voxel} ---------------"
    python Preprocessing_block.py ${PATH_voxel}


    PATH_RAW="${PATH_DATA}${dir}${image_method}/RawData/"

    echo "------------ ${PATH_RAW} ---------------"
    python MovingAverageLine.py ${PATH_RAW}

    python TAUautocor.py ${PATH_RAW}

    Rscript TDAvec_autocor.r ${PATH_RAW}


    PATH_MAL="${PATH_DATA}${dir}${image_method}/MAL5/"

    echo "------------ ${PATH_MAL} ---------------"
    python TAUautocor.py ${PATH_MAL}

    Rscript TDAvec_autocor.r ${PATH_MAL}

  done

done
