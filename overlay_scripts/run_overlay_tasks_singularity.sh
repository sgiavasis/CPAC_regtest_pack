#!/bin/bash

# Check if all required parameters are provided
if [ "$#" -ne 6 ]; then
    echo "Usage: $0 sub_ses_workdir cpac_test_repo quickviz_repo singularity_image output_dir home_dir"
    exit 1
fi

# Extract input parameters
sub_ses_workdir="$1"
cpac_test_repo="$2"
quickviz_repo="$3"
singularity_image="$4"
output_dir="$5"
home_dir="$6"

# Execute Singularity commands
# Command 1
singularity exec -B "${home_dir}:${home_dir} \
                 -B "${cpac_test_repo}:/container/cpac_regtest_pack_repo" \
                 -B "${sub_ses_workdir}:${sub_ses_workdir}" \
                 -B "${output_dir}:/container/output_dir" \
                 "${singularity_image}" \
                 python /container/cpac_regtest_pack_repo/overlay_scripts/cpac_file_processor.py \
                 ${sub_ses_workdir} \
                 /container/cpac_regtest_pack_repo/overlay_scripts/mappings.tsv \
                 /container/output_dir

# Command 2
singularity exec -B "${home_dir}:${home_dir} \
                 -B "${cpac_test_repo}:/container/cpac_regtest_pack_repo" \
                 -B "${quickviz_repo}:/container/quickviz_repo" \
                 -B "${output_dir}:/container/output_dir" \
                 "${singularity_image}" \
                 python /container/cpac_regtest_pack_repo/overlay_scripts/cpac_file_overlay.py \
                 /container/output_dir \
                 /container/cpac_regtest_pack_repo/overlay_scripts/mappings.tsv \
                 /container/quickviz_repo/code

# Command 3
singularity exec -B "${home_dir}:${home_dir} \
                 -B "${cpac_test_repo}:/container/cpac_regtest_pack_repo" \
                 -B "${output_dir}:/container/output_dir" \
                 "${singularity_image}" \
                 python /container/cpac_regtest_pack_repo/overlay_scripts/cpac_html_report.py \
                 /container/output_dir \
                 /container/cpac_regtest_pack_repo/overlay_scripts/mappings.tsv

