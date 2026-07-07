import streamlit as st
import time

# ==========================
# 基础配置：团支部列表
# ==========================
CLASS_LIST = [
    "24级软工1班团支部",
    "24级软工2班团支部",
    "24级计科1班团支部",
    "24级计科2班团支部"
]

# ==========================
# 核心配置：加分/扣分两大模块 + 一级分类 + 二级小项
# ==========================
ADD_SCORE_CONFIG = {
    "思想政治与综合素养类": [
        {"name": "思想品德类荣誉（国家级）", "default": 30.0, "max": 30.0, "min": 0.0},
        {"name": "思想品德类荣誉（省级）", "default": 20.0, "max": 30.0, "min": 0.0},
        {"name": "思想品德类荣誉（校级）", "default": 10.0, "max": 30.0, "min": 0.0},
        {"name": "好人好事表彰（国家级）", "default": 20.0, "max": 30.0, "min": 0.0},
        {"name": "好人好事表彰（省级）", "default": 15.0, "max": 30.0, "min": 0.0},
        {"name": "好人好事表彰（校级）", "default": 10.0, "max": 30.0, "min": 0.0},
        {"name": "网络理论学习/知识竞赛", "default": 0.5, "max": 10.0, "min": 0.0},
        {"name": "青马工程/国学班（国家级）", "default": 30.0, "max": 30.0, "min": 0.0},
        {"name": "青马工程/国学班（省级）", "default": 20.0, "max": 30.0, "min": 0.0},
        {"name": "青马工程/铁军先锋团（校级）", "default": 12.0, "max": 30.0, "min": 0.0},
        {"name": "青马工程/骨干班（院级）", "default": 8.0, "max": 30.0, "min": 0.0},
        {"name": "军训标兵（校级）", "default": 8.0, "max": 8.0, "min": 0.0},
        {"name": "军训标兵（院级）", "default": 5.0, "max": 8.0, "min": 0.0},
        {"name": "主题团日/班会（发言）", "default": 2.0, "max": 15.0, "min": 0.0},
        {"name": "主题团日/班会（观众）", "default": 0.5, "max": 15.0, "min": 0.0},
        {"name": "个人综合性荣誉（国家级）", "default": 25.0, "max": 25.0, "min": 0.0},
        {"name": "个人综合性荣誉（省级）", "default": 15.0, "max": 25.0, "min": 0.0},
        {"name": "个人综合性荣誉（校级）", "default": 8.0, "max": 25.0, "min": 0.0},
        {"name": "个人综合性荣誉（院级）", "default": 5.0, "max": 25.0, "min": 0.0},
        {"name": "集体综合性荣誉（负责人·国家级）", "default": 20.0, "max": 20.0, "min": 0.0},
        {"name": "集体综合性荣誉（成员·国家级）", "default": 10.0, "max": 20.0, "min": 0.0},
        {"name": "集体综合性荣誉（负责人·省级）", "default": 10.0, "max": 20.0, "min": 0.0},
        {"name": "集体综合性荣誉（成员·省级）", "default": 5.0, "max": 20.0, "min": 0.0},
        {"name": "其他（自定义）", "default": 1.0, "max": 100.0, "min": 0.0}
    ],
    "社会实践与志愿服务类": [
        {"name": "三下乡重点队（国家级）", "default": 12.0, "max": 25.0, "min": 0.0},
        {"name": "三下乡重点队（省级）", "default": 9.0, "max": 25.0, "min": 0.0},
        {"name": "三下乡重点队（校级）", "default": 5.0, "max": 25.0, "min": 0.0},
        {"name": "三下乡普通实践队", "default": 2.0, "max": 25.0, "min": 0.0},
        {"name": "返家乡实践（表彰·省级）", "default": 12.0, "max": 20.0, "min": 0.0},
        {"name": "返家乡实践（表彰·校级）", "default": 8.0, "max": 20.0, "min": 0.0},
        {"name": "返家乡实践（参与）", "default": 1.0, "max": 5.0, "min": 0.0},
        {"name": "调研报告（团队）", "default": 5.0, "max": 15.0, "min": 0.0},
        {"name": "调研报告（个人）", "default": 10.0, "max": 15.0, "min": 0.0},
        {"name": "校内志愿活动（2小时）", "default": 1.0, "max": 30.0, "min": 0.0},
        {"name": "无偿献血", "default": 2.0, "max": 30.0, "min": 0.0},
        {"name": "朋辈导师（优秀）", "default": 10.0, "max": 10.0, "min": 0.0},
        {"name": "朋辈导师（良好）", "default": 8.0, "max": 10.0, "min": 0.0},
        {"name": "朋辈导师（合格）", "default": 6.0, "max": 10.0, "min": 0.0},
        {"name": "学生干部（优秀）", "default": 18.0, "max": 30.0, "min": 0.0},
        {"name": "学生干部（良好）", "default": 13.0, "max": 30.0, "min": 0.0},
        {"name": "学生干部（合格）", "default": 8.0, "max": 30.0, "min": 0.0},
        {"name": "信息员（优秀）", "default": 8.0, "max": 10.0, "min": 0.0},
        {"name": "信息员（良好）", "default": 7.0, "max": 10.0, "min": 0.0},
        {"name": "信息员（合格）", "default": 6.0, "max": 10.0, "min": 0.0},
        {"name": "其他（自定义）", "default": 1.0, "max": 100.0, "min": 0.0}
    ],
    "科研创新与学科竞赛类": [
        {"name": "普刊学术论文（一作）", "default": 10.0, "max": 30.0, "min": 0.0},
        {"name": "核心期刊论文（一作）", "default": 30.0, "max": 100.0, "min": 0.0},
        {"name": "挑战杯/互联网+（国奖）", "default": 40.0, "max": 100.0, "min": 0.0},
        {"name": "挑战杯/互联网+（省奖）", "default": 25.0, "max": 100.0, "min": 0.0},
        {"name": "挑战杯/互联网+（校奖）", "default": 12.0, "max": 30.0, "min": 0.0},
        {"name": "大创项目（国家级结项）", "default": 30.0, "max": 30.0, "min": 0.0},
        {"name": "大创项目（省级结项）", "default": 20.0, "max": 30.0, "min": 0.0},
        {"name": "大创项目（校级结项）", "default": 10.0, "max": 30.0, "min": 0.0},
        {"name": "发明专利（一作）", "default": 30.0, "max": 100.0, "min": 0.0},
        {"name": "实用新型专利（一作）", "default": 20.0, "max": 100.0, "min": 0.0},
        {"name": "软件著作权（一作）", "default": 20.0, "max": 100.0, "min": 0.0},
        {"name": "学科竞赛（国家级A类）", "default": 40.0, "max": 100.0, "min": 0.0},
        {"name": "学科竞赛（省级A类）", "default": 25.0, "max": 100.0, "min": 0.0},
        {"name": "学科竞赛（校级）", "default": 8.0, "max": 40.0, "min": 0.0},
        {"name": "计算机二级/英语四六级证书", "default": 8.0, "max": 50.0, "min": 0.0},
        {"name": "职业资格证书（高级）", "default": 20.0, "max": 50.0, "min": 0.0},
        {"name": "创办企业（法人）", "default": 15.0, "max": 30.0, "min": 0.0},
        {"name": "创业培训合格证书", "default": 5.0, "max": 15.0, "min": 0.0},
        {"name": "其他（自定义）", "default": 1.0, "max": 100.0, "min": 0.0}
    ],
    "文体艺术与身心发展类": [
        {"name": "非思政类专题讲座（发言）", "default": 2.0, "max": 10.0, "min": 0.0},
        {"name": "非思政类专题讲座（观众）", "default": 0.5, "max": 10.0, "min": 0.0},
        {"name": "文艺比赛（国家级）", "default": 25.0, "max": 30.0, "min": 0.0},
        {"name": "文艺比赛（省级）", "default": 12.0, "max": 30.0, "min": 0.0},
        {"name": "文艺比赛（校级）", "default": 8.0, "max": 30.0, "min": 0.0},
        {"name": "校级文艺演出（演职人员）", "default": 5.0, "max": 20.0, "min": 0.0},
        {"name": "书院文艺活动（演职人员）", "default": 3.0, "max": 20.0, "min": 0.0},
        {"name": "体育比赛（国家级）", "default": 25.0, "max": 100.0, "min": 0.0},
        {"name": "体育比赛（省级）", "default": 12.0, "max": 50.0, "min": 0.0},
        {"name": "体育比赛（校级）", "default": 6.0, "max": 30.0, "min": 0.0},
        {"name": "运动会/篮球赛（参与）", "default": 3.0, "max": 30.0, "min": 0.0},
        {"name": "趣味体育活动", "default": 1.0, "max": 10.0, "min": 0.0},
        {"name": "心理类竞赛（校级）", "default": 8.0, "max": 30.0, "min": 0.0},
        {"name": "演讲/辩论/征文比赛（校级）", "default": 6.0, "max": 30.0, "min": 0.0},
        {"name": "社团活动参与", "default": 0.5, "max": 10.0, "min": 0.0},
        {"name": "新闻宣传（校级媒体）", "default": 2.0, "max": 30.0, "min": 0.0},
        {"name": "新闻宣传（省级媒体）", "default": 5.0, "max": 30.0, "min": 0.0},
        {"name": "其他（自定义）", "default": 1.0, "max": 100.0, "min": 0.0}
    ]
}

