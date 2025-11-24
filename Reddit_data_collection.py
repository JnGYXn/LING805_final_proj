import requests
import pandas as pd
from praw_rec import reddit
from praw.models import MoreComments



Rednote = reddit.subreddit("Rednote")

# Collect new posts from r/Rednote

posts = []
for submission in Rednote.new(limit=None):
    posts.append({
        "Title": submission.title, # get post titles
        "Content": submission.selftext, # get post content
        "Tokens" : len((submission.title + " " + submission.selftext).split()) # get token count
    }) 

df_posts = pd.DataFrame(posts, columns = ["Title", "Content", "Tokens"])
print("Total posts collected:", len(df_posts))
print("Total tokens in the posts collected:", df_posts['Tokens'].sum())
df_posts.to_csv("rednote_new_all.csv", index=False, encoding="utf-8")



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
            "Comment_id": comment.id,
            "Comments": comment.body,
            "Score": comment.score,
            "Token_count": len(comment.body.split())
        })
    print(f"Total comments from {name}: {len(submission.comments.list())}")

df_comments = pd.DataFrame(comments, columns = ["Comment_id", "Comments", "Score", "Token_count"])
print ("Total tokens in the comments collected:", df_comments['Token_count'].sum())
df_comments.to_csv("reddit_comments.csv", index=False, encoding="utf-8")