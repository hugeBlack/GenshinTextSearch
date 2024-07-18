<script setup>
import {VideoPlay} from '@element-plus/icons-vue'
import api from "@/api/keywordQuery";
import * as converter from "@/assets/wem2wav";
import {ref, watch} from "vue";

const props = defineProps(['voicePath', 'langCode'])
const emit = defineEmits(['onVoicePlay'])

let audioUrl = undefined

const icon = ref()

const getAudioUrl = async () => {
    if(!audioUrl){
        let buffer = await api.getVoiceOver(props.voicePath, props.langCode)
        audioUrl= await converter.convertBufferedArray(buffer)

    }
    return audioUrl
}

const scrollTo = () => {
    icon.value.scrollIntoView({"behavior":"smooth", "block":"center"})
}

const playVoice = async ()=> {
    await getAudioUrl()

    emit('onVoicePlay', audioUrl)
}

watch(props, ()=>{
    audioUrl = undefined;
})
defineExpose({'getAudioUrl':getAudioUrl, "scrollTo": scrollTo})

</script>

<template>
    <el-tooltip :content="voicePath">
        <span ref="icon">
            <el-icon @click="playVoice"><VideoPlay /></el-icon>
        </span>

    </el-tooltip>
</template>

<style scoped>



</style>