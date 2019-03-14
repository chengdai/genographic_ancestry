for i in {2..3}; do ./king -b ./bed_file/NG_32589_108003_phased_all_reordered.bed \
--unrelated --kinship --cpu 20 --degree ${i} --prefix ./king_out/NG_32589_108003_relatedness_deg${i}; done
