#!/bin/bash  
if [[ $# -eq 0 ]] ; then
    echo 'Please pass the path of the two directories you want to compare the files of as arguments.'
    echo 'The first argument should be the path to the 1st folder and the second argument should be the path to the 2nd folder.'
    echo 'The name of the files in the two folders to be compared should be the same.'
    exit 0
fi

path_1=$1 # path to the first folder with metric or surface files
path_2=$2 #path to bash the second folder with metric or surface files
# Please note that the file names of the two files that re to be compared in the two folders should be the same.

## For metric files (.shape.gii or .label.gii files)
file_name=()

cd $path_1
metric_files=$(find . -type f -name "*.shape.gii") # -name should have the name of the file type you want to compare. Eg "*,shape.gii", "*.label.gii"
mkdir nifti_files
mkdir "$path_2"/nifti_files
for eachfile in $metric_files
do
   
   file_name="$(<<< "${eachfile}" sed -r "s/.+\/(.+)\..+/\1/")"   
   echo $file_name
   assign_filename="$(cut -d. -f1-3 <<<$file_name)"
   echo $assign_filename
   folder=$(echo $eachfile | cut -d'/' -f 2)
   echo $folder
   nifti_file1="$path_1"/"nifti_files"/"$assign_filename"."nii"
   nifti_file2="$path_2"/"nifti_files"/"$assign_filename"."nii"
   wb_command -metric-convert -to-nifti "$path_1"/"$folder"/"$file_name"."gii" "$path_1"/"nifti_files"/"$assign_filename"."nii"
   wb_command -metric-convert -to-nifti "$path_2"/"$folder"/"$file_name"."gii" "$path_2"/"nifti_files"/"$assign_filename"."nii"
   corr_val="$(3ddot -demenan "$path_1"/"nifti_files"/"$assign_filename"."nii" "$path_2"/"nifti_files"/"$assign_filename"."nii")"
   echo "The correlation between the files" $nifti_file1 and $nifti_file2 "is" $corr_val
done


# for .surf.gii files
file_name=()
cd $path_1
surface_files=$(find . -type f -name "*.surf.gii")
mkdir nifti_files
mkdir "$path_2"/nifti_files
for eachfile in $surface_files
do
   
   file_name="$(<<< "${eachfile}" sed -r "s/.+\/(.+)\..+/\1/")"   
   echo $file_name
   assign_filename=$(echo "$file_name" | cut -d '.' -f -3)
   echo $assign_filename
   folder=$(echo $eachfile | cut -d'/' -f 2)
   echo $folder
   nifti_file1="$path_1"/"nifti_files"/"$assign_filename"."nii"
   nifti_file2="$path_2"/"nifti_files"/"$assign_filename"."nii"
   wb_command -surface-coordinates-to-metric "$path_1"/"$folder"/"$file_name"."gii" "$path_1"/"nifti_files"/"$assign_filename"."func"."gii"
   wb_command -surface-coordinates-to-metric "$path_2"/"$file_name"."gii" "$path_2"/"nifti_files"/"$assign_filename"."func"."gii"
   wb_command -metric-convert -to-nifti "$path_1"/"nifti_files"/"$assign_filename"."func"."gii" "$path_1"/"nifti_files"/"$assign_filename"."nii"
   wb_command -metric-convert -to-nifti "$path_2"/"nifti_files"/"$assign_filename"."func"."gii" "$path_2"/"nifti_files"/"$assign_filename"."nii"
   cd "/CPAC_regtest_pack" # cd to path with https://github.com/sgiavasis/CPAC_regtest_pack
   corr_val="$(python3 corr_two_ts.py  "$path_1"/"nifti_files"/"$assign_filename"."nii" "$path_2"/"nifti_files"/"$assign_filename"."nii")"
   echo "The correlation between the files" $nifti_file1 and $nifti_file2 "is" $corr_val
done

