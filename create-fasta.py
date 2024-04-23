from datasets import load_dataset


dataset = load_dataset("anudaw/genome-classification")
train_data = dataset['train']
test_data = dataset['test']

with open("blastdb/db.fasta", "w") as fasta_file:
    for i in range(48000):
        fasta_file.write(">" + train_data[i]['label'] + f"{i}" + "\n")

        for i in range(0, 1000, 60):
            fasta_file.write(train_data[i]['seq'][i:i+60] + "\n")

