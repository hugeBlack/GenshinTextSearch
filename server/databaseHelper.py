import sqlite3
from contextlib import closing

# 没人会给一个词典搞高并发吧？
conn = sqlite3.connect("test.db",check_same_thread=False)


def selectTextMapFromKeyword(keyWord: str, langCode: int):
    # [hash] 反正最后还得去数据库查一遍目标语言，不如不查content
    with closing(conn.cursor()) as cursor:
        sql1 = "select hash, content from textMap where lang=? and content like '%{}%' limit 200".format(keyWord)
        cursor.execute(sql1, (langCode,))
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
        # 不知道上面这么写有没有问题，下面先留着
        # else:
        #     # 有好多结果！如果能通过角色id反查，就反查，否则直接摆烂，返回第一个
        #     if matches[0][1] == 0:
        #         return matches[0][0]
        #
        #     # 查出谁说的话
        #     sql2 = "select avatarId from fetters where voiceFileTextTextMapHash=? limit 1"
        #     cursor.execute(sql2, (textHash,))
        #     matches2 = cursor.fetchall()
        #     avatarId = matches2[0][0]
        #     for voice in matches:
        #         if voice[1] == avatarId:
        #             return voice[0]

            # 没人说过？不对吧，返回第一个
            # return matches[0][0]


def selectVoicePathFromTextHashInDialogue(textHash: int):
    # str
    with closing(conn.cursor()) as cursor:
        sql1 = "select voicePath from dialogue join voice on voice.dialogueId= dialogue.dialogueId where textHash=?"
        cursor.execute(sql1, (textHash,))
        matches = cursor.fetchall()
        if len(matches) > 0:
            return matches[0][0]
        return None


if __name__ == "__main__":
    print(selectVoicePathFromTextHashInFetter(2276797319))