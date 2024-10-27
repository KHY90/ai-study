# STEP 1: Import the necessary modules.
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python.components import processors
from mediapipe.tasks.python import vision

# STEP 2: Create an ImageClassifier object. 추론기를 객체로 만든다
base_options = python.BaseOptions(model_asset_path='models\efficientnet_lite0.tflite')
options = vision.ImageClassifierOptions(
    base_options=base_options, max_results=3)
classifier = vision.ImageClassifier.create_from_options(options)
# max_results=3 결과를 3개만 보겠다.

# STEP 3: Load the input image. 이미지를 넣는다.
image = mp.Image.create_from_file('burger.jpg')

# STEP 4: Classify the input image. 이미지를 추론기에 넣는다.
classification_result = classifier.classify(image)
# print(classification_result)

# ClassificationResult(
#   classifications=[
#     Classifications(
#       categories=[
#         Category(index=933, score=0.9790240526199341, display_name='', category_name='cheeseburger'),
#         Category(index=931, score=0.0008637145510874689, display_name='', category_name='bagel'), 
#         Category(index=947, score=0.0005722717614844441, display_name='', category_name='mushroom')
#         ], 
#     head_index=0, head_name='probability')
#     ],
#   timestamp_ms=0
#   )

# STEP 5: Process the classification result. In this case, visualize it. 결과
top_category = classification_result.classifications[0].categories[0]
print(f"{top_category.category_name} ({top_category.score:.2f})")
