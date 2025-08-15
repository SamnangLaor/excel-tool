from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Load model and tokenizer
model_name = "facebook/nllb-200-distilled-600M"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

model_name = "facebook/nllb-200-distilled-600M"  # You can choose a larger model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def translate(text, src_lang="eng_Latn", tgt_lang="khm_Khmr"):
    # Tokenize input text
    inputs = tokenizer(text, return_tensors="pt")

    # Generate translation
    translated_tokens = model.generate(
        **inputs,
        forced_bos_token_id=tokenizer.convert_tokens_to_ids(tgt_lang)
    )

    return tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]

# Example usage
text = "Device set to use cpu"
translated_text = translate(text, src_lang="eng_Latn", tgt_lang="khm_Khmr")
print(translated_text)