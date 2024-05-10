from flask import Blueprint, render_template, abort
from main import cache, entries
import urllib.parse


blog_bp = Blueprint('blog', __name__)

@blog_bp.route("/blogs", methods=['GET'])
@cache.cached(timeout=60 * 60 * 24 * 7)
def blogs():
    return render_template("blogs.html", medium_feed=entries)


@blog_bp.route("/blogs/<string:title>", methods=['GET'])
@cache.cached(timeout=60 * 60 * 24 * 7)
def blog(title):
    for rss_blog in entries:
        if rss_blog.url_title == urllib.parse.quote_plus(title):
            blog_number = entries.index(rss_blog)
   # return 404 if failed to match blog                 
    try:
        blog = entries[blog_number]
    except NameError:
        abort(404)
    
    return render_template("blog.html", blog=blog)

