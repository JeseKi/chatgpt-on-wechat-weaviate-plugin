# chatgpt-on-wechat-weaviate-plugin

## 1. 用途
此插件旨在将Weaviate向量数据库集成到个人微信中，并可与ChatGPT配合使用。

## 2. 环境
插件兼容Python 3.10。

## 3. 安装方法
要安装此插件，请按照[插件安装说明](https://github.com/zhayujie/chatgpt-on-wechat/blob/master/plugins/README.md#%E6%8F%92%E4%BB%B6%E5%AE%89%E8%A3%85%E6%96%B9%E6%B3%95)中的步骤进行。

## 4. 启动方法
要启动此插件，请导航到此插件的目录，复制`config.json.template`，然后将其重命名为`config.json`。在其中填入你的数据，格式如下：

```json
{
    "weaviate_url" : "YOUR_WEAVIATE_URL_HERE", # 你的Weaviate URL
    "weaviate_key" : "YOUR_WEAVIATE_KEY_HERE", # 你的Weaviate API密钥
    "query_class" : "YOURCLASS", # 你的查询类
    "query_limit" : 1, # 查询返回的条目限制
    "query_fields" : ["question", "answer"], # 需要查询的字段
    "response_fields" : { # 需要返回的字段
        "Question" : "question",
        "Answer" : "answer"
    }
}
```

然后，导航到`chatgpt-on-wechat`的根目录下的`plugins/plugins.json`文件，将以下行添加到`plugins`部分：

```json
"weaviate_database": {
    "enabled": true,
    "priority": 100
},
```

完成这些步骤后，即可正常使用插件。