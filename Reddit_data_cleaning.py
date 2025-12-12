import pandas as pd
import re
import string
from typing import List, Dict, Tuple
import stanza

# normalization: punct, urls, emoji, whtespaces
def _normalize_text(text: str, encoding="utf-8-sig") -> str:
  punct = re.compile (r'[' + re.escape(string.punctuation) + r'“”‘’—，。、《》~{}]+')
  urls = re.compile(r'https?://\S+|www\.\S+', flags=0)
  emoji = re.compile( '['
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags
    "\U00002700-\U000027BF"  # misc symbols
    "\U0001F900-\U0001F9FF"  # supplemental symbols
    "\U0001FA70-\U0001FAFF"  # extended symbols
    ']+')

  text = punct.sub (r" ", text)
  text = urls.sub(r" ", text)
  text = emoji.sub(r" ", text)
  text = re.sub(r'\s+', ' ', text).strip()
  return text 


# language classification & parsing & tagging

CHIN_re = re.compile(r"[\u4E00-\u9FFF\u3400-\u4DBF\uF900-\uFAFF]") # Chinese character ranges

def split_mixed_by_script(text: str) -> List[Tuple[str, str]]:
    """
    Splits text into runs labeled 'CHIN' or 'ENG'.
    Returns list of (chunk_text, label).
    """
    if not text:
        return []

    runs = []
    current_run = text[0]
    current_is_CHIN = bool(CHIN_re.match(text[0]))   

    for character in text[1:]:
        is_CHIN = bool(CHIN_re.match(character))
        if is_CHIN == current_is_CHIN:
            current_run += character # Chinese chunks or English chunks
        else:
            runs.append((current_run, 'CHIN' if current_is_CHIN else 'ENG'))
            current_run = character 
            current_is_CHIN = is_CHIN 
    # append last run
    runs.append((current_run, 'CHIN' if current_is_CHIN else 'ENG'))
    return runs

def tag_mixed_text(text: str) -> pd.DataFrame:
    """
    Takes a mixed Chinese-English text and returns a DataFrame with columns:
    token, upos, xpos (if available), lemma (if available), lang
    """
    stanza.download('zh')
    stanza.download('en')

    nlp_zh = stanza.Pipeline(lang='zh', processors='tokenize,pos,lemma', use_gpu=False)
    nlp_en = stanza.Pipeline(lang='en', processors='tokenize,pos,lemma', use_gpu=False)
    
    rows = []
    runs = split_mixed_by_script(_normalize_text(text))

    for chunk, label in runs:
        if label == 'CHIN':
            doc = nlp_zh(chunk)
            lang = 'zh'
        else:
            doc = nlp_en(chunk)
            lang = 'en'

        # stanza organizes doc.sentences -> sentence.tokens -> token.words
        for sent in doc.sentences:
            for token in sent.tokens:
                for word in token.words:
                    rows.append({
                        'token': word.text,
                        'upos': word.upos,   # universal POS
                        'xpos': word.xpos if hasattr(word, 'xpos') else None,
                        'lemma': word.lemma if hasattr(word, 'lemma') else None,
                        'lang': lang
                    })

    return pd.DataFrame(rows)



if __name__ == "__main__":
    sample_text = "今天很闲 but the weather is 很 bad。我 don't want to go out 😂."

    cleaned_text = _normalize_text(sample_text)
    print("Normalized text:")
    print(cleaned_text)

    runs = split_mixed_by_script(cleaned_text)
    print("Segmented runs:")
    print(runs)

    df_tagged_text = tag_mixed_text(sample_text)
    print("\nPOS tagged output:")
    print(df_tagged_text)