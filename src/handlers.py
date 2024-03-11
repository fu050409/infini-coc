# Initialized `handlers.py` generated by ipm.
# Regists your handlers here.
# Documents at https://ipm.hydroroll.team/

from infini.register import Register
from infini.input import Input
from infini.output import Output
from infini.router import Command

from diceutils.utils import format_str, format_msg, get_user_id
from diceutils.dicer import Dicer
from diceutils.cards import CardsPool, Cards
from diceutils.parser import Positional, CommandParser, Commands, Bool, Optional
from diceutils.charactors import manager

from .madness import madness_end, manias, temporary_madness, phobias
from .utils import rollcount, db, initialized

import random

register = Register()

CardsPool.register("coc")

coc_cards: Cards = CardsPool.get("coc")
coc_cache_cards: Cards = CardsPool._cache_cards_pool.get("coc")


def judger(
    input: Input, dice: Dicer, exp: int | None, name: str = None, reason: str = None
) -> Output:
    """类 COC 模式技能检定结果"""
    result = dice.roll().calc()

    if isinstance(exp, int):
        if result == 100:
            judge = "大失败!"
        elif exp < 50 and result > 95:
            judge = "大失败!"
        elif result == 1:
            judge = "大成功!"
        elif result <= exp // 5:
            judge = "极难成功"
        elif result <= exp // 2:
            judge = "困难成功"
        elif result <= exp:
            judge = "成功"
        else:
            judge = "失败"
    else:
        judge = ""

    return input.output(
        "text",
        "coc.ra",
        block=True,
        variables={
            "name": name,
            "value": exp,
            "desc": dice.description(),
            "reason": reason,
            "judge": judge,
        },
    )


@register.handler(Command("coc"), priority=1)
def coc_hander(input: Input):
    args = format_msg(input.get_plain_text(), begin=".coc", zh_en=True)
    user_id = get_user_id(input)

    commands = CommandParser(
        Commands(
            [
                Positional("roll", int, 1),
                Bool("cache", False),
                Optional("set", int),
                Optional("age", int),
                Optional("name", str),
                Optional("sex", str),
            ]
        ),
        args=args,
        auto=True,
    ).results

    round = commands["roll"]
    if round > 9:
        yield input.output(
            "text",
            "coc.coc.roll.too_much_round",
            block=True,
            variables={"round": round},
        )

    if commands["set"] or commands["set"] == 0:
        if (cache_card := coc_cache_cards.get(user_id, commands["set"])) is None:
            yield input.output(
                "text",
                "coc.coc.set.card_not_found",
                block=True,
                variables={"sequence": commands["set"]},
            )

        coc_cards.update(user_id, attributes=cache_card)

        charactor = manager.build_card("coc")
        charactor.loads(cache_card)
        coc_cache_cards.clear(user_id)

        yield input.output(
            "text",
            "coc.coc.set",
            block=True,
            variables={
                "sequence": commands["set"],
                "card": {
                    "meta": charactor.display_group("meta"),
                    "basic": charactor.display_group("basic"),
                },
            },
        )

    if commands["cache"]:
        if (cache_cards := coc_cache_cards.getall(user_id)) is None:
            yield input.output(
                "text",
                "coc.coc.cache.not_found",
                block=True,
            )

        cards = []
        for i, item in enumerate(cache_cards):
            charactor = manager.build_card("coc")
            charactor.loads(item)
            count = rollcount(charactor)
            cards.append(
                {
                    "sequence": i,
                    "meta": charactor.display_group("meta"),
                    "basic": charactor.display_group("basic"),
                    "count": count,
                }
            )
            i += 1

        yield input.output(
            "text", "coc.coc.cache", block=True, variables={"cards": cards}
        )

    age = commands["age"]
    name = commands["name"]
    sex = commands["sex"]

    rolled = coc_cache_cards.count(user_id)

    cards = []
    for i in range(round):
        charactor = initialized(manager.build_card("coc"))
        if age:
            charactor.set("age", age)
        if sex:
            charactor.set("sex", sex)
        if name:
            charactor.set("name", name)

        coc_cache_cards.update(user_id, rolled + i, attributes=charactor.dumps())
        count = rollcount(charactor)

        cards.append(
            {
                "sequence": rolled + i,
                "meta": charactor.display_group("meta"),
                "basic": charactor.display_group("basic"),
                "count": count,
            }
        )

    yield input.output("text", "coc.coc.roll", block=True, variables={"cards": cards})


@register.handler(Command("ra", alias=["rc"]), priority=1)
def ra_hander(input: Input):
    args = format_msg(input.get_plain_text(), begin=(".ra", ".rc"))
    user_id = get_user_id(input)

    if len(args) == 0:
        yield input.output("text", "coc.ra.help", block=True)

    if len(args) > 4:
        yield input.output(
            "text",
            "coc.ra.error.to_much_args",
            block=True,
            variables={"given": len(args)},
        )

    skill_name = args[0]

    if not (card_data := coc_cards.get(user_id)):
        if len(args) == 1:
            yield judger(input, Dicer(), 0, name=skill_name)

        yield judger(input, Dicer(), int(args[1]), name=skill_name)

    charactor = manager.build_card("coc")
    charactor.loads(card_data)

    if not (exp := charactor.get(skill_name)):
        if len(args) == 1:
            exp = 0
        elif not args[1].isdigit():
            yield input.output("text", "coc.ra.error.invalid_value", block=True)
        else:
            exp = int(args[1])

        yield judger(input, Dicer(), exp, name=skill_name)
    elif exp and len(args) > 1:
        if not args[1].isdigit():
            yield input.output("text", "coc.ra.error.invalid_value", block=True)

        yield input.output(
            "text", "coc.ra.record_exsists", variables={"name": skill_name, "exp": exp}
        )
        yield judger(input, Dicer(), int(args[1]), name=args[0])

    yield judger(input, Dicer(), exp, name=skill_name)


