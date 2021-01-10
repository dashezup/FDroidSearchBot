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
        def __new__(cls, item):
            app_info = ""
            app_name = item.find('name').text
            app_id = item.find('id').text
            app_link = f"https://f-droid.org/packages/{app_id}/"
            app_summary_short, app_summary_full = Result.get_summary(item)
            app_source = item.find('source').text
            app_tracker = item.find('tracker').text
            app_license = item.find('license').text
            app_categories = item.find('categories').text
            app_marketversion = item.find('marketversion').text
            app_marketvercode = item.find('marketvercode').text
            app_lastupdated = item.find('lastupdated').text
            app_info = (f"**{app_name}**\n"
                        f"__{app_summary_full}__\n"
                        f"[F-Droid]({app_link})"
                        f" | [Source]({app_source})"
                        f" | [Tracker]({app_tracker})\n"
                        f"License: `{app_license}`\n"
                        f"Categories: `{app_categories}`\n"
                        f"Version: `{app_marketversion} "
                        f"({app_marketvercode})`\n"
                        f"Last Updated: `{app_lastupdated}`\n")
            # icon
            app_icon_default = ("https://f-droid.org/"
                                "assets/ic_repo_app_default.png")
            try:
                app_icon = item.find('icon').text
                if app_icon.endswith('.xml'):
                    app_icon_link = app_icon_default
                else:
                    app_icon_link = ("https://ftp.fau.de/"
                                     f"fdroid/repo/icons-640/{app_icon}")
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
                    app_info += f"Anti-Features: {tags}"
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
            )


APPLIST = []
for app in ET.parse('index.xml').getroot().findall('application'):
    name = app.find('name').text
    APPLIST.append((name, Result.Method(app)))


THUMB_FDROID = ("https://assets.gitlab-static.net/uploads/-/system/project/"
                "avatar/36189/ic_launcher.png")
DEFAULT_RESULTS = [
    InlineQueryResultArticle(
        title="F-Droid",
        input_message_content=InputTextMessageContent(
            "**[F-Droid](https://f-droid.org/)** is an installable "
            "catalogue of FOSS (Free and Open Source Software) applications "
            "for the Android platform. The client makes it easy to browse, "
            "install, and keep track of updates on your device.\n"
            "[DOWNLOAD F-DROID](https://f-droid.org/F-Droid.apk)",
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
]
