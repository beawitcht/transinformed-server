import feedparser, re, urllib.parse
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
        item.url_title = urllib.parse.quote_plus(item.url_title)

        # format summary
        max_length = 60
        if len(item.summary) > max_length:
            item.summary = item.summary[:max_length] + "..."
        item.summary = re.sub("<[^>]*>", "",item.summary)
        item.summary = item.summary.replace(u"\u00A0", " ")

        # format tags
        if hasattr(item, 'tags'):
            for term in item.tags:
                tags += term['term'] + ','
            item.tags = tags[:-1]


        # format content
        # remove tracking pixels from RSS
        tracking_pixel = re.compile(r'<img[^>]*height="1"[^>]*>')
        match = tracking_pixel.search(item.content[0].value)
        while match:
            item.content[0].value = item.content[0].value.replace(match.group(), '')
            match = tracking_pixel.search(item.content[0].value)

        # get first image for use as card image
        first_img = re.compile(r'<img([\w\W]+?)/>')
        img_match = first_img.search(item.content[0].value)
        if img_match:
            card_img = img_match.group()
            #append class
            item.card_img = card_img.replace('<img', '<img class="card-image"', 1)
            #use local img
            item.card_img = item.card_img.replace('https://cdn-images-1.medium.com/max/1024/', '/static/images/thumbs/', 1)
            item.card_img = item.card_img.replace('" />', '.jpg" />', 1)

    return entries
