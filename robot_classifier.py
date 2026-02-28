# robot_classifier.py - 升级版
import requests
import json

class EmotionClassifier:
    def __init__(self):
        # 使用免费的中文情感分析API
        self.api_url = "https://api-inference.huggingface.co/models/uer/roberta-base-finetuned-jd-full-chinese"
        self.headers = {"Authorization": "Bearer hf_your_token_here"}
        
        # 备用关键词分类（当API不可用时）
        self.backup_dict = {
            "自我怀疑": ["我不行", "我好差", "做不到", "没能力", "笨", "废物", "没用", "失败"],
            "焦虑": ["担心", "害怕", "紧张", "睡不着", "怎么办", "焦虑", "恐慌"],
            "人际关系": ["朋友", "吵架", "不理解", "冷战", "绝交", "误会", "关系"],
            "愤怒+委屈": ["生气", "凭什么", "不公平", "委屈", "憋屈", "愤怒", "火大"],
            "心累+倦怠": ["累了", "没意思", "无聊", "重复", "疲惫", "倦怠", "心累"],
            "孤独": ["一个人", "孤单", "没人理", "寂寞", "空荡荡", "孤独", "孤立"]
        }
    
    def guess_emotion(self, text):
        """使用AI模型进行情感分类"""
        try:
            # 调用情感分析API
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={"inputs": text[:512]}  # 限制长度
            )
            
            if response.status_code == 200:
                result = response.json()
                # 解析返回的情感标签
                # 这里需要根据API返回格式调整
                # 假设返回格式是 [{"label": "positive", "score": 0.98}]
                emotion = self.map_to_our_categories(result)
                return emotion
        except:
            pass  # API调用失败时使用备用方案
        
        # 备用：关键词匹配
        return self.keyword_classify(text)
    
    def keyword_classify(self, text):
        """关键词分类（备用）"""
        scores = {emotion: 0 for emotion in self.backup_dict}
        for emotion, keywords in self.backup_dict.items():
            for word in keywords:
                if word in text:
                    scores[emotion] += 1
        
        if max(scores.values()) == 0:
            return "未知"
        return max(scores, key=scores.get)
    
    def map_to_our_categories(self, api_result):
        """将API返回映射到我们的6个类别"""
        # 这里需要根据实际API返回调整
        # 假设API返回情感强度
        return "焦虑"  # 暂时返回固定值
