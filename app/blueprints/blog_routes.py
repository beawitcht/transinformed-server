from flask import Blueprint, render_template, abort
from main import cache
from utilities import prepare_blogs
import urllib.parse

# get blogs
entries = prepare_blogs("https://medium.com/feed/@transinformed")

blog_bp = Blueprint('blog', __name__)

@blog_bp.route("/", methods=['GET'])
@cache.cached(timeout=60 * 60 * 24 * 7)
def blogs():
    return render_template("index.html", medium_feed=entries)


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
    
    return render_template(f"blogs/{blog.title}.html", blog=blog)

