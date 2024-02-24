# Initialized `events.py` generated by ipm.
# Regists your text events and regist global variables here.
# Documents at https://ipm.hydroroll.team/

from infini.register import Register


register = Register()

# `.coc` 指令
register.regist_textevent(
    "coc.coc.roll",
    "{% for card in cards %}"
    "天命序列[{{ card.sequence }}]:\n"
    "{{ card.meta }}\n"
    "{{ card.basic }}\n"
    "共计: {{ card.count[0] }}/{{ card.count[1] }}{% if not loop.last %}\n\n{% endif %}"
    "{% endfor %}",
)
register.regist_textevent(
    "coc.coc.roll.too_much_round", "天命次数[{{ round }}]超出预期."
)
register.regist_textevent("coc.coc.roll.age_change", "{{ text }}")
register.regist_textevent(
    "coc.coc.set", "使用人物卡序列[{{ sequence }}]:\n{{ card_detail }}"
)
register.regist_textevent(
    "coc.coc.set.card_not_found", "未找到序列为[{{ sequence }}]的人物卡."
)
register.regist_textevent(
    "coc.coc.cache",
    "已缓存的天命人物卡:\n"
    "{% for card in cards %}"
    "天命序列[{{ card.sequence }}]:\n"
    "{{ card.meta }}\n"
    "{{ card.basic }}\n"
    "共计: {{ card.count[0] }}/{{ card.count[1] }}{% if not loop.last %}\n\n{% endif %}"
    "{% endfor %}",
)
register.regist_textevent("coc.coc.cache.not_found", "未查询到缓存的人物卡.")

# `.ra` 指令
register.regist_textevent("coc.ra.help", "使用`.help ra`指令查看指令使用方法.")
register.regist_textevent(
    "coc.ra.error.to_much_args",
    "错误: 参数过多(最多4需要但 {{ given }} 给予).",
)
register.regist_textevent(
    "coc.ra.error.invalid_value",
    "技能值应当为整型数, 使用`.help ra`查看技能检定指令使用帮助.",
)
register.regist_textevent(
    "coc.ra.record_exsists",
    "你已经设置了技能[{{ name }}:{{ exp }}], 但你指定了检定值, 使用指定检定值作为替代.",
)
register.regist_textevent(
    "dg.docimasy.skill",
    '[{{ username if username else "用户" }}]'
    "{% if reason %}由于[{{ reason }}]{% endif %}"
    "进行技能[{{ name }}:{{ value }}]检定: {{ desc }}, 检定[{{ judge }}].",
)

# `.sc` 指令
register.regist_textevent(
    "coc.sc",
    '[{{ username if username else "用户" }}]'
    "调查员[{{ card_name }}]进行[精神状态: {{ san_before }}]检定: 1D100={{ docimasy_number }}, 检定{{ docimasy_status }}. "
    "[{{ card_name }}]理智降低了 {{ down }} 点, {{ docimasy_result }}. "
    "当前[{{ card_name }}]的 SAN 值为: {{ san }}.",
)
register.regist_textevent("coc.sc.help", "使用[.help sc]查看使用帮助.")
register.regist_textevent(
    "coc.sc.assign", "用户指定了应当检定的 SAN 值, 这会使得本次检定不会被记录."
)
register.regist_textevent(
    "coc.sc.error",
    "产生了未知的错误[{{ error }}], 你可以使用`.help sc`指令查看指令使用方法."
    "如果你确信这是一个错误, 建议联系开发者获得更多帮助.",
)

# `.en` 指令
register.regist_textevent(
    "coc.encourage",
    "[{SenderCard}]进行技能[{SkillName}:{Value}]成长检定: {DiceDescription}\n检定{DocimasyStatus}, 技能增长{EnDiceDesc}.",
)

# `.ti` 指令
register.regist_textevent(
    "coc.ti",
    '[{{ username if username else "用户" }}]临时疯狂检定1D10={{ i }}\n'
    "{{ temporary_madness }}"
    "{% if i == 9 %}"
    "\n恐惧症状为: \n{{ phobias }}"
    "{% elif i == 10 %}"
    "\n狂躁症状为: \n{{ manias }}"
    "{% endif %}"
    "\n该症状将会持续1D10={{ sustain }}轮",
)


register.regist_textevent(
    "coc.li",
    '[{{ username if username else "用户" }}]总结疯狂判定1D10={{ i }}\n'
    "{{ madness }}"
    "{% if i in [2, 3, 6, 9, 10] %}\n调查员将在1D10={{ sustain }}小时后醒来.{% endif %}"
    "{% if i == 9 %}"
    "\n恐惧症状为: \n{{ phobias }}"
    "{% elif i == 10 %}"
    "\n狂躁症状为: \n{{ manias }}"
    "{% endif %}",
)
