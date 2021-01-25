from datetime import datetime
import xml.etree.ElementTree as ET
from pyrogram import emoji
from pyrogram.types import (InlineQueryResultArticle,
                            InputTextMessageContent,
                            InlineKeyboardMarkup,
                            InlineKeyboardButton)


class Result:
    DESCRIPTION_MAX_LEN = 60

    @staticmethod
    def get_summary(item):
        full = item.find('summary').text
        if full is not None:
            short = full[: Result.DESCRIPTION_MAX_LEN].strip()
            if len(short) >= Result.DESCRIPTION_MAX_LEN - 1:
                short += "…"
        else:
            short = full
        return short, full

    class Method:
        def __new__(cls, repo, repo_web, item, query_arg):
            repo_name = repo.get('name').split()[0]
            repo_url = repo.get('url')
            app_info = ""
            app_name = item.find('name').text
            app_id = item.find('id').text
            fdroid_link = f"https://f-droid.org/packages/{app_id}/"
            app_link = f"{repo_web}/{app_id}/"
            app_summary_short, app_summary_full = Result.get_summary(item)
            app_source = item.find('source').text
            app_tracker = item.find('tracker').text
            app_license = item.find('license').text
            app_categories = item.find('categories').text.replace(",", ", ")
            app_marketversion = item.find('marketversion').text
            if app_marketversion:
                app_version = app_marketversion
            else:
                app_version = item.find('package').find('version').text + "(?)"
            app_marketvercode = item.find('marketvercode').text
            app_lastupdated = item.find('lastupdated').text
            app_info = (f"{emoji.MOBILE_PHONE_WITH_ARROW} **{app_name}**\n\n"
                        f"{emoji.INFORMATION} {app_summary_full}\n\n"
                        f"{emoji.LINK} **[{repo_name}]({app_link})**"
                        f" | [Source]({app_source})"
                        f" | [Tracker]({app_tracker})\n"
                        f"- ID: `{app_id}`\n"
                        f"- License: `{app_license}`\n"
                        f"- Categories: `{app_categories}`\n"
                        f"- Version: `{app_version}` - "
                        f"`{app_marketvercode}`\n"
                        f"- Last Updated: `{app_lastupdated}`\n")
            # icon
            app_icon_default = ("https://f-droid.org/"
                                "assets/ic_repo_app_default.png")
            try:
                app_icon = item.find('icon').text
                if app_icon.endswith('.xml'):
                    app_icon_link = app_icon_default
                else:
                    app_icon_link = (f"{repo_url}/icons-640/{app_icon}")
            except AttributeError:
                app_icon_link = app_icon_default
            # antifeatures
            try:
                app_antifeatures = item.find('antifeatures').text
                if app_antifeatures is not None:
                    list_antifeatures = [
                        "#" + tag for tag in app_antifeatures.split(",")
                    ]
                    tags = " ".join(list_antifeatures)
                    app_info += f"- Anti-Features: {tags}"
            except AttributeError:
                pass
            return InlineQueryResultArticle(
                title=f"{app_name}",
                description=f"App - {app_summary_short}",
                input_message_content=InputTextMessageContent(
                    app_info,
                    disable_web_page_preview=True,
                ),
                url=app_link,
                thumb_url=app_icon_link,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                f"Search on {repo_name}",
                                switch_inline_query_current_chat=(query_arg
                                                                  + app_name)
                            ),
                            InlineKeyboardButton(
                                "Try to Open on F-Droid",
                                url=fdroid_link
                            )
                        ]
                    ]
                )
            )


APPLIST_FDROID = []
xml_root = ET.parse('data/fdroid.xml').getroot()
repo_fdroid = xml_root.find('repo')
repo_fdroid_name = repo_fdroid.get('name')
repo_fdroid_time = (
    datetime.utcfromtimestamp(int(repo_fdroid.get('timestamp')))
    .strftime('%Y-%m-%d %H:%M:%S')
)
repo_fdroid_description = (
    repo_fdroid.find('description').text.replace('\n', '')
)
repo_fdroid_web = 'https://f-droid.org/packages'
repo_fdroid_allapp = xml_root.findall('application')
for app in repo_fdroid_allapp:
    app_name = app.find('name').text
    APPLIST_FDROID.append(
        (app_name, Result.Method(repo_fdroid,
                                 repo_fdroid_web,
                                 app,
                                 query_arg=""))
    )

APPLIST_IZZY = []
xml_root = ET.parse('data/izzy.xml').getroot()
repo_izzy = xml_root.find('repo')
repo_izzy_name = repo_izzy.get('name')
repo_izzy_time = (
    datetime.utcfromtimestamp(int(repo_izzy.get('timestamp')))
    .strftime('%Y-%m-%d %H:%M:%S')
)
repo_izzy_description = repo_izzy.find('description').text
repo_izzy_web = 'https://apt.izzysoft.de/fdroid/index/apk'
repo_izzy_allapp = xml_root.findall('application')
for app in repo_izzy_allapp:
    name = app.find('name').text
    APPLIST_IZZY.append(
        (name, Result.Method(repo_izzy, repo_izzy_web, app, query_arg="!i "))
    )

THUMB_FDROID = ("https://assets.gitlab-static.net/uploads/-/system/project/"
                "avatar/36189/ic_launcher.png")
THUMB_IZZY = ("https://assets.gitlab-static.net/uploads/-/system/project/"
              "avatar/4877469/iod_logo.png")
RESULT_ARTICLE_FDROID = InlineQueryResultArticle(
    title="F-Droid",
    input_message_content=InputTextMessageContent(
        (f"{emoji.LABEL} **[{repo_fdroid_name}]({repo_fdroid_web})** "
         f"({len(repo_fdroid_allapp)} Apps)\n\n"
         f"{emoji.INFORMATION} {repo_fdroid_description}\n\n"
         f"{emoji.CALENDAR} `{repo_fdroid_time}`\n\n"
         f"**[DOWNLOAD F-DROID](https://f-droid.org/F-Droid.apk)**"),
        disable_web_page_preview=True,
    ),
    url="https://f-droid.org/",
    reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    f"{emoji.MAGNIFYING_GLASS_TILTED_RIGHT}  "
                    "Search Apps on F-Droid",
                    switch_inline_query_current_chat=""
                )
            ]
        ]
    ),
    description="Free and Open Source Android App Repository",
    thumb_url=THUMB_FDROID,
)
RESULT_ARTICLE_IZZY = InlineQueryResultArticle(
    title="IzzyOnDroid",
    input_message_content=InputTextMessageContent(
        (f"{emoji.LABEL} **[{repo_izzy_name}]({repo_izzy_web})** "
         f"({len(repo_izzy_allapp)} Apps)\n\n"
         f"{emoji.INFORMATION} {repo_izzy_description}\n\n"
         f"{emoji.CALENDAR} `{repo_izzy_time}`"),
        disable_web_page_preview=True,
    ),
    url="https://apt.izzysoft.de/fdroid/",
    reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    f"{emoji.MAGNIFYING_GLASS_TILTED_RIGHT}  "
                    "Search Apps on IzzyOnDroid",
                    switch_inline_query_current_chat="!i "
                )
            ]
        ]
    ),
    description="Free and Open Source Android App Repository",
    thumb_url=THUMB_IZZY,
)
RESULTS_IZZY = [RESULT_ARTICLE_IZZY]
RESULTS_FDROID_AND_IZZY = [RESULT_ARTICLE_FDROID, RESULT_ARTICLE_IZZY]
