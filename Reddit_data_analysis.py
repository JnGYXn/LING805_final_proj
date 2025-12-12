import pandas as pd
from collections import Counter
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from Reddit_data_cleaning import tag_mixed_text
from wordcloud import WordCloud
import matplotlib.pyplot as plt



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
        for tok in row[token_column].split():
            if row["lang"] == "en" and tok in stopwords_en:
                continue
            if row["lang"] == "zh" and tok in stopwords_zh:
                continue
            if tok:
                counter[tok] += 1

    # Convert to DataFrame
    freq_df = (
        pd.DataFrame(counter.items(), columns=["item", "frequency"])
        .sort_values("frequency", ascending=False)
        .reset_index(drop=True)
    )
    return freq_df

if __name__ == "__main__":  
    
    df = pd.read_csv("reddit_comments.csv", encoding="utf-8-sig")
    df = df.head(100)
    text = " ".join(df["Content"].astype(str))
    df_tagged_text = tag_mixed_text(text)
    freq_list = frequency_list(df_tagged_text, token_column="token", lang_filter=None)
    print("Frequency List:")    
    print(freq_list.head(20))

    freq_dict = dict(zip(freq_list["item"], freq_list["frequency"]))

    wordcloud = WordCloud(
    width=1600,
    height=800,
    background_color="white",
    colormap="viridis"
    ).generate_from_frequencies(freq_dict)

    plt.figure(figsize=(16, 8))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()