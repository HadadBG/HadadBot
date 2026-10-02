import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

BASE_MODEL = "meta-llama/Llama-3.2-1B-Instruct"
ADAPTER = "./llama-intent"
OUTPUT = "./llama-intent-merged"

print("1. Cargando tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)

print("2. Cargando modelo base en CPU...")

base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    torch_dtype=torch.float16,
    device_map="cpu",
    low_cpu_mem_usage=True
)

print("3. Cargando LoRA...")

model = PeftModel.from_pretrained(
    base_model,
    ADAPTER
)

print("4. Fusionando LoRA...")

merged_model = model.merge_and_unload()

print("5. Guardando modelo fusionado...")

merged_model.save_pretrained(
    OUTPUT,
    safe_serialization=True
)

tokenizer.save_pretrained(OUTPUT)

print()
print("================================")
print("Modelo fusionado correctamente")
print(f"Salida: {OUTPUT}")
print("================================")