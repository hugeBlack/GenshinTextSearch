<script setup>
import {VideoPlay} from '@element-plus/icons-vue'
import api from "@/api/keywordQuery";
import * as converter from "@/assets/wem2wav";
import {watch} from "vue";

const props = defineProps(['voicePath', 'langCode'])
const emit = defineEmits(['onVoicePlay'])

let audioUrl = undefined

const playVoice = async ()=> {
    if(!audioUrl){
        let buffer = await api.getVoiceOver(props.voicePath, props.langCode)
        audioUrl= await converter.convertBufferedArray(buffer)

    }

    emit('onVoicePlay', audioUrl)
}

watch(props, ()=>{
    audioUrl = undefined;
})

</script>

<template>
    <el-tooltip :content="voicePath">
        <el-icon @click="playVoice"><VideoPlay /></el-icon>
    </el-tooltip>
</template>

<style scoped>



</style>