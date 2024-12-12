from transformers import M2M100Tokenizer, M2M100ForConditionalGeneration

def translate_m2m(text, src_lang="en", tgt_lang="hi"):
    """Translate text from source language to target language."""
    model_name = "facebook/m2m100_418M"
    tokenizer = M2M100Tokenizer.from_pretrained(model_name)
    model = M2M100ForConditionalGeneration.from_pretrained(model_name)

    tokenizer.src_lang = src_lang
    inputs = tokenizer(text, return_tensors="pt")

    generated_tokens = model.generate(**inputs, forced_bos_token_id=tokenizer.get_lang_id(tgt_lang))
    return tokenizer.decode(generated_tokens[0], skip_special_tokens=True)
