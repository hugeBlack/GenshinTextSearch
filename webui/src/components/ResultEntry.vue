<script setup>
// 显示多语言翻译的组件
import global from '@/global/global.js'
import PlayVoiceButton from "@/components/PlayVoiceButton.vue";

import StylizedText from "@/components/StylizedText.vue";
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
const emit = defineEmits(['onVoicePlay'])



const onVoicePlay = (voiceUrl) => {
    emit('onVoicePlay', voiceUrl)
}
/**
 *
 * @type {Ref<HTMLElement>}
 */





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
            <StylizedText :text="translate" />
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