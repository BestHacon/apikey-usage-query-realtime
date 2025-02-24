# APIKey使用情况实时统计
## 介绍
+ 本项目借助LLM返回体Respone统计Token使用情况和费用开销。主要使用场景为实验过程中的APIKey使用统计。
+ 支持OpenAI和Gemini的大部分模型，可以自主添加。
## 示例
```python
from apikey_query.src.query import QueryCost
from google import genai
client = genai.Client()
response = client.models.generate_content(
  model="gemini-1.5-flash",
  contents=["1+1=?"])
print(response.text)
print(QueryCost().get_cost(response))
 ```