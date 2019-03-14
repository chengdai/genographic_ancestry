import gzip, argparse, sys

def get_tracts(gz_file):

	with gzip.open(gz_file, 'r') as rfmix:
		print "Reading Viterbi file and identifying tracts"
		# read first line -> set as the initial state of the chromosome tracts
		# 0-indexed
		previous_line = rfmix.readline().strip().split()
		num_haplotypes = len(previous_line)
		haplotypes = xrange(num_haplotypes)
		previous_index = [0]*num_haplotypes
		index = 0

		# initialize dictionary to store tracts
		tracts = dict((haplotype,[]) for haplotype in haplotypes)

		for line in rfmix:
			index += 1
			line = line.strip().split()

			for haplotype in haplotypes:
				if line[haplotype] != previous_line[haplotype]:
					tracts[haplotype].append((int(previous_line[haplotype]), previous_index[haplotype], index-1))
					
					# reset index tracker to current index
					previous_index[haplotype] = index

			# keep track of previous line
			previous_line = line
		for haplotype in haplotypes:
			tracts[haplotype].append((int(previous_line[haplotype]), previous_index[haplotype], index))
	
	rfmix.close()
	return tracts

def write_tracts(sample_file, map_file, out_path, tracts, ancestry_map, chromosome):
	with open(map_file, 'r') as snp_map:
		positions = [line.split()[:2] for line in snp_map]

	ind_index = 0
	with open(sample_file, 'r') as sample:
		print "Calculating tract lengths and writing individual tract files"
		for line in sample:
			ind = line.strip()
			out_A = []
			out_B = []

			# write first haplotype
			for tract in tracts[2*ind_index]:
				out_A.append('\t'.join((chromosome, positions[tract[1]][0] , positions[tract[2]][0], ancestry_map[tract[0]], positions[tract[1]][1] , positions[tract[2]][1]))+'\n')
			with open(out_path + ind+'_A.bed', 'a') as out_A_file:
				out_A_file.writelines(out_A)
			out_A_file.close()

			# write second haplotype
			for tract in tracts[2*ind_index+1]:
				out_B.append('\t'.join((chromosome, positions[tract[1]][0] , positions[tract[2]][0], ancestry_map[tract[0]], positions[tract[1]][1] , positions[tract[2]][1]))+'\n')
			with open(out_path + ind+'_B.bed', 'a') as out_B_file:
				out_B_file.writelines(out_B)
			out_B_file.close()
			ind_index += 1
	snp_map.close()
	sample.close()




if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Convert RFMix output into bed files for each individual.')
	parser.add_argument('--viterbi_file', help = 'Outputted viterbi file')
	parser.add_argument('--sample_file', help = 'Inputted sample file')
	parser.add_argument('--map_file', help = 'Genome map file')
	parser.add_argument('--out_path', help = 'Folder to output all the files')
	parser.add_argument('--ancestry_seq', help = 'Comma separated order to which the reference ancestries are written')
	parser.add_argument('--chromosome', help = 'Chromosome order')
	
	args = parser.parse_args()
	
	viterbi_file = args.viterbi_file
	sample_file = args.sample_file
	map_file = args.map_file
	out_path = args.out_path
	ancestry_seq = args.ancestry_seq
	chromosome = args.chromosome

	ancestry_seq = ancestry_seq.split(',')
	ancestry_map = dict(zip(range(1, len(ancestry_seq)+1), ancestry_seq))

	write_tracts(sample_file, map_file, out_path, get_tracts(viterbi_file), ancestry_map, chromosome)
