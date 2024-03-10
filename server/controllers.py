import io

import databaseHelper
import languagePackReader
import config


def selectVoicePathFromTextHash(textHash: int):
    voicePath: str = databaseHelper.selectVoicePathFromTextHashInDialogue(textHash)
    if voicePath is not None:
        # TODO 显示任务的名称
        return voicePath, "WIP-Dialogue"

    voicePath = databaseHelper.selectVoicePathFromTextHashInFetter(textHash)
    if voicePath is not None:
        # TODO 显示角色的名称-谈话标题
        return voicePath, "WIP-Fetter"

    return None, None


def getTranslateObj(keyword: str, langCode: int):
    # 找出目标语言的textMap包含keyword的文本
    ans = []

    contents = databaseHelper.selectTextMapFromKeyword(keyword, langCode)
    # TODO 用户可以自定义目标语言
    langs = config.getResultLanguages()

    for content in contents:
        obj = {'translates': {}, 'voicePaths': []}
        translates = databaseHelper.selectTextMapFromTextHash(content[0], langs)
        for translate in translates:
            obj['translates'][translate[1]] = translate[0]

        voicePath, origin = selectVoicePathFromTextHash(content[0])
        if voicePath is not None:
            voiceExist = False
            for lang in langs:
                if lang in languagePackReader.langPackages and languagePackReader.checkAudioBin(voicePath, lang):
                    voiceExist = True
                    break

            if voiceExist:
                obj['voicePaths'].append(voicePath)

        obj['origin'] = origin

        ans.append(obj)

    return ans


def getVoiceBinStream(voicePath, langCode):
    wemBin = languagePackReader.getAudioBin(voicePath, langCode)
    if wemBin is None:
        return None
    return io.BytesIO(wemBin)


def getLoadedVoicePacks():
    ans = {}
    for packId in languagePackReader.langPackages:
        ans[packId] = languagePackReader.langCodes[packId]

    return ans


def getImportedTextMapLangs():
    langs = databaseHelper.getImportedTextMapLangs()
    ans = {}
    for langItem in langs:
        ans[langItem[0]] = langItem[1]

    return ans


def getConfig():
    return config.config


def setDefaultSearchLanguage(newLanguage: int):
    config.setDefaultSearchLanguage(newLanguage)


def setResultLanguages(newLanguages: list[int]):
    config.setResultLanguages(newLanguages)


def saveConfig():
    config.saveConfig()
