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
