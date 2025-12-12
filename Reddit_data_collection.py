import requests
import pandas as pd
import praw
from praw.models import MoreComments

# Read Reddit API credentials
with open ("client_secret.txt", "r") as file1, open ("password.txt", "r") as file2:
    CLIENT_SECRET = file1.read().strip()
    PASSWORD = file2.read().strip()

reddit = praw.Reddit(
    client_id="Edymr3QzbizFwCJCblYtjQ",
    client_secret=CLIENT_SECRET,
    password=PASSWORD,
    user_agent="python:reddit_data_collector:1.0 (by /u/No_Speech4672)",
    username="No_Speech4672",
)

print(reddit.user.me())

# Access r/Rednote
Rednote = reddit.subreddit("Rednote")

# Collect new posts from r/Rednote
posts = []
for submission in Rednote.new(limit=None):
    posts.append({
        "Title": submission.title, # get post titles
        "Content": submission.selftext, # get post content
        "Token_count" : len((submission.title + " " + submission.selftext).split()) # get token count
    }) 

df_posts = pd.DataFrame(posts, columns = ["Title", "Content", "Token_count"])
print("Total posts collected:", len(df_posts))
print("Total tokens in the posts collected:", df_posts['Token_count'].sum())
df_posts.to_csv("rednote_new_all.csv", index=False, encoding="utf-8-sig")



# Collect comments from r/Rednote
comments = []
submissions = [
    ("Post_1_as_a_chinese_user_some_advices", reddit.submission(id='1i1k0fq')), # https://www.reddit.com/r/rednote/comments/1i1k0fq/as_a_chinese_user_some_advices_and_cultural/
    ("Post_2_making_the_jump_from_tiktok_to_rednote", reddit.submission(id='1i0ao9w')), # https://www.reddit.com/r/rednote/comments/1i0ao9w/making_the_jump_from_tiktok_to_rednotexiaohongshu/
    ("Post_3_how_rednote_is_perceived", reddit.submission(id='1iz8b8i')), # https://www.reddit.com/r/rednote/comments/1iz8b8i/how_rednote_is_perceived_by_chinese_people/
    ("Post_4_heres_how_i_feel", reddit.submission(id='1i20bfv'))  # https://www.reddit.com/r/rednote/comments/1i20bfv/heres_how_i_feel_about_tiktok_refugees_on_rednote/
]

for name, submission in submissions:
    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():
        comments.append ({
            "Score": comment.score,
            "Content": comment.body,
            "Token_count": len(comment.body.split())
        })
    print(f"Total comments from {name}: {len(submission.comments.list())}")

df_comments = pd.DataFrame(comments, columns = ["Score", "Content", "Token_count"])
print ("Total tokens in the comments collected:", df_comments['Token_count'].sum())
df_comments.to_csv("reddit_comments.csv", index=False, encoding="utf-8-sig")

df_merged = pd.concat([df_posts, df_comments], axis=0) # add vertically
df_merged.to_csv("merged_data.csv", index=False, encoding="utf-8-sig")
