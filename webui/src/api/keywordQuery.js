import request from "@/utils/request";
import axios from "axios";

const queryBaidu = (keyword) => {
    return {
        "k": "KEYWORD",
        "v": "KEYWORD EXPLAIN"
    }
    // return request.post("/api/baiduQuery", {
    //     keyword: keyword
    // });
};

const queryByKeyword = (keyword, langCode) => {
    // return {contents: [
    //         {
    //             "type": "Dialogue",
    //             "origin": "TASK NAME etc.",
    //             "voicePaths": [],
    //             "translates":{
    //                 1: "TRANSLATE_CHINESE",
    //                 4: "TRANSLATE_ENGLISH"
    //             }
    //         },
    //         {
    //             "type": "Fetter",
    //             "origin": "AVATAR NAME etc.",
    //             "voicePaths": ["VOICE_PATH2"],
    //             "translates":{
    //                 1: "TRANSLATE_CHINESE2",
    //                 4: "TRANSLATE_ENGLISH2"
    //             }
    //         }
    //     ],
    //     time: 0.01
    // }

    return request.post("/api/keywordQuery", {
        keyword: keyword,
        langCode: langCode
    });
};

/**
 *
 * @param voicePath
 * @param langCode
 * @return {Promise<ArrayBuffer|null>}
 */
const getVoiceOver = async (voicePath, langCode) => {

    let ans = await axios.post(request.defaults.baseURL ? request.defaults.baseURL: "" + "api/getVoiceOver", {
        voicePath: voicePath,
        langCode: parseInt(langCode)
    }, {
        responseType: 'arraybuffer',
    });

    if(ans.headers.has("Error")) {
        console.log("戳了")
        return null
    }

    return ans.data
};




const getTalkFromHash = (textHash) => {
    return request.post("/api/getTalkFromHash", {
        "textHash": textHash
    });
};

export default {
    queryBaidu,
    queryByKeyword,
    getVoiceOver,
    getTalkFromHash
};