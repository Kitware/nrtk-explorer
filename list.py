from huggingface_hub import list_models

models = list_models(task="object-detection", library="transformers", cardData=True)

for model in models:
    if model.card_data and model.card_data.datasets:
        print(model.id)
        print("datasets", model.card_data.datasets)
