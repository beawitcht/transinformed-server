from pathlib import Path
from utilities import prepare_blogs

path = Path(__file__).parent.resolve()
output = path / "templates" / "blogs"

# get blogs
entries = prepare_blogs("https://medium.com/feed/@transinformed")

for blog in entries:
    # set as html
    blog_content = blog.content[0].value
    
    # modify with classes - should be done here as much as possible to minimise adjustments needed
    blog_content = blog_content.replace("<h4>", " <h4 class=\"blog-description description-text\">", 1)
    blog_content = blog_content.replace("<h3>", "<h3 class=\"blog-header\">")
    blog_content = blog_content.replace("<img", "<img class=\"blog-image-container blog-image\"")
    blog_content = blog_content.replace("<figcaption>", "<figcaption class=\"blog-image-caption\">")
    blog_content = blog_content.replace("<p>", "<p class=\"blog-paragraph\">")
    blog_content = blog_content.replace("<em>", "<em class=\"blog-disclaimer\">")
    blog_content = blog_content.replace("<blockquote>", "<blockquote class=\"blog-quote\">")
    blog_content = blog_content.replace("<h4>", " <h4 class=\"blog-subheading blog-subheading-layout\">")
    

    blog_file_path = output / f"{blog.title}.html"
    if not blog_file_path.is_file():
        with open(blog_file_path, 'w+') as f:
            # output to html file with inheritance of blog.html - allows for modifying HTML directly for formatting
            # when articles are updated, they will need to be manually deleted and re-created
            f.write("{% extends 'blog.html' %}\n{{ super() }}\n{% block blog_body %}\n" + blog_content + "\n{% endblock %}\n{% block ad %}\n{{ super() }}\n{% endblock %}")

        print(f"{blog.title} added!")
