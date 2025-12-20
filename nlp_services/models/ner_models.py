import spacy
from typing import List

class NER_Model:
  def __init__(self):
    self.ner =spacy.load("en_core_web_sm")
  
  def extract_org_entities(self,text:str)->List[str]:
    """
    Extract ORG entities (companies, institutions).
    """

    if not text:
      return []
    
    doc = self.nlp(text)
    orgs = set()

    for ent in doc.ents:
      if ent.lable_ == "ORG":
        orgs.add(ent.text.strip())
    
    return list(orgs)