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
for file_g in folder_germ:
    # Extract the prefix part of the file name
    prefix = file_g.split('-')[0]
    # Check if the corresponding file exists in both anno_path and som_path directories
    if not any(file.startswith(prefix) for file in folder_anno) or not any(file.startswith(prefix) for file in folder_som):
        raise FileNotFoundError(f"Sample not found in all folders: {prefix}")
# Comparing the somatic and germline files
for file_g, file_s, file_an in zip_longest(folder_germ, folder_som, folder_anno):
    file_g_parts = file_g.split('-')
    command1 = f"bcftools index -t {som_path}/{file_s}"
    print(command1)
    subprocess.run(command1, shell=True, check=True)
    if file_g_parts[0] in file_s and file_s.endswith("vcf.gz"):
        os.makedirs(file_g_parts[0], exist_ok=True)
        command2 = f"bcftools isec -n +2 {os.path.join(germ_path,file_g)} {os.path.join(som_path,file_s)} | bgzip -c > {output_base_dir}/{file_g_parts[0]}/{file_g}-{file_s}-compare.vcf.gz"
        subprocess.run(command2, shell=True,check=True)  