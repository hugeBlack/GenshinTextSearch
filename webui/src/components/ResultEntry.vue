<script setup>
// 显示多语言翻译的组件
import global from '@/global/global.js'
import PlayVoiceButton from "@/components/PlayVoiceButton.vue";
import StylizedText from "@/components/StylizedText.vue";
import {useRouter} from "vue-router";
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
const props = defineProps(['translateObj', 'keyword'])
const emit = defineEmits(['onVoicePlay'])
const router = useRouter()


const onVoicePlay = (voiceUrl) => {
    emit('onVoicePlay', voiceUrl)
}

const gotoTalk = () => {
    if(!props.translateObj.isTalk) return
    router.push(`/talk?textHash=${props.translateObj.hash}&keyword=${props.keyword}`)
}

</script>

<template>

    <div class="entry">

        <div class="translate" v-for="(translate, translateKey) in props.translateObj.translates">
            <p class="info">{{global.languages[translateKey]}}:
                <span v-if="global.voiceLanguages[translateKey]">
                    <PlayVoiceButton v-for="voice in props.translateObj.voicePaths"
                                     :voice-path="voice" :lang-code="translateKey"
                                     @on-voice-play="onVoicePlay"
                    />
                </span>

            </p>
            <StylizedText :text="translate" :keyword="$props.keyword"/>
        </div>
        <p class="info">
            <span class="origin" :class="{talkOrigin: props.translateObj.isTalk}" @click="gotoTalk">
                来源：{{props.translateObj.origin}}
                <span class="gotoIcon" v-if="props.translateObj.isTalk">&gt</span>
            </span>
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

.talkOrigin {
    cursor: pointer;
    transition: 0.3s;
}

.talkOrigin:hover {
    opacity: 0.8;
}

.talkOrigin>.gotoIcon {
    transition: 0.3s;
    margin-left: 0;
}
.talkOrigin:hover>.gotoIcon {
    padding-left: 5px;
}
</style>