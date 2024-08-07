import request from "@/utils/request";

/**
 * 获得数据库中导入的TextMap语言列表
 */
const getImportedTextLanguages = () => {
    // return {
    //     1: "Chinese",
    //     4: "English(US)",
    //     9: "Japaneses"
    // }

    return request.get("/api/getImportedTextLanguages");
};


/**
 * 获得游戏安装的语音列表
 */
const getImportedVoiceLanguages = () => {
    return request.get("/api/getImportedVoiceLanguages");
}

const saveConfig = (resultLanguages, defaultSearchLanguage, sourceLanguage, isMale) => {
    let tmp = []
    for(let code of resultLanguages){
        tmp.push(parseInt(code))
    }

    return request.post("/api/saveSettings", {
        'config' :{
            "resultLanguages": tmp,
            "defaultSearchLanguage": parseInt(defaultSearchLanguage),
            "sourceLanguage": parseInt(sourceLanguage),
            "isMale": isMale
        }
    })
}

const getConfig = () => {
    return request.get("/api/getSettings")
}

export default {
    getImportedTextLanguages,
    getImportedVoiceLanguages,
    getConfig,
    saveConfig
}