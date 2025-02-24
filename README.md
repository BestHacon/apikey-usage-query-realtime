# Real-Time API Key Usage Statistics  
## Introduction  
+ This project leverages the response body (Response) from LLM to track token usage and cost expenditure in real-time. The primary use case is to monitor API key usage during experimental processes.  
+ Supports most models from OpenAI and Gemini, with the ability to add additional models as needed.  
## Example  
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