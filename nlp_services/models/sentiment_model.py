from typing import Dict,List
import torch
from transformers import AutoTokenization, AutoModelForSequenceClassification

class FinBERTSentimentModel:
    """
    Finance-domain sentiment model using FinBERT (ProsusAI).
    Outputs sentiment in range [-1, 1].
    """
    MODEL_NAME ="prosusai/finbert"

    LABEL_TO_SCORE: Dict[str,float] ={
        "positive": 1.0,
        "neutral" : 0.0,
        "negative": -1.0,
    }

    def __init__(self):
      print(f"... Loading FinBERT ({self.MODEL_NAME})... this might take a moment.")
      self.tokenizer = AutoTokenization.from_pretrained(self.MODEL_NAME)
      self.model = AutoModelForSequenceClassification.from_pretrained(self.MODEL_NAME)
      self.model.eval()
    
    def score(self,text:str)->float:
      """
      Returns a single float score between -1.0 (Negative) and 1.0 (Positive).
      """
      if not text or not text.strip():
         return 0.0
      
      #Tokenization
      inputs = self.tokenizer(
         text,
         return_tensors = "pt",
         truncation = True,
         padding = True,
         max_length = 512,
      )

      #Inference
      with torch.no_grad():
         outputs = self.model(**inputs)
         # Apply SoftMax to get probabilities [0.1, 0.8, 0.1]
         probs = torch.softmax(outputs.logits, dim=1)[0]
      
      #Calculate weighted score
      # id2label is usually {0: 'positive', 1: 'negative', 2: 'neutral'}
      labels = self.model.config.id2label
      sentiment_score = 0.0

      for idx, prob in enumerate(probs):
         label_name = labels[idx].lower()
         # Multiply probability by the score weight
         # e.g., 0.8 * 0.0 (Neutral) + 0.1 * 1.0 (Pos) + 0.1 * -1.0 (Neg)
         if label_name is self.LABEL_TO_SCORE:
            sentiment_score += prob.item() * self.LABEL_TO_SCORE[label_name]

      return float(sentiment_score)
    
if __name__ == "__main__":
   model = FinBERTSentimentModel()
   print(f"Test Score: {model.score('Growth is strong and profits are high.')}")