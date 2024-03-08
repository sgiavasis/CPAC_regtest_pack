import argparse
import os
import pandas as pd
import shutil
import glob
import subprocess

def process_files(root_dir, tsv_file, output_dir):
    # Read the TSV file into a DataFrame
    df = pd.read_csv(tsv_file, delimiter='\t')

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        wildcard_path = os.path.join(root_dir, row['Wildcard Path'])

        # Use glob to find files matching the wildcard path and ending with .nii or .nii.gz
        files = glob.glob(os.path.join(wildcard_path, '*.nii')) + glob.glob(os.path.join(wildcard_path, '*.nii.gz')) + \
                glob.glob(f"{wildcard_path}*.nii*")

        # If files are found for this wildcard path, process the first one and move to the next wildcard path
        if files:
            file = files[0]  # Take the first file found
            # Extract subject ID and scan ID from the path
            subject_id = file.split('cpac_sub-')[1].split('/')[0]
            scan_id = file.split('_scan_')[1].split('/')[0] if '_scan_' in file else None

            # Construct the new filename
            new_filename = f"{subject_id}_{row['New Filename']}"
            if scan_id:
                new_filename = f"sub-{subject_id}_scan-{scan_id}_{row['New Filename']}"
            else:
                new_filename = f"sub-{subject_id}_{row['New Filename']}"

            # Copy the file to the output directory with the new filename
            if 'nii.gz' in file:
                new_filename += '.nii.gz'
            elif '.gz' in file:
                new_filename += '.gz'

            new_file = os.path.join(output_dir, new_filename)
            
            if row['Timeseries'] == 'Yes':
                subprocess.run(['3dcalc', '-a', f"{file}[0]", '-expr', 'a', '-prefix', new_file])
            else:
                shutil.copy(file, new_file)
            
            print(f"Copied {file} to {new_filename}")

            # Move to the next wildcard path
            continue

def main():
    parser = argparse.ArgumentParser(description='Process files according to a TSV mapping file.')
    parser.add_argument('root_dir', type=str, help='Root directory containing subdirectories')
    parser.add_argument('tsv_file', type=str, help='Path to the TSV file containing mappings')
    parser.add_argument('output_dir', type=str, help='Output directory for copied files')
    
    args = parser.parse_args()
    
    process_files(args.root_dir, args.tsv_file, args.output_dir)

if __name__ == "__main__":
    main()

