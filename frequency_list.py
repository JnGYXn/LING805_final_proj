import pandas as pd
from collections import Counter
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords



def frequency_list(
        df,
        token_column="token",        
        lang_filter=None       # optionally restrict to "en" or "zh"
    ) -> pd.DataFrame:
    """
    Generate a frequency list from a DataFrame containing Stanza token output.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing a column with token lists.
    token_column : str
        Column name storing token lists.
    lang_filter : str or None
        If set to "en" or "zh", only include rows of that language.
    Returns
    -------
    pd.DataFrame
        A frequency list with columns [item, frequency], sorted by frequency desc.
    """

    # Optionally filter by language
    if lang_filter is not None:
        df = df[df["lang"] == lang_filter]

    counter = Counter()

    # Counting occurrences
    stopwords_en = set(stopwords.words("english"))
    stopwords_zh = set(stopwords.words("chinese"))

    for _, row in df.iterrows():
        tokens = row[token_column]
        for tok in tokens:
            if row["lang"] == "en" and tok.get("lemma") in stopwords_en:
                continue
            if row["lang"] == "zh" and tok.get("lemma") in stopwords_zh:
                continue
            value = tok.get(field, None) if isinstance(tok, dict) else tok
            if value:
                counter[value] += 1

    # Convert to DataFrame
    freq_df = (
        pd.DataFrame(counter.items(), columns=["item", "frequency"])
        .sort_values("frequency", ascending=False)
        .reset_index(drop=True)
    )
    return freq_df

if __name__ == "__main__":  
    # Example usage
    data = {
        "lang": ["en", "en", "en", "zh", "zh", "zh"],
        "token": [
            [{"text": "Hello"}, {"text":"world"}],
            [{"text": "Hello"}, {"text": "everyone"}],
            [{"text": "the"}, {"text": "is"}],
            [{"text": "你好"}, {"text": "世界"}],
            [{"text": "你好"}, {"text": "朋友"}],
            [{"text": "的"}, {"text": "是"}]
        ]
    }
    df = pd.DataFrame(data)

    freq_en = frequency_list(df, token_column="token", lang_filter="en")
    print("English Frequency List:")
    print(freq_en)

    freq_zh = frequency_list(df, token_column="token", lang_filter="zh")
    print("\nChinese Frequency List:")
    print(freq_zh)