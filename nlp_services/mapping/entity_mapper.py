from typing import List,Dict,Set

class EntityMapper:
  def __init__(self,alias_map:Dict[str,List[str]]):
    """
    alias_map example:
        {
            "TCS": ["Tata Consultancy Services", "TCS"],
            "INFY": ["Infosys", "Infosys Ltd"]
        }
    """
    self.alias_map = alias_map
    self.normalized_map = self._build_normalized_map()
  
  def _normalize(self,text:str)->str:
    """
      Standardizes text to lowercase and stripped for comparison.
    """
    return text.lower().strip()
  
  def _build_normalized_map(self)->Dict[str,str]:
    """
    Flattens the alias map into a reverse lookup:
      {
        "tata consultancy services": "TCS",
        "tcs": "TCS",
        "infosys": "INFY"
      }
    """
    normalized = {}
    for ticker, aliases in self.alias_map.items():
      for alias in aliases:
        norm_alias = self._normalize(alias)
        normalized[norm_alias] = ticker
    return normalized
  
  def map_entities(self,entities: List[str])->List[str]:
    """
      Input: ["Tata Consultancy Services", "RBI", "Unknown Corp"]
      Output: ["TCS"]
    """
    matched_tickers:Set[str] =set()

    for entity in entities:
      norm_entity = self._normalize(entity)

      # Exact Match
      if norm_entity in self.normalized_map:
        matched_tickers.add(self.normalized_map[norm_entity])
        continue

      # Partial Match
      for alias_norm , ticker in self.normalized_map.items():
        if alias_norm in norm_entity or norm_entity in alias_norm:
          if len(norm_entity)>2 and len(alias_norm)>2:
            matched_tickers.add(ticker)
  
    return list(matched_tickers)


    
    
