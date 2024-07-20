<script setup>
import global from "@/global/global"
import api from "@/api/keywordQuery";

import {useRoute} from "vue-router";
import {onActivated, onDeactivated, reactive, ref, watch} from "vue";
import PlayVoiceButton from "@/components/PlayVoiceButton.vue";
import StylizedText from "@/components/StylizedText.vue";
import AudioPlayer from "@liripeng/vue-audio-player";
import {Close, VideoPlay} from "@element-plus/icons-vue";

const route = useRoute()
const keyword = ref("")
const questName = ref("对话文本")
const textHash = ref(0)
const queryTime = ref("0")
const dialogues = ref([])

let playVoiceButtonDict = {}
let playableDialogueIdList = []

const reloadPage = () => {
    textHash.value = parseInt(route.query.textHash)
    keyword.value = route.query.keyword
    playVoiceButtonDict = {}
    playableDialogueIdList = []
    reloadTalk()
}


const reloadTalk = () => {
    api.getTalkFromHash(textHash.value).then(res => {
        let resJson = res.json
        queryTime.value = resJson.time.toFixed(2)
        let talkContents = resJson.contents
        questName.value = talkContents.talkQuestName
        dialogues.value = talkContents.dialogues

    }).catch(err => {
        if(!err.network) err.defaultHandler()
    })
}



// 播放器相关开始
/**
 *
 * @type {Ref<AudioPlayer>}
 */
const voicePlayer = ref()
const showPlayer = ref(false)
const autoLoop = ref(true)
let firstShowPlayer = true
const audio = ref([])
const currentPlayingIndex = ref(-1)
const autoScroll = ref(true)
const voiceListLoadingInfo = reactive(({
    showLoadingDialogue: false,
    total: 1,
    current: 0,
    percentage: 0,
    audioLoaded: false
}))



const onHidePlayerButtonClicked = () => {
    showPlayer.value = false
}

const onShowPlayerButtonClicked = () => {
    showPlayer.value = true
}

const onVoicePlay = (voiceUrl, dialogueId) => {
    currentPlayingIndex.value = 0
    voicePlayer.value.currentPlayIndex = 0
    playableDialogueIdList = [dialogueId]
    if(firstShowPlayer){
        showPlayer.value = true;
        firstShowPlayer = false
    }

    if(audio.value.length > 0 && voiceUrl === audio.value[0]){
        if(voicePlayer.value.isPlaying){
            voicePlayer.value.pause()
        }else{
            voicePlayer.value.play()
        }

    }else{
        audio.value = [voiceUrl]
        // 要等一会才能播放
        setTimeout(()=>{
            voicePlayer.value.play()
        }, 100)

    }

}

const playAllLangVoice = async (langCode) => {
    let newAudios = []
    playableDialogueIdList = []
    voiceListLoadingInfo.total = dialogues.value.length
    voiceListLoadingInfo.current = 0
    voiceListLoadingInfo.percentage = 0
    if (!voiceListLoadingInfo.audioLoaded)
        voiceListLoadingInfo.showLoadingDialogue = true
    for(let dialogue of dialogues.value) {
        if(!playVoiceButtonDict[langCode][dialogue.dialogueId]) {
            voiceListLoadingInfo.current += 1;
            voiceListLoadingInfo.percentage = 100 * voiceListLoadingInfo.current / voiceListLoadingInfo.total
            continue
        }
        let currentUrl = await playVoiceButtonDict[langCode][dialogue.dialogueId].getAudioUrl()
        newAudios.push(currentUrl)
        playableDialogueIdList.push(dialogue.dialogueId)
        voiceListLoadingInfo.current += 1;
        voiceListLoadingInfo.percentage = 100 * voiceListLoadingInfo.current / voiceListLoadingInfo.total
    }

    voiceListLoadingInfo.showLoadingDialogue = false
    voiceListLoadingInfo.audioLoaded = true


    if(newAudios.length === 0) return

    if(firstShowPlayer){
        showPlayer.value = true;
        firstShowPlayer = false
    }


    audio.value = newAudios
    voicePlayer.value.currentPlayIndex = 0
    // 要等一会才能播放
    setTimeout(()=>{
        voicePlayer.value.play()
    }, 100)


}

const registerVoicePlayButton = (buttonObj, langCode, dialogueId) => {
    if(!(langCode in playVoiceButtonDict)) {
        playVoiceButtonDict[langCode] = {}
    }
    playVoiceButtonDict[langCode][dialogueId] = buttonObj
}

const onBeforeNextAudio = (next) => {
    if(voicePlayer.value.currentPlayIndex < audio.value.length - 1) {
        next()
    }
}

const onPlay = () => {
    currentPlayingIndex.value = voicePlayer.value.currentPlayIndex
    if(autoScroll.value) {
        let dialogueId = playableDialogueIdList[currentPlayingIndex.value]
        let langCode = Object.getOwnPropertyNames(playVoiceButtonDict)[0]
        let voiceButton = playVoiceButtonDict[langCode][dialogueId]
        voiceButton.scrollTo()
    }


}

