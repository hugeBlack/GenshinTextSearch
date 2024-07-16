import io

import databaseHelper
import languagePackReader
import config
import placeholderHandler


def selectVoicePathFromTextHash(textHash: int):
    voicePath: str = databaseHelper.selectVoicePathFromTextHashInDialogue(textHash)
    if voicePath is not None:
        return voicePath

    voicePath = databaseHelper.selectVoicePathFromTextHashInFetter(textHash)
    if voicePath is not None:
        return voicePath

    return None


def selectVoiceOriginFromTextHash(textHash: int, langCode: int) -> tuple[str, bool]:
    origin = databaseHelper.getSourceFromDialogue(textHash, langCode)
    if origin is not None:
        return origin, True

    origin = databaseHelper.getSourceFromFetter(textHash, langCode)
    if origin is not None:
        return origin, False

    # TODO 支持更多类型的语音
    return "其他文本", False


def getTranslateObj(keyword: str, langCode: int):
    # 找出目标语言的textMap包含keyword的文本
    ans = []

    contents = databaseHelper.selectTextMapFromKeyword(keyword, langCode)

    langs = config.getResultLanguages()
    sourceLangCode = config.getSourceLanguage()

    for content in contents:
        obj = {'translates': {}, 'voicePaths': [], 'isTalk': False, 'hash': content[0]}
        translates = databaseHelper.selectTextMapFromTextHash(content[0], langs)
        for translate in translates:
            # #开头的要进行占位符替换
            if translate[0].startswith("#"):
                obj['translates'][translate[1]] = placeholderHandler.replace(translate[0], config.getIsMale(), translate[1])
            else:
                obj['translates'][translate[1]] = translate[0]

        voicePath = selectVoicePathFromTextHash(content[0])
        origin, isTalk = selectVoiceOriginFromTextHash(content[0], sourceLangCode)
        obj['isTalk'] = isTalk

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


# 根据hash值查询整个对话的内容
def getTalkFromHash(textHash, langCode):
    return None


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


def setSourceLanguage(newSourceLanguage):
    config.setSourceLanguage(newSourceLanguage)


def setIsMale(isMale: bool):
    config.setIsMale(isMale)



