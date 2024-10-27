# 스텝 1 : import modules
from fastapi import FastAPI, Form
from transformers import pipeline

# step 2 : create inference object(instance)
classifier = pipeline("sentiment-analysis", model="snunlp/KR-FinBert-SC")

app = FastAPI()

@app.post("/inference/")
async def login(text: str = Form()):

    # step 3 : prepare data
    # step 4 : inference
    result = classifier(text)

    # step 5 : Post processing
    print(result)
    
    return {"result": result}