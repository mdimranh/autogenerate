from __main__ import app

from manage.urls import url_pattern

for urls in url_pattern:
    for url in urls:
        app.add_url_rule(url[0], methods=url[1], view_func=url[2])