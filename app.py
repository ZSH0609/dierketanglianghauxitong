import streamlit as st
import streamlit_authenticator as stauth

# --------------------------
# 1. 账号配置（可自行添加/修改）
# 密码已自动加密，修改密码看下方注释
# --------------------------
hashed_passwords = stauth.Hasher(['admin123', '123456']).generate()

config = {
    "credentials": {
        "usernames": {
            "admin": {
                "name": "管理员",
                "password": hashed_passwords[0],
                "roles": ["admin"]  # 管理员权限
            },
            "student1": {
                "name": "张三",
                "password": hashed_passwords[1],
                "roles": ["student"]  # 学生权限
            }
        }
    },
    "cookie": {
        "name": "second_class_cookie",
        "key": "random_secret_key_2026",
        "expiry_days": 30
    }
}

# --------------------------
# 2. 初始化登录组件
# --------------------------
authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"]
)

name, auth_status, username = authenticator.login("第二课堂学分系统", "main")

# --------------------------
# 3. 登录后业务逻辑
# --------------------------
if auth_status:
    # 侧边栏：欢迎信息 + 退出按钮
    authenticator.logout("退出登录", "sidebar")
    st.sidebar.write(f"当前用户：{name}")
    user_role = st.session_state["roles"][0]

    st.title("📚 第二课堂学分管理系统")
    st.divider()

    # 初始化内存数据库（重启会清空，后续对接云端数据库）
    if "score_data" not in st.session_state:
        st.session_state.score_data = []

    # ========== 管理员功能：录入学分 ==========
    if user_role == "admin":
        st.subheader("✏️ 学分录入")
        col1, col2 = st.columns(2)
        with col1:
            stu_name = st.text_input("学生姓名")
            stu_id = st.text_input("学号")
        with col2:
            # 第二课堂五大类，可按需修改分类名称
            thought = st.number_input("思想引领学分", min_value=0.0, step=0.5)
            study = st.number_input("学业发展学分", min_value=0.0, step=0.5)
        
        col3, col4 = st.columns(2)
        with col3:
            culture = st.number_input("文体活动学分", min_value=0.0, step=0.5)
            practice = st.number_input("社会实践学分", min_value=0.0, step=0.5)
        with col4:
            volunteer = st.number_input("志愿服务学分", min_value=0.0, step=0.5)

        # 自动计算总分
        total_score = thought + study + culture + practice + volunteer
        st.metric("✅ 系统自动计算总学分", total_score)

        if st.button("保存记录", type="primary"):
            if not stu_name or not stu_id:
                st.error("请填写姓名和学号")
            else:
                st.session_state.score_data.append({
                    "姓名": stu_name,
                    "学号": stu_id,
                    "思想引领": thought,
                    "学业发展": study,
                    "文体活动": culture,
                    "社会实践": practice,
                    "志愿服务": volunteer,
                    "总学分": total_score
                })
                st.success("录入成功！")
        
        st.divider()
        st.subheader("📊 全部学生学分列表")
        if st.session_state.score_data:
            st.dataframe(st.session_state.score_data, use_container_width=True)
        else:
            st.info("暂无数据，请先录入")

    # ========== 学生功能：仅查看自己的学分 ==========
    elif user_role == "student":
        st.subheader("🔍 我的学分明细")
        my_scores = [item for item in st.session_state.score_data if item["姓名"] == name]
        
        if my_scores:
            st.dataframe(my_scores, use_container_width=True)
            st.metric("我的总学分", my_scores[0]["总学分"])
        else:
            st.info("暂未查询到你的学分记录，请联系管理员录入")

# 登录失败/未登录状态
elif auth_status == False:
    st.error("用户名或密码错误")
elif auth_status == None:
    st.warning("请输入账号密码登录")