import requests
import json
from os.path import basename
from urllib.parse import urlparse
from datetime import datetime


class Comment:

    def __init__(self, article, commentId=0, fatherId=0, writer='', title='', content='', createdate=None, positive_likes=0, negative_likes=0):
        self.article = article
        self.commentId = commentId
        self.fatherId = fatherId
        self.writer = writer
        self.title = title
        self.content = content
        self.createdate = createdate
        self.positive_likes = positive_likes
        self.negative_likes = negative_likes

    def GetReplies(self):
        replies = []
        all_comments = self.article.GetComments()
        for comment in all_comments:
            if comment.fatherId == self.commentId:
                replies.append(comment)
        return replies

    def Dislike(self):
        r = requests.post('https://dal.walla.co.il/talkback/emotion/', params={'id':str(self.commentId), 'emotion':'0'})
        return json.loads(r.text)

    def Like(self):
        r = requests.post('https://dal.walla.co.il/talkback/emotion/', params={'id':str(self.commentId), 'emotion':'1'})
        return json.loads(r.text)

    def Reply(self, writer, content):
        r = requests.post('https://dal.walla.co.il/talkback/',
                          params={'object-id':self.article.article_id,
                                  'father-id':self.commentId,
                                  'type':'1',
                                  'writer':writer,
                                  'content':content}).text
        r_json = json.loads(r)
        if r_json['result'] == 'success':
            return Comment(article=self.article,
                           commentId=r_json['data'],
                           fatherId=self.commentId,
                           writer=writer,
                           content=content
                           )
        else:
            return r_json


class Article:

    def __init__(self, article_url):
        self.article_url = article_url
        self.article_id = basename(urlparse(article_url).path)

    def GetComments(self):
        r = requests.get('https://dal.walla.co.il/talkback/list/' + self.article_id, params={'type':'1', 'page':'1'})
        r_json = json.loads(r.text)['data']['list']
        return self._GetComments(r_json)

    def GetCommentsByWriter(self, writer):
        comments = []
        all_comments = self.GetComments()
        for comment in all_comments:
            if comment.writer == writer:
                comments.append(comment)
        return comments

    def PostComment(self, writer, content, title):
        r = requests.post('https://dal.walla.co.il/talkback/',
                          params={'object-id': self.article_url,
                                  'type': '1',
                                  'writer': writer,
                                  'content': content,
                                  'title': title}).text
        r_json = json.loads(r)
        if 'result' in r_json.keys():
            if r_json['result'] == 'success':

                return Comment(commentId=r_json['data'],
                               writer=writer,
                               title=title,
                               content=content
                            )
            else:
                return r_json
        else:
            return r_json
    def _GetComments(self, commentList):
        comments = []
        for commentDict in commentList:
            createdate = datetime.strptime(commentDict['createDate'], '%H:%M %d.%m.%y')
            comment = Comment(article=self,
                              commentId=commentDict['id'],
                              fatherId=commentDict['fatherId'],
                              writer=commentDict['writer'],
                              title=commentDict['title'],
                              content=commentDict['content'],
                              createdate=createdate,
                              positive_likes=commentDict['positive'],
                              negative_likes=commentDict['negative']
                              )
            comments.append(comment)
            if len(commentDict['children']) != 0:
                comments += self._GetComments(commentDict['children'])

        return comments

