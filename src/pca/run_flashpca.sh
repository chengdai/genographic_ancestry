cd output

../flashpca/flashpca --bfile ../input/1000G/1000G_108003_combined --outpc 1000G_108003_combined_pcs.txt \
--outvec 1000G_108003_combined_pve.txt -v --outload  1000G_108003_combined_snp_loading.txt \
--outmeansd  1000G_108003_combined_meansd.txt --memory 50000 -d 20

../flashpca/flashpca -p --inload 1000G_108003_combined_snp_loading.txt \
--inmeansd 1000G_108003_combined_meansd.txt \
--bed ../input/NG/NG_32589_108003_phased_all_reordered.bed \
--fam ../input/NG/NG_32589_108003_phased_all_reordered.fam \
--bim ../input/NG/NG_32589_108003_phased_all_reordered.bim \
--outproj NG_32589_108003_proj_all_1000G.txt \
-d 20 -v --memory 50000 \
cd ..
