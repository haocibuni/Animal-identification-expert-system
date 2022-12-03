<template>
    <div class="container">


        <!--头部标题-->
        <div class="head">
            <p>Travel Assistant</p>
        </div>


        <video class="bg_video" src="../assets/back.mp4" width="100%" autoplay loop muted></video>

        <div class="main">
            <div style="overflow:hidden;margin-top:-7px;margin-left: 15% ;">
                <iframe src="https://lbs.amap.com/console/show/picker" frameborder="0"
                        style="width: 80%;height: 500px;"></iframe>
            </div>

            <div>
                <div class="input">
                    <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px"
                             class="demo-ruleForm">
                        <el-form-item label="坐标：" prop="input1" style="margin-top: 10px">
                            <el-input type="text" v-model="ruleForm.input1" autocomplete="off">
                                <i slot="prefix" class="el-icon-takeaway-box"></i>
                            </el-input>
                        </el-form-item>
                        <el-form-item label="地名：" prop="input2" style="margin-top: -10px">
                            <el-input type="text" v-model="ruleForm.input2" autocomplete="off">
                                <i slot="prefix" class="el-icon-office-building"></i>
                            </el-input>
                        </el-form-item>
                        <el-button type="danger" round @click="check('ruleForm')" icon="el-icon-circle-plus-outline"
                                   style="margin-left: 50px">添加
                        </el-button>
                        <el-button type="success" @click="getShort">开始计算最短路径</el-button>
                    </el-form>
                </div>
            </div>

            <div style="float: left">
                <!--标签动态生成-->
                <el-tag
                        :key="tag"
                        v-for="tag in dynamicTags"
                        closable
                        :disable-transitions="false"
                        @close="handleClose(tag)">
                    {{tag}}
                </el-tag>
            </div>
            <div style="clear: both"></div>
        </div>

        <div style="color:yellow">
            <p style="font-size: 40px">最短路径{{this.bestLine}}</p>
            <p style="font-size: 40px">最短距离{{this.shortLine}}</p>

        </div>
    </div>
</template>

<script>
    export default {
        name: "bestLocation",
        data() {

            //用于进行输入校验
            var check1 = (rule, value, callback) => {
                if (value === "") {
                    callback(new Error('请输入地点的坐标'));
                } else {
                    callback();
                }
            };

            var check2 = (rule, value, callback) => {
                if (value === "") {
                    callback(new Error('请输入地点名称'));
                } else {
                    callback();
                }
            };

            return {

                // 输入框
                ruleForm: {
                    input1: "",
                    input2: "",
                },

                // 校验规则
                rules: {
                    input1: [
                        {validator: check1, trigger: 'blur'}
                    ],
                    input2: [
                        {validator: check2, trigger: 'blur'}
                    ]
                },


                // 地点标签
                dynamicTags: [],

                //坐标X
                x: [],
                //坐标Y
                y: [],

                bestLine: [],
                shortLine: "",

                show: false,


                h: "123"

            }
        },
        methods: {
            check(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        // alert('submit!');
                        let that = this;
                        let input = that.ruleForm.input1;
                        //分解输入的字符串得到该点的经纬度坐标
                        if (input.length > 0) {
                            let x = input.split(",")[0];
                            let y = input.split(",")[1];


                            // 添加新的标签
                            that.dynamicTags.push(that.ruleForm.input2);

                            //分别添加对应的坐标
                            that.x.push(x);
                            that.y.push(y);


                            that.ruleForm.input1 = "";
                            that.ruleForm.input2 = "";

                        }
                    } else {
                        // console.log('error submit!!');
                        return false;
                    }
                });
            },


            // 标签
            handleClose(tag) {
                this.dynamicTags.splice(this.dynamicTags.indexOf(tag), 1);
                this.x.splice(this.x.indexOf(tag), 1);
                this.y.splice(this.y.indexOf(tag), 1);
            },

            //最后提交所有坐标和地点
            getShort() {

                let that = this;

                //首先要判断是否地点数>=3


                if (that.dynamicTags.length <= 2) {
                    that.$message({
                        message: '对不起，地点至少为3个',
                        type: 'warning'
                    });
                } else {

                    console.log(that.x)
                    console.log(that.y)
                    console.log(that.dynamicTags)


                    const loading = this.$loading({
                        lock: true,
                        text: 'Loading',
                        spinner: 'el-icon-loading',
                        background: 'rgba(0, 0, 0, 0.7)'
                    });


                    let qsData = that.$qs.stringify({
                        x: that.x,
                        y: that.y,
                        slot: that.dynamicTags
                    });

                    that.$axios({
                        method: 'post',
                        url: "http://www.test.com/test",
                        data: qsData
                    }).then(function (response) {

                        loading.close();

                        // console.log(response);

                        that.shortLine = response.data[1];

                        let line = response.data[0];

                        let newLine = line[1];

                        for (var i = 2; i < line.length; i++) {
                            if (line[i] !== '[' && line[i] !== ']' && line[i] !== ' ') {
                                newLine = newLine.concat(line[i]);
                            }
                        }

                        newLine = newLine.split(',');
                        console.log(newLine);
                        let sum = 0;

                        // 坑:这个地方一定要提前赋值为空,否则还会保留之前的信息
                        that.bestLine = [];
                        for (var j = 0; j < newLine.length; j++) {
                            that.bestLine[sum++] = that.dynamicTags[parseInt(newLine[j])];
                        }

                    }).catch(function (error) {
                        console.log(error)
                    })
                }
            }

        }
    }
</script>

<style scoped>
    .head {
        background: #42b983;
        height: 50px;
        position: fixed;
        z-index: 2;
        width: 100%;
        top: 0;

    }

    p {
        font-weight: bold;
        font-size: 40px;
        text-align: center;
        font-family: 方正手迹-鲸鱼岛;
    }

    .main {
        margin-top: 10px;

    }

    .bg_video {
        position: fixed;
        z-index: -99;
    }

    .input {
        float: left;
        margin-left: 12%;
        text-align: center;
        width: 25%;
        margin-right: 15%;
    }


    /*标签*/
    .el-tag + .el-tag {
        margin-left: 10px;
    }

    .button-new-tag {
        margin-left: 10px;
        height: 32px;
        line-height: 30px;
        padding-top: 0;
        padding-bottom: 0;
    }

    .input-new-tag {
        width: 90px;
        margin-left: 10px;
        vertical-align: bottom;
    }
</style>
