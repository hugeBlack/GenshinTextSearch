<script setup>
// 这是个icon+链接的按钮，具体参考主页右上角，icon传入flaticon的class，传入fl-xx-xxx就行，为空就不会显示图标，图标也不会占位
// hasNotification控制是否显示右上角红点，color设置默认颜色，鼠标移动到上面或者点击透明度会发生变化以适应背景

import {ref} from "vue";

const props = defineProps({
    fontColor: String,
    icon: String,
    text: String,
    hasNotification: Boolean
})

</script>

<template>
    <div class="buttonHolder" :class="{ hasNotification: hasNotification }">
        <i v-if="icon!==''" class="icon fi" :class="icon">
            <span class="redDot"></span>
        </i>
        <div class="buttonTxt">
            {{text}}
        </div>

    </div>
</template>

<style scoped>
    .buttonHolder{
        display: flex;
        align-items: center;
        user-select: none;
        cursor: pointer;
        position: relative;
    }

    .buttonHolder:hover{
        opacity: 0.9;

    }

    .buttonHolder:active{
        opacity: 0.99;
    }

    .buttonHolder .icon{
        margin-right: 10px;
        position: relative;
        height: 1em;
        width: 1em;
    }

    .buttonHolder>*{
        color: v-bind(fontColor);
    }

    .buttonTxt{
        font-size: 10px;
    }

    .hasNotification .icon .redDot{
        position: absolute;
        right: 0;
        top: 0;
        height: 8px;
        width: 8px;
        border-radius: 4px;
        background-color: var(--el-color-error);
    }
</style>