const tableRowClassName = ({row, rowIndex}) => {
    if(currentPlayingIndex.value >= 0 && row.dialogueId === playableDialogueIdList[currentPlayingIndex.value] ) {
        return 'playingDialogue'
    }
    return ''
}

onActivated(() => {
    reloadPage()
    voiceListLoadingInfo.audioLoaded = false
})

onDeactivated(() => {
    voicePlayer.value && voicePlayer.value.pause()
})

</script>

<template>
    <div class="viewWrapper">
        <h1 class="pageTitle">剧情对话查询</h1>
        <div class="helpText">
            <p>来源：{{questName}}</p>
            <p>查询用时： {{queryTime}} ms</p>
        </div>
        <el-table :data="dialogues" :row-class-name="tableRowClassName">
            <el-table-column prop="talker" label="角色" width="100" />
            <template v-for="langCode in global.config.resultLanguages">
                <el-table-column width="40">
                    <template #header>
                        <el-tooltip :content="'播放全部' + global.languages[langCode] + '语音'">
                            <el-icon @click="playAllLangVoice(langCode)"><VideoPlay /></el-icon>
                        </el-tooltip>
                    </template>
                    <template #default="scope">
                        <span v-if="global.voiceLanguages[langCode]">
                            <PlayVoiceButton v-for="voice in scope.row.voicePaths"
                                             :voice-path="voice" :lang-code="langCode"
                                             @on-voice-play="(url) =>{ onVoicePlay(url, scope.row.dialogueId)}"
                                             :ref = "(el) => {registerVoicePlayButton(el, langCode, scope.row.dialogueId)}"
                            />
                        </span>
                    </template>
                </el-table-column>
                <el-table-column :label="global.languages[langCode]" >
                    <template #default="scope">
                        <StylizedText :text="scope.row.translates[langCode]" :keyword="keyword"/>
                    </template>
                </el-table-column>
            </template>

        </el-table>

        <el-form style="margin-top: 10px;" :inline="true">
            <el-form-item label="自动连续播放">
                <el-switch v-model="autoLoop" />
            </el-form-item>
            <el-form-item label="自动滚动">
                <el-switch v-model="autoScroll" />
            </el-form-item>
        </el-form>


    </div>

    <div class="viewWrapper voicePlayerContainer" v-show="showPlayer">
        <span class="hideIcon" @click="onHidePlayerButtonClicked">
            <el-icon>
                <Close />
            </el-icon>
        </span>

        <AudioPlayer
            ref="voicePlayer"
            :audio-list="audio"
            :is-loop="autoLoop"
            :progress-interval="25"
            theme-color="var(--el-color-primary)"
            :before-next="onBeforeNextAudio"
            @play="onPlay">
        </AudioPlayer>
    </div>

    <div class="showPlayerButton" @click="onShowPlayerButtonClicked" v-show="!showPlayer">
        <i class="fi fi-sr-waveform-path"></i>
    </div>

    <el-dialog
        v-model="voiceListLoadingInfo.showLoadingDialogue" :width="300"
        :show-close="false" title="下载并转换语音" :close-on-press-escape="false">
        <el-progress :percentage="voiceListLoadingInfo.percentage">
            {{voiceListLoadingInfo.current}} / {{voiceListLoadingInfo.total}}
        </el-progress>
    </el-dialog>

</template>

<style scoped>
.viewWrapper{
    position: relative;
    width: 85%;
    margin: 0 auto;
    background-color: #fff;
    box-shadow: 0 3px 3px rgba(36,37,38,.05);
    border-radius: 3px;
    padding: 20px;
}

.pageTitle {
    border-bottom: 1px #ccc solid;
    padding-bottom: 10px;
}

.helpText {
    margin: 20px 0 20px 0;
    color: #999;
}

.voicePlayerContainer {
    margin-top: 10px;
    bottom: 0;
    position: sticky !important;
    box-shadow: 0 0 5px 5px rgba(36,37,38,.05);
    z-index: 9999;
}

.showPlayerButton{
    position: absolute;
    right: 7.5%;
    bottom: 80px;
    height: 70px;
    width: 70px;
    border-radius: 50%;
    background-color: var(--el-color-primary);
    color: #fff;
    font-size: 25px;
    box-shadow: 0 6px 15px rgba(36,37,38,.2);
    text-align: center;
    line-height: 75px;
    cursor: pointer;
    z-index: 9999;
}

.showPlayerButton:hover{
    background-color: var(--el-color-primary-light-3);
}

.hideIcon {
    cursor: pointer;
    position: absolute;
    top: 10px;
    right: 10px;
}

.hideIcon:hover {
    color: #888;
}

:deep( .playingDialogue) {
    background-color: var(--el-color-primary-light-9);
}


</style>