DEDUCT_SCORE_CONFIG = {
    "思想政治表现": [
        {"name": "未完成理论学习任务", "default": -2.0, "max": 0.0, "min": -10.0},
        {"name": "集体活动无故不到", "default": -3.0, "max": 0.0, "min": -10.0},
        {"name": "集体活动迟到/早退", "default": -1.0, "max": 0.0, "min": -10.0},
        {"name": "学生干部工作弄虚作假", "default": -5.0, "max": 0.0, "min": -30.0},
        {"name": "违反民族宗教政策行为", "default": -20.0, "max": 0.0, "min": -100.0},
        {"name": "其他（自定义）", "default": -1.0, "max": 0.0, "min": -100.0}
    ],
    "文明行为养成": [
        {"name": "公开发表不当言论", "default": -10.0, "max": 0.0, "min": -15.0},
        {"name": "公共场所不文明行为", "default": -5.0, "max": 0.0, "min": -10.0},
        {"name": "宿舍卫生检查不合格", "default": -1.0, "max": 0.0, "min": -10.0},
        {"name": "阻挠宿舍卫生检查", "default": -3.0, "max": 0.0, "min": -5.0},
        {"name": "教室卫生未完成值日", "default": -1.0, "max": 0.0, "min": -5.0},
        {"name": "其他（自定义）", "default": -1.0, "max": 0.0, "min": -100.0}
    ],
    "安全行为管理": [
        {"name": "违反治安管理处罚法", "default": -50.0, "max": 0.0, "min": -100.0},
        {"name": "校园欺凌", "default": -30.0, "max": 0.0, "min": -50.0},
        {"name": "参与打架斗殴", "default": -20.0, "max": 0.0, "min": -50.0},
        {"name": "校内酗酒", "default": -20.0, "max": 0.0, "min": -50.0},
        {"name": "违规使用大功率电器", "default": -15.0, "max": 0.0, "min": -30.0},
        {"name": "私拉乱接电源", "default": -10.0, "max": 0.0, "min": -30.0},
        {"name": "损坏消防设施", "default": -20.0, "max": 0.0, "min": -50.0},
        {"name": "不参加消防培训演训", "default": -5.0, "max": 0.0, "min": -10.0},
        {"name": "其他（自定义）", "default": -1.0, "max": 0.0, "min": -100.0}
    ],
    "校规校纪遵守": [
        {"name": "教学考勤迟到/早退", "default": -1.0, "max": 0.0, "min": -20.0},
        {"name": "教学考勤旷课", "default": -3.0, "max": 0.0, "min": -50.0},
        {"name": "周末晚点名无故不到", "default": -1.0, "max": 0.0, "min": -10.0},
        {"name": "宿舍晚归", "default": -3.0, "max": 0.0, "min": -20.0},
        {"name": "宿舍夜不归宿", "default": -10.0, "max": 0.0, "min": -20.0},
        {"name": "会议活动迟到/早退", "default": -1.0, "max": 0.0, "min": -10.0},
        {"name": "会议活动缺勤", "default": -3.0, "max": 0.0, "min": -10.0},
        {"name": "书院通报批评", "default": -8.0, "max": 0.0, "min": -20.0},
        {"name": "学校通报批评", "default": -10.0, "max": 0.0, "min": -30.0},
        {"name": "警告处分", "default": -15.0, "max": 0.0, "min": -50.0},
        {"name": "严重警告处分", "default": -20.0, "max": 0.0, "min": -50.0},
        {"name": "记过处分", "default": -25.0, "max": 0.0, "min": -50.0},
        {"name": "留校察看处分", "default": -50.0, "max": 0.0, "min": -100.0},
        {"name": "其他（自定义）", "default": -1.0, "max": 0.0, "min": -100.0}
    ]
}

