import torch
from datasets import load_dataset
from peft import LoraConfig
from trl import SFTTrainer, SFTConfig

from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
print("CUDA disponible:", torch.cuda.is_available())
print("Versión CUDA de PyTorch:", torch.version.cuda)
from huggingface_hub import whoami

MODEL_NAME = "meta-llama/Llama-3.2-1B-Instruct"


tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)


def tokenize_example(example):

    messages = example["messages"]

    prompt_messages = messages[:-1]
    answer = messages[-1]["content"]

    prompt_text = tokenizer.apply_chat_template(
        prompt_messages,
        tokenize=False,
        add_generation_prompt=True
    )

    full_text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=False
    )

    prompt_ids = tokenizer(
        prompt_text,
        add_special_tokens=False
    )["input_ids"]

    full_ids = tokenizer(
        full_text,
        add_special_tokens=False
    )["input_ids"]

    labels = [-100] * len(prompt_ids)

    labels += full_ids[len(prompt_ids):]

    return {
        "input_ids": full_ids,
        "labels": labels,
        "attention_mask": [1] * len(full_ids)
    }

if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))



dataset = load_dataset(
    "json",
    data_files={
        "train": "train.jsonl",
        "validation": "validation.jsonl"
    }
)

tokenized_dataset = dataset.map(
    tokenize_example,
    remove_columns=dataset["train"].column_names
)
print(tokenized_dataset)
print(tokenized_dataset["train"][0])


import torch

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
)

from peft import (
    LoraConfig,
    get_peft_model,
    prepare_model_for_kbit_training,
)



from transformers import DataCollatorForSeq2Seq

data_collator = DataCollatorForSeq2Seq(
    tokenizer=tokenizer,
    padding=True,
    label_pad_token_id=-100,
    return_tensors="pt"
)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token


bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.float16,
)


model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=bnb_config,
    dtype=torch.float16,
    device_map="auto",
)
model = prepare_model_for_kbit_training(model)
peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
    target_modules=[
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
        "gate_proj",
        "up_proj",
        "down_proj",
    ],
)

model = get_peft_model(model, peft_config)

model.print_trainable_parameters()
for name, param in model.named_parameters():
    if param.requires_grad:
        print(name, param.dtype)
        break


from transformers import TrainingArguments, Trainer

training_args = TrainingArguments(
    output_dir="./llama-intent",

    num_train_epochs=3,

    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,

    gradient_accumulation_steps=8,

    learning_rate=2e-4,

    logging_steps=1,

    eval_strategy="epoch",
    save_strategy="epoch",

    fp16=True,
    bf16=False,

    optim="paged_adamw_32bit",

    report_to="none",

    gradient_checkpointing=True,

    max_grad_norm=0.3,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["validation"],
    data_collator=data_collator,
)
result = trainer.train()

trainer.save_model("./llama-intent")
tokenizer.save_pretrained("./llama-intent")