import random, csv, os

COVID_PATH = "./data/species/hiv"
HIV_PATH = "./data/species/hiv"
INFLUENZA_PATH = "./data/species/hiv"
TRAIN_CSV_PATH = "train.csv"
TEST_CSV_PATH = "test.csv"
TRAIN_TEST_SPLIT_RATIO = 0.8
SEQ_LENGTH = 8000


def get_data(fasta_files_dir, label):
    data = []
    for file in os.listdir(fasta_files_dir):
        with open(os.path.join(fasta_files_dir, file), "r") as f:
            lines = f.readlines()
            sequence = lines[1]
            data.append((sequence, label))
    return data


def truncate_sequences(data, length):
    # Truncate sequences to 8k nucleotides
    for i in range(len(data)):
        seq, label = data[i]
        startIndex = random.randint(0, len(seq) - 8000)
        data[i] = (seq[startIndex : startIndex + 8000], label)


def write_to_csv(csv_name, data):
    with open(csv_name, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["seq", "label"])
        writer.writerows(data)


def split_dataset(data, ratio):
    random.shuffle(data)
    splitIndex = int(ratio * len(data))
    return data[:splitIndex], data[splitIndex:]


def main():
    """
    Convert dataset to a single CSV with columns seq and label, where label = H | I | C for HIV, Influenza and COVID respectively.

    Truncate each sequence to be 8k nucleotides long
    """
    random.seed(42)
    # Load data
    # data is of the format [(seq, label), ...]
    train_data = []
    test_data = []

    # Collect raw data
    hiv_data = get_data(HIV_PATH, "H")
    influenza_data = get_data(INFLUENZA_PATH, "H")
    covid_data = get_data(COVID_PATH, "H")

    print("Collected raw data")

    # Truncate such that every dataset has the same number of sequences
    min_data_count = min(len(hiv_data), len(influenza_data), len(covid_data))
    print("HIV data count: ", len(hiv_data))  # 20525
    print("Influenza data count: ", len(influenza_data))  # 20525
    print("COVID data count: ", len(covid_data))  # 20525
    print("Min data count: ", min_data_count) # 20525
    random.shuffle(hiv_data)
    random.shuffle(influenza_data)
    random.shuffle(covid_data)
    hiv_data = hiv_data[:min_data_count]
    influenza_data = influenza_data[:min_data_count]
    covid_data = covid_data[:min_data_count]

    # Split data into train and test
    hiv_train_data, hiv_test_data = split_dataset(hiv_data, TRAIN_TEST_SPLIT_RATIO)
    influenza_train_data, influenza_test_data = split_dataset(
        influenza_data, TRAIN_TEST_SPLIT_RATIO
    )
    covid_train_data, covid_test_data = split_dataset(
        covid_data, TRAIN_TEST_SPLIT_RATIO
    )

    print("Split data into train and test")

    # Combine data
    train_data.extend(hiv_train_data)
    train_data.extend(influenza_train_data)
    train_data.extend(covid_train_data)
    test_data.extend(hiv_test_data)
    test_data.extend(influenza_test_data)
    test_data.extend(covid_test_data)

    # Truncate sequences to 8k nucleotides
    truncate_sequences(train_data, SEQ_LENGTH)
    truncate_sequences(test_data, SEQ_LENGTH)

    print("Writing to CSV")
    # Write to CSV
    write_to_csv(TRAIN_CSV_PATH, train_data)
    write_to_csv(TEST_CSV_PATH, test_data)


if __name__ == "__main__":
    main()