@register.handler(Command("at"))
def at(input: Input):
    args = format_msg(input.get_plain_text(), begin=".at", zh_en=False)

    first = args[0] if args else ""
    second = args[1] if len(args) > 1 else None

    if not Dicer.check(first):
        roll_string = second or "1d6"
        reason = first
    else:
        roll_string = first
        reason = second

    user_id = get_user_id(input)
    charactor = manager.build_card("coc")
    charactor.loads((coc_cards.get(user_id) or {}))

    dice = Dicer(roll_string + db(charactor)).roll()

    yield input.output(
        "text",
        "coc.at",
        block=True,
        variables={
            "desc": dice.description(),
            "damage": dice.outcome,
            "reason": reason,
        },
    )


@register.handler(Command("dam"), priority=0)
def dam(input: Input):
    args = format_msg(input.get_plain_text(), begin=".dam", zh_en=False)

    user_id = get_user_id(input)

    first = args[0] if args else ""
    second = args[1] if len(args) > 1 else None

    if not Dicer.check(first):
        roll_string = second or "1d6"
        reason = first
    else:
        roll_string = first
        reason = second

    charactor = manager.build_card("coc")
    charactor.loads(coc_cards.get(user_id) or {})
    max_hp = charactor.get("mhp") or 0

    dice = Dicer(roll_string).roll()

    hp = charactor.get("hp") or 0
    if hp < 0:
        hp = 0
    hp = max(hp - dice.outcome, 0)

    if dice.outcome < max_hp / 2:
        if hp > 0:
            state = "轻伤"
        else:
            state = "昏迷"
    elif dice.outcome >= max_hp / 2:
        if hp > 0:
            state = "重伤"
        else:
            state = "濒死"
    else:
        state = "健康"

    charactor.set("hp", hp)
    coc_cards.update(user_id, attributes=charactor.dumps())
    return input.output(
        "text",
        "coc.dam",
        block=True,
        variables={
            "desc": dice.description(),
            "damage": dice.outcome,
            "reason": reason,
            "state": state,
        },
    )


@register.handler(Command("sc"), priority=2)
def sc_handler(input: Input):
    text = format_str(input.get_plain_text(), begin=".sc")
    if not text:
        yield input.output("text", "coc.sc.help", block=True)

    using_card: bool
    user_id = get_user_id(input)

    try:
        args = list(filter(None, text.split(" ")))
        s_and_f = args[0].split("/")
        success = Dicer(s_and_f[0]).roll().outcome
        failure = Dicer(s_and_f[1]).roll().outcome

        if len(args) > 1:
            card = {"san": int(args[1]), "name": "未指定"}
            yield input.output("text", "coc.sc.assign")
            using_card = False
        else:
            if not (card := coc_cards.get(user_id)):
                card = {"san": 0, "name": "未指定"}
            using_card = True

        charactor = manager.build_card("coc")
        charactor.loads(card)

        docimasy_number = Dicer().roll().calc()
        san_before = charactor.get("san")

        if docimasy_number <= san_before:
            down = success
            docimasy_status = "成功"
        else:
            down = failure
            docimasy_status = "失败"
        if down >= san_before:
            docimasy_result = "陷入了永久性疯狂"
        elif down >= (san_before // 5):
            docimasy_result = "陷入了不定性疯狂"
        elif down >= 5:
            docimasy_result = "陷入了临时性疯狂"
        else:
            docimasy_result = "未受到严重影响"

        charactor.set("san", max(san_before - down, 0))

        if using_card:
            coc_cards.update(user_id, attributes=charactor.dumps())

        yield input.output(
            "text",
            "coc.sc",
            block=True,
            variables={
                "card_name": card["name"],
                "san_before": san_before,
                "san": card["san"],
                "docimasy_number": docimasy_number,
                "docimasy_status": docimasy_status,
                "docimasy_result": docimasy_result,
                "down": down,
            },
        )
    except Exception as error:
        yield input.output(
            "text", "coc.sc.error", block=True, variables={"error": str(error)}
        )


@register.handler(Command("ti"), priority=2)
def ti_handler(input: Input):
    i = random.randint(1, 10)
    j = random.randint(1, 100)

    return input.output(
        "text",
        "coc.ti",
        block=True,
        variables={
            "i": i,
            "temporary_madness": temporary_madness[i - 1],
            "phobias": phobias[j - 1],
            "manias": manias[j - 1],
            "sustain": random.randint(1, 10),
        },
    )


@register.handler(Command("li"), priority=2)
def li_handler(input: Input):
    i = random.randint(1, 10)
    j = random.randint(1, 100)

    return input.output(
        "text",
        "coc.li",
        block=True,
        variables={
            "i": i,
            "madness": madness_end[i - 1],
            "phobias": phobias[j - 1],
            "manias": manias[j - 1],
            "sustain": random.randint(1, 10),
        },
    )
