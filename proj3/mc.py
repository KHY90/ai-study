# step 1 : import module
from transformers import AutoTokenizer
from transformers import AutoModelForMultipleChoice
import torch

# step 2 : create inference object(instance)
tokenizer = AutoTokenizer.from_pretrained("stevhliu/my_awesome_swag_model")
model = AutoModelForMultipleChoice.from_pretrained("stevhliu/my_awesome_swag_model")
labels = torch.tensor(0).unsqueeze(0)

# step 3 : prepare data
prompt = "France has a bread law, Le Décret Pain, with strict rules on what is allowed in a traditional baguette."
candidate1 = "The law does not apply to croissants and brioche."
candidate2 = "The law applies to baguettes."

# step 4 : inference
inputs = tokenizer([[prompt, candidate1], [prompt, candidate2]], return_tensors="pt", padding=True)
outputs = model(**{k: v.unsqueeze(0) for k, v in inputs.items()}, labels=labels)
logits = outputs.logits
predicted_class = logits.argmax().item()

# step 5 : post processing
print(predicted_class)
