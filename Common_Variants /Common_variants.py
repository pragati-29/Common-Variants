# Importing packages
import pandas as pd
import os
import subprocess

folders = ['XEOAC', 'XE5AL']

for folder in folders:
    files = os.listdir(f"/media/bioinfoa/bioinfo2/Pragati/Common_Variant/{folder}")
    tab_files = [f for f in files if f.endswith('.tab')]
    
    for file in files:
        if file.endswith('.vcf.gz') and '-F' in file:
            file_prefix = file.split('.')[0]
            corresponding_files = [f for f in files if '-B' in f and f.endswith('.vcf.gz')]
            
            for corresponding_file in corresponding_files:
                command = f"bcftools isec -n +2 /media/bioinfoa/bioinfo2/Pragati/Common_Variant/{folder}/{file} /media/bioinfoa/bioinfo2/Pragati/Common_Variant/{folder}/{corresponding_file} | bgzip -c > {folder}/{file_prefix}-{corresponding_file.split('.')[0]}-out-F.vcf.gz"
                subprocess.run(command, shell=True)
                
            # Process '.tab' files
            for tab_file in tab_files:
                annotate_file = "/media/bioinfoa/bioinfo2/Pragati/Common_Variant/" + folder + "/" + tab_file
                file_anno = pd.read_csv(annotate_file, sep="\t", index_col=0)
                
                for corresponding_file in corresponding_files:
                    com_file = file_prefix + "-" + corresponding_file.split('.')[0] + "-out-F.vcf.gz"
                    
                    if '-B' in com_file and '-cf' not in com_file:
                        compared_file = pd.read_csv(com_file, index_col=0, header=None, comment="#", sep="\t")
                        compared_file.rename(columns={0:'CHROM', 1:'POS', 2:'REF', 3:'ALT'}, inplace=True)
                        file_anno['Present in Germline'] = file_anno.apply(lambda x: 'P' if any((compared_file['POS'] == x['POS']) & (compared_file['REF'] == x['REF']) & (compared_file['ALT'] == x['ALT'])) else 'A', axis=1)
                    
                    if '-B' in com_file and '-cf' in com_file:
                        compared_file = pd.read_csv(com_file, index_col=0, header=None, comment="#", sep="\t")
                        compared_file.rename(columns={0:'CHROM', 1:'POS', 2:'REF', 3:'ALT'}, inplace=True) 
                        file_anno['Present in cf'] = file_anno.apply(lambda x: 'P' if any((compared_file['POS'] == x['POS']) & (compared_file['REF'] == x['REF']) & (compared_file['ALT'] == x['ALT'])) else 'A', axis=1)
                
                # Save the annotated file
                file_anno.to_csv(folder + '/' + file_prefix + '-annotated.csv')
