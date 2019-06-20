for i in {1..22};
do java -Xmx30000m -jar ibdseq.r1206.jar \
gt=NG_34554_108004_phased_chr${i}.vcf.gz \
out=./ibdseq_outputs/NG_34554_108004_phased_chr${i} \
chrom=${i} \
nthreads=16; \
done
