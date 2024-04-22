import os


def main():
    with open("train.fasta", "r") as f:
        file_data = f.readlines()
    sampleCount = 0
    samples = set()
    duplicates = set()
    for line_index in range(len(file_data)):
        if file_data[line_index][0] == ">":
            sampleCount += 1
            if len(file_data[line_index]) > 43:
                print(file_data[line_index])
            file_data[line_index] = file_data[line_index][:43]
            if file_data[line_index] in samples:
                print("Duplicate found!")
                print(file_data[line_index])
                duplicates.add(line_index)
            samples.add(file_data[line_index])
    print(len(duplicates))
    for index in sorted(duplicates, reverse=True):
        file_data.pop(index)
        file_data.pop(index)
    os.system("rm train.fasta")
    with open("train.fasta", "w") as f:
        for line in file_data:
            f.write(line + "\n")
    print(sampleCount)


if __name__ == "__main__":
    main()
