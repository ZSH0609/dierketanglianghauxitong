import streamlit as st
import streamlit_authenticator as stauth

# --------------------------
# 账号配置
# 测试账号：
# 管理员：用户名 admin  密码 admin123
# 学生：  用户名 zhangsan  密码 123456
# --------------------------
hashed_pw = stauth.Hasher(['admin123', '123456']).generate()

config = {
    "credentials": {
        "usernames": {
            "admin": {
                "name": "系统管理员",
                "password": hashed_pw[0],
                "roles": ["admin"]
            },
            "zhangsan": {
                "name": "张三",
                "password": hashed_pw[1],
                "roles": ["student"]
            }
        }
    },
    "cookie": {
        "name": "second_class_cookie",
        "key": "second_class_secret_key_2026",
        "expiry_days": 30
    }
}

# --------------------------
# 页面初始化
# --------------------------
st.set_page_config(page_title="第二课堂学分系统", layout="wide")

# 初始化认证器
authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"]
)

# 适配0.3.x新版：用fields设置表单标题，不再用form_name
name, authentication_status, username = authenticator.login(
    location="main",
    fields={
        "Form name": "第二课堂学分管理系统",
        "Username": "用户名",
        "Password": "密码",
        "Login": "登录"
    }
)

# --------------------------
# 登录后业务逻辑
# --------------------------
if authentication_status:
    # 从配置里取角色，不依赖session_state，兼容性更强
    user_info = config["credentials"]["usernames"].get(username, {})
    role = user_info.get("roles", ["student"])[0]

    # 侧边栏信息
    with st.sidebar:
        st.subheader(f"👤 {name}")
        role_text = "管理员" if role == "admin" else "学生"
        st.caption(f"身份：{role_text}")
        st.divider()

        # 按角色显示菜单
        if role == "admin":
            menu = st.radio("功能菜单", ["学分录入", "全部学分列表"])
        else:
            menu = st.radio("功能菜单", ["我的学分明细"])
        
        st.divider()
        authenticator.logout("退出登录", "sidebar")

    # 初始化内存数据（临时存储，重启会清空）
    if "score_list" not in st.session_state:
        st.session_state.score_list = []

    # ========== 管理员：学分录入 ==========
    if role == "admin" and menu == "学分录入":
        st.title("✏️ 学分录入")
        st.caption("填写分项学分，系统自动计算总学分")
        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            stu_name = st.text_input("学生姓名")
            stu_id = st.text_input("学号")
        with col2:
            thought = st.number_input("思想引领学分", min_value=0.0, step=0.5, value=0.0)
            study = st.number_input("学业发展学分", min_value=0.0, step=0.5, value=0.0)
        
        col3, col4, col5 = st.columns(3)
        with col3:
            culture = st.number_input("文体活动学分", min_value=0.0, step=0.5, value=0.0)
        with col4:
            practice = st.number_input("社会实践学分", min_value=0.0, step=0.5, value=0.0)
        with col5:
            volunteer = st.number_input("志愿服务学分", min_value=0.0, step=0.5, value=0.0)

        # 自动计算总分
        total_score = thought + study + culture + practice + volunteer
        st.metric("✅ 系统自动计算总学分", total_score)

        if st.button("保存记录", type="primary", use_container_width=True):
            if not stu_name or not stu_id:
                st.error("请填写学生姓名和学号")
            else:
                st.session_state.score_list.append({
                    "姓名": stu_name,
                    "学号": stu_id,
                    "思想引领": thought,
                    "学业发展": study,
                    "文体活动": culture,
                    "社会实践": practice,
                    "志愿服务": volunteer,
                    "总学分": total_score
                })
                st.success("录入成功！可在「全部学分列表」查看")

    # ========== 管理员：全量学分列表 ==========
    elif role == "admin" and menu == "全部学分列表":
        st.title("📊 全体学生学分总览")
        st.divider()
        if st.session_state.score_list:
            st.dataframe(st.session_state.score_list, use_container_width=True, hide_index=True)
            st.caption(f"共 {len(st.session_state.score_list)} 条记录")
        else:
            st.info("暂无数据，请先到「学分录入」添加记录")

    # ========== 学生：个人学分查询 ==========
    elif role == "student" and menu == "我的学分明细":
        st.title("🔍 我的第二课堂学分明细")
        st.divider()
        my_scores = [item for item in st.session_state.score_list if item["姓名"] == name]
        if my_scores:
            st.dataframe(my_scores, use_container_width=True, hide_index=True)
            st.metric("累计总学分", my_scores[0]["总学分"])
        else:
            st.info("暂未查询到你的学分记录，请联系管理员录入")

# 登录状态处理
elif authentication_status == False:
    st.error("用户名或密码错误，请重试")
elif authentication_status == None:
    st.info("请输入账号密码登录系统")
