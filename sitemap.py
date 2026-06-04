"""This module generates sitemap using specific library. It contains functions
to register static pages and pages with variable index in the link"""

from flask_sitemap import Sitemap

from data import db_session
from data.news import News
from data.stories import Stories

sitemap = Sitemap()


def get_last_story_publication_date():
    """This fuction get newest story publictaion date and converts it to the
    format YYYY-MM-DD. It view only checked (visible to all users) stories"""
    try:
        with db_session.create_session() as active_sess:
            return (
                active_sess.query(Stories.date)
                .filter(Stories.checked is True)
                .order_by(Stories.date.desc())
                .first()
            )[0].strftime("%Y-%m-%d")
    except TypeError:
        return "1970-01-01"


def get_last_news_publication_date():
    """This fuction get newest news publictaion date and converts it to the
    format YYYY-MM-DD"""
    try:
        with db_session.create_session() as active_sess:
            return (active_sess.query(News.date).order_by(News.date.desc()).first())[
                0
            ].strftime("%Y-%m-%d")
    except TypeError:
        return "1970-01-01"


@sitemap.register_generator
def static_sitemap():
    """This fucntion registrates sitemap for static pages with all parameters"""
    yield ("index", {}, "2026-06-04", "monthly", 1.0)
    yield ("about", {}, "2026-04-30", "monthly", 0.5)
    yield (
        "stories_handlers.show_stories",
        {},
        get_last_story_publication_date(),
        "weekly",
        0.8,
    )
    yield (
        "news.news_list",
        {},
        get_last_news_publication_date(),
        "monthly",
        0.8,
    )


@sitemap.register_generator
def news_sitemap():
    """This fucntion registrates sitemap for news pages with all parameters"""
    with db_session.create_session() as active_sess:
        query = active_sess.query(News.id, News.date).yield_per(100)
        for news in query:
            print(news)
            yield "news.view_publication", {"news_num": news.id}, news[1].strftime(
                "%Y-%m-%d"
            ), "monthly", 0.7
