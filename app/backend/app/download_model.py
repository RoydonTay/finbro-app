from transformers import AutoModelForSequenceClassification, AutoTokenizer

# This script downloads the model and adds it to the directory app/models/<model_name>. You should see it appear

# download model (replace with your model from HF repo)
MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

# save the model
save_dir = "models/roberta-base"
tokenizer.save_pretrained(save_dir)
model.save_pretrained(save_dir)