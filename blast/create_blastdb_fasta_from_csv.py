import os, csv
from datasets import load_dataset

def main():
    print("Loading datasets")
    train_dataset = load_dataset("addykan/genome-classification-with-random", split = "train")
    test_dataset = load_dataset("addykan/genome-classification-with-random", split = "test")
    print("Loaded datasets")
    print("Generating train data")
    virus_counts = { "influenza": 0, "hiv": 0, "covid": 0 }
    fasta_file_data = ""
    for datum in train_dataset:
        seq = datum["seq"]
        label = datum["label"]
        if label == "H":
            virus = "hiv"
        elif label == "I":
            virus = "influenza"
        elif label == "C":
            virus = "covid"
        virus_counts[virus] += 1
        fasta_file_data += f">{virus}_{virus_counts[virus]}\n{seq}\n"

    print("Writing train data")
    with open("train_hf.fasta", "w") as f:
        f.write(fasta_file_data)
    print("Wrote train data")
    print("Writing test data")
    # In a directory named test_hf, write each datum as a unique fasta file where the first line is >virus_i and the seocond line is the sequence
    test_dir = "test_hf"
    os.makedirs(test_dir, exist_ok=True)
    for i, datum in enumerate(test_dataset):
        seq = datum["seq"]
        label = datum["label"]
        if label == "H":
            virus = "hiv"
        elif label == "I":
            virus = "influenza"
        elif label == "C":
            virus = "covid"
        with open(f"{test_dir}/{virus}_{i}.fasta", "w") as f:
            f.write(f">{virus}_{i}\n{seq}\n")
    print("Wrote test data")
    


if __name__ == '__main__':
    main()