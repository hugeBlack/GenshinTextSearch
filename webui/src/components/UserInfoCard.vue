<script setup>
//这是个展示用户的头像、用户名、用户组的组件，具体参考首页左上角
// 传入一个对象，至少要有user_id、user_name、user_group、avatar_url、verified这5个属性
import globalData from "@/global/global.js"
import router from "@/router";
const props = defineProps({
    userInfo: Object,
    showAvatarBorder: Boolean,
})

let userGroupNameDict = {
    "none": "点击登录",
    "normal": "普通用户",
    "admin": "管理员"
}

const click = () => {
    if(props.userInfo.user_id === globalData.userInfo.user_id){
        if(globalData.login) router.push("/user")
    }else{
        router.push("/user/" + props.userInfo.user_id)
    }

}

</script>

<template>
    <div class="avatarHolder" @click="click">
        <el-avatar class="avatar" :size="50" :src="userInfo.avatar_url" :class="{showAvatarBorder: showAvatarBorder}"/>
        <div class="userInfoHolder">
            <div class="userName">{{ userInfo.stu_name }}</div>
            <div class="userGroup"><span>{{ userInfo.grade }}</span><i class="fi fi-ss-hexagon-check verifiedIcon" :class="{notVisible:!userInfo.verified}"></i></div>
        </div>
    </div>
</template>

<style scoped>

.avatarHolder{
    display: inline-flex;
    align-items: center;
    flex-direction: row;
    cursor: pointer;
}

.el-avatar{
    min-width: 50px;
}

.userInfoHolder{
    opacity: 1;
    transition: opacity 0.3s ease;
}

.avatarHolder:hover>.userInfoHolder{
    opacity: 0.7;
}


.avatarHolder .avatar{
    margin-right: 10px;
}
.showAvatarBorder {
    border: 5px var(--el-color-primary-light-7) solid;
}

.avatarHolder .userName{
    font-weight: bold;
    font-size: 15px;
}

.avatarHolder .userGroup{
    font-size: 10px;
}

.userInfoHolder{
    margin-top:7px;
    line-height: 18px;
}

.verifiedIcon{
    color: var(--el-color-primary);
    visibility: visible;
    vertical-align: middle;
    margin-left: 5px;
}

.notVisible{
    visibility: hidden;
}

</style>