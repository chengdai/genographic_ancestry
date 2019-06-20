from scipy import interpolate
import pandas
import numpy
import sys
import gzip

def write_ibd_lengths(ibd_file, genetic_map_file, out_file, min_ibd_cm):
    #Interpolate physicial position from genetic map
    genetic_map = pandas.read_table(genetic_map_file, sep = '\s+', header = None)
    genetic_map_interpolate = interpolate.interp1d(numpy.ndarray.flatten(genetic_map.iloc[:,3].values), numpy.ndarray.flatten(genetic_map.iloc[:,2].values))
    
    batch_size = 10000000
    batch = []
    
    with open(ibd_file,'r') as ibd, open(out_file, 'w') as ibd_lengths_file:
        #read line and calculate length (make sure to not save in memory)
        for line in ibd:
            line = line.split()
            [start,end] = genetic_map_interpolate([line[5],line[6]])
            length = end - start
            if length >= min_ibd_cm:
                batch.append('\t'.join((line[0], line[2], str(length), line[7])) + '\n')
            if len(batch) == batch_size:
                ibd_lengths_file.writelines(batch)
                batch = []
        ibd_lengths_file.writelines(batch)
        batch = []
    ibd.close()
    ibd_lengths_file.close()
            
def main():
    ibd_file = sys.argv[1]
    genetic_map_file = sys.argv[2]
    out_file = sys.argv[3]
    min_ibd_cm = sys.argv[4]
    
    print '\nInput file: ' + ibd_file + '\n' + 'Genetic map: ' + genetic_map_file + '\n' + 'Output file: ' + out_file + '\n' + 'Minimum IBD length (in cM): ' + min_ibd_cm
    
    write_ibd_lengths(ibd_file, genetic_map_file, out_file, float(min_ibd_cm))
    
if __name__ == '__main__':
    main()