ADD_CATEGORIES = list(ADD_SCORE_CONFIG.keys())
DEDUCT_CATEGORIES = list(DEDUCT_SCORE_CONFIG.keys())

# ==========================
# 初始化系统数据
# ==========================
def init_data():
    if "users" not in st.session_state:
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
            },
            "student3": {
                "name": "王五",
                "password": "123456",
                "role": "student",
                "belong_class": "24级软工1班团支部"
            }
        }

    if "score_records" not in st.session_state:
        st.session_state.score_records = []
    
    # 初始化提交确认状态
    if "confirm_submit" not in st.session_state:
        st.session_state.confirm_submit = False
    if "pending_data" not in st.session_state:
        st.session_state.pending_data = None

# ==========================
# 工具函数
# ==========================
def get_student_item_total(stu_id, top_type, category, item_name):
    total = 0.0
    for r in st.session_state.score_records:
        if (r["学号"] == stu_id 
            and r["操作类型"] == top_type 
            and r["一级分类"] == category 
            and r["小项名称"] == item_name):
            total += r["分数值"]
    return total

def calc_score_summary():
    summary = {}
    for record in st.session_state.score_records:
        stu_id = record["学号"]
        if stu_id not in summary:
            summary[stu_id] = {
                "姓名": record["姓名"],
                "学号": record["学号"],
                "所属班级": record["所属班级"],
                **{c: 0.0 for c in ADD_CATEGORIES},
                "加分合计": 0.0,
                **{c: 0.0 for c in DEDUCT_CATEGORIES},
                "扣分合计": 0.0,
                "最终净学分": 0.0
            }
        if record["操作类型"] == "加分":
            summary[stu_id][record["一级分类"]] += record["分数值"]
            summary[stu_id]["加分合计"] += record["分数值"]
        else:
            summary[stu_id][record["一级分类"]] += record["分数值"]
            summary[stu_id]["扣分合计"] += record["分数值"]
        summary[stu_id]["最终净学分"] = summary[stu_id]["加分合计"] + summary[stu_id]["扣分合计"]
    return list(summary.values())

