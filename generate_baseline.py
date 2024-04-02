from Bio.Blast import NCBIWWW
from typing import List, Tuple
import typing


def main():
    for i in range(50):
        file = f"data/species/hiv/hiv_{i}.fna"
        with open(file, "r") as f:
            lines = f.readlines()
            sequence = lines[1]
            blast_result = NCBIWWW.qblast("blastn", "nr", sequence, expect = 0.001)
    
            blast_output_file = f"hiv_{i}_results.xml"
            with open(blast_output_file, "w") as output_handle:
                output_handle.write(blast_result.read())

            print(f"BLAST search results saved to {blast_output_file}")

if __name__ == "__main__":
    main()