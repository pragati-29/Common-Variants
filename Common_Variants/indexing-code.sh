for file in /media/bioinfoa/bioinfo2/Pragati/Common_Variant/Try/somatic/*; do
    bcftools index  -tf "$file"
done
