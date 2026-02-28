# robot_maker.py - 升级版
import random
from datetime import datetime

class StoryMaker:
    def __init__(self):
        # 专业的RAG案例模板
        self.templates = {
            "自我怀疑": self._self_doubt_template,
            "焦虑": self._anxiety_template,
            "人际关系": self._relationship_template,
            "愤怒+委屈": self._anger_template,
            "心累+倦怠": self._burnout_template,
            "孤独": self._loneliness_template,
            "未知": self._default_template
        }
        
        # 案例库种子数据
        self.case_seeds = {
            "自我怀疑": [
                "考试失败后的自我否定",
                "工作失误后的能力怀疑",
                "对比他人产生的自卑感"
            ],
            "焦虑": [
                "对未来不确定性的担忧",
                "重大事件前的紧张失眠",
                "多重压力下的恐慌感"
            ]
            # ... 其他情绪类似
        }
    
    def make_cookie(self, emotion, original_text, user_id="user001"):
        """生成专业RAG案例"""
        if emotion not in self.templates:
            emotion = "未知"
        
        # 调用对应情绪的模板函数
        template_func = self.templates[emotion]
        return template_func(original_text, user_id)
    
    def _self_doubt_template(self, text, user_id):
        """自我怀疑的RAG模板"""
        case_id = f"SD-{datetime.now().strftime('%Y%m%d')}-{random.randint(100,999)}"
        
        # 从原始文本提取关键信息
        keywords = self._extract_keywords(text)
        
        return f"""
## 案例ID: {case_id}
**情绪标签**: 自我怀疑、能力焦虑、价值困惑
**适用场景**: 当用户因{keywords.get('trigger', '某次失败')}而质疑自身能力，陷入'我是否足够好'的循环时。
**核心情境**: 用户在面对{keywords.get('situation', '挑战性任务')}时，表现出对自身能力的深度怀疑，常伴随'{keywords.get('feeling', '沮丧')}'等具体感受。

**用户表达（可模拟的提问）参考**:
- "我是不是根本不适合做这个？怎么努力都没用。"
- "看到别人都做得那么好，我觉得自己好差劲。"

**参考回应/素材（AI可学习与调用的核心）**:
"这种感觉我特别理解。**许多成功人士在早期都经历过类似的自我怀疑时刻**。比如乔布斯曾在被自己创立的公司开除后，形容自己'成了公众的失败典型'。但正是这段低谷，让他后来创造了更辉煌的成就。你的自我怀疑，可能正是深度反思和成长的前奏。"

**细节颗粒度解析**:
- **L2 具体感受**: 用户提到'{keywords.get('keyword1', '无力感')}'、'{keywords.get('keyword2', '挫败感')}'
- **L3 心理矛盾**: 既渴望成功，又害怕尝试；既想证明自己，又担心再次失败
- **L4 认知重构**: 将'自我怀疑'重构为'深度反思的信号'和'成长必经阶段'
- **L5 叙事框架**: 名人低谷经历对比 → 普遍化困境 → 提供新的理解视角 → 指向积极可能性

**原始文本摘要**: "{text[:100]}..."
**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**生成者**: {user_id}
"""
    
    def _extract_keywords(self, text):
        """简单关键词提取（可后续升级为NLP模型）"""
        keywords = {
            'trigger': '挑战',
            'situation': '困难情境',
            'feeling': '挫败',
            'keyword1': '能力不足',
            'keyword2': '不如他人'
        }
        # 这里可以添加简单的关键词提取逻辑
        if "考试" in text:
            keywords['trigger'] = "考试失利"
        if "工作" in text:
            keywords['trigger'] = "工作失误"
        return keywords
    
    # 其他情绪模板类似，限于篇幅省略...
    def _anxiety_template(self, text, user_id):
        case_id = f"AX-{datetime.now().strftime('%Y%m%d')}-{random.randint(100,999)}"
        return f"""
## 案例ID: {case_id}
**情绪标签**: 焦虑、不确定性压力、未来恐惧
**适用场景**: 当用户面临重大决策或未知变化，产生'万一搞砸了怎么办'的灾难化思维时。
**核心情境**: 用户因'{text[:20]}...'等具体事件，陷入对未来的过度担忧，表现出生理性焦虑反应。

**用户表达（可模拟的提问）参考**:
- "我每天晚上都睡不着，一直在想如果失败了怎么办。"
- "心一直悬着，什么事都做不进去，完全被焦虑控制了。"

**参考回应/素材（AI可学习与调用的核心）**:
"焦虑其实是你的大脑在试图保护你。**研究表明，适度的焦虑能提升表现约15%**。就像运动员上场前的紧张，是身体在调动资源。你可以试着问自己：'最坏的结果是什么？我能否承受？' 往往你会发现，即使最坏情况发生，你也有应对的能力。"

**细节颗粒度解析**:
- **L2 具体感受**: 失眠、心慌、注意力无法集中
- **L3 心理矛盾**: 既想逃避压力源，又知道必须面对
- **L4 认知重构**: 将'焦虑'重构为'身体的预警系统'和'表现提升信号'
- **L5 叙事框架**: 科学依据引入 → 类比解释 → 提供具体工具（灾难化思维破解）→ 增强控制感

**原始文本摘要**: "{text[:100]}..."
"""
    
    # 其他模板函数...
