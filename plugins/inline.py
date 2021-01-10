"""F-Droid Search Bot (inline)"""
from pyrogram import Client
from pyrogram import emoji
from pyrogram.types import InlineQuery
from utils import repodata

CACHE_TIME = 5


@Client.on_inline_query()
async def inline(_, query: InlineQuery):
    string = query.query.lower()

    if string == "":
        await query.answer(
            results=repodata.DEFAULT_RESULTS,
            cache_time=CACHE_TIME,
            switch_pm_text=(f"{emoji.MAGNIFYING_GLASS_TILTED_RIGHT} "
                            "Type to search Apps on F-Droid"),
            switch_pm_parameter="start",
        )
        return

    results = []
    offset = int(query.offset or 0)
    switch_pm_text = f"{emoji.FIRE} Apps on F-Droid"

    if offset:
        await query.answer(
            results=[],
            cache_time=CACHE_TIME,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter="start",
            next_offset="",
        )

    for i in repodata.APPLIST:
        if string in i[0].lower():
            results.append(i[1])

    if results:
        count = len(results)
        switch_pm_text = (f"{emoji.FIRE} {count} "
                          f"Result{'s' if count > 1 else ''} for \"{string}\"")
        await query.answer(
            results=results[:50],
            cache_time=CACHE_TIME,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter="start"
        )
    else:
        await query.answer(
            results=[],
            cache_time=CACHE_TIME,
            switch_pm_text=f'{emoji.CROSS_MARK} No results for "{string}"',
            switch_pm_parameter="start",
        )
