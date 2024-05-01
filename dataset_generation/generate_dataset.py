import random, csv, os, statistics

COVID_PATH = "./data/species/covid"
HIV_PATH = "./data/species/hiv"
INFLUENZA_PATH = "./data/species/influenza"
TRAIN_CSV_PATH = "train.csv"
TEST_CSV_PATH = "test.csv"
TRAIN_TEST_SPLIT_RATIO = 0.8
SEQ_LENGTH = 1000
SAMPLES_PER_CLASS = 20000


def get_data(fasta_files_dir, label):
    data = []
    seqs = []
    for file in os.listdir(fasta_files_dir):
        with open(os.path.join(fasta_files_dir, file), "r") as f:
            lines = f.readlines()
            sequence = lines[1]
            data.append((sequence, label))
            seqs.append(sequence)
    print("Median seq length:", statistics.median([len(seq) for seq in seqs]))
    print("Mean seq length:", statistics.mean([len(seq) for seq in seqs]))
    return data


def truncate_sequences(data, length):
    # Truncate sequences to 8k nucleotides
    for i in range(len(data)):
        seq, label = data[i]
        startIndex = random.randint(0, len(seq) - length)
        data[i] = (seq[startIndex : startIndex + length], label)


def write_to_csv(csv_name, data):
    with open(csv_name, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["seq", "label"])
        writer.writerows(data)


def split_dataset(data, ratio):
    random.shuffle(data)
    splitIndex = int(ratio * len(data))
    return data[:splitIndex], data[splitIndex:]


def reduce_samples_to_limit(data, limit):
    values_per_label = dict()
    for seq, label in data:
        if label not in values_per_label:
            values_per_label[label] = []
        if len(values_per_label[label]) >= limit:
            continue
        values_per_label[label].append((seq, label))
    new_data = []
    for label in values_per_label:
        new_data.extend(values_per_label[label])
    return new_data


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
    print("HIV data count: ", len(hiv_data))  # 20525
    influenza_data = get_data(INFLUENZA_PATH, "I")
    print("Influenza data count: ", len(influenza_data))  # 
    covid_data = get_data(COVID_PATH, "C")
    print("COVID data count: ", len(covid_data))  # 20525

    print("Collected raw data")

    # Truncate such that every dataset has the same number of sequences
    min_data_count = min(len(hiv_data), len(influenza_data), len(covid_data))
    print("Min data count: ", min_data_count) # 20525
    random.shuffle(hiv_data)
    random.shuffle(influenza_data)
    random.shuffle(covid_data)

    hiv_lengths = [len(seq) for seq, label in hiv_data]
    influenza_lengths = [len(seq) for seq, label in influenza_data]
    covid_lengths = [len(seq) for seq, label in covid_data]
    print("HIV median seq length:", statistics.median(hiv_lengths))
    print("HIV mean seq length:", statistics.mean(hiv_lengths))
    print("Influenza median seq length:", statistics.median(influenza_lengths))
    print("Influenza mean seq length:", statistics.mean(influenza_lengths))
    print("COVID median seq length:", statistics.median(covid_lengths))
    print("COVID mean seq length:", statistics.mean(covid_lengths))

    # hiv_data = hiv_data[:min_data_count]
    # influenza_data = influenza_data[:min_data_count]
    # covid_data = covid_data[:min_data_count]

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

    # Truncate to correct length
    # min_train_seq_length = min([len(seq) for seq, label in train_data])
    # min_test_seq_length = min([len(seq) for seq, label in test_data])
    # min_seq_length = min(min_train_seq_length, min_test_seq_length)
    print("Removing sequences shorter than 1k nucleotides")
    train_data = list(filter(lambda x: len(x[0]) >= SEQ_LENGTH, train_data))
    test_data = list(filter(lambda x: len(x[0]) >= SEQ_LENGTH, test_data))
    truncate_sequences(train_data, SEQ_LENGTH)
    truncate_sequences(test_data, SEQ_LENGTH)

    hiv_train_count = sum([1 for _, label in train_data if label == "H"])
    hiv_test_count = sum([1 for _, label in test_data if label == "H"])
    influenza_train_count = sum([1 for _, label in train_data if label == "I"])
    influenza_test_count = sum([1 for _, label in test_data if label == "I"])
    covid_train_count = sum([1 for _, label in train_data if label == "C"])
    covid_test_count = sum([1 for _, label in test_data if label == "C"])
    print("HIV train count: ", hiv_train_count)
    print("HIV test count: ", hiv_test_count)
    print("Influenza train count: ", influenza_train_count)
    print("Influenza test count: ", influenza_test_count)
    print("COVID train count: ", covid_train_count)
    print("COVID test count: ", covid_test_count)

    # Reduce to 20k samples each across train and test, per class
    print("Reducing to 20k samples per class")
    train_data = reduce_samples_to_limit(
        train_data, SAMPLES_PER_CLASS * TRAIN_TEST_SPLIT_RATIO
    )
    test_data = reduce_samples_to_limit(
        test_data, SAMPLES_PER_CLASS * (1 - TRAIN_TEST_SPLIT_RATIO)
    )

    hiv_train_count = sum([1 for _, label in train_data if label == "H"])
    hiv_test_count = sum([1 for _, label in test_data if label == "H"])
    influenza_train_count = sum([1 for _, label in train_data if label == "I"])
    influenza_test_count = sum([1 for _, label in test_data if label == "I"])
    covid_train_count = sum([1 for _, label in train_data if label == "C"])
    covid_test_count = sum([1 for _, label in test_data if label == "C"])
    print("HIV train count: ", hiv_train_count)
    print("HIV test count: ", hiv_test_count)
    print("Influenza train count: ", influenza_train_count)
    print("Influenza test count: ", influenza_test_count)
    print("COVID train count: ", covid_train_count)
    print("COVID test count: ", covid_test_count)
    return
    print("Writing to CSV")
    # Write to CSV
    write_to_csv(TRAIN_CSV_PATH, train_data)
    write_to_csv(TEST_CSV_PATH, test_data)


if __name__ == "__main__":
    main()
