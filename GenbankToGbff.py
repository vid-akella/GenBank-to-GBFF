#!/usr/bin/env python3
#
"""script to take in all .gb files within specified directory, order the sequences by decreasing order of size and
output as a concatenated gbff file into a new output directory specified by the user """

"""import necessary libraries"""
from Bio import SeqIO
import os


class GbToGbff:
    # has path to input, output, list of gb files, and dictionary of seq records

    def __init__(self, gbff, infile_path, out_path):
        self.name = gbff
        self.infile_path = str(infile_path)
        self.outfile_path = str(out_path)
        self.file_list = list()
        self.seq_recs = dict()

    # create function that finds all .gb files and joins to path
    def find_gb_files(self):
        file_lst = list()
        for file in os.listdir(self.infile_path):
            if file.endswith(".gb"):
                file_path = (os.path.join(self.infile_path, file))
                file_lst.append(file_path)
        self.file_list = file_lst

    # function reads .gb files into seq records and sort by length of sequence
    def read_gb_files(self):
        seqrec_dict = {}
        seqlen_dict = {}
        sorted_seqrecs = {}
        for gb in self.file_list:
            with open(gb, "r"):
                input_rec = SeqIO.read(gb, "genbank")  # read each gb file into a seq record
                seqrec_dict[input_rec.id] = input_rec   # store all records in a dictionary
                seqlen_dict[input_rec.id] = len(input_rec.seq)
        # sort dictionary by seq length
        sorted_seqlen = dict(sorted(seqlen_dict.items(), key=lambda x: x[1], reverse=True))
        for rec in sorted_seqlen:
            sorted_seqrecs[rec] = seqrec_dict[rec]
        self.seq_recs = sorted_seqrecs  # add sorted recs as attribute of object

    # function orders records in decreasing size of sequence
    def write_gbff(self):
        with open(self.name, "w") as output_handle:
            for rec in self.seq_recs:
                SeqIO.write(self.seq_recs[rec], output_handle, "genbank")


def main():
    """
Takes user input for folder path that contains .gb file, output file path where gbff is written
Also checks to make sure input path is correct. Instantiates GbToGbff object once parameters are given.
Summarizes output at the end.
    """
    input_gb_path: str = input("Folder that contains .gb files(provide path): ")
    if os.path.exists(input_gb_path):       # test to ensure valid path is provided
        pass
    else:
        exit("The path does not exist. Check and submit again.")
    # get user specified path and file name for generating gbff
    outfile_path: str = input("Enter path for output gbff: ")
    gbff_name: str = input("Enter a name for the GBFF:")
    if gbff_name.endswith('.gbff'):
        pass
    else:
        gbff_name += '.gbff'
        print('Output file name is set to', gbff_name)

    # create gb_to_gbff object for the genome in question
    org_genome = GbToGbff(gbff_name, input_gb_path, outfile_path)
    org_genome.find_gb_files()
    org_genome.read_gb_files()
    org_genome.write_gbff()

    # print confirmation to user with summary of gbff created
    print(f'Combined {len(org_genome.file_list):d} genbank(.gb) files into a single GBFF')


if __name__ == '__main__':
    main()
