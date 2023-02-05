import feedparser, re
# formats blogs from rss to usable for the site
def prepare_blogs(url):
    feed = feedparser.parse(url)
    entries = feed.entries
    for item in entries:
        tags=''
        # remove queries from url
        item.link = item.link.split('?')[0]
        # add url title with hyphens
        item.url_title = item.title.replace(" ", "-")
        
        # format summary
        if len(item.summary) > 150:
            item.summary = item.summary[:150] + "..."
        item.summary = re.sub("<[^>]*>", "",item.summary)
        item.summary = item.summary.replace(u"\u00A0", " ")

        # format tags       
        for term in item.tags:
            tags += term['term'] + ','
        item.tags = tags[:-1]

        
    
    return entries