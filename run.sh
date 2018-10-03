PATH_DATA="../Data_tappingBlock-2fe_Active/analysis_by_programs/"

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
   # python Preprocessing_state.py ${PATH_voxel}
    #
    # python TAUautocor.py ${PATH_RAW}

    # kizami = 300, 100
    # Rscript TDAvec_autocor_custom.r ${PATH_RAW}
    # Rscript TDAvec_autocor_custom2.r ${PATH_RAW}
    #
    # # remoce 2-dim hole, 300, 100
    # python ReVectrize_ProposedMethod.py ${PATH_RAW}
    # python ReVectrize_ProposedMethod2.py ${PATH_RAW}

    # python RAWvec_SPMts.py ${PATH_RAW}

    # python SVM_RAWvec_SPMts.py ${PATH_RAW}

    #
    # echo "------------ python ML_SVM_RAWts.py ---------------"
    # python ML_SVM_RAWts.py ${PATH_RAW}
    #
    # echo "------------ python ML_1dCNN_RAWts.py ---------------"
    # python ML_1dCNN_RAWts.py ${PATH_RAW}
    #

    # echo "------------ python ML_SVM_ProposedMethod.py ---------------"
    # python ML_SVM_ProposedMethod.py ${PATH_RAW}
    #

    #
    # echo "------------ python ML_1dCNN_ProposedMethod.py ---------------"
    # python ML_1dCNN_ProposedMethod.py ${PATH_RAW}

    # echo "------------ python ML_SVM_RAWpt.py ---------------"
    # python ML_SVM_RAWpt.py ${PATH_RAW}

    echo "------------ python ML_SVM_spm.py ---------------"
    python ML_SVM_spm.py ${PATH_RAW}

    #
    # PATH_MAL="${PATH_DATA}${dir}${image_method}/MAL5/"
    #
    # echo "------------ ${PATH_MAL} ---------------"
    # python TAUautocor.py ${PATH_MAL}
    #
    # Rscript TDAvec_autocor.r ${PATH_MAL}


  done

done
