import re
import databaseHelper


def replace(textMap: str, playerIsMale: bool, lang: int):
    # 主要处理3种情况： {M#xxxx}{F#xxx}
    # #{PLAYERAVATAR#SEXPRO[INFO_MALE_PRONOUN_HE|INFO_FEMALE_PRONOUN_SHE]}是特别的，不需要神之眼也可以使用元素力。
    # #以前，我也做过蘑菇菜肴给那菈吃。而且因为好吃，{MATEAVATAR#SEXPRO[INFO_MALE_PRONOUN_HE|INFO_FEMALE_PRONOUN_SHE]}咽下去的时候还特别用力。
    # 处理散兵的名字#（……！！难道是{REALNAME[ID(1)|HOSTONLY(true)]}那时候的…？）
    text1 = re.sub(r'\{M#(.*?)}\{F#(.*?)}', '\\1' if playerIsMale else '\\2', textMap)
    text1 = re.sub(r'\{F#(.*?)}\{M#(.*?)}', '\\2' if playerIsMale else '\\1', text1)

    def replaceSexPro(match: 're.Match'):
        isMate = match.group(1) == "MATE"
        if isMate == playerIsMale:
            return databaseHelper.getManualTextMap(match.group(3), lang)
        else:
            return databaseHelper.getManualTextMap(match.group(2), lang)

    text2 = re.sub(r'\{(.*?)AVATAR#SEXPRO\[(.*?)\|(.*?)]}', replaceSexPro, text1)

    wanderName = databaseHelper.getWanderName(lang)
    text3 = re.sub(r"\{REALNAME\[ID\(1\)\|HOSTONLY\(true\)]}", wanderName, text2)

    travellerName = databaseHelper.getTravellerName(lang)
    text4 = re.sub(r"\{NICKNAME}", travellerName, text3)

    # 最后去掉前面的#号
    return text4


if __name__ == "__main__":
    print(replace(
        "#嗯，{NICKNAME}{M#他们}{F#她们}今天也会来参加庆祝活动。\n{PLAYERAVATAR#SEXPRO[INFO_MALE_PRONOUN_HE|INFO_FEMALE_PRONOUN_SHE]}是特别的，不需要神之眼也可以使用元素力。{REALNAME[ID(1)|HOSTONLY(true)]}",
        True, 1))
