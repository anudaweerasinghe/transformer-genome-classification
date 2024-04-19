#LOAD DATASET

#FOR EACH IN TEST SET
    #PARSE INTO A .FASTA FILE 
    #USE THE SUBPROCESS MODULE TO RUN BLAST ON THIS
    #FROM THIS, PARSE THE RESULT TO GET THE FIRST MATCH
    #WITH THE FIRST MATCH, CHECK THE CLASSFICATION
    #CMP to ground truth

from datasets import load_dataset
import subprocess
import os

dataset = load_dataset("anudaw/genome-classification")
train_data = dataset['train']
test_data = dataset['test']

mismatches = 0
iterations = 12000
for i in range(iterations):
    with open("temp.fasta","w") as temp:
        temp.write(">seq\n")
        temp.write(test_data[i]["seq"])
    
    blastcall = subprocess.run(["blastn", "-db", "blastdb/db/baseline", "-query", "temp.fasta"],
                    capture_output=True, text=True)
    output = blastcall.stdout
    if "No hits found" in output:
        mismatches += 1
        continue
    split_output = output.split("\n")
    result = split_output[21][0]
    print(result, test_data[i]["label"])
    if result != test_data[i]["label"]:
        mismatches += 1
    os.remove("temp.fasta")
    print(f"{i} sequences processed")

print(f"Number of mismatches {mismatches}")
print(f"Percentage: {mismatches/12000}")
        