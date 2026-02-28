class EmotionClassifier:
    def __init__(self):
        self.emotion_dict = {
            "自我怀疑": ["我不行", "我好差", "做不到", "没能力", "笨", "废物", "没用"],
            "焦虑": ["担心", "害怕", "紧张", "睡不着", "怎么办", "焦虑", "恐慌"],
            "人际关系": ["朋友", "吵架", "不理解", "冷战", "绝交", "误会", "关系"],
            "愤怒+委屈": ["生气", "凭什么", "不公平", "委屈", "憋屈", "愤怒", "火大"],
            "心累+倦怠": ["累了", "没意思", "无聊", "重复", "疲惫", "倦怠", "心累"],
            "孤独": ["一个人", "孤单", "没人理", "寂寞", "空荡荡", "孤独", "孤立"]
        }
    
    def guess_emotion(self, text):
        scores = {emotion: 0 for emotion in self.emotion_dict}
        
        for emotion, keywords in self.emotion_dict.items():
            for word in keywords:
                if word in text:
                    scores[emotion] += 1
        
        if max(scores.values()) == 0:
            return "未知"
        else:
            return max(scores, key=scores.get)