import sqlite3
from contextlib import closing
import os

# 没人会给一个词典搞高并发吧？
conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), "data.db"), check_same_thread=False)


def selectTextMapFromKeyword(keyWord: str, langCode: int):
    # [hash] 反正最后还得去数据库查一遍目标语言，不如不查content
    with closing(conn.cursor()) as cursor:
        sql1 = "select hash, content from textMap where lang=? and content like ? limit 200"
        cursor.execute(sql1, (langCode, '%{}%'.format(keyWord)))
        matches = cursor.fetchall()
        return matches


def selectTextMapFromTextHash(textHash: int, langs: list[int] = None):
    # [text, langCode]

    with closing(conn.cursor()) as cursor:
        if langs is not None and len(langs) > 0:
            langStr = ','.join([str(i) for i in langs])
            sql1 = "select content, lang from textMap where hash=? and lang in ({})".format(langStr)
        else:
            sql1 = "select content, lang from textMap where hash=?"
        cursor.execute(sql1, (textHash,))
        matches = cursor.fetchall()
        return matches


def selectVoicePathFromTextHashInFetter(textHash: int):
    with closing(conn.cursor()) as cursor:
        # fetter中，只要voice指定了avatarId，则fetter和voice的avatarId必须匹配
        sql1 = ("select voicePath,voice.avatarId from fetters, voice "
                "where voiceFileTextTextMapHash=? and fetters.voiceFile=voice.dialogueId "
                "and (fetters.avatarId=voice.avatarId or voice.avatarId=0)")
        cursor.execute(sql1, (textHash,))
        matches = cursor.fetchall()
        if len(matches) >= 1:
            return matches[0][0]
        elif len(matches) == 0:
            return None


# 实际是从talk里拿
def selectVoicePathFromTextHashInDialogue(textHash: int):
    # str
    with closing(conn.cursor()) as cursor:
        sql1 = "select voicePath from dialogue join voice on voice.dialogueId= dialogue.dialogueId where textHash=?"
        cursor.execute(sql1, (textHash,))
        matches = cursor.fetchall()
        if len(matches) > 0:
            return matches[0][0]
        return None


def getImportedTextMapLangs():
    # [(id, displayName)]
    with closing(conn.cursor()) as cursor:
        sql1 = "select id,displayName from langCode where imported=1"
        cursor.execute(sql1, )
        matches = cursor.fetchall()
        return matches


# 如果是角色语音，则返回角色名+标题，否则返回None
def getSourceFromFetter(textHash: int, langCode: int = 1):
    # 获得语音标题
    with closing(conn.cursor()) as cursor:
        sql1 = 'select avatarId, content from fetters, textMap where voiceFileTextTextMapHash=? and voiceTitleTextMapHash = hash and lang=?'
        cursor.execute(sql1, (textHash, langCode))
        ans = cursor.fetchall()
        if len(ans) == 0:
            return None
        avatarId, voiceTitle = ans[0]

        # 接下来获得角色名称
        sql2 = 'select content from avatar, textMap where avatarId=? and avatar.nameTextMapHash=textMap.hash and lang=?'

        cursor.execute(sql2, (avatarId, langCode))
        ans2 = cursor.fetchall()
        if len(ans2) == 0:
            return None
        avatarName = ans2[0][0]

        return "{} · {}".format(avatarName, voiceTitle)


wanderNames = {}
travellerNames = {}


def getCharterName(avatarId: int, langCode: int = 1):
    with closing(conn.cursor()) as cursor:
        # 接下来获得角色名称
        sql2 = 'select content from avatar, textMap where avatarId=? and avatar.nameTextMapHash=textMap.hash and lang=?'

        cursor.execute(sql2, (avatarId, langCode,))
        ans2 = cursor.fetchall()
        if len(ans2) == 0:
            return None

        return ans2[0][0]


# 获得散兵名字
def getWanderName(langCode: int = 1):
    if langCode not in wanderNames:
        wanderNames[langCode] = getCharterName(10000075, langCode)
    return wanderNames[langCode]


# 获得旅行者名字
def getTravellerName(langCode: int = 1):
    if langCode not in travellerNames:
        travellerNames[langCode] = getCharterName(10000005, langCode)
    return travellerNames[langCode]


# 通过textHash查询对话信息，返回[talkId, talkerType, talkerId, coopQuestId]
def getTalkInfo(textHash: int) -> 'tuple[int, str, int, int | None] | None':
    with closing(conn.cursor()) as cursor:
        # 先搞到talkId
        sql1 = 'select talkerType, talkerId, talkId, coopQuestId from dialogue where textHash=?'
        cursor.execute(sql1, (textHash,))
        ans = cursor.fetchall()
        if len(ans) == 0:
            return None
        talkerType, talkerId, talkId, coopQuestId = ans[0]
        return talkId, talkerType, talkerId, coopQuestId


