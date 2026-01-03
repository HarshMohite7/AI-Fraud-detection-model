from ml.inference.model_loader import load_model

model = load_model('ml/model/fund_model.pt')

def detect_fund(data):
    # Placeholder inference logic
    return 0.95 # fraud probability
