from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Choose the model you want to download (in this case, NLLB)
model_name = "facebook/nllb-200-distilled-600M"

# Download the model and tokenizer
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Save the model and tokenizer locally
model.save_pretrained("./local_model")
tokenizer.save_pretrained("./local_tokenizer")

print("Model and tokenizer downloaded and saved locally!")