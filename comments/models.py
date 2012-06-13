from django.contrib.auth.models import User
from django.db import models
from django.template.base import Template
from django.template.context import Context
from ratings.models import Business
from test.test_support import temp_cwd

_CommentTemplate = Template("""
<li>{{ comment.descr }}
    <div class="comment" id="comment_{{comment.pk}}">
        <form action="." name="addReply" class="comment" id="comment_form_{{comment.pk}}" method="post">
            <input type="text" name="comment" id="comment_{{comment.pk}}"/>
            <input type="hidden" name="cid" id="comment_{{comment.pk}}" value="{{comment.pk}}"/> 
            <input id="bid" value="{{comment.business.id}}" type="hidden" name="bid" />
        </form>
    </div>
{% if comemnt.reply_to %}
    <ul>
 
        {% for reply in  replies%}
        {{ reply }}
        {% endfor %}
    </ul>
    
         
{% endif %}
</li>
""".strip())


# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(User)
    date = models.DateField(auto_now=True)
    business = models.ForeignKey(Business)
    reply_to = models.ForeignKey('self', related_name='replies', 
        null=True, blank=True)
    descr = models.TextField(max_length=2000)
    
    @property
    def html(self):
        temp= _CommentTemplate.render(Context({
            'comment': self,
            'replies': [reply.html() for reply in self.replies.all()]
        }))
        print(temp)
        return temp


class CommentRating(models.Model):
    comment = models.ForeignKey(Comment)
    user = models.ForeignKey(User)
    rating = models.PositiveSmallIntegerField()
    
