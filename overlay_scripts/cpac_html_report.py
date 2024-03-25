import argparse
import os
import shutil
import tarfile
import pandas as pd

def generate_html(output_dir, tsv_file):
    # Read the TSV file into a DataFrame
    df = pd.read_csv(tsv_file, delimiter='\t')

    # Create a sub-directory within the output directory to store the HTML page and PNG files
    html_dir = os.path.join(output_dir, 'html_files')
    os.makedirs(html_dir, exist_ok=True)

    # Create HTML file
    html_file_path = os.path.join(html_dir, 'gallery.html')
    with open(html_file_path, 'w') as html_file:
        html_file.write('<!DOCTYPE html>\n<html>\n<head>\n<title>Image Gallery</title>\n</head>\n<body>\n')

        # Iterate through rows in the DataFrame
        for index, row in df.iterrows():
            new_filename = row['New Filename']

            # Find corresponding PNG file in the output directory
            for file in os.listdir(output_dir):
                if new_filename in file and file.endswith('.png'):
                    # Write an image tag for each PNG file with its title based on the filename
                    html_file.write(f'<h2>{file}</h2>\n')
                    html_file.write(f'<img src="{file}" alt="{file}">\n')

                    # Move PNG files to the new sub-directory
                    shutil.move(os.path.join(output_dir, file), os.path.join(html_dir, file))
                    #break

        html_file.write('</body>\n</html>')

    # Tarball the entire directory
    tarball_name = os.path.join(output_dir, 'html_files.tar.gz')
    with tarfile.open(tarball_name, 'w:gz') as tar:
        tar.add(html_dir, arcname=os.path.basename(html_dir))

def main():
    parser = argparse.ArgumentParser(description='Generate an HTML page with embedded PNG files and tarball them.')
    parser.add_argument('output_dir', type=str, help='Path to the output directory')
    parser.add_argument('tsv_file', type=str, help='Path to the TSV file containing mappings')

    args = parser.parse_args()

    generate_html(args.output_dir, args.tsv_file)

if __name__ == "__main__":
    main()

