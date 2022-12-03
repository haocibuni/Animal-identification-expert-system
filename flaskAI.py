from flask import Flask
from flask import request
from flask import Response, json

# 解决跨域问题
from flask_cors import *

app = Flask(__name__)
CORS(app, supports_credentials=True)
# route()装饰器来告诉Flask触发函数的URL

# 特征数组，用于记录规则的前提和规则结论
features = ["有毛发", "有奶", "有羽毛", "会飞", "下蛋",
            "吃肉", "有犬齿", "有爪", "眼盯前方", "有蹄",
            "嚼反刍动物", "黄褐色", "暗斑点", "黑色条纹", "长脖子",
            "长腿", "不会飞", "会游泳", "黑白二色", "善飞",
            "哺乳动物", "鸟", "食肉动物", "有蹄类动物", "金钱豹",
            "虎", "长颈鹿", "斑马", "鸵鸟", "企鹅", "信天翁"]

# 根据特征数组分类，特征0，中间结论1，最终结论2
conclusion = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2]

# 定义规则前提数组
rule = [
    [0],
    [1],
    [2],
    [3, 4],
    [5],
    [6, 7, 8],
    [20, 9],
    [20, 10],
    [20, 22, 11, 12],
    [20, 22, 11, 13],
    [23, 14, 15, 12],
    [23, 13],
    [21, 14, 15, 18, 16],
    [21, 17, 16, 18],
    [21, 19]
]

# 定义规则结论数组
result = [20, 20, 21, 21, 22, 22, 23, 23, 24, 25, 26, 27, 28, 29, 30]

# 返回所有的规则(前提和结论)
@app.route('/getrules', methods=['POST', 'GET'])
def getrules():
    global rule
    global features
    global result
    # 将规则返回成汉字数组 将结论返回为汉字数组 规则和结论的数组长度一致
    strRules = [list() for i in range(len(rule))]
    strResult = []
    # 向每条规则中添加各个特征
    for i in range(len(rule)):
        for j in range(len(rule[i])):
            strRules[i].append(features[rule[i][j]])
    # 向结果中添加对应特征
    for k in range(len(result)):
        strResult.append(features[result[k]])
    # 以json形式返回数据
    return Response(json.dumps({'rules': strRules, 'result': strResult}), content_type='application/json')


# 增加规则(前提,结论和结论类型)
@app.route('/add', methods=['POST', 'GET'])
def add():
    # 得到传递过来的参数
    data1 = request.get_json(silent=True)
    newRules = data1['newrules']
    newResult = data1['newresult']
    newType = data1['newtype']
    global rule
    global features
    global result
    global conclusion

    # 将新规则前提中的新特征添加到特征数组，如果已经存在则不添加
    # 将新规则前提中的新特征类型定义为特征
    for i in range(len(newRules)):
        if newRules[i] not in features:
            features.append(newRules[i])
            conclusion.append(0)

    # 将该新规则通过特征数组转化为下标数组添加到规则前提数组中 newruleArr为临时规则前提数组变量
    newruleArr = []
    for i in range(len(newRules)):
        for j in range(len(features)):
            if newRules[i] == features[j]:
                newruleArr.append(j)
                break
    rule.append(newruleArr)

    # 判断结论是否存在 如果不存在则添加该结论到特征数组 将特征类型添加到分类数组  将结论在特征数组中的下标添加到结论数组
    if newResult not in features:
        features.append(newResult)
        conclusion.append(int(newType))
        result.append(features.index(newResult))
    # 如果存在则结论在特征数组中的下标添加到结论数组
    else:
        result.append(features.index(newResult))
    # 添加成功返回200
    return Response(json.dumps({'code': 200}), content_type='application/json')


# 分析得到结论
@app.route('/test', methods=['POST', 'GET'])
def test():
    # 动物产生式识别系统
    str1 = request.get_json(silent=True)
    r = ""
    global rule
    global features
    global result
    global conclusion
    # 这个地方要处理一下,防止出现很多得规则,找个变量承载
    # 切片复制，只复制值，地址空间不同 防止扩充全局变量
    R = rule[:]
    res = result[:]
    C = conclusion[:]
    F = features[:]
    # 扩充规则库 遍历规则前提数组和规则结论数组
    length = len(R)
    for i in range(length):
        # 将新规则添加到规则数组中
        for j in range(len(res)):
            if res[j] in R[i]:
                # 一个规则的结论在另一条规则的前提中 将两条规则的前提拼接 将该前提中的规则结论剔除
                arr = R[i] + R[j]
                arr.remove(res[j])
                # 将该新规则添加到规则库中
                R.append(arr)
                # 将新结论添加到结论库中
                res.append(res[j])

    # 扩充后规则数组长度
    # print(len(rule))
    # 思路，将各个功能转换为函数，传值时单独设计一位用于判断此次请求的操作是什么，根据不同的值返回不同的结果
    # 输入相关信息
    # msg = ["有犬齿", "眼盯前方", "有毛发", "吃肉", "有爪", "有奶", "黄褐色", "黑色条纹"]
    # msg = ["有毛发", "有奶", "有蹄", "嚼反刍动物", "长脖子", "长腿", "暗斑点", ]
    # msg = ["长脖子"]

    # 获取前端获得的字符数组
    msg = str1['msg']
    # 将msg中文数组通过特征数组转换为数字数组
    msgArr = []
    for i in range(len(msg)):
        for j in range(len(features)):
            if msg[i] == features[j]:
                msgArr.append(j)
                break
    # num表示是否最终结论 num2表示是否存在结论
    num = 0
    num2 = 0
    # 开始匹配对应的规则
    for i in range(len(R)):
        # 判断输入的规则前提 是否包含该规则的前提
        d = [False for c in R[i] if c not in msgArr]
        # 包含所有的前提规则
        if not d:
            # 将该规则的结论加入msgArr数组
            msgArr.append(res[i])
            # 判断该规则是否存在最终结论
            for j in range(len(msgArr)):
                if C[msgArr[j]] == 2:
                    num = 1
                    num2 = 1
                    r = features[msgArr[j]]
                    break
            if num == 1:
                break

    if num == 0:
        # 说明未有最终结论
        for j in range(len(msgArr)):
            if C[msgArr[j]] == 1:
                # print(features[msgArr[j]])
                r = features[msgArr[j]]
                num2 = 1
                break
    if num2 == 0:
        # print("条件不足,无法判断这是个啥东西")
        r = "条件不足,无法判断这是个啥东西"
    # print(msgArr)
    return r


if __name__ == '__main__':
    app.run()
