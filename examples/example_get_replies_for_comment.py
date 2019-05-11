from walla import *

article = Article('https://news.walla.co.il/item/3232618')

comments = article.GetCommentsByWriter('ניר נצרת עילית ')

for comment in comments:
    if not(comment.HasFatherComment()):
        replies = comment.GetReplies()
        for reply in replies:
            print("--------")
            print("Found reply for comment ID:" + str(comment.commentId))
            print("--------")
            print("Reply title:" + reply.title)
            print("Reply content:" + reply.content)
            print("Reply writer:" + reply.writer)
            print("Positive Reply likes:" + str(reply.positive_likes))
            print("Negative Reply likes:" + str(reply.negative_likes))