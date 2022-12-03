<template>
    <div class="head" @click="go">
        <p>欢迎使用动物产生式识别系统</p>
    </div>
</template>

<script>
    export default {
        name: "headers",
        methods: {
            go() {
                this.$router.push('/')
            }
        }
    }
</script>

<style scoped>

    .head {
        background: #42b983;
        height: 50px;
        /*与height保持一致使得文字居中*/
        line-height: 50px;
        text-align: center;
        font-family: 方正手迹-鲸鱼岛;
        color: black;
        font-size: 25px;
    }
    .head:hover{
        cursor:pointer
    }
</style>
