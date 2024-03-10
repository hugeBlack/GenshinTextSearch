<script setup>
// 显示多语言翻译的组件
import global from '@/global/global.js'
import { VideoPlay } from '@element-plus/icons-vue'
import * as converter from "@/assets/wem2wav"
import {computed, watch} from "vue";
import api from "@/api/keywordQuery"
/**
 *         {
 *             "type": "Dialogue",
 *             "origin": "TASK NAME etc.",
 *             "voicePaths": [],
 *             "translates":{
 *                 1: "TRANSLATE_CHINESE",
 *                 4: "TRANSLATE_ENGLISH"
 *             }
 *         },
 */
const props = defineProps(['translateObj'])

const getLines = (translate) => {
    return translate.split("\\n")
}

/**
 *
 * @type {Audio}
 */
let audio = undefined
let audioUrl = {}

const playVoice = async (voicePaths, langCode) =>{
    if(audio){
        audio.pause()
    }

    if(audioUrl[langCode]){
        audio = new Audio(audioUrl[langCode])
        audio.play()
        return
    }

    let buffer = await api.getVoiceOver(voicePaths, langCode)
    let url = await converter.convertBufferedArray(buffer)
    audio = new Audio(url)
    audioUrl[langCode] = url
    audio.play()
}

watch(props, ()=>{
    audio = undefined;
    audioUrl = {};
})

</script>

<template>

    <div class="entry">

        <div class="translate" v-for="(translate, translateKey) in props.translateObj.translates">
            <p class="info">{{global.languages[translateKey]}}:
                <span v-if="global.voiceLanguages[translateKey]">
                    <el-tooltip v-for="voice in props.translateObj.voicePaths" :content="voice">
                        <el-icon @click="playVoice(voice, translateKey)"><VideoPlay /></el-icon>
                    </el-tooltip>
                </span>

            </p>
            <p v-for="line in getLines(translate)">
                {{line}}
            </p>

        </div>
        <p class="info">
            <span class="origin">来源：{{props.translateObj.origin}}</span>
        </p>
    </div>

</template>

<style scoped>
.translate{
    margin-bottom: 10px;
}

.entry{
    padding-bottom: 20px;
    padding-top: 20px;
    line-height: 30px;
}
.info{
    font-size: 14px;
}

.voice{
    margin-right: 10px;
}

.origin{
    color: #ab9d96;
}
</style>