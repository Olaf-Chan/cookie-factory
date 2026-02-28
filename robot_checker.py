class CookieChecker:
    def check_cookie(self, cookie_text):
        score = 0
        feedback = []
        
        if "心情标签：" in cookie_text:
            score += 1
            feedback.append("✅ 有心情标签")
        else:
            feedback.append("❌ 缺少心情标签")
        
        if "小故事：" in cookie_text:
            score += 1
            feedback.append("✅ 有小故事")
        else:
            feedback.append("❌ 缺少小故事")
        
        if "可以这样安慰" in cookie_text:
            score += 1
            feedback.append("✅ 有安慰话术")
        else:
            feedback.append("❌ 缺少安慰话术")
        
        if "特别细节：" in cookie_text:
            score += 1
            feedback.append("✅ 有细节")
        else:
            feedback.append("❌ 缺少细节")
        
        total_score = (score / 4) * 5
        
        return {
            "score": round(total_score, 1),
            "passed": total_score >= 3.5,
            "feedback": feedback
        }