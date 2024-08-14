# Common Variant Analysis Script
This script automates the analysis of common variants using the vcf files (*.vcf.gz) and adds information to the annotated (*final.tab) file.  
## **Requirements:**  
  - Python (Pandas,Subprocess,os)  
  - Bcftools  
## **Input:**  
  - List of names of sample folders (eg:[XEOAC, XE5AL])   
      Example:XE5AL: somatic file, germline and cf files, *final.tab file  
  - Path of the parent folder  
## **Output:** 
  - Common variants in vcf.gz files  
  - *annotated.csv file (Annotated file with information of germline and cf variants)  
**Note**
-Please zip files using bgzip and make index file of each file (except .tab)

# Modified common variant code
  script :- Modified-common-variants-code.py
## **Requirements:**  
  - Python (Pandas,Subprocess,os)  
  - Bcftools
## **Input:**  
  - Path of Somatic folder  
  - Path of Germline and cf folder
  - Path of Annotation folder (Somatic)
  - Extension of Annotation file
  - Path of Output directory
![common-var-input](https://github.com/user-attachments/assets/f8df6564-9eb1-4a3d-b85f-d8020e4df5a5)

## **Output:** 
  - Folders of samples 
      - Compared variant files for both cf-DNA and germline. 
      - *annotated.tsv file (Annotated file with information of germline and cf variants)
       ![image](https://github.com/user-attachments/assets/6f3197c6-0c40-4020-bf25-519907ad9b4a)
       ![image](https://github.com/user-attachments/assets/2d8e381e-4612-4a94-8b51-27f47d9c932d)  

**Note**
-Please zip files using bgzip and make index file of each file (except .tab)

