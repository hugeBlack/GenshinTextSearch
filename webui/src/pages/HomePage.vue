<script setup>

import { changeTheme } from "@/assets/changeTheme";
import router from "@/router";
import { onBeforeMount, onMounted, reactive, ref, watch } from "vue";
import UserInfoCard from "@/components/UserInfoCard.vue";
import globalData from "@/global/global"
import { ElMenuItem, ElSubMenu } from "element-plus";
import global from "@/global/global";
import api from "@/api/basicInfo";

function loginButtonClicked() {
    router.push("/login")
}

const menuItemClick = (ke) => {
    router.push(ke.index)
}


const notificationBox = ref();

const avatarClicked = () => {
    if (!isLogin.value) {
        router.push("/login")
    }
}

const menus = reactive({
    v: [
        { "title": "首页", "icon": "fi-rr-home", "path": "/" },
        { "title": "设置", "icon": "fi-rr-settings", "path": "/settings" },
    ]
});

let userInfo = reactive({
    data: {
        user_phone: "",
        user_name: "未登录",
        user_id: 123456,
        user_group: "none",
        avatar_url: "/webstatic/defaultAvatar.jpg",
        unread_notification: false,
        verified: false
    }

});

const isLogin = ref(false);
const loadComplete = ref(true);
const gotUserInfo = ref(false)




const getSidebarPath = () => {
    let path = router.currentRoute.value.path.split("/")
    if (path.length === 1) {
        return ""
    } else {
        return "/" + path[1];
    }


}

const menu = ref();
let contentDom = undefined;
const loaded = ref(false)

onMounted(async () => {
    (() => {
        let menuItemNow = getSidebarPath();
        for (let item of menus.v) {
            if (!item.children) continue;
            for (let child of item.children) {
                if (child.path === menuItemNow) {
                    menu.value.open(item.path);
                }
            }
        }
        contentDom = document.querySelector(".content")
    })()

    global.languages = (await api.getImportedTextLanguages()).json
    global.voiceLanguages = (await api.getImportedVoiceLanguages()).json
    global.config = (await api.getConfig()).json

    loaded.value = true
})


watch(router.currentRoute, () => {
    contentDom.scrollTo({ left: 0, top: 0 })
})

</script>

<template>
    <div class="pageWrapper">
        <div class="headerHolder">
            <div class="leftTitle">
                <!--                <img alt="" src="../assets/logo.png">-->
                Genshin Text Search
            </div>

        </div>
        <div class="contentHolder">
            <div class="sideBar">
                <div class="userInfoWrapper">
                    <UserInfoCard :user-info="userInfo.data" showAvatarBorder @click="avatarClicked"></UserInfoCard>
                </div>


                <el-menu v-if="loadComplete" :default-active="getSidebarPath()" class="sideBarMenu" ref="menu">
                    <component v-for="item in menus.v" :is="item.children ? ElSubMenu : ElMenuItem" :index="item.path"
                        v-on="item.children ? {} : { click: menuItemClick }">
                        <template #title>
                            <i class="fi" :class="item.icon"></i>
                            <span>{{ item.title }}</span>
                        </template>
                        <el-menu-item v-if="item.children" v-for="child in item.children" :index="child.path"
                            @click="menuItemClick">
                            <i class="fi" :class="child.icon"></i>
                            <span>{{ child.title }}</span>
                        </el-menu-item>
                    </component>
                </el-menu>
            </div>

            <div class="content">
                <RouterView v-if="loaded"></RouterView>
            </div>
        </div>
    </div>
</template>


<style scoped>
.headerHolder {
    width: 100%;
    height: 50px;
    box-sizing: border-box;
    background-color: var(--el-color-primary);
    display: flex;
    justify-content: space-between;
    max-height: 50px;
    flex: 1;
}

.headerHolder>div {
    display: flex;
    align-items: center;
    margin: 0 20px;
}

.pageWrapper {
    height: 100vh;
    width: 100%;
    min-width: 1200px;
    max-height: 100vh;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
}

.leftTitle img {
    max-height: 50px;
    margin-right: 20px;
}

.rightTitle img {
    height: 60px;
}

.rightTitle>* {
    margin: 0 10px;
}

.line {
    border-left: #fff 1px solid;
    height: 1em;
    width: 1px;
    margin: 0 5px;
}

.contentHolder {
    display: flex;
    justify-items: stretch;
    flex: 3;
    overflow: hidden;

}


.content {
    overflow-y: auto;
    background-color: var(--el-color-primary-light-9);
    flex: 1;
}

.sideBar {
    width: 230px;
    min-width: 230px;
    max-width: 230px;
    flex: 3;
}

.sideBar .sideBarMenu {
    border-right: none;
}

.sideBar .sideBarMenu i {
    margin-right: 10px;
    font-size: 1.1em;
}

.userInfoWrapper {
    padding: 10px 20px;
    border-bottom: 1px #eee solid;
}

.leftTitle {
    color: #fff;
}
</style>