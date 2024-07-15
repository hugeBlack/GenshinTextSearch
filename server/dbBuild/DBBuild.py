import os
import sqlite3
import json
from DBConfig import conn, DATA_PATH
import voiceItemImport
from tqdm import tqdm


def importTalk(fileName: str):
    cursor = conn.cursor()
    obj = json.load(open(DATA_PATH + "\\BinOutput\\Talk\\" + fileName, encoding='utf-8'))

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
    folders = os.listdir(DATA_PATH + "\\BinOutput\\Talk\\")
    for folder in folders:
        if not os.path.isdir(DATA_PATH + "\\BinOutput\\Talk\\" + folder):
            continue

        files = os.listdir(DATA_PATH + "\\BinOutput\\Talk\\" + folder)
        print("importing talk " + folder)
        for val, fileName in tqdm(enumerate(files), total=len(files)):
            # print("Now: {} {}/{}".format(fileName, val, n))
            importTalk(folder + "\\" + fileName)


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


def importQuest(fileName: str):
    cursor = conn.cursor()
    obj = json.load(open(DATA_PATH + "\\BinOutput\\Quest\\" + fileName, encoding='utf-8'))

    sql1 = 'insert into quest(questId, titleTextMapHash, chapterId) VALUES (?,?,?)'
    sql2 = 'insert into questTalk(questId, talkId) values (?,?)'

    if 'id' in obj:
        keyQuestId = 'id'
        keyTitleTextMapHash = 'titleTextMapHash'
        keyChapterId = 'chapterId'
        keyTalks = 'talks'
        keyTalkId = 'id'
    else:
        keyQuestId = 'CCFPGAKINNB'
        keyTitleTextMapHash = 'HLAINHJACPJ'
        keyChapterId = 'FLCLAPBOOHF'
        keyTalks = 'PCNNNPLAEAI'
        keyTalkId = 'CCFPGAKINNB'

    questId = obj[keyQuestId]

    if keyTitleTextMapHash in obj:
        titleTextMapHash = obj[keyTitleTextMapHash]
    else:
        titleTextMapHash = None
        print("questId {} don't have TitleTextMapHash!".format(questId))

    if keyChapterId in obj:
        chapterId = obj[keyChapterId]
    else:
        chapterId = None

    cursor.execute(sql1, (questId, titleTextMapHash, chapterId))

    if keyTalks not in obj:
        print("questId {} don't have talk!".format(questId))
    else:

        for talk in obj[keyTalks]:
            talkId = talk[keyTalkId]
            cursor.execute(sql2, (questId, talkId))
            pass

    cursor.close()


def importAllQuests():
    files = os.listdir(DATA_PATH + "\\BinOutput\\Quest\\")
    n = len(files)
    for val, fileName in tqdm(enumerate(files), total=len(files)):
        # print("Now: {} {}/{}".format(fileName, val, n))
        importQuest(fileName)
    conn.commit()


def importChapters():
    cursor = conn.cursor()
    chapters = json.load(open(DATA_PATH + "\\ExcelBinOutput\\ChapterExcelConfigData.json", encoding='utf-8'))
    sql1 = "insert into chapter(chapterId, chapterTitleTextMapHash, chapterNumTextMapHash) values (?,?,?)"

    for chapter in chapters:
        cursor.execute(sql1,(chapter['id'], chapter['chapterTitleTextMapHash'], chapter['chapterNumTextMapHash']))

    cursor.close()
    conn.commit()


def main():
    print("Importing talks...")
    importAllTalkItems()
    print("Importing avatars...")
    importAvatars()
    print("Importing fetters...")
    importFetters()
    print("Importing quests...")
    importAllQuests()
    print("Importing chapters...")
    importChapters()
    print("Importing voices...")
    voiceItemImport.loadAvatars()
    voiceItemImport.importAllVoiceItems()
    print("Done!")


if __name__ == "__main__":
    main()
    pass

