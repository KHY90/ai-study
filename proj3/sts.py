# sentence_transformers
# step 1 : import modules
from sentence_transformers import SentenceTransformer

# step 2
# model = SentenceTransformer("all-MiniLM-L6-v2")
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# step 3
# sentences = [
#     "The weather is lovely today.",
#     "It's so sunny outside!",
#     "He drove to the stadium.",
# ]
sentences1 = "밥 먹었니"
sentences2 = "식사합시다"

# step 4
embeddings1 = model.encode(sentences1)
embeddings2 = model.encode(sentences2)

print(embeddings1.shape)

# step 5
similarities = model.similarity(embeddings1, embeddings2)
print(similarities)
