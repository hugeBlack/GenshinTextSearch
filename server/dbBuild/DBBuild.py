import os
import sqlite3
import json

DATA_PATH = r'G:\AnimeGameData'

conn = sqlite3.connect("../test.db")


def importTextMap(mapName: str):
    cursor = conn.cursor()

    sql1 = "insert or ignore into langCode(codeName) values (?)"
    # 创建
    cursor.execute(sql1, (mapName,))
    cursor.fetchall()

    sql2 = "select id from langCode where codeName = ?"
    cursor.execute(sql2, (mapName,))
    ans2 = cursor.fetchall()
    langId = ans2[0][0]

    # 加数据
    sql3 = "insert or ignore into textMap(hash, content, lang) values (?,?,?)"
    textMap = json.load(open(DATA_PATH + "\\TextMap\\" + mapName, encoding='utf-8'))
    for hashVal, content in textMap.items():
        cursor.execute(sql3, (hashVal, content, langId))

    cursor.close()
    conn.commit()


def importAllTextMap():
    files = os.listdir(DATA_PATH + "\\TextMap")
    for fileName in files:
        print("Now: " + fileName)
        importTextMap(fileName)




def importTalk(fileName: str):
    cursor = conn.cursor()
    obj = json.load(open(DATA_PATH + "\\BinOutput\\Talk\\Quest\\" + fileName, encoding='utf-8'))

    if 'talkId' in obj:
        talkIdKey = 'talkId'
        dialogueListKey = 'dialogList'
        dialogueIdKey = 'id'
        talkRoleKey = 'talkRole'
        talkRoleTypeKey = 'type'
        talkRoleIdKey = 'id'
        talkContentTextMapHashKey = 'talkContentTextMapHash'
    elif 'FEOACBMDCKJ' in obj:
        talkIdKey = 'FEOACBMDCKJ'
        dialogueListKey = 'AAOAAFLLOJI'
        dialogueIdKey = 'CCFPGAKINNB'
        talkRoleKey = 'HJLEMJIGNFE'
        talkRoleTypeKey = '_type'
        talkRoleIdKey = '_id'
        talkContentTextMapHashKey = 'BDOKCLNNDGN'
    else:
        print("Skipping " + fileName)
        return

    talkId = obj[talkIdKey]
    if dialogueListKey not in obj or len(obj[dialogueListKey]) == 0:
        return

    sql1 = "insert or ignore into dialogue(dialogueId, talkerId, talkerType, talkId, textHash) values (?,?,?,?,?)"

    for dialogue in obj[dialogueListKey]:
        dialogueId = dialogue[dialogueIdKey]
        if talkRoleKey in dialogue and \
                talkRoleIdKey in dialogue[talkRoleKey] and \
                talkRoleTypeKey in dialogue[talkRoleKey]:
            talkRoleId = dialogue[talkRoleKey][talkRoleIdKey]
            talkRoleType = dialogue[talkRoleKey][talkRoleTypeKey]
        else:
            talkRoleId = -1
            talkRoleType = None

        if talkContentTextMapHashKey not in dialogue:
            continue
        textHash = dialogue[talkContentTextMapHashKey]
        cursor.execute(sql1, (dialogueId, talkRoleId, talkRoleType, talkId, textHash))

    cursor.close()
    conn.commit()


def importAllTalkItems():
    files = os.listdir(DATA_PATH + "\\BinOutput\\Talk\\Quest\\")
    n = len(files)
    for val, fileName in enumerate(files):
        print("Now: {} {}/{}".format(fileName, val, n))
        importTalk(fileName)


def importAvatars():
    cursor = conn.cursor()
    avatars = json.load(open(DATA_PATH + "\\ExcelBinOutput\\AvatarExcelConfigData.json", encoding='utf-8'))

    sql1 = "insert into avatar(avatarId, nameTextMapHash) values (?,?)"

    for avatar in avatars:
        cursor.execute(sql1, (avatar['id'], avatar['nameTextMapHash']))

    cursor.close()
    conn.commit()


def importFetters():
    cursor = conn.cursor()
    fetters = json.load(open(DATA_PATH + "\\ExcelBinOutput\\FettersExcelConfigData.json", encoding='utf-8'))
    sql1 = "insert into fetters(fetterId, avatarId, voiceTitleTextMapHash, voiceFileTextTextMapHash, voiceFile) values (?,?,?,?,?)"

    for fetter in fetters:
        cursor.execute(sql1,(fetter['fetterId'], fetter['avatarId'], fetter['voiceTitleTextMapHash'], fetter['voiceFileTextTextMapHash'], fetter['voiceFile']))

    cursor.close()
    conn.commit()



if __name__ == "__main__":
    # importFetters()
    pass

