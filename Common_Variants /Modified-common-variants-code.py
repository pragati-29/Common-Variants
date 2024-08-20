import os
import pandas as pd
import subprocess
import argparse

def create_output_dir(output_dir):
    """Create the output directory if it doesn't exist."""
    os.makedirs(output_dir, exist_ok=True)

def check_columns(file_anno):
    """Ensure the required columns are present in the annotation file."""
    required_columns = ['CHROM', 'POS', 'REF', 'ALT']
    missing_columns = [col for col in required_columns if col not in file_anno.columns]
    if missing_columns:
        raise ValueError(f"Missing columns in file: {missing_columns}")

def load_annotation_file(file_path, file_type):
    """Load the annotation file based on its type."""
    if file_type == "csv":
        return pd.read_csv(file_path)
    elif file_type in ["tsv", "tab"]:
        return pd.read_csv(file_path, sep='\t')
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

def process_files(germ_path, som_path, anno_path, annotation_file_type, output_base_dir):
    """Main logic for comparing files and annotating results."""
    # Create output directory
    create_output_dir(output_base_dir)
    
    # List files in directories
    folder_germ = os.listdir(germ_path)
    folder_som = os.listdir(som_path)
    folder_anno = os.listdir(anno_path)
    
    # Iterate through the germline and somatic files
    for germ in folder_germ:
        germ_prefix = germ.split('-')[0]
        corresponding_som = [som for som in folder_som if som.startswith(germ_prefix) and som.endswith("vcf.gz")]
        corresponding_anno = [anno for anno in folder_anno if anno.startswith(germ_prefix)]
        
        if not corresponding_som or not corresponding_anno:
            print(f"Skipping {germ_prefix} as it does not have corresponding somatic or annotation files.")
            continue
        
        # Assume there is only one matching file for somatic and annotation per germline file
        som = corresponding_som[0]
        anno = corresponding_anno[0]
        
        sample_output_dir = os.path.join(output_base_dir, germ_prefix)
        create_output_dir(sample_output_dir)
        
        # Load annotation file
        annotate_file = os.path.join(anno_path, anno)
        file_anno = load_annotation_file(annotate_file, annotation_file_type)
        check_columns(file_anno)
        # Run bcftools isec command
        #print(output_vcf,sample_output_dir)
        if germ.endswith('vcf.gz') and germ.split('-')[0] in som:
            output_vcf = os.path.join(sample_output_dir, f"{germ.split('.')[0]}-{som.split('.')[0]}-compare.vcf.gz")
            command = f"bcftools isec -n +2 {os.path.join(germ_path, germ)} {os.path.join(som_path, som)} | bgzip -c > {output_vcf}"
            #print(command)
        subprocess.run(command, shell=True, check=True)
        for x in os.listdir(sample_output_dir):
            try: 
                if '-B' in x and '-cf' not in x: 
                    new_file= sample_output_dir +"/"+x 
                    compared_file = pd.read_csv(new_file, index_col=0, header=None, comment="#", sep="\t")
                    compared_file.rename(columns={0:'CHROM', 1:'POS', 2:'REF', 3:'ALT'}, inplace=True)
                    file_anno['Present in Germline'] =file_anno.apply(lambda x: 'P' if any((compared_file['POS'] == x['POS']) & (compared_file['REF'] == x['REF']) & (compared_file['ALT'] == x['ALT'])) else 'A', axis=1)
                if '-B' in x and '-cf' in x:
                    new_file= sample_output_dir +"/"+x 
                    compared_file = pd.read_csv(new_file, index_col=0, header=None, comment="#", sep="\t")
                    compared_file.rename(columns={0:'CHROM', 1:'POS', 2:'REF', 3:'ALT'}, inplace=True)
                    file_anno['Present in cf'] =file_anno.apply(lambda x: 'P' if any((compared_file['POS'] == x['POS']) & (compared_file['REF'] == x['REF']) & (compared_file['ALT'] == x['ALT'])) else 'A', axis=1)   
            except:
                continue
        file_anno.to_csv(sample_output_dir + '/' + anno.split('.')[0] + '-annotated.csv')    
        # Save the annotated file
def main(germ_path, som_path, anno_path, annotation_file_type, output_base_dir):
    """Main function to execute the workflow."""
    process_files(germ_path, som_path, anno_path, annotation_file_type, output_base_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process file paths for germline, somatic, and annotation directories.')
    parser.add_argument('--germ_path', type=str, required=True, help='Path to the germline directory')
    parser.add_argument('--som_path', type=str, required=True, help='Path to the somatic directory')
    parser.add_argument('--anno_path', type=str, required=True, help='Path to the annotation directory')
    parser.add_argument('--annotation_file_type', type=str, required=True, help='Extension of the annotation file')
    parser.add_argument('--output_base_dir', type=str, required=True, help='Path to the output directory')

    args = parser.parse_args()
    main(args.germ_path, args.som_path, args.anno_path, args.annotation_file_type, args.output_base_dir)
