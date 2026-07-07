import streamlit as st
import time

# ==========================
# 基础配置：团支部班级列表、分数类型
# ==========================
CLASS_LIST = [
    "24级软工1班团支部",
    "24级软工2班团支部",
    "24级计科1班团支部",
    "24级计科2班团支部"
]

SCORE_TYPES = [
    "思想引领",
    "学业发展",
    "文体活动",
    "社会实践",
    "志愿服务"
]

# ==========================
# 初始化系统数据（首次运行自动加载）
# ==========================
def init_data():
    if "users" not in st.session_state:
        # 用户表格式：用户名: {name, password, role, belong_class}
        # role: super_admin(超级管理员) / class_admin(团支部管理员) / student(学生)
        st.session_state.users = {
            "superadmin": {
                "name": "系统管理员",
                "password": "admin123",
                "role": "super_admin",
                "belong_class": "全部"
            },
            "admin1": {
                "name": "软工1班管理员",
                "password": "123456",
                "role": "class_admin",
                "belong_class": "24级软工1班团支部"
            },
            "student1": {
                "name": "张三",
                "password": "123456",
                "role": "student",
                "belong_class": "24级软工1班团支部"
            },
            "student2": {
                "name": "李四",
                "password": "123456",
                "role": "student",
                "belong_class": "24级软工1班团支部"
            }
        }

    if "score_records" not in st.session_state:
        # 加分记录表：每条记录包含学生信息、分数类型、加分值、事由、时间
        st.session_state.score_records = []

# ==========================
# 工具函数：计算学生学分汇总
# ==========================
def calc_score_summary():
    summary = {}
    for record in st.session_state.score_records:
        stu_id = record["学号"]
        if stu_id not in summary:
            summary[stu_id] = {
                "姓名": record["姓名"],
                "学号": record["学号"],
                "所属班级": record["所属班级"],
                **{t: 0.0 for t in SCORE_TYPES},
                "最终总学分": 0.0
            }
        summary[stu_id][record["分数类型"]] += record["加分值"]
        summary[stu_id]["最终总学分"] += record["加分值"]
    return list(summary.values())

# ==========================
# 登录页面
# ==========================
def login_page():
    st.markdown("<h1 style='text-align: center;'>🏫 第二课堂学分管理系统</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>书院团支部量化学分管理平台</p>", unsafe_allow_html=True)
    st.divider()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("用户登录")
        username = st.text_input("用户名")
        password = st.text_input("密码", type="password")
        
        if st.button("登录", type="primary", use_container_width=True):
            users = st.session_state.users
            if username in users:
                user = users[username]
                if user["password"] == password:
                    st.session_state.login_status = True
                    st.session_state.username = username
                    st.session_state.user_name = user["name"]
                    st.session_state.user_role = user["role"]
                    st.session_state.belong_class = user["belong_class"]
                    st.success("登录成功，正在跳转...")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("密码错误")
            else:
                st.error("用户名不存在")

