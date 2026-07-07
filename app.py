import streamlit as st

# --------------------------
# 账号配置（在这里添加/修改账号密码）
# 格式：用户名: {"name": "显示姓名", "password": "密码", "role": "admin/student"}
# --------------------------
USER_CONFIG = {
    "admin": {
        "name": "系统管理员",
        "password": "admin123",
        "role": "admin"
    },
    "zhangsan": {
        "name": "张三",
        "password": "123456",
        "role": "student"
    }
}

# --------------------------
# 页面初始化
# --------------------------
st.set_page_config(page_title="第二课堂学分系统", layout="wide")

# 初始化登录状态
if "login_status" not in st.session_state:
    st.session_state.login_status = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "current_role" not in st.session_state:
    st.session_state.current_role = None

# --------------------------
# 登录页面
# --------------------------
def login_page():
    st.markdown("<h1 style='text-align: center;'>第二课堂学分管理系统</h1>", unsafe_allow_html=True)
    st.divider()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("用户登录")
        username = st.text_input("用户名")
        password = st.text_input("密码", type="password")
        
        if st.button("登录", type="primary", use_container_width=True):
            if username in USER_CONFIG:
                user = USER_CONFIG[username]
                if user["password"] == password:
                    st.session_state.login_status = True
                    st.session_state.current_user = user["name"]
                    st.session_state.current_role = user["role"]
                    st.rerun()
                else:
                    st.error("密码错误")
            else:
                st.error("用户名不存在")

# --------------------------
# 退出登录
# --------------------------
def logout():
    st.session_state.login_status = False
    st.session_state.current_user = None
    st.session_state.current_role = None
    st.rerun()

# --------------------------
# 主业务逻辑
# --------------------------
def main_page():
    # 侧边栏
    with st.sidebar:
        st.subheader(f"👤 {st.session_state.current_user}")
        role_text = "管理员" if st.session_state.current_role == "admin" else "学生"
        st.caption(f"身份：{role_text}")
        st.divider()
        
        # 按角色显示菜单
        if st.session_state.current_role == "admin":
            menu = st.radio("功能菜单", ["学分录入", "全部学分列表"])
        else:
            menu = st.radio("功能菜单", ["我的学分明细"])
        
        st.divider()
        if st.button("退出登录", use_container_width=True):
            logout()

    # 初始化内存数据（临时存储，重启会清空）
    if "score_list" not in st.session_state:
        st.session_state.score_list = []

    # ========== 管理员：学分录入 ==========
    if st.session_state.current_role == "admin" and menu == "学分录入":
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
    elif st.session_state.current_role == "admin" and menu == "全部学分列表":
        st.title("📊 全体学生学分总览")
        st.divider()
        if st.session_state.score_list:
            st.dataframe(st.session_state.score_list, use_container_width=True, hide_index=True)
            st.caption(f"共 {len(st.session_state.score_list)} 条记录")
        else:
            st.info("暂无数据，请先到「学分录入」添加记录")

    # ========== 学生：个人学分查询 ==========
    elif st.session_state.current_role == "student" and menu == "我的学分明细":
        st.title("🔍 我的第二课堂学分明细")
        st.divider()
        my_scores = [item for item in st.session_state.score_list if item["姓名"] == st.session_state.current_user]
        if my_scores:
            st.dataframe(my_scores, use_container_width=True, hide_index=True)
            st.metric("累计总学分", my_scores[0]["总学分"])
        else:
            st.info("暂未查询到你的学分记录，请联系管理员录入")

# --------------------------
# 程序入口
# --------------------------
if not st.session_state.login_status:
    login_page()
else:
    main_page()
