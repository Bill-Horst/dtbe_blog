from django.contrib.sitemaps import Sitemap

from .models import Post

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.published.all() # gets all the posts and their urls - by default, get_absolute_url() is used

    def lastmod(self, obj):
        return obj.updated