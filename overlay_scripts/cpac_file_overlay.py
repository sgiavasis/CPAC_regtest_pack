import argparse
import os
import pandas as pd
import subprocess

def process_files(output_dir, tsv_file, repository_path):
    # Read the TSV file into a DataFrame
    df = pd.read_csv(tsv_file, delimiter='\t')

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        new_filename = row['New Filename']
        overlay = row['Overlay']

        # Find files in the output directory that match the new filename
        for file in os.listdir(output_dir):
            if new_filename in file:
                file_path = os.path.join(output_dir, file)

                if overlay == "None":
                    # Run plot_nii_3dheatmap.py if overlay is None
                    filename = file.rstrip('.gz').rstrip('.nii')
                    output_png = os.path.join(output_dir, f"{filename}.png")
                    subprocess.run([
                        'python', os.path.join(repository_path, 'plot_nii_3dheatmap.py'),
                        file_path, output_png
                    ])
                else:
                    # Find reference file based on overlay
                    for ref_file in os.listdir(output_dir):
                       if overlay in ref_file and '.nii' in ref_file:
                            ref_file_path = os.path.join(output_dir, ref_file)
                            filename = file.rstrip('.gz').rstrip('.nii')
                            output_png = os.path.join(output_dir, f"{filename}.png")
                            subprocess.run([
                                'python', os.path.join(repository_path, 'plot_nii_overlay.py'),
                                file_path, output_png, '-b', ref_file_path
                            ])
                            break

def main():
    parser = argparse.ArgumentParser(description='Process files according to a TSV mapping file.')
    parser.add_argument('output_dir', type=str, help='Path to the output directory')
    parser.add_argument('tsv_file', type=str, help='Path to the TSV file containing mappings')
    parser.add_argument('repository_path', type=str, help='Path to the GitHub repository containing scripts')
    
    args = parser.parse_args()
    
    process_files(args.output_dir, args.tsv_file, args.repository_path)

if __name__ == "__main__":
    main()

