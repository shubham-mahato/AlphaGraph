import sys
from pathlib import Path

# Add root to sys.path
ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

from nlp_services.models.sentiment_model import FinBERTSentimentModel

def test_finbert_smoke():
    print("\n🚀 Initializing FinBERT Smoke Test...")
    model = FinBERTSentimentModel()

    # Case 1: Good News
    pos_text = "TCS reports 20% increase in quarterly profits and strong guidance."
    pos_score = model.score(pos_text)
    print(f"Positive Text: {pos_score:.4f}")

    # Case 2: Bad News
    neg_text = "TCS shares plunge after CEO resigns amid fraud allegations."
    neg_score = model.score(neg_text)
    print(f"Negative Text: {neg_score:.4f}")

    # Assertions
    assert pos_score > 0.2, "Positive text should have positive score"
    assert neg_score < -0.2, "Negative text should have negative score"
    
    print("✅ FinBERT Smoke Test PASSED!")

if __name__ == "__main__":
    test_finbert_smoke()