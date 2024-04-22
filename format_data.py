import os, random

INFLUENZA_DATA_INPUT_PATH = "data_raw/influenza/influenzaFASTA.fa"
HIV_DATA_INPUT_PATH = "data_raw/hiv/hiv-db_unaligned.fasta"
COVID_DATA_INPUT_PATH = "data_raw/covid/subsets"
DATA_OUTPUT_PATH = "data/species"


def get_influenza_data():
    with open(INFLUENZA_DATA_INPUT_PATH, "r") as f:
        lines = f.readlines()
        sequences = []
        currSequence = ""
        for line in lines:
            if line[0] == ">":
                if currSequence:
                    sequences.append(currSequence)
                currSequence = line
            else:
                currSequence += line.strip()
        if currSequence:
            sequences.append(currSequence)
        return sequences


def get_hiv_data():
    with open(HIV_DATA_INPUT_PATH, "r") as f:
        lines = f.readlines()
        sequences = []
        currSequence = ""
        for line in lines:
            if line[0] == ">":
                if currSequence:
                    sequences.append(currSequence)
                currSequence = line
            else:
                currSequence += line.strip().upper()
        if currSequence:
            sequences.append(currSequence)
        return sequences


def get_covid_data():
    """
    We have multiple files in the COVID_DATA_INPUT_PATH directory.

    Each file contains many FASTA sequences, and we want to concatenate all of them into a single list of sequences.
    """
    sequences = []
    for file in os.listdir(COVID_DATA_INPUT_PATH):
        with open(os.path.join(COVID_DATA_INPUT_PATH, file), "r") as f:
            lines = f.readlines()
            currSequence = ""
            for line in lines:
                if line[0] == ">":
                    if currSequence:
                        sequences.append(currSequence)
                    currSequence = line
                else:
                    currSequence += line.strip()
            if currSequence:
                sequences.append(currSequence)
    return sequences


def generate_training_data(virus, sequences):
    """
    Your folder structure should look like this:
    data
    |-- species/
        |-- chimpanzee/
            |-- chr1.fna
            |-- chr2.fna
            |-- ...
        |-- hippo/
            |-- chr1.fna
            |-- chr2.fna
            |-- ...
    We are already given that the data and species folders are created. We want to loop through
    the sequences list and write each sequence to a file in the appropriate species folder, named after virus.
    """
    os.makedirs(f"{DATA_OUTPUT_PATH}/{virus}", exist_ok=True)
    for file in os.listdir(f"{DATA_OUTPUT_PATH}/{virus}"):
        os.remove(f"{DATA_OUTPUT_PATH}/{virus}/{file}")
    for i, sequence in enumerate(sequences):
        with open(f"{DATA_OUTPUT_PATH}/{virus}/{virus}_{i}.fna", "w") as f:
            f.write(sequence)


def main():
    influenza_sequences = get_influenza_data()
    print("Influenza sequences: ", len(influenza_sequences))
    influenza_sequences = sorted(
        influenza_sequences, key=lambda x: len(x), reverse=True
    )
    hiv_sequences = get_hiv_data()
    print("HIV sequences: ", len(hiv_sequences))
    hiv_sequences = sorted(hiv_sequences, key=lambda x: len(x), reverse=True)
    covid_sequences = get_covid_data()
    print("COVID sequences: ", len(covid_sequences))
    covid_sequences = sorted(covid_sequences, key=lambda x: len(x), reverse=True)
    min_sequence_count = min(
        len(influenza_sequences), len(hiv_sequences), len(covid_sequences)
    )
    print("Shortest sequence length: ", min_sequence_count)
    generate_training_data("influenza", influenza_sequences)
    print("Wrote influenza data")
    generate_training_data("hiv", hiv_sequences)
    print("Wrote HIV data")
    generate_training_data("covid", covid_sequences)
    print("Wrote COVID data")


if __name__ == "__main__":
    main()
