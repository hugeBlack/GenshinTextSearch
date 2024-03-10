import sqlite3
import time

conn = sqlite3.connect("test.db", check_same_thread=False)


# 如果是角色语音，则返回角色名+标题，否则返回None
def getSourceFromFetter(textHash: int):
    # 获得语音标题
    cursor = conn.cursor()
    sql1 = 'select avatarId, content from fetters, textMap where voiceFileTextTextMapHash=? and voiceTitleTextMapHash = hash'
    cursor.execute(sql1, (textHash,))
    ans = cursor.fetchall()
    if len(ans) == 0:
        return None
    avatarId, voiceTitle = ans[0]

    # 接下来获得角色名称
    sql2 = 'select content from avatar, textMap where avatarId=? and avatar.nameTextMapHash=textMap.hash'

    cursor.execute(sql2, (avatarId,))
    ans2 = cursor.fetchall()
    if len(ans2) == 0:
        return None
    avatarName = ans2[0][0]

    cursor.close()
    return "{} {}".format(avatarName, voiceTitle)


# 如果是任务对话，则返回章节号+章节名+任务名，否则返回None
def getSourceFromDialogue(textHash: int):
    cursor = conn.cursor()

    # 先搞到talkId
    sql1 = 'select talkId from dialogue where textHash=?'
    cursor.execute(sql1, (textHash,))
    ans = cursor.fetchall()
    if len(ans) == 0:
        return None
    talkId = ans[0][0]

    # 搞到questId，与任务的标题
    sql2 = ('select quest.questId, content from questTalk, quest, textMap '
            'where talkId=? and quest.questId=questTalk.questId and titleTextMapHash=hash')
    cursor.execute(sql2, (talkId,))
    ans2 = cursor.fetchall()
    if len(ans2) == 0:
        # 应该不会出现吧？
        return "任务文本"
    questId, questTitle = ans2[0]

    # 尝试找到任务属于哪个章节
    sql3 = 'select chapterTitleTextMapHash,chapterNumTextMapHash from chapter, quest where questId=? and quest.chapterId=chapter.chapterId'
    cursor.execute(sql3, (questId,))
    ans3 = cursor.fetchall()
    if len(ans3) == 0:
        # 没找到对应的章节，直接返回任务标题
        return questTitle
    chapterTitleTextMapHash, chapterNumTextMapHash = ans3[0]

    sql4 = 'select content from textMap where hash=?'
    cursor.execute(sql4, (chapterTitleTextMapHash,))
    ans4 = cursor.fetchall()
    if len(ans4) == 0:
        # 没找到对应的章节名称，直接返回任务标题
        return questTitle

    chapterTitleText = ans4[0][0]

    cursor.execute(sql4, (chapterNumTextMapHash,))
    ans5 = cursor.fetchall()

    if len(ans5) > 0:
        chapterNumText = ans5[0][0]
        return '{} {} {}'.format(chapterNumText, chapterTitleText, questTitle)
    else:
        return '{} {}'.format(chapterTitleText, questTitle)


if __name__ == "__main__":
    start = time.time()
    print(getSourceFromFetter(3472380287))
    end = time.time()
    print((end - start)*1000)

