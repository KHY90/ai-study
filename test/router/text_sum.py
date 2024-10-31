from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

app = FastAPI()

model_name = "csebuetnlp/mT5_multilingual_XLSum"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

WHITESPACE_HANDLER = lambda k: re.sub('\s+', ' ', re.sub('\n+', ' ', k.strip()))

class Article(BaseModel):
    text: str

@app.post("/summarize/")
async def summarize_article(article: Article):
    try:
        
        processed_text = WHITESPACE_HANDLER(article.text)
        
        input_ids = tokenizer(
            [processed_text],
            return_tensors="pt",
            padding="max_length",
            truncation=True,
            max_length=512
        )["input_ids"]

        output_ids = model.generate(
            input_ids=input_ids,
            max_length=84,
            no_repeat_ngram_size=2,
            num_beams=4
        )[0]

        summary = tokenizer.decode(
            output_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False
        )

        return {"summary": summary}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

