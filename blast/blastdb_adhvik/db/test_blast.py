import os

TEST_PATH = "../../test_hf"


def main():
    correct = 0
    total = 0
    for file in os.listdir(TEST_PATH):
        total += 1
        relative_path = os.path.join(TEST_PATH, file)
        # with open(relative_path, "r") as f:
        #     data = f.readlines()
        #     data[1] = data[1].strip()[:30]
        #     with open("input.txt", "w") as fasta_file:
        #         fasta_file.writelines(data)
        #         fasta_file.write("\n")
        os.system(
            f"blastn -query {relative_path} -db train.fasta -outfmt 6 -num_threads 8 > output.txt"
        )
        with open("output.txt", "r") as f:
            lines = f.readlines()
            if len(lines) == 0:
                continue
            species = lines[0].split()[1].split("_")[0]
            expected_species = file.split("_")[0]
            # print("Expected:", expected_species)
            # print("Predicted:", species)
            if species == expected_species:
                correct += 1
        os.system("rm output.txt")
        if total % 10 == 0:
            print(
                f"Iteration {total}: {correct}/{total} ({correct/total*100:.2f}%)"
            )

    print(f"Accuracy: {correct}/{total} ({correct/total*100:.2f}%)")


if __name__ == "__main__":
    main()
