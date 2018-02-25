PATH_DATA="../Data_block/analysis_by_programs/"

# DIRs=`ls -F ${PATH_DATA} | grep /`
#
# for dir in $DIRs
# do
#
#   PATH="${PATH_DATA}${dir}"
#
#   echo "-------------${PATH}------------"
#
#   python result_Subject.py ${PATH}
#
#
# done

PATH="../Data_block/analysis_by_programs/20170130ar/"

python result_Subject.py ../Data_block/analysis_by_programs/20170130ar/

echo ${PATH}
