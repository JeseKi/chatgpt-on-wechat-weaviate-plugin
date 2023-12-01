import weaviate
import json
import codecs

from common.log import logger
from bridge.context import ContextType
from plugins.plugin import Plugin
import plugins
from plugins.event import Event, EventAction, EventContext
from config import conf
from .config import *


@plugins.register(name="weaviate_database", desc="Combine Weaviate vector database with LLM.", version="1.0", author="JeseKi", desire_priority= 100)
class Weaviate_database(Plugin):
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info("[Weaviate] inited")
        self.weaviate_client = weaviate.Client(
            url = weaviate_url,
            auth_client_secret = weaviate.AuthApiKey(api_key=weaviate_key),
            additional_headers = {
                "X-OpenAI-Api-Key": conf().get("open_ai_api_key")
            }
        )

    def on_handle_context(self, e_context: EventContext):
        prompt = e_context['context'].content
        if e_context['context'].type != ContextType.TEXT:
            return

        # 读取配置文件的值
        query_class = config['query_class']
        query_limit = config['query_limit']
        query_fields = config['query_fields']
        response_fields = config['response_fields']

        # 发起查询请求
        response = (
            self.weaviate_client.query
            .get(query_class, query_fields)
            .with_near_text({
                "concepts": [f"{prompt}"]
            })
            .with_limit(query_limit)
            .with_additional(["distance"])
            .do()
        )
        # 获取查询结果
        datas = response['data']['Get'][query_class]
        
        # 初始化一个列表来存储结果
        results = []
        
        # 遍历查询结果
        for data in datas:
            # 初始化一个字典来存储当前结果
            result = {}
            
            # 遍历response_fields
            for key, value in response_fields.items():
                # 获取值并将其添加到结果字典中
                value = data.get(value)
                if value is not None:
                    result[key] = value

            # 将结果字典添加到结果列表中
            results.append(result)
        
        # 将结果列表转换为JSON字符串
        results_str = json.dumps(results, indent=4)
        # 解码字符串
        decoded_data = codecs.decode(results_str, 'unicode_escape')
        # 将查询结果添加到上下文内容中
        e_context['context'].content += f"\n---\n{decoded_data}\n---\n以上是相关数据库所给的内容."
        # 继续处理事件
        e_context.action = EventAction.CONTINUE