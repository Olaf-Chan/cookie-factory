import streamlit as st
import time
import json
from datetime import datetime
from robot_classifier import EmotionClassifier
from robot_maker import StoryMaker
from robot_checker import CookieChecker

# 给工厂起个标题
st.set_page_config(page_title="饼干工厂", page_icon="🍪")
st.title("🍪 我的故事饼干工厂")
st.write("欢迎！这里可以自动制作情绪陪伴小故事")

# 添加导航栏
menu = st.sidebar.selectbox(
    "想去哪里？",
    ["🏠 首页", "🎯 做饼干", "🔁 批量生产", "👀 检查饼干", "📦 打包饼干"]
)

def save_to_warehouse(cookie_data):
    """保存到仓库"""
    try:
        with open("warehouse.json", "r", encoding="utf-8") as f:
            warehouse = json.load(f)
    except:
        warehouse = []
    
    cookie_data["id"] = len(warehouse) + 1
    cookie_data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    warehouse.append(cookie_data)
    
    with open("warehouse.json", "w", encoding="utf-8") as f:
        json.dump(warehouse, f, ensure_ascii=False, indent=2)
    
    return cookie_data["id"]

if menu == "🏠 首页":
    st.header("工厂介绍")
    st.write("""
    ## 这里有4个机器人：
    1. 🎭 **场景分类员**：判断心情类型
    2. 🧱 **故事模具工**：制作故事饼干
    3. 🔍 **饼干质检员**：检查饼干质量
    4. 📚 **仓库管理员**：存放到仓库
    
    ## 工作流程：
    原料 → 分类 → 制作 → 检查 → 入库
    """)

elif menu == "🎯 做饼干":
    st.header("开始做饼干！")
    user_text = st.text_area("请粘贴一段聊天记录（比如朋友说心情不好的对话）")
    
    if st.button("开始制作") and user_text:
        st.info("机器人开始工作啦...")
        
        # 1号机器人工作
        with st.spinner("🎭 场景分类员在判断心情..."):
            classifier = EmotionClassifier()
            emotion = classifier.guess_emotion(user_text)
        
        # 2号机器人工作
        with st.spinner("🧱 故事模具工在制作饼干..."):
            maker = StoryMaker()
            cookie = maker.make_cookie(emotion, user_text)
        
        # 3号机器人工作
        with st.spinner("🔍 饼干质检员在检查..."):
            checker = CookieChecker()
            check_result = checker.check_cookie(cookie)
        
        # 显示结果
        st.success(f"✅ 制作完成！识别为：{emotion}")
        st.markdown(cookie)
        
        st.write("### 📊 质检报告")
        st.write(f"**得分：{check_result['score']}/5.0**")
        for fb in check_result['feedback']:
            st.write(f"- {fb}")
        
        if check_result['passed']:
            st.success("✅ 通过质检！可以入库")
            if 'consecutive_pass' not in st.session_state:
                st.session_state.consecutive_pass = 0
            st.session_state.consecutive_pass += 1
        else:
            st.warning("⚠️ 需要改进")
            st.session_state.consecutive_pass = 0
        
        st.write(f"📈 连续通过次数：{st.session_state.get('consecutive_pass', 0)}")
        
        # 保存按钮
        if st.button("💾 保存到仓库") and check_result['passed']:
            cookie_data = {
                "emotion": emotion,
                "content": cookie,
                "score": check_result['score'],
                "original": user_text[:100]
            }
            
            cookie_id = save_to_warehouse(cookie_data)
            st.success(f"✅ 已保存到仓库！饼干ID：{cookie_id}")

