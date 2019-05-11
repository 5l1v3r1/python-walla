from walla import *

article = Article('https://food.walla.co.il/item/3234854')

comments = article.GetComments()

for comment in comments:
    if comment.HasFatherComment():
        print("--------")
        print("Found reply for comment ID:" + str(comment.GetFatherComment().commentId))
        print("--------")
        print("Reply title:" + comment.title)
        print("Reply content:" + comment.content)
        print("Reply writer:" + comment.writer)
        print("Positive Reply likes:" + str(comment.positive_likes))
        print("Negative Reply likes:" + str(comment.negative_likes))