# ==========================
# 登录页面
# ==========================
def login_page():
    st.markdown("<h1 style='text-align: center;'>🏫 第二课堂学分管理系统</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>洛阳师范学院 · 书院综合素质量化平台</p>", unsafe_allow_html=True)
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
    for key in ["login_status", "username", "user_name", "user_role", "belong_class", "confirm_submit", "pending_data"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

# ==========================
# 1. 用户权限管理
# ==========================
def user_manage_page():
    st.title("👥 用户权限管理")
    st.caption("新增、编辑、删除用户，分配管辖班级与角色权限")
    st.divider()

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
# 2. 学分录入（修复版）
# ==========================
def score_input_page():
    st.title("✏️ 学分录入")
    st.caption("加分/扣分双模块，三级分类联动，必填项校验，超限强制提醒")
    st.divider()

    user_role = st.session_state.user_role
    belong_class = st.session_state.belong_class

    # 班级权限控制
    if user_role == "super_admin":
        select_class = st.selectbox("选择操作班级", ["请选择班级"] + CLASS_LIST)
    else:
        select_class = belong_class
        st.info(f"您当前仅可操作：{belong_class}")

    # 班级未选中时不显示后续内容
    if select_class == "请选择班级":
        st.info("请先选择操作班级")
        return

    # 筛选对应班级学生
    class_students = [
        (uname, info["name"])
        for uname, info in st.session_state.users.items()
        if info["role"] == "student" and info["belong_class"] == select_class
    ]

    if not class_students:
        st.warning("该班级暂无学生账号，请先在「用户管理」中添加")
        return

    # ========== 三级分类选择（默认全为空） ==========
    col1, col2, col3 = st.columns(3)
    with col1:
        top_type = st.selectbox("操作类型", ["请选择操作类型", "加分", "扣分"])
        if top_type == "请选择操作类型":
            st.stop()
        config = ADD_SCORE_CONFIG if top_type == "加分" else DEDUCT_SCORE_CONFIG
        category_list = list(config.keys())
    
    with col2:
        selected_category = st.selectbox("选择一级分类", ["请选择一级分类"] + category_list)
        if selected_category == "请选择一级分类":
            st.stop()
        item_list = config[selected_category]
        item_names = [item["name"] for item in item_list]
    
    with col3:
        selected_item_name = st.selectbox("选择具体项目", ["请选择具体项目"] + item_names)
        if selected_item_name == "请选择具体项目":
            st.stop()
        selected_item = next(item for item in item_list if item["name"] == selected_item_name)
        default_score = selected_item["default"]
        max_score = selected_item["max"]
        min_score = selected_item["min"]

    # 自定义项目输入框
    custom_item_name = ""
    if selected_item_name == "其他（自定义）":
        custom_item_name = st.text_input("* 请输入自定义项目名称", placeholder="例如：班级临时任务加分")

    # ========== 分值与事由（事由必填） ==========
    col4, col5 = st.columns(2)
    with col4:
        # 输入框强制限制单次输入范围
        score_value = st.number_input(
            f"分数值（范围 {min_score} ~ {max_score}）",
            min_value=float(min_score),
            max_value=float(max_score),
            value=float(default_score),
            step=0.5,
            format="%.1f"
        )
    with col5:
        reason = st.text_input("* 事由说明（必填）", placeholder="例如：2026年3月主题团日活动参与")

    # ========== 批量选择学生 ==========
    st.subheader("👥 选择操作学生（可多选）")
    student_options = [f"{name}（{uname}）" for uname, name in class_students]
    selected_students = st.multiselect(
        "勾选要操作的学生",
        options=student_options
    )

    # ========== 预校验 + 确认提交逻辑 ==========
    # 重置确认状态
    if not st.session_state.confirm_submit:
        if st.button("预校验并提交", type="primary", use_container_width=True):
            # 1. 必填项校验
            if not selected_students:
                st.error("请至少选择一名学生")
            elif not reason.strip():
                st.error("事由说明为必填项，请填写后再提交")
            elif selected_item_name == "其他（自定义）" and not custom_item_name.strip():
                st.error("自定义项目请填写项目名称")
            else:
                # 2. 计算超限情况
                final_item_name = custom_item_name.strip() if selected_item_name == "其他（自定义）" else selected_item_name
                warning_list = []
                
                for opt in selected_students:
                    stu_id = opt.split("（")[1].replace("）", "")
                    stu_name = st.session_state.users[stu_id]["name"]
                    current_total = get_student_item_total(stu_id, top_type, selected_category, final_item_name)
                    new_total = current_total + score_value

                    if top_type == "加分" and new_total > max_score:
                        warning_list.append(f"⚠️ {stu_name}：「{final_item_name}」上限 {max_score} 分，提交后累计 {new_total:.1f} 分，已超出上限")
                    elif top_type == "扣分" and new_total < min_score:
                        warning_list.append(f"⚠️ {stu_name}：「{final_item_name}」下限 {min_score} 分，提交后累计 {new_total:.1f} 分，已超出下限")

                # 3. 缓存待提交数据
                st.session_state.pending_data = {
                    "top_type": top_type,
                    "category": selected_category,
                    "item_name": final_item_name,
                    "score_value": score_value,
                    "reason": reason.strip(),
                    "select_class": select_class,
                    "selected_students": selected_students
                }

                # 4. 显示警告并进入确认状态
                if warning_list:
                    st.warning("以下学生已超出该项目分数限制（仅提醒，确认后仍可提交）：\n" + "\n".join(warning_list))
                st.session_state.confirm_submit = True
                st.rerun()

    # 确认提交阶段
    else:
        st.info("已完成校验，确认无误后点击下方按钮完成提交")
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("确认提交", type="primary", use_container_width=True):
                data = st.session_state.pending_data
                success_count = 0

                for opt in data["selected_students"]:
                    stu_id = opt.split("（")[1].replace("）", "")
                    stu_name = st.session_state.users[stu_id]["name"]
                    
                    st.session_state.score_records.append({
                        "姓名": stu_name,
                        "学号": stu_id,
                        "所属班级": data["select_class"],
                        "操作类型": data["top_type"],
                        "一级分类": data["category"],
                        "小项名称": data["item_name"],
                        "分数值": data["score_value"],
                        "事由": data["reason"],
                        "录入人": st.session_state.user_name,
                        "录入时间": time.strftime("%Y-%m-%d %H:%M")
                    })
                    success_count += 1

                st.success(f"操作成功，已为 {success_count} 名学生完成{data['top_type']}")
                # 重置状态
                st.session_state.confirm_submit = False
                st.session_state.pending_data = None
                st.rerun()
        
        with col_btn2:
            if st.button("取消返回修改", use_container_width=True):
                st.session_state.confirm_submit = False
                st.session_state.pending_data = None
                st.rerun()

# ==========================
# 3. 学分总览
# ==========================
def score_summary_page():
    st.title("📊 学分总览")
    st.caption("按班级筛选，自动展示各分类总分、加扣分合计与最终净学分")
    st.divider()

    user_role = st.session_state.user_role
    belong_class = st.session_state.belong_class
    summary = calc_score_summary()

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

    filtered = summary
    if filter_class != "全部":
        filtered = [item for item in filtered if item["所属班级"] == filter_class]
    if search_name:
        filtered = [item for item in filtered if search_name in item["姓名"] or search_name in item["学号"]]

    if filtered:
        show_columns = ["姓名", "学号", "所属班级"] + ADD_CATEGORIES + ["加分合计"] + DEDUCT_CATEGORIES + ["扣分合计", "最终净学分"]
        st.dataframe(filtered, use_container_width=True, hide_index=True, column_order=show_columns)
    else:
        st.info("暂无符合条件的数据")

# ==========================
# 4. 加扣分记录明细
# ==========================
def score_records_page():
    st.title("📝 加扣分记录明细")
    st.divider()

    user_role = st.session_state.user_role
    belong_class = st.session_state.belong_class
    records = st.session_state.score_records

    col1, col2, col3 = st.columns(3)
    with col1:
        if user_role == "super_admin":
            filter_class = st.selectbox("筛选班级", ["全部"] + CLASS_LIST)
        else:
            filter_class = belong_class
    with col2:
        filter_type = st.selectbox("筛选操作类型", ["全部", "加分", "扣分"])
    with col3:
        search_name = st.text_input("搜索学生姓名")

    filtered = records
    if filter_class != "全部":
        filtered = [r for r in filtered if r["所属班级"] == filter_class]
    if filter_type != "全部":
        filtered = [r for r in filtered if r["操作类型"] == filter_type]
    if search_name:
        filtered = [r for r in filtered if search_name in r["姓名"]]

    if filtered:
        st.dataframe(filtered, use_container_width=True, hide_index=True)
        st.caption(f"共 {len(filtered)} 条记录")
    else:
        st.info("暂无记录")

# ==========================
# 5. 学生个人页面
# ==========================
def student_my_page():
    st.title("🔍 我的第二课堂学分")
    st.divider()

    my_id = st.session_state.username
    my_name = st.session_state.user_name

    st.subheader("📈 学分汇总")
    summary = calc_score_summary()
    my_summary = [item for item in summary if item["学号"] == my_id]
    
    if my_summary:
        show_columns = ["姓名", "学号", "所属班级"] + ADD_CATEGORIES + ["加分合计"] + DEDUCT_CATEGORIES + ["扣分合计", "最终净学分"]
        st.dataframe(my_summary, use_container_width=True, hide_index=True, column_order=show_columns)
        st.metric("最终净学分", my_summary[0]["最终净学分"])
    else:
        st.info("暂无加扣分记录")

    st.divider()
    st.subheader("📝 我的加扣分明细")
    my_records = [r for r in st.session_state.score_records if r["学号"] == my_id]
    if my_records:
        st.dataframe(my_records, use_container_width=True, hide_index=True)
    else:
        st.info("暂无记录")

# ==========================
# 主页面入口
# ==========================
def main_page():
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

        role = st.session_state.user_role
        if role == "super_admin":
            menu = st.radio("功能菜单", [
                "用户权限管理",
                "学分录入",
                "学分总览",
                "加扣分记录明细"
            ])
        elif role == "class_admin":
            menu = st.radio("功能菜单", [
                "学分录入",
                "学分总览",
                "加扣分记录明细"
            ])
        else:
            menu = st.radio("功能菜单", [
                "我的学分"
            ])
        
        st.divider()
        if st.button("退出登录", use_container_width=True):
            logout()

    if menu == "用户权限管理":
        user_manage_page()
    elif menu == "学分录入":
        score_input_page()
    elif menu == "学分总览":
        score_summary_page()
    elif menu == "加扣分记录明细":
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
