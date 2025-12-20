from textblob import TextBlob

class SentimentModel:
  def score(self,text:str)->float:
    """
    Returns sentiment in range [-1.0, 1.0].
    """

    if not text:
      return 0.0
    
    blob = TextBlob(text)
    return float(blob.sentiment.polarity)
  