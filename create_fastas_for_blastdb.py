import os, shutil, random

BLASTDB_PATH = "blastdb_adhvik"


def get_data(virus):
    directory = os.path.join("data/species", virus)
    sequencePaths = []
    for file in os.listdir(directory):
        sequencePaths.append(os.path.join(directory, file))
    return sequencePaths


def generate_training_data(virus, sequences, num_sequences):
    random.seed(0)
    random.shuffle(sequences)
    return sequences[:num_sequences]


def main():
    train_paths = []
    test_paths = []
    # We want 16000 filepaths of training data and 4000 filepaths of test data
    # for each virus. Then we want to copy these files to blastdb_adhvik/train and blastdb_adhvik/test.
    for virus in ["influenza", "hiv", "covid"]:
        sequences = get_data(virus)
        train_paths.extend(generate_training_data(virus, sequences, 16000))
        test_paths.extend(generate_training_data(virus, sequences, 4000))

    print(len(train_paths))
    print(len(test_paths))
    print("Cleaning up old files")
    os.system("rm -rf " + BLASTDB_PATH + "/train/*")
    os.system("rm -rf " + BLASTDB_PATH + "/test/*")
    # os.makedirs(os.path.join(BLASTDB_PATH, "train"))
    # os.makedirs(os.path.join(BLASTDB_PATH, "test"))
    print("Writing train data")
    for path in train_paths:
        shutil.copy(path, os.path.join(BLASTDB_PATH, "train"))

    print("Writing test data")
    for path in test_paths:
        shutil.copy(path, os.path.join(BLASTDB_PATH, "test"))

    print("Creating train.fasta")
    train_path = "train.fasta"
    os.system(f"rm {train_path}")
    os.system(f"touch {train_path}")
    counts = {"hiv": 0, "influenza": 0, "covid": 0}
    for train_file in os.listdir(os.path.join(BLASTDB_PATH, "train")):
        virus = train_file.split("_")[0]
        counts[virus] += 1
        with open(os.path.join(BLASTDB_PATH, "train", train_file), "r") as f:
            data = f.readlines()
            data[0] = f">{virus}_{counts[virus]}\n"

            data[1] = data[1].strip()[:30]
            with open(train_path, "a") as fasta_file:
                fasta_file.writelines(data)
                fasta_file.write("\n")
    print("Created train.fasta")


if __name__ == "__main__":
    main()
