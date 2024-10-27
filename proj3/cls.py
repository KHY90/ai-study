# Text classification
# 스텝 1 : import modules
from transformers import pipeline

# step 2 : create inference object(instance)
# classifier = pipeline("sentiment-analysis", model="stevhliu/my_awesome_model")
classifier = pipeline("sentiment-analysis", model="snunlp/KR-FinBert-SC")

# step 3 : prepare data
text = "This was a masterpiece."
text2 = "11월8일 배송 갤폴드Z SE, 출시 첫날 판매량 왜 제한했나"

# step 4 : inference
result = classifier(text2)

# step 5 : Post processing
print(result)