import pandas as pd
from Reddit_data_cleaning import _normalize_text, tag_mixed_text, split_mixed_by_script
from Reddit_data_analysis import frequency_list
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# the merged data is too big for stanza to handle at once, so only use comments for analysis
df = pd.read_csv("reddit_comments.csv", encoding="utf-8-sig")
df = df.head(100)
text = " ".join(df["Content"].astype(str))

#with open("first_comment.txt", "r", encoding="utf-8-sig") as f:
#    text = f.read()

text = _normalize_text(text)
df_tagged = tag_mixed_text(text)
print("Tagged DataFrame:")
print(df_tagged.head())

# visualize - wordcloud
freq_df = frequency_list(df_tagged, token_column="token", field="lemma", lang_filter=None)
freq_dict = dict(zip(freq_df["item"], freq_df["frequency"]))

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

# visualize - barplot
top_lemma = freq_df.head(20)

plt.figure(figsize=(10, 8))
sns.barplot(
    data=top_lemma,
    x="frequency",
    y="lemma",
    palette="viridis"
)

plt.title("Top 20 Most Frequent Lemmas")
plt.xlabel("Frequency")
plt.ylabel("Lemma")
plt.tight_layout()
plt.show()