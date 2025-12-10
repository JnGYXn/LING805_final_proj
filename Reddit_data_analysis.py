import pandas as pd
from collections import Counter



def frequency_list(
        df,
        token_column="token",
        field="lemma",         
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
    field : str
        Which token field to count ("lemma" or "text").
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
    for _, row in df.iterrows():
        tokens = row[token_column]
        for tok in tokens:
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