# ==========================
# 退出登录
# ==========================
def logout():
    for key in ["login_status", "username", "user_name", "user_role", "belong_class"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

# ==========================
# 1. 超级管理员：用户管理页面
# ==========================
def user_manage_page():
    st.title("👥 用户权限管理")
    st.caption("新增、编辑、删除用户，分配管辖班级与角色权限")
    st.divider()

    # 新增用户区域
    with st.expander("➕ 新增用户", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            new_username = st.text_input("用户名（登录用）")
            new_name = st.text_input("真实姓名")
            new_password = st.text_input("初始密码", type="password")
        with col2:
            new_role = st.selectbox("用户角色", ["class_admin(团支部管理员)", "student(学生)"])
            new_class = st.selectbox("所属/管辖班级", CLASS_LIST)
        
        if st.button("确认新增", type="primary"):
            if not new_username or not new_name or not new_password:
                st.error("请填写完整信息")
            elif new_username in st.session_state.users:
                st.error("用户名已存在")
            else:
                role_key = new_role.split("(")[0]
                st.session_state.users[new_username] = {
                    "name": new_name,
                    "password": new_password,
                    "role": role_key,
                    "belong_class": new_class
                }
                st.success("用户新增成功")
                st.rerun()

    # 用户列表
    st.subheader("📋 全部用户列表")
    users = st.session_state.users
    user_list = []
    for uname, info in users.items():
        role_text = {
            "super_admin": "超级管理员",
            "class_admin": "团支部管理员",
            "student": "学生"
        }[info["role"]]
        user_list.append({
            "用户名": uname,
            "姓名": info["name"],
            "角色": role_text,
            "所属/管辖班级": info["belong_class"]
        })
    
    st.dataframe(user_list, use_container_width=True, hide_index=True)

    # 编辑/删除用户
    st.divider()
    st.subheader("✏️ 编辑/删除用户")
    edit_username = st.selectbox("选择要操作的用户名", [u for u in users.keys() if u != "superadmin"])
    
    if edit_username:
        user_info = users[edit_username]
        col1, col2 = st.columns(2)
        with col1:
            edit_name = st.text_input("修改姓名", value=user_info["name"])
            edit_password = st.text_input("修改密码（不填则不变）", type="password")
        with col2:
            edit_role = st.selectbox(
                "修改角色",
                ["class_admin", "student"],
                index=0 if user_info["role"] == "class_admin" else 1
            )
            edit_class = st.selectbox(
                "修改所属/管辖班级",
                CLASS_LIST,
                index=CLASS_LIST.index(user_info["belong_class"]) if user_info["belong_class"] in CLASS_LIST else 0
            )
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("保存修改", use_container_width=True):
                st.session_state.users[edit_username]["name"] = edit_name
                if edit_password:
                    st.session_state.users[edit_username]["password"] = edit_password
                st.session_state.users[edit_username]["role"] = edit_role
                st.session_state.users[edit_username]["belong_class"] = edit_class
                st.success("修改成功")
                st.rerun()
        with col_btn2:
            if st.button("删除该用户", use_container_width=True, type="secondary"):
                del st.session_state.users[edit_username]
                st.success("删除成功")
                st.rerun()

# ==========================
# 2. 学分录入页面
# ==========================
def score_input_page():
    st.title("✏️ 学分录入")
    st.caption("选择学生与分数类型，系统自动累计分类总分与最终总学分")
    st.divider()

    user_role = st.session_state.user_role
    belong_class = st.session_state.belong_class

    # 权限控制：班级管理员只能选本班学生
    if user_role == "super_admin":
        select_class = st.selectbox("选择班级", CLASS_LIST)
    else:
        select_class = belong_class
        st.info(f"您当前仅可操作：{belong_class}")

    # 筛选出对应班级的学生
    class_students = [
        (uname, info["name"])
        for uname, info in st.session_state.users.items()
        if info["role"] == "student" and info["belong_class"] == select_class
    ]

    if not class_students:
        st.warning("该班级暂无学生账号，请先在「用户管理」中添加")
        return

    col1, col2 = st.columns(2)
    with col1:
        student_option = st.selectbox("选择学生", [f"{name}（{uname}）" for uname, name in class_students])
        stu_id = student_option.split("（")[1].replace("）", "")
        stu_name = st.session_state.users[stu_id]["name"]
        score_type = st.selectbox("分数类型", SCORE_TYPES)
    with col2:
        score_value = st.number_input("加分值", min_value=0.0, step=0.5, value=0.5)
        reason = st.text_input("加分事由（如：参加团日活动）")

    if st.button("确认加分", type="primary", use_container_width=True):
        if score_value <= 0:
            st.error("加分值必须大于0")
        else:
            st.session_state.score_records.append({
                "姓名": stu_name,
                "学号": stu_id,
                "所属班级": select_class,
                "分数类型": score_type,
                "加分值": score_value,
                "加分事由": reason,
                "录入人": st.session_state.user_name,
                "录入时间": time.strftime("%Y-%m-%d %H:%M")
            })
            st.success(f"已为 {stu_name} 成功加 {score_value} 分")
            st.rerun()

# ==========================
# 3. 学分总览页面（带筛选）
# ==========================
def score_summary_page():
    st.title("📊 学分总览")
    st.caption("按班级筛选，自动展示各分类总分与最终总学分")
    st.divider()

    user_role = st.session_state.user_role
    belong_class = st.session_state.belong_class
    summary = calc_score_summary()

    # 筛选区域
    col1, col2, col3 = st.columns(3)
    with col1:
        if user_role == "super_admin":
            filter_class = st.selectbox("筛选班级", ["全部"] + CLASS_LIST)
        else:
            filter_class = belong_class
            st.info(f"仅展示：{belong_class}")
    with col2:
        search_name = st.text_input("搜索姓名/学号")
    with col3:
        st.write("")
        st.write("")
        st.caption(f"共 {len(summary)} 名学生")

    # 应用筛选
    filtered = summary
    if filter_class != "全部":
        filtered = [item for item in filtered if item["所属班级"] == filter_class]
    if search_name:
        filtered = [item for item in filtered if search_name in item["姓名"] or search_name in item["学号"]]

    if filtered:
        # 调整列顺序：基本信息在前，分类总分在中间，最终总分在最后
        show_columns = ["姓名", "学号", "所属班级"] + SCORE_TYPES + ["最终总学分"]
        st.dataframe(filtered, use_container_width=True, hide_index=True, column_order=show_columns)
    else:
        st.info("暂无符合条件的数据")

# ==========================
# 4. 加分记录明细页面
# ==========================
def score_records_page():
    st.title("📝 加分记录明细")
    st.divider()

    user_role = st.session_state.user_role
    belong_class = st.session_state.belong_class
    records = st.session_state.score_records

    # 筛选
    col1, col2, col3 = st.columns(3)
    with col1:
        if user_role == "super_admin":
            filter_class = st.selectbox("筛选班级", ["全部"] + CLASS_LIST)
        else:
            filter_class = belong_class
    with col2:
        filter_type = st.selectbox("筛选分数类型", ["全部"] + SCORE_TYPES)
    with col3:
        search_name = st.text_input("搜索学生姓名")

    # 应用筛选
    filtered = records
    if filter_class != "全部":
        filtered = [r for r in filtered if r["所属班级"] == filter_class]
    if filter_type != "全部":
        filtered = [r for r in filtered if r["分数类型"] == filter_type]
    if search_name:
        filtered = [r for r in filtered if search_name in r["姓名"]]

    if filtered:
        st.dataframe(filtered, use_container_width=True, hide_index=True)
        st.caption(f"共 {len(filtered)} 条加分记录")
    else:
        st.info("暂无加分记录")

# ==========================
# 5. 学生个人页面
# ==========================
def student_my_page():
    st.title("🔍 我的第二课堂学分")
    st.divider()

    my_id = st.session_state.username
    my_name = st.session_state.user_name
    my_class = st.session_state.belong_class

    st.subheader("📈 学分汇总")
    summary = calc_score_summary()
    my_summary = [item for item in summary if item["学号"] == my_id]
    
    if my_summary:
        show_columns = ["姓名", "学号", "所属班级"] + SCORE_TYPES + ["最终总学分"]
        st.dataframe(my_summary, use_container_width=True, hide_index=True, column_order=show_columns)
        st.metric("累计总学分", my_summary[0]["最终总学分"])
    else:
        st.info("暂无加分记录")

    st.divider()
    st.subheader("📝 我的加分明细")
    my_records = [r for r in st.session_state.score_records if r["学号"] == my_id]
    if my_records:
        st.dataframe(my_records, use_container_width=True, hide_index=True)
    else:
        st.info("暂无加分记录")

# ==========================
# 主页面入口
# ==========================
def main_page():
    # 侧边栏
    with st.sidebar:
        st.subheader(f"👤 {st.session_state.user_name}")
        role_text = {
            "super_admin": "超级管理员",
            "class_admin": "团支部管理员",
            "student": "学生"
        }[st.session_state.user_role]
        st.caption(f"身份：{role_text}")
        if st.session_state.user_role != "super_admin":
            st.caption(f"班级：{st.session_state.belong_class}")
        st.divider()

        # 按角色显示菜单
        role = st.session_state.user_role
        if role == "super_admin":
            menu = st.radio("功能菜单", [
                "用户权限管理",
                "学分录入",
                "学分总览",
                "加分记录明细"
            ])
        elif role == "class_admin":
            menu = st.radio("功能菜单", [
                "学分录入",
                "学分总览",
                "加分记录明细"
            ])
        else:
            menu = st.radio("功能菜单", [
                "我的学分"
            ])
        
        st.divider()
        if st.button("退出登录", use_container_width=True):
            logout()

    # 页面路由
    if menu == "用户权限管理":
        user_manage_page()
    elif menu == "学分录入":
        score_input_page()
    elif menu == "学分总览":
        score_summary_page()
    elif menu == "加分记录明细":
        score_records_page()
    elif menu == "我的学分":
        student_my_page()

# ==========================
# 程序入口
# ==========================
if __name__ == "__main__":
    st.set_page_config(page_title="第二课堂学分系统", layout="wide")
    init_data()

    if "login_status" not in st.session_state or not st.session_state.login_status:
        login_page()
    else:
        main_page()
