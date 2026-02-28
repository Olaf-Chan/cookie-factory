# robot_checker.py - 升级版
class CookieChecker:
    def __init__(self):
        self.criteria = {
            "情感准确性": {
                "权重": 0.3,
                "说明": "案例标签是否准确匹配原始文本的情绪"
            },
            "细节丰富度": {
                "权重": 0.3,
                "说明": "是否包含L2-L5的完整细节层次"
            },
            "实用价值": {
                "权重": 0.25,
                "说明": "是否提供可操作的心理洞察或具体建议"
            },
            "结构规范性": {
                "权重": 0.15,
                "说明": "是否符合RAG案例的标准格式"
            }
        }
    
    def check_cookie(self, cookie_text):
        """四维度专业评估"""
        scores = {}
        feedback = []
        
        # 1. 情感准确性评估
        emotion_score = self._assess_emotion_accuracy(cookie_text)
        scores["情感准确性"] = emotion_score
        feedback.append(f"✅ 情感准确性: {emotion_score}/5")
        
        # 2. 细节丰富度评估
        detail_score = self._assess_detail_level(cookie_text)
        scores["细节丰富度"] = detail_score
        feedback.append(f"✅ 细节丰富度: {detail_score}/5")
        
        # 3. 实用价值评估
        practical_score = self._assess_practical_value(cookie_text)
        scores["实用价值"] = practical_score
        feedback.append(f"✅ 实用价值: {practical_score}/5")
        
        # 4. 结构规范性评估
        structure_score = self._assess_structure(cookie_text)
        scores["结构规范性"] = structure_score
        feedback.append(f"✅ 结构规范性: {structure_score}/5")
        
        # 计算加权总分
        weighted_score = sum(
            scores[dim] * self.criteria[dim]["权重"] 
            for dim in scores
        )
        
        return {
            "score": round(weighted_score, 2),
            "passed": weighted_score >= 3.0,  # 3.0分通过
            "scores": scores,
            "feedback": feedback,
            "criteria": self.criteria
        }
    
    def _assess_emotion_accuracy(self, text):
        """评估情感准确性"""
        required_emotions = ["情绪标签", "适用场景", "核心情境"]
        score = 0
        for req in required_emotions:
            if req in text:
                score += 1
        return min(5, score * 1.7)  # 转换为5分制
    
    def _assess_detail_level(self, text):
        """评估细节层次"""
        levels = ["L2", "L3", "L4", "L5"]
        found = sum(1 for level in levels if level in text)
        return min(5, found * 1.25)
    
    def _assess_practical_value(self, text):
        """评估实用价值"""
        indicators = ["可以这样", "比如", "研究表明", "你可以", "建议", "尝试"]
        found = sum(1 for indicator in indicators if indicator in text)
        return min(5, found)
    
    def _assess_structure(self, text):
        """评估结构完整性"""
        sections = ["案例ID", "情绪标签", "适用场景", "核心情境", 
                   "用户表达", "参考回应", "细节颗粒度解析"]
        found = sum(1 for section in sections if section in text)
        return min(5, found * 0.7)
