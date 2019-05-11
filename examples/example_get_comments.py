from walla import *

article = Article('https://food.walla.co.il/item/3234854')

comments = article.GetComments()

for comment in comments:
    print("-----------")
    print("Comment title:" + comment.title)
    print("Comment content:" + comment.content)
    print("Comment writer:" + comment.writer)
    print("Positive Comment likes:" + str(comment.positive_likes))
    print("Negative Comment likes:" + str(comment.negative_likes))