from django import template
from ..models import Post
from django.db.models import Count

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()

@register.inclusion_tag('blog/post/latest_posts.html') # inclusion tags have to return a dictionary
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
    # 'Count' in the next line counts the number of comments on each post (published post in this case)
    # each published post gets 'total_comments' "annotated" to it
    # a QuerySet is returned with the annotated published posts and ordered by the total_comments field (or annotation)
    # only the desired number (indicated by 'count' variable) is returned... in this case it's the top commented posts
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]