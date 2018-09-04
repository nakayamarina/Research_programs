PATH_DATA="../Data_state/analysis_by_programs/"

DIRs=`ls -F ${PATH_DATA} | grep /`

for dir in $DIRs
do

  for image_method in 12ch 32ch mb
  do

    PATH_voxel="${PATH_DATA}${dir}${image_method}/"

    # echo "------------ ${PATH_voxel} ---------------"
    # python Preprocessing_block.py ${PATH_voxel}


    PATH_RAW="${PATH_DATA}${dir}${image_method}/RawData/"

    echo "------------ ${PATH_RAW} ---------------"
    # python MovingAverageLine.py ${PATH_RAW}
    #
    # python TAUautocor.py ${PATH_RAW}
    #
    # Rscript TDAvec_autocor.r ${PATH_RAW}

    # python RAWvec_SPMts.py ${PATH_RAW}

    # python SVM_RAWvec_SPMts.py ${PATH_RAW}

    Rscript TDAvec_autocor_custom.r ${PATH_RAW}

    python ReVectrize_ProposedMethod.py ${PATH_RAW}



    echo "------------ python ML_SVM_RAWts.py ---------------"
    python ML_SVM_RAWts.py ${PATH_RAW}

    echo "------------ python ML_1dCNN_RAWts.py ---------------"
    python ML_1dCNN_RAWts.py ${PATH_RAW}

    echo "------------ python ML_SVM_ProposedMethod4.py 300 01---------------"
    python ML_SVM_ProposedMethod4.py ${PATH_RAW}

    echo "------------ python ML_SVM_ProposedMethod3.py 100 01---------------"
    python ML_SVM_ProposedMethod3.py ${PATH_RAW}

    echo "------------ python ML_SVM_ProposedMethod2.py 300 012---------------"
    python ML_SVM_ProposedMethod2.py ${PATH_RAW}

    echo "------------ python ML_SVM_ProposedMethod.py 100 012---------------"
    python ML_SVM_ProposedMethod.py ${PATH_RAW}

    echo "------------ python ML_1dCNN_ProposedMethod4.py 300 01---------------"
    python ML_1dCNN_ProposedMethod4.py ${PATH_RAW}

    echo "------------ python ML_1dCNN_ProposedMethod4.py 100 01---------------"
    python ML_1dCNN_ProposedMethod3.py ${PATH_RAW}

    echo "------------ python ML_1dCNN_ProposedMethod4.py 300 012---------------"
    python ML_1dCNN_ProposedMethod2.py ${PATH_RAW}

    echo "------------ python ML_1dCNN_ProposedMethod4.py 100 012---------------"
    python ML_1dCNN_ProposedMethod.py ${PATH_RAW}

    echo "------------ python ML_SVM_RAWpt.py ---------------"
    python ML_SVM_RAWpt.py ${PATH_RAW}

    #
    # PATH_MAL="${PATH_DATA}${dir}${image_method}/MAL5/"
    #
    # echo "------------ ${PATH_MAL} ---------------"
    # python TAUautocor.py ${PATH_MAL}
    #
    # Rscript TDAvec_autocor.r ${PATH_MAL}


  done

done
