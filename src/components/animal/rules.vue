<template>
    <div class="">
        <Headers></Headers>
        <div class="content">
            <el-card class="box-card">
                <li v-for="(item,index) in rules">{{index+1}}----{{item}}----{{result[index]}}
                    <el-divider></el-divider>
                </li>
            </el-card>
        </div>
    </div>
</template>

<script>
    import Headers from "./headers";

    export default {
        name: "rules",
        components: {Headers},
        data() {
            return {
                result: [],
                rules: []
            }
        },
        // 在模板渲染成html后调用，通常是初始化页面完成后，再对html的dom节点进行一些需要的操作。
        mounted() {
            let that = this;
            // 将该数据信息传递给后端
            that.$axios({
                method: 'post',
                url: "http://49.232.199.15:5000/getrules",
            }).then(function (response) {
                console.log(response.data)
                let data = response.data
                that.result = data.result
                that.rules = data.rules
            }).catch(function (error) {
                console.log(error)
            })
        }
    }
</script>

<style scoped>
    .content {
        margin: 0 auto;
        width: 60%;
        margin-top: 30px;

    }

    li {
        font-weight: bold;
        text-align: center;
    }
</style>