# 根据talkerType和Id找到说话人的名称
def getTalkerName(talkerType: str, talkerId: int, langCode: int = 1) -> 'str | None':
    with closing(conn.cursor()) as cursor:
        talkerName = None
        if talkerType == "TALK_ROLE_NPC":
            sqlGetNpcName = 'select content from npc, textMap indexed by textMap_hash_index where npcId = ? and textHash = hash and lang = ?'
            cursor.execute(sqlGetNpcName, (talkerId, langCode))
            ansNpcName = cursor.fetchall()
            if len(ansNpcName) > 0:
                talkerName = ansNpcName[0][0]
        elif talkerType == "TALK_ROLE_PLAYER":
            talkerName = "主角"
        elif talkerType == "TALK_ROLE_MATE_AVATAR":
            talkerName = "反主"

        if talkerName == '#{REALNAME[ID(1)|HOSTONLY(true)]}':
            talkerName = getWanderName(langCode)
        return talkerName


def getTalkQuestId(talkId: int) -> int | None:
    with closing(conn.cursor()) as cursor:

        # 搞到questId，与任务的标题
        sql2 = ('select quest.questId from questTalk, quest '
                'where talkId=? and quest.questId=questTalk.questId')
        cursor.execute(sql2, (talkId,))
        ans2 = cursor.fetchall()
        if len(ans2) == 0:
            # 如果查询到没有属于某个任务的talk就会到这里
            return None
        return ans2[0][0]


def getQuestName(questId, langCode):
    with closing(conn.cursor()) as cursor:
        sql2 = ('select content from quest, textMap '
                'where quest.questId=? and titleTextMapHash=hash and lang=?')
        cursor.execute(sql2, (questId, langCode))
        ans2 = cursor.fetchall()
        if len(ans2) == 0:
            # 如果查询到没有属于某个任务的talk就会到这里
            return "对话文本"

        questTitle = ans2[0][0]

        # 尝试找到任务属于哪个章节
        sql3 = 'select chapterTitleTextMapHash,chapterNumTextMapHash from chapter, quest where questId=? and quest.chapterId=chapter.chapterId'
        cursor.execute(sql3, (questId,))
        ans3 = cursor.fetchall()
        if len(ans3) == 0:
            # 没找到对应的章节，直接返回任务标题
            return questTitle
        chapterTitleTextMapHash, chapterNumTextMapHash = ans3[0]

        sql4 = 'select content from textMap where hash=? and lang=?'
        cursor.execute(sql4, (chapterTitleTextMapHash, langCode))
        ans4 = cursor.fetchall()
        if len(ans4) == 0:
            # 没找到对应的章节名称，直接返回任务标题
            return questTitle

        chapterTitleText = ans4[0][0]

        cursor.execute(sql4, (chapterNumTextMapHash, langCode))
        ans5 = cursor.fetchall()

        if len(ans5) > 0:
            chapterNumText = ans5[0][0]
            questCompleteName = '{} · {} · {}'.format(chapterNumText, chapterTitleText, questTitle)
        else:
            questCompleteName = '{} · {}'.format(chapterTitleText, questTitle)

        return questCompleteName


# 通过talkId尝试找到对话所属的任务全量名称
def getTalkQuestName(talkId: int, langCode: int = 1) -> str:
    questId = getTalkQuestId(talkId)
    if questId is None:
        return "对话文本"

    questCompleteName = getQuestName(questId, langCode)
    return questCompleteName


def getCoopTalkQuestName(coopQuestId, langCode):
    # 直接除以100把subQuestId变为questId
    questCompleteName = getQuestName(coopQuestId // 100, langCode)
    return questCompleteName


# 如果是任务对话，则返回章节号+章节名+任务名，否则返回None
def getSourceFromDialogue(textHash: int, langCode: int = 1):
    talkInfo = getTalkInfo(textHash)
    if talkInfo is None:
        return None

    talkId, talkerType, talkerId, coopQuestId = talkInfo

    talkerName = getTalkerName(talkerType, talkerId, langCode)

    if coopQuestId is None:
        questCompleteName = getTalkQuestName(talkId, langCode)
    else:
        questCompleteName = getCoopTalkQuestName(coopQuestId, langCode)

    if talkerName is None:
        return questCompleteName
    else:
        return f"{talkerName}, {questCompleteName}"


def getManualTextMap(placeHolderName, lang):
    with closing(conn.cursor()) as cursor:
        sql1 = 'select content from manualTextMap, textMap where textMapId=? and textHash = hash and lang=?'
        cursor.execute(sql1, (placeHolderName, lang))
        ans = cursor.fetchall()
        if len(ans) > 0:
            return ans[0][0]
        else:
            return None


# 根据talk的id查找整个talk，返回为[tuple[textHash, talkerType, talkerId, dialogueId]]
def getTalkContent(talkId: int, coopQuestId: 'int | None') -> 'list[tuple[int, str, int, int]] | None':
    with closing(conn.cursor()) as cursor:
        if coopQuestId is None:
            sql1 = 'select textHash, talkerType, talkerId, dialogueId from dialogue where talkId = ? and coopQuestId is null'
            cursor.execute(sql1, (talkId,))
            ans = cursor.fetchall()
        else:
            sql1 = 'select textHash, talkerType, talkerId, dialogueId from dialogue where talkId = ? and coopQuestId = ?'
            cursor.execute(sql1, (talkId, coopQuestId))
            ans = cursor.fetchall()
        if len(ans) > 0:
            return ans
        else:
            return None