elif menu == "🔁 批量生产":
    st.header("批量生产饼干")
    
    consecutive_pass = st.session_state.get('consecutive_pass', 0)
    
    if consecutive_pass < 3:
        st.warning(f"🔒 需要连续通过3个饼干才能解锁批量生产")
        st.write(f"当前连续通过：{consecutive_pass}/3")
        st.progress(consecutive_pass / 3)
    else:
        st.success("🎉 已解锁批量生产！")
        
        uploaded_file = st.file_uploader("上传聊天记录文件（每行一段）", type=['txt'])
        
        if uploaded_file and st.button("开始批量生产"):
            lines = uploaded_file.read().decode("utf-8").splitlines()
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, line in enumerate(lines):
                if line.strip():
                    status_text.text(f"正在处理第 {i+1}/{len(lines)} 条...")
                    
                    classifier = EmotionClassifier()
                    maker = StoryMaker()
                    checker = CookieChecker()
                    
                    emotion = classifier.guess_emotion(line)
                    cookie = maker.make_cookie(emotion, line)
                    result = checker.check_cookie(cookie)
                    
                    if result['passed']:
                        cookie_data = {
                            "emotion": emotion,
                            "content": cookie,
                            "score": result['score'],
                            "original": line[:100]
                        }
                        save_to_warehouse(cookie_data)
                    
                    progress_bar.progress((i + 1) / len(lines))
            
            st.balloons()
            st.success(f"批量生产完成！处理了 {len(lines)} 条记录")

elif menu == "👀 检查饼干":
    st.header("检查做好的饼干")
    try:
        with open("warehouse.json", "r", encoding="utf-8") as f:
            warehouse = json.load(f)
        
        st.write(f"仓库里共有 {len(warehouse)} 个饼干")
        
        for cookie in warehouse[-5:]:  # 显示最近5个
            with st.expander(f"饼干#{cookie['id']} - {cookie['emotion']} ({cookie['score']}/5)"):
                st.markdown(cookie['content'])
                st.caption(f"原话：{cookie['original']}")
    except:
        st.info("仓库还是空的，先去做些饼干吧！")

elif menu == "📦 打包饼干":
    st.header("打包饼干给伙伴")
    
    try:
        with open("warehouse.json", "r", encoding="utf-8") as f:
            warehouse = json.load(f)
        
        st.write(f"仓库里共有 {len(warehouse)} 个饼干")
        
        emotion_count = {}
        for cookie in warehouse:
            emotion = cookie.get("emotion", "未知")
            emotion_count[emotion] = emotion_count.get(emotion, 0) + 1
        
        st.write("### 📊 饼干分类统计")
        for emotion, count in emotion_count.items():
            st.write(f"- {emotion}: {count} 个")
        
        st.write("### 📤 导出选项")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("导出为TXT文件"):
                with open("饼干工厂_全部饼干.txt", "w", encoding="utf-8") as f:
                    for cookie in warehouse:
                        f.write(f"\n{'='*60}\n")
                        f.write(f"饼干ID: {cookie['id']}\n")
                        f.write(f"心情: {cookie['emotion']}\n")
                        f.write(cookie['content'])
                        f.write(f"\n原话片段: {cookie['original']}\n")
                
                with open("饼干工厂_全部饼干.txt", "r", encoding="utf-8") as f:
                    st.download_button(
                        label="📥 下载TXT文件",
                        data=f.read(),
                        file_name="情绪陪伴饼干.txt",
                        mime="text/plain"
                    )
        
        with col2:
            if st.button("导出为Excel文件"):
                import pandas as pd
                
                data = []
                for cookie in warehouse:
                    data.append({
                        "ID": cookie['id'],
                        "心情": cookie['emotion'],
                        "得分": cookie['score'],
                        "原话": cookie['original'],
                        "内容": cookie['content'][:200] + "..."
                    })
                
                df = pd.DataFrame(data)
                df.to_excel("饼干工厂_全部饼干.xlsx", index=False)
                
                with open("饼干工厂_全部饼干.xlsx", "rb") as f:
                    st.download_button(
                        label="📥 下载Excel文件",
                        data=f.read(),
                        file_name="情绪陪伴饼干.xlsx",
                        mime="application/vnd.ms-excel"
                    )
    
    except FileNotFoundError:
        st.info("仓库还是空的，先去做些饼干吧！")