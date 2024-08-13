import os
import shutil
import pandas as pd
import subprocess
import argparse
import errno
from itertools import  zip_longest
germ_path = "/media/bioinfoa/bioinfo2/Pragati/Common_Variant/Try/germline"
som_path = "/media/bioinfoa/bioinfo2/Pragati/Common_Variant/Try/somatic"
anno_path = "/media/bioinfoa/bioinfo2/Pragati/Common_Variant/Try/anno"
annotation_file_type = input("Enter the extension of the annotation file:")
folder_germ = os.listdir(germ_path)
folder_som = os.listdir(som_path)
folder_anno = os.listdir(anno_path)
sample_suffixes = set([file.split('-')[0] for file in folder_germ + folder_som + folder_anno])
output_base_dir = "/media/bioinfoa/bioinfo2/Pragati/Common_Variant/Try/output"
# Check
def check_columns(file_anno):
    required_columns = ['CHROM', 'POS', 'REF','ALT']  # Define the required columns here
    missing_columns = [col for col in required_columns if col not in file_anno.columns]
    if missing_columns:
        raise ValueError(f"Missing columns in file: {missing_columns}")
for tab_file in folder_anno:
    if annotation_file_type == "csv":
        file_anno = pd.read_csv(anno_path + "/" +tab_file)
    elif annotation_file_type == "tsv" or annotation_file_type == "tab":
        file_anno = pd.read_csv(anno_path + "/" + tab_file, sep='\t')
    else:
        raise ValueError(f"Unsupported file type: {tab_file}")
    #column check
    check_columns(file_anno)
# Check if files exist in all folders
'''for file_g in folder_germ:
    # Extract the prefix part of the file name
    prefix = file_g.split('-')[0]
    print(prefix)
    # Check if the corresponding file exists in both anno_path and som_path directories
    if not any(file.startswith(prefix) for file in folder_anno) or not any(file.startswith(prefix) for file in folder_som):
        raise FileNotFoundError(f"Sample not found in all folders: {prefix}")'''
# Comparing the somatic and germline files
try:
    for som, anno in zip(folder_som, folder_anno):
      # Load the annotation file once per `anno`
      annotate_file = os.path.join(anno_path, anno)
      if annotation_file_type == "csv":
          file_anno = pd.read_csv(annotate_file, index_col=0)
      elif annotation_file_type in ["tsv", "tab"]:
          file_anno = pd.read_csv(annotate_file, sep='\t', index_col=0)
      for germ in folder_germ:
          if som.split('-')[0] in germ and som.endswith("vcf.gz") and germ.endswith("vcf.gz"):
              os.makedirs(os.path.join(output_base_dir, som.split('-')[0]), exist_ok=True)
              command3 = f"bcftools isec -n +2 {os.path.join(germ_path, germ)} {os.path.join(som_path, som)} | bgzip -c > {output_base_dir}/{som.split('-')[0]}/{germ.split('.')[0]}-{som.split('.')[0]}-compare.vcf.gz"
              subprocess.run(command3, shell=True, check=True)
              filename = germ.split('.')[0] + "-" + som.split('.')[0] + "-compare.vcf.gz"
              # Add 'Present in Germline' column if applicable
              if '-B' in filename and '-cf' not in filename:
                  filepath = os.path.join(output_base_dir, germ.split('-')[0], filename)
                  compared_file = pd.read_csv(filepath, index_col=0, header=None, comment="#", sep="\t")
                  compared_file.rename(columns={0: 'CHROM', 1: 'POS', 2: 'REF', 3: 'ALT'}, inplace=True)
                  file_anno['Present in Germline'] = file_anno.apply(
                      lambda x: 'P' if any((compared_file['POS'] == x['POS']) & (compared_file['REF'] == x['REF']) & (compared_file['ALT'] == x['ALT'])) else 'A',
                      axis=1
                  )
              # Add 'Present in cf' column if applicable
              if '-B' in filename and '-cf' in filename:
                  filepath = os.path.join(output_base_dir, germ.split('-')[0], filename)
                  compared_file = pd.read_csv(filepath, index_col=0, header=None, comment="#", sep="\t")
                  compared_file.rename(columns={0: 'CHROM', 1: 'POS', 2: 'REF', 3: 'ALT'}, inplace=True)
                  file_anno['Present in cf'] = file_anno.apply(
                      lambda x: 'P' if any((compared_file['POS'] == x['POS']) & (compared_file['REF'] == x['REF']) & (compared_file['ALT'] == x['ALT'])) else 'A',
                      axis=1
                  )
      # Save the file after both columns are added (if applicable)
      output_filepath = os.path.join(output_base_dir, som.split('-')[0], f"{anno.split('.')[0]}-annotated.tsv")
      file_anno.to_csv(output_filepath, sep='\t')
      print(f"Saved: {output_filepath}")

except subprocess.CalledProcessError as e:
    print(f"An error occurred: {e}")