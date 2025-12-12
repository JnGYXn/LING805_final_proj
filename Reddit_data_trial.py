import pandas as pd
from Reddit_data_cleaning import tag_mixed_text
from frequency_list import frequency_list
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# the merged data is too big for stanza to handle at once
df = pd.read_csv("reddit_comments.csv", encoding="utf-8-sig")
df = df.head(100)
text = " ".join(df["Content"].astype(str))

df_tagged_text = tag_mixed_text(text)
print("Tagged DataFrame:")
print(df_tagged_text.head())

#freq_df = frequency_list (df_tagged, token_column="token", field="lemma", lang_filter=None)
#print("Frequency DataFrame:")   
#print(freq_df.head(20)) 

#df_tagged["lemma_clean"] = (
 #   df_tagged["lemma"]
  #  .fillna(df_tagged["token"])
   # .astype(str)
    #.str.lower()
#)

freq_df = frequency_list (df_tagged_text, token_column="token", lang_filter=None)
freq_df.columns = ["item", "frequency"]

# visualize - wordcloud
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