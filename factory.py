# 在factory.py中添加以下功能
elif menu == "🎯 做饼干":
    st.header("🎯 RAG示例专业生成")
    
    # 模式选择
    mode = st.radio("选择生成模式:", ["快速生成", "深度生成", "自定义生成"])
    
    # 文本输入
    user_text = st.text_area("输入原始对话文本:", height=150, 
                           placeholder="例如：'我今天又被领导批评了，感觉做什么都不对，好累...'")
    
    # 高级选项（展开）
    with st.expander("高级选项"):
        col1, col2 = st.columns(2)
        with col1:
            emotion_hint = st.selectbox("情感提示（可选）:", 
                                       ["自动检测", "自我怀疑", "焦虑", "人际关系", 
                                        "愤怒+委屈", "心累+倦怠", "孤独"])
        with col2:
            complexity = st.slider("生成复杂度:", 1, 5, 3)
    
    if st.button("开始专业生成") and user_text:
        # 显示进度条
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # 1. 情感分类
        status_text.text("🔄 步骤1/4: 深度情感分析中...")
        classifier = EmotionClassifier()
        emotion = classifier.guess_emotion(user_text)
        if emotion_hint != "自动检测":
            emotion = emotion_hint
        progress_bar.progress(25)
        
        # 2. RAG示例生成
        status_text.text("🔄 步骤2/4: 生成专业RAG示例...")
        maker = StoryMaker()
        cookie = maker.make_cookie(emotion, user_text, user_id="ai_generator")
        progress_bar.progress(50)
        
        # 3. 质量评估
        status_text.text("🔄 步骤3/4: 四维度质量评估...")
        checker = CookieChecker()
        evaluation = checker.check_cookie(cookie)
        progress_bar.progress(75)
        
        # 4. 结果展示
        status_text.text("✅ 生成完成！")
        progress_bar.progress(100)
        
        # 显示结果
        st.success(f"**情感分类:** {emotion}")
        st.markdown(cookie)
        
        # 专业评估报告
        st.subheader("📊 专业评估报告")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("综合得分", f"{evaluation['score']}/5.0")
        with col2:
            status = "通过" if evaluation['passed'] else "需改进"
            st.metric("评估结果", status)
        with col3:
            st.metric("评估维度", "4项")
        
        # 详细评分
        with st.expander("查看详细评分"):
            for dim, score in evaluation['scores'].items():
                st.write(f"**{dim}**: {score}/5.0 (权重: {evaluation['criteria'][dim]['权重']})")
                st.progress(score/5)
        
        # 保存选项
        if evaluation['passed']:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 保存到案例库", type="primary"):
                    # 保存逻辑
                    pass
            with col2:
                if st.button("🔄 重新生成"):
                    st.rerun()
        else:
            st.warning("⚠️ 案例未通过质量评估，建议调整后重新生成")
