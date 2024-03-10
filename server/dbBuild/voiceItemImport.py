import os
import sqlite3
import json
from contextlib import closing

DATA_PATH = r'G:\AnimeGameData'

conn = sqlite3.connect("../test.db")

avatars: 'list[tuple[int,str]]' = []

# 去掉switch的角色名->角色ID
avatarMappings = {}


def loadAvatars():
    global avatars
    sql1 = "select avatarId,content from avatar, textMap where avatarId<11000000 and textMap.lang=4 and avatar.nameTextMapHash=textMap.hash"
    cursor = conn.cursor()
    ans = cursor.execute(sql1)
    for avatar in ans:
        avatars.append((avatar[0], avatar[1].replace(" ", "").lower()))

    # 特殊处理
    avatarMappings['qin'] = 10000003
    avatarMappings['ambor'] = 10000021
    avatarMappings['hero'] = 10000005
    avatarMappings['heroine'] = 10000007


def getAvatarIdFromVoiceItemAvatarName(avatarNameFromVoiceItem: str):
    rawName = avatarNameFromVoiceItem[7:].lower()
    # GCG的怪物语音就不要了~
    if rawName.startswith("gcg"):
        return 0

    rawNameTranslate = {
        "tartaglia_melee": 'tartaglia'
    }
    if rawName in rawNameTranslate:
        rawName = rawNameTranslate[rawName]

    if rawName in avatarMappings:
        return avatarMappings[rawName]

    for avatar in avatars:
        if avatar[1].find(rawName) != -1:
            avatarMappings[rawName] = avatar[0]
            return avatar[0]

    raise Exception("AVATAR NOT FOUND!")


def importVoiceItem(fileName: str):
    cursor = conn.cursor()

    sql1 = "insert or ignore into voice(dialogueId, voicePath,gameTrigger, avatarId) values (?,?,?,?)"
    textMap = json.load(open(DATA_PATH + "\\BinOutput\\Voice\\Items\\" + fileName, encoding='utf-8'))
    for _, content in textMap.items():
        p1 = None
        p2 = None
        p3 = None
        p4 = None

        if 'Guid' in content:
            p1 = 'gameTriggerArgs'
            p2 = 'SourceNames'
            p3 = 'sourceFileName'
            p4 = 'GameTrigger'

        elif 'JFNDAOJCHPO' in content:
            p1 = 'FMHLBONJKPJ'
            p2 = 'OFEEIPOMNKD'
            p3 = 'CBGLAJNLFCB'
            p4 = 'BFKCDJLLGNJ'

        elif 'HLGGFCENLPA' in content:
            p1 = 'FFDHLEAFBLM'
            p2 = 'EIKJKDICKMJ'
            p3 = 'HLGOMILNFNK'
            p4 = 'BEHKGKMMAPD'

        if p2 not in content or p1 not in content:
            continue

        dialogueId = content[p1]
        gameTrigger = content[p4]
        for voice in content[p2]:
            voicePath = voice[p3]
            if dialogueId is None or voicePath is None or gameTrigger is None:
                raise "ERROR!"

            avatarId = 0
            # 没啥好办法，通过avatarName获得角色名称，再转换为角色id
            if 'Guid' in content and voice['avatarName'] != '':
                avatarId = getAvatarIdFromVoiceItemAvatarName(voice['avatarName'])
                # print(voice['avatarName'], avatarId)

            cursor.execute(sql1, (dialogueId, voicePath, gameTrigger, avatarId))

    cursor.close()
    conn.commit()


def importAllVoiceItems():
    files = os.listdir(DATA_PATH + "\\BinOutput\\Voice\\Items\\")
    n = len(files)
    for val, fileName in enumerate(files):
        print("Now: {} {}/{}".format(fileName, val, n))
        importVoiceItem(fileName)


if __name__ == "__main__":
    loadAvatars()
    importAllVoiceItems()
