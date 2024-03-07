<script setup>
import {changeTheme} from "@/assets/changeTheme";
import router from "@/router";

const goBack = () =>{
    router.go(-1)
}

</script>

<template>
    <div class="pageWrapper">
        <div class="contentWrapper">
            <div class="errorCode">404</div>
            <div class="errorMsg"><i class="fi fi-sr-info"></i><span> 啊呀，你请求的页面未找到。</span></div>
            <el-button type="primary" @click="goBack" round>返回上一页</el-button>
        </div>


    </div>
</template>


<style scoped>
.pageWrapper {
    height: 100vh;
    width: 100vw;
    box-sizing: border-box;
    background-color: var(--el-color-primary-light-9);
    display: flex;
    justify-content: center;
    align-items: center;
}

.contentWrapper{
    text-align: center;
}

.errorCode{
    font-size: 150px;
    font-weight: 500;
    color: var(--el-color-primary);
}

.errorMsg{
    font-size: 20px;
    margin-bottom: 20px;
}
</style>