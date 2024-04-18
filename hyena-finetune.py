from transformers import AutoModelForSequenceClassification, AutoTokenizer
from transformers import TrainingArguments, Trainer, logging
import torch
from datasets import load_dataset
import os

os.environ["WANDB_PROJECT"] = "CompBio-Evo"  # name your W&B project
os.environ["WANDB_LOG_MODEL"] = "checkpoint"  # log all model checkpoints

# instantiate pretrained model
checkpoint = 'LongSafari/hyenadna-tiny-16k-seqlen-d128'
max_length = 160_000

# bfloat16 for better speed and reduced memory usage
tokenizer = AutoTokenizer.from_pretrained(checkpoint, trust_remote_code=True)
model = AutoModelForSequenceClassification.from_pretrained(checkpoint, torch_dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)

ds = load_dataset("anudaw/genome-classification")

def preprocess_function(examples):
    return tokenizer(examples['seq'], truncation=True)

tokenized_ds = ds.map(preprocess_function, batched=True)

# Initialize Trainer
# Note that we're using extremely small batch sizes to maximize
# our ability to fit long sequences in memory!
args = {
    "output_dir": "tmp",
    "num_train_epochs": 1,
    "per_device_train_batch_size": 1,
    "gradient_accumulation_steps": 4,
    "gradient_checkpointing": True,
    "learning_rate": 2e-5,
}
training_args = TrainingArguments(**args)

trainer = Trainer(model=model, args=training_args, train_dataset=tokenized_ds["train"], eval_dataset=tokenized_ds["test"])
result = trainer.train()

print(result)

# Now we can save_pretrained() or push_to_hub() to share the trained model!

