import re
import typing

from osrsbox import items_api
from osrsbox.items_api.item_properties import ItemProperties

import rsapi.util


ITEMS = items_api.load()
SKILLS = [
    ("Overall",                 "Overall", "data:image/gif;base64,R0lGODlhEAAQAIcAAAAAAP///wgICNEYGnYPEXYQEZcVGHsSE8dUVaYXG4QTGIQTF3YRFWoPElQMD00LDYoUGIMTF3oSFn8TF3IRFGMPElAMD08MDm8RFFsOEZopLGpAQcR3eqGFhksLDkQKDTcIC0gLDkAKDUQLDlQOEpQkKsBJT/zr7NEaKKUYJSsHCogdJbU6RFE1OHwWIndoauhMYtElQ+QxUNOPn8IhS6mdoYd+grujrm9iaV1YW8m0yZSPlMjEzHVyeREXQUZSpi4/nzA/kzE1TBojTygtRCQsP0JHURgfKz5KXSsxO4CMnR8oNCgyQCo0QUlWaCs2RDRBUSw3RD5MXUBOX0dWaUlYa11rfbzP5nJ7hiY0RB8qNh8oMi05RzdFVTZEU0dYazE9Skpbbk1ecVxvhTtHVVRleG2DmyY2RyQyQD5OX0NUZU5hdHWFlhgjLS9CUyUxPDlJWD5OXWuCmIuapr7W50VTXL7a677Y6b3X6LvV5r3Y6HaDikJMUGyDi6S5wWmFii03OF1pY3SDe32Ngz1FQHKAd0FKREdQSnuKgISXiY6ikqKtpG+EchpZISJnKzN5PHCpdw9JFBtcIiJjKCpvMS1yM0aPTUSHS16hZQo9DhVSGj2FQ1pxW3mPeqi6qWl1aMPFvv/3cf/eIf/nWP/oaP/XBP/aKP/dO//pef/pif/aTvm4Av/IJd+2RP/VV//FOee1O/+1CP+2GP+8J9moOP/JTP/LXP/QY//WfbqTQcabRuCxVf/NZf/+/P+hAP+oFP/Nfv/Ujf+2SPSOBt6BC9d/FP+nN//Dd//FfM9vAJNNAP+pR7pkE/+LIP+2df+gVaFDAMlPAKM+AOhlFc5dFZNSKdpTD9dZFfV7PB0QCsNMGRgHAXgqDNFbL29OQkgUBOBQHug2AM82DSsSC7tWOKNONVgUAzkVDGMVBO5QLNg+IJ0sF2wOAKU9M+ZjV7JDPN3JyKc3M7BYVFAMDJ4nJ6ErKqEuLsNFRM5eXsi0tO7a2pyUlJaOjv/+/gEBAf///yH5BAMAAP8ALAAAAAAQABAAAAitAP8JHEiwoEGBAhImPDhQACRIni4JYPhPgKeLlyRSFIAJU0SNBRUKsGRJUaVKEwkKuHcP38iSlRylRIivZj0BmzYlciRT5bt3COjh1OlI0syKP4MKePSokySjKuPFM1FiaVNJmkRWlEpVACVKjDRlBQLkR0J79kys8Ao264+3Q86mXTtp0qdIAoQI+RFXgAYNLNY2asQpkwAiRIL0LVGChQt/gwsLKFIkiA8BAQEAOw=="),
    ("Attack",                  "Att",     "data:image/gif;base64,R0lGODlhEAAQALMAAEY8L7u5A3huYVpQQ1BGOWRaTYJ4a3d7CXd3dwAAAP///wAAAAAAAAAAAAAAAAAAACH5BAEAAAoALAAAAAAQABAAAAQ+UMlJZbqp6otQ1hPXfaDokZV5gQpnnCwnwGWCFPRmD3mIIYRe6HAIHIS+YmAVAwCIqFTCmThEKYkl5urjaiIAOw=="),
    ("Defence",                 "Def",     "data:image/gif;base64,R0lGODlhEAAQAKIAAFtbVZCQkHd3dwAAAP///wAAAAAAAAAAACH5BAEAAAQALAAAAAAQABAAAANBSLrcOzBKyAa4IovAR8Xa1n1ABomB94Anl5LmgKqKNUXvekN5zcouGsFSErRGq+KxN7TERJSKU5MSPqZVx1XSSAAAOw=="),
    ("Strength",                "Str",     "data:image/gif;base64,R0lGODlhDQAQAKIFAEY8L9CyhAAAAQAAAKGSev///wAAAAAAACH5BAEAAAUALAAAAAANABAAAANEWFois1C10BwcjRAQgJXBBnCchYXaSDoCqqUb1YovEE+baNvOGbgjgkDhe2kai5breFEahxCnhhKR/qDJn5Z6GXi/0AQAOw=="),
    ("Hitpoints",               "HP",      "data:image/gif;base64,R0lGODlhEAAQAKIFAHo9CbM5AwAAAQAAAN1PAf///wAAAAAAACH5BAEAAAUALAAAAAAQABAAAANEWCUso6MJtQa5joUAxmNX6BEb0IFhepWn6nKtm8KRPJu1TdKazDILQeDFASo0m5XJSEFuihNKU2BaRqVTK3Yr2Xo93gQAOw=="),
    ("Ranged",                  "Range",   "data:image/gif;base64,R0lGODlhEgASAKIGAAlsAjUvG3V7fHo9CQAAAQAAAP///wAAACH5BAEAAAYALAAAAAASABIAAANoaLrcW6QYSGp0hoyoh9+SpXTd53GbUkDCFkGnUDGFIKyqF1x0LUuQwEnSs60Kuw/v4SMEjh1io7YjFjzSyTFgBGIfBADg2YQNpAVxAHA0RheVNVtrGzIqAN7KtoTjmBp9GA9fg1NHBgkAOw=="),
    ("Prayer",                  "Pray",    "data:image/gif;base64,R0lGODlhDwAPAMQdALfOu83n0JayoarCsLPLuJm1o6zDsb/Xw87o0RMTDa/Es6jArp25p7vRvZWwnqG2pcTcx9Dq0rrSvcHYxLDItM/p0rjPu8vkzsTex9bx2Ke9rMbgygAAAP///wAAAAAAACH5BAEAAB0ALAAAAAAPAA8AAAVeYCeOHUeeJHeZaFpcFNtynHAN9Fw7l7HkqVqBgThYfjKhgxHJXA6GAa4UqAYqmewGw8WYOAQCAILIYBqatCyRAEwgm4biARzRAICNhi4LEvR1KBwSGwp9MxuHLSUtIQA7"),
    ("Magic",                   "Mage",    "data:image/gif;base64,R0lGODlhEAAPAKIGAK6oBXo9CQAG/gAAAQAAABsGkv///wAAACH5BAEAAAYALAAAAAAQAA8AAANJaLrT+3AQQQiEZJQixl3ZtnmfQYijdTWj1n1aIW2d+jQsTZWx+D6VEKqQyZhigaQSEBBQKsMlwOkMDjnUqkdy8lEzJAVu3LAlAAA7"),
    ("Cooking",                 "Cook",    "data:image/gif;base64,R0lGODlhDQAQAKIFAPf33aaMEHtnCV1QEQAAAP///wAAAAAAACH5BAEAAAUALAAAAAANABAAAAM7WEWs2xAQR6R7M7fLO/vgRgzkIARoMC2k4J7o+rSxzJhvPeO5ercvmOAHDA4JglLR9VE6ISPnYIMJrRIAOw=="),
    ("Woodcutting",             "WC",      "data:image/gif;base64,R0lGODlhDwAQAKIHAHo9CQAAASocB1g6DACpAAlsAgAAAP///yH5BAEAAAcALAAAAAAPABAAAANSeHoW/mYpQwu5ly5KisVZxHkdGBoe2X3YmK4W6aaDkNoUWgxe3eMMQ2dg8AV4muBuwBQEgBuUQFADFJLR4gCQk0gMAG7EG61hyQbqdkwO5tiHBAA7"),
    ("Fletching",               "Fletch",  "data:image/gif;base64,R0lGODlhEAAQAKIAAIQuCCR7CT8uCwAAAP///wAAAAAAAAAAACH5BAEAAAQALAAAAAAQABAAAAM7SLo7zrCNMGKc9Fk1RcjVNXhgyDiCo6YQ+rgmAcujxtXVLKU5fvq6G29l4wBUH57IkaRsbpjYRiVVJAAAOw=="),
    ("Fishing",                 "Fish",    "data:image/gif;base64,R0lGODlhEQARAKIGACUlJUY8L1VbWnV7fAAAAAAAAf///wAAACH5BAEAAAYALAAAAAARABEAAANXaGpE9aWtCYO9MK5iM79CsUFjVIRTujQEIKoQO8za5MxDgc9Eqg8CAe7XowRPQKCwuHoIg8FcI4ZUhiI9wlBo1b0Yv1loOrb9rgovDMlkqcAC5pvymCsSADs="),
    ("Firemaking",              "FM",      "data:image/gif;base64,R0lGODlhEAAQAKIAALM5A91PAa6oBVg6DAAAAP///wAAAAAAACH5BAEAAAUALAAAAAAQABAAAANQWLrUvbA4IuqETeSg6VNU0ATkqIFhFQCcwD0hUAH0/EoCTdJsflO6XG0lI0hChAFBpHwZj8mBUqqETRrU6iSr5VazVqzUMX4yosZLBGpeuxMAOw=="),
    ("Crafting",                "Craft",   "data:image/gif;base64,R0lGODlhDwAQAKIEAHJCClcxC3d3dwAAAP///wAAAAAAAAAAACH5BAEAAAQALAAAAAAPABAAAANCSLo6znAN8ZobbFJMRghVJ4yP81XOuHUeeGmkdQ4AkFJSS794Plsclu0HcdRuIaHtQuIYl5Zm5xhkxXZVIOYSiSQAADs="),
    ("Smithing",                "Smith",   "data:image/gif;base64,R0lGODlhEAAQAKIFAFVbWjUvG0Y8L3V7fAAAAP///wAAAAAAACH5BAEAAAUALAAAAAAQABAAAANFWErcpBCyQaljkoJtiQjPcgFVAEYRww0YKpqdWzDCR7Kh5H2qle6ghk9UCy5IIRovR0DOgK0joFGMHqlLV2NmssocMlQCADs="),
    ("Mining",                  "Mine",    "data:image/gif;base64,R0lGODlhEAAQAKIFAFVbWjUvG0Y8L3V7fAAAAP///wAAAAAAACH5BAEAAAUALAAAAAAQABAAAANFWErcpBCyQaljkoJtiQjPcgFVAEYRww0YKpqdWzDCR7Kh5H2qle6ghk9UCy5IIRovR0DOgK0joFGMHqlLV2NmssocMlQCADs="),
    ("Herblore",                "Herb",    "data:image/gif;base64,R0lGODlhEAAQAKIAAADvAAB7AADVAACpAABmAAAAAP///wAAACH5BAEAAAYALAAAAAAQABAAAANAaLrc/jDKQiO95FZWBiUg5Sna4IGZqQHXgILeKgjsmwHzNZu2mRuFnevlExSAlF2AEBjkNkjTshlzaK6SrFaRAAA7"),
    ("Agility",                 "Agi",     "data:image/gif;base64,R0lGODlhEAAQAJEAAFZLOgAAAP///wAAACH5BAEAAAIALAAAAAAQABAAAAI2lB0Zxx0AVmMKqikS3FFJzW3aZ3GPiJxnZ0nZo3puGmMH2NlZmGDg2qMAf0JRJUIxDoUyD6MAADs="),
    ("Thieving",                "Thief",   "data:image/gif;base64,R0lGODlhEAAQAIMAAAAAAP///x8fH////wLoLxTQwALoL478uP6/Z478uBJ+0N17wP7BpwAAAKkS99jAfCH5BAMAAAEALAAAAAAQABAAAAQsMMhJq7046x2A/yAFjmNHCmQ4ASggehULv67EtrU5Cnzqgjyc6oXjzDhITgQAOw=="),
    ("Slayer",                  "Slay",    "data:image/gif;base64,R0lGODlhEAAQAOYAALqmm5F+c2dmZxcTELWspmZZUV5dFHNzc7y9vcy3qklDO6usrHhqYtzX0ywoJmhfWJaUBE5OTnp6eri2BTIsKzozK01MFv7+/kM6NEU9OOvi3eXc1ltbW8rKytbEuezk4EA3K7GYic7OztC/s6CgoENDQ0lISMCpm/T09J2Ylq2WidPRz9DLyIOCDcG3sZqGeoqEFj8/QJ6cIvXv66eoqD82MaOPg83LAqemAsbHx/r6+ezq6O/p5eLVzkpAOk9PDl9SSUE1Nkw/N7ufjVZMRlFRUVpYUC0tACAfHT84H97SytvMw4eGAYqJAQAAAP///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAE8ALAAAAAAQABAAAAe/gE+Cgk6FhoaDiU4WTT9IFSADTomDixATP0GRk5RPhRktEzBJhYqHSEYyNxClhE4OsEgRAg8GOKyuQAAuDCUSByYDR0ycTgUjHylIBxICJiMPSMUJHx4+MQcHRTk0DQrFGxc6BBQCHCIIDixCpU4nGx8ABCIkCx0cKwwRhipDIzMXDlDIgGDBASUMTBQK8OIEjws0SpBAcSCABgIZFgYI4eGCxw1LOjTY8UDSwhchemhI8CIAABsFfLQ7RPPQk0AAOw=="),
    ("Farming",                 "Farm",    "data:image/gif;base64,R0lGODlhEAAQANUAAAAAAP///1tpxlRht1xqx1xpxlxqxlVit1tqxj84Lp6QfXFnWnBmWWFWSFdOQ5KEc56PfXhtX7CgjKaXhIN3aHRpXJ6Qfo+Ccm5kWLCgjXBmWoR3aIZ5anhsX5KEdJGDc56Pfo+Bcot+b3hrXoR2aJCBcot9b4Z5bP///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAACgALAAAAAAQABAAAAaHQJRwiAIYAcSkEHBqnpDKZdOIeRKNUigAg9FOtyPtqLvkUgkCRMGAIBcxCepoMDgMRosK0uhwbEkKGRMhJwwNHVp9GBcPEiAhGAwADYkOGBQQEhMnJl2UQwCWFBaanRqTUEWWFx4SEBwikp+gGBsggh9cDRGpbyUeGSAnuVhJW1zIvcZHxUJBADs="),
    ("Runecrafting",            "RC",      "data:image/gif;base64,R0lGODlhEAAQAKIAALA5BIs3CZCQkFlaVXd3dwAAAQAAAP///yH5BAEAAAcALAAAAAAQABAAAANUeLpnZSwuYwCVsYBdcKOFFlLQVAhCGJwE8SgOmhZr276ncIeFfce2QM3nYtlUIdsApPPReoNop+dcFaLSxpUwoAWw0pJD+sS+JiDR44LRcDxoUiQBADs="),
    ("Hunter",                  "Hunt",    "data:image/gif;base64,R0lGODlhEAAQAMQAACsbHCgaGyocHS4fIi4gIy8hJC8iJjYuMCodIjAjKCkdIi4iJzEmKjAmKjUoLzotNDonNDUtMzcqNC0oKyMcIwAAABUbEiYrHCAhEyorHxkZGf///wAAAAAAAAAAAAAAACH5BAEAABsALAAAAAAQABAAAAVG4CaOHDmeZFByKko+zwqXLjdvdnzSuayLLF4rCMT9ODwh8uYyxnpNJzLQwiGVQCF1SNsFYMzaF/yooljkcte73a531ysqBAA7"),
    ("Construction",            "Cons",    "data:image/gif;base64,R0lGODlhEAAQAIMAAAAAAP///5mZmf8AAGZmZsjIyPmMPAAAAHzl1NaRtHzlyEZJRxBhOaIAEAAAAP///yH5BAMAAAEALAAAAAAQABAAAAQ/MMhJq704awm6/2BnjGNXnKggEMMgmmihru0LxDPtAnuaEyxXT5ZTBXkmASC3DNaWgMBSKQVaPZMOB7Tper0RADs="),
    "League Points",
    "Bounty Hunter - Hunter",
    "Bounty Hunter - Rogue",
    ("Clue Scrolls (all)",      "Clue [All]",      ""),
    ("Clue Scrolls (beginner)", "Clue [Beginner]", ""),
    ("Clue Scrolls (easy)",     "Clue [Easy]",     ""),
    ("Clue Scrolls (medium)",   "Clue [Med]",      ""),
    ("Clue Scrolls (hard)",     "Clue [Hard]",     ""),
    ("Clue Scrolls (elite)",    "Clue [Elite]",    ""),
    ("Clue Scrolls (master)",   "Clue [Master]",   ""),
    "LMS - Rank",
    "Abyssal Sire",
    "Alchemical Hydra",
    ("Barrows Chests",          "Barrows",         ""),
    "Bryophyta",
    "Callisto",
    "Cerberus",
    "Chambers of Xeric",
    "Chambers of Xeric: Challenge Mode",
    "Chaos Elemental",
    "Chaos Fanatic",
    "Commander Zilyana",
    "Corporeal Beast",
    "Crazy Archaeologist",
    "Dagannoth Prime",
    "Dagannoth Rex",
    "Dagannoth Supreme",
    "Deranged Archaeologist",
    "General Graardor",
    "Giant Mole",
    "Grotesque Guardians",
    "Hespori",
    "Kalphite Queen",
    "King Black Dragon",
    "Kraken",
    "Kree'Arra",
    "K'ril Tsutsaroth",
    "Mimic",
    "Nightmare",
    "Obor",
    "Sarachnis",
    "Scorpia",
    "Skotizo",
    "The Gauntlet",
    "The Corrupted Gauntlet",
    "Theatre of Blood",
    "Thermonuclear Smoke Devil",
    "TzKal-Zuk",
    "TzTok-Jad",
    "Venenatis",
    "Vet'ion",
    "Vorkath",
    "Wintertodt",
    "Zalcano",
    "Zulrah",
]
HISCORES_PATH = "m=hiscore_oldschool/index_lite.ws"
HISCORES_LEAGUES_PATH = "m=hiscore_oldschool_seasonal/index_lite.ws"
NEWS_PATH = "m=news/latest_news.rss"
GE_PATH = "m=itemdb_oldschool/api/catalogue/detail.json"


class ItemError(Exception):
    def __init__(self, msg, query):
        self.msg = msg
        self.query = query


class TooManyResults(ItemError):
    def __init__(self, msg, query, items):
        super().__init__(msg, query)
        self.items = items

    def __str__(self):
        return f"TooManyResults: ('{self.msg}', '{self.query}', #'{len(self.items)}')"


def _hiscores(player: str, path: str):
    with rsapi.util.request(path, player=player) as resp:
        return rsapi.util.parse_scores(resp.text, SKILLS)


def hiscores(player: str) -> dict:
    return _hiscores(player, HISCORES_PATH)


def hiscores_leagues(player: str) -> dict:
    return _hiscores(player, HISCORES_LEAGUES_PATH)


def news() -> dict:
    with rsapi.util.request(NEWS_PATH, oldschool=True) as resp:
        return rsapi.util.parse_news(resp.text)


def _items_iter(item_q: typing.Union[int, str]):
    if isinstance(item_q, int):
        for item in ITEMS:
            if item.id == item_q:
                yield item
    elif isinstance(item_q, str):
        r = re.compile(item_q, re.IGNORECASE)
        for item in ITEMS:
            if item.linked_id_item is not None:
                continue
            if item.duplicate:
                continue
            if item.name.lower() == item_q.lower():
                yield item
            elif r.search(item.name):
                yield item
    else:
        raise Exception("Bad argument type")


def items(item_q: typing.Union[int, str]) -> typing.List[ItemProperties]:
    ret = list(_items_iter(item_q))
    if not ret:
        raise ItemError("No items found", item_q)
    return ret


def alch(item_q: typing.Union[int, str]) -> dict:
    items_= items(item_q)
    if not items_:
        raise ItemError("No matching items found", item_q)

    return {
        i.id: {
            "name": i.name,
            "highalch": i.highalch,
            "lowalch": i.lowalch,
        } for i in items_
    }


def _ge_price_normalize(price):
    suffixes = {
        "k": 10**3,
        "m": 10**6,
        "b": 10**9,
    }
    if isinstance(price, str):
        # 'price': '1.2b '
        price = price.replace(" ", "")
        price = price.replace(",", "")
        try:
            multiplier = suffixes[price[-1]]
            price = multiplier * float(price[:-1])
        except KeyError:
            pass
    return int(price)

def _ge_parse(data):
    def parse_price_point(node):
        return {
            "price": _ge_price_normalize(node["price"]),
            "trend": node["trend"],
        }

    item = data["item"]
    return {
        "current": parse_price_point(item["current"]),
        "today": parse_price_point(item["today"]),
        "day30": item["day30"],
        "day90": item["day90"],
        "day180": item["day180"],
    }


def _ge_get(id_):
    with rsapi.util.request(GE_PATH, item=id_) as resp:
        return _ge_parse(resp.json())


def ge(item_q: typing.Union[int, str], limit=10) -> dict:
    items_ = [i for i in items(item_q) if i.tradeable_on_ge]
    if not items_:
        raise ItemError("No tradeable items found", item_q)
    if len(items_) > limit:
        raise TooManyResults("Too many results", item_q, items_)

    return {
        i.id: {
            "name": i.name,
            "ge": _ge_get(i.id),
        }
        for i in items_
    }


def price(item_q: typing.Union[int, str], limit=10) -> dict:
    items_ = items(item_q)
    if not items_:
        raise ItemError("No matching items found", item_q)
    if len(items_) > limit:
        raise TooManyResults("Too many results", item_q, items_)

    ret = {}
    for item in items_:
        entry = {
            "name": item.name,
            "tradeable": item.tradeable,
            "tradeable_on_ge": item.tradeable_on_ge,
            "alch": {
                "highalch": item.highalch,
                "lowalch": item.lowalch,
            },
        }
        if item.tradeable_on_ge:
            entry["ge"] = _ge_get(item.id)
        ret[item.id] = entry

    return ret
