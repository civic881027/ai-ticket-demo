import ollama
import json
from django.conf import settings
from django.core.cache import cache
from typing import Dict, Any

class OllamaService:
    def __init__(self):
        self.host = settings.OLLAMA_HOST
        self.model = settings.OLLAMA_MODEL
        self.client = ollama.Client(host=self.host)
    
    def categorize_ticket(self, title: str, description: str) -> Dict[str, Any]:
        """
        使用AI分類工單並建議優先級
        """
        cache_key = f"categorize_{hash(title + description)}"
        cached_result = cache.get(cache_key)
        #print('cached_result',cached_result)
        if cached_result:
            return cached_result
        
        prompt = f"""
        請分析以下客服工單，並提供分類和優先級建議：
        
        標題: {title}
        描述: {description}
        
        請以JSON格式回覆，包含：
        1. category: 工單分類（技術問題、帳戶問題、產品諮詢、投訴建議）
        2. priority: 優先級（low、medium、high、urgent）
        3. reasoning: 分類理由
        
        範例回覆格式：
        {{"category": "技術問題", "priority": "high", "reasoning": "用戶無法登入系統，影響正常使用"}}
        """
        
        try:
            #print('prompt',prompt)
            response = self.client.chat(
                model=self.model,
                messages=[{
                    'role': 'user',
                    'content': prompt
                }]
            )
            
            # 解析回應
            response_text = response['message']['content']
            #print(f"Ollama 回應內容: {response_text}")  # 新增印出調試
            # 嘗試解析JSON
            try:
                result = json.loads(response_text)
                # 驗證回應格式
                if all(key in result for key in ['category', 'priority', 'reasoning']):
                    cache.set(cache_key, result, 3600)  # 快取1小時
                    return result
            except json.JSONDecodeError:
                pass
            
            # 如果JSON解析失敗，返回默認值
            default_result = {
                'category': '一般諮詢',
                'priority': 'medium',
                'reasoning': 'AI無法正確分析，使用預設分類'
            }
            return default_result
            
        except Exception as e:
            #print(f"Ollama服務錯誤: {e}")
            return {
                'category': '一般諮詢',
                'priority': 'medium',
                'reasoning': f'服務錯誤: {str(e)}'
            }
    
    def generate_response(self, ticket) -> str:
        """
        根據工單內容生成建議回覆
        """
        cache_key = f"response_{ticket.id}_{ticket.updated_at.timestamp()}"
        cached_response = cache.get(cache_key)
        
        if cached_response:
            return cached_response
        
        prompt = f"""
        作為客服專員，請針對以下工單提供專業且友善的回覆建議：
        
        工單標題: {ticket.title}
        工單描述: {ticket.description}
        工單分類: {ticket.category}
        優先級: {ticket.get_priority_display()}
        
        請提供一個專業、友善且有幫助的回覆，包含：
        1. 對問題的理解確認
        2. 可能的解決方案或後續步驟
        3. 預期的處理時間
        
        回覆應該以繁體中文撰寫，語氣親切專業。
        """
        
        try:
            response = self.client.chat(
                model=self.model,
                messages=[{
                    'role': 'user',
                    'content': prompt
                }]
            )
            
            ai_response = response['message']['content']
            cache.set(cache_key, ai_response, 1800)  # 快取30分鐘
            return ai_response
            
        except Exception as e:
            #print(f"生成回覆錯誤: {e}")
            return "抱歉，AI助手暫時無法提供回覆建議，請稍後再試。"
