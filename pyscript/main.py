from extractEML import GMAIL_EXTRACTOR
from extension_dt_model import DT_MODEL
    
run = GMAIL_EXTRACTOR()
input = run.value()

predict = DT_MODEL(input)
prediction = predict.result()

print(input)
print(prediction)