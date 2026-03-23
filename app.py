# ============================================================
# TradeReply AI / 外贸客服 Agent
# 本地规则版 MVP — 随时可扩展为真实 API 版
# ============================================================
# 未来接 API 的位置已用 [API HOOK] 标注
# ============================================================

import streamlit as st
import time
import json
from datetime import datetime

# ── 页面基础配置 ──────────────────────────────────────────────
st.set_page_config(
    page_title="TradeReply AI · 外贸客服Agent",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── 全局 CSS（黑白灰高级感） ───────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

/* ── Reset & Base ── */
html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
}
.stApp {
    background: #0d0d0d;
    color: #e8e8e8;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header {visibility: hidden;}
.block-container {
    padding: 2.5rem 3rem 4rem 3rem;
    max-width: 1100px;
}

/* ── Title area ── */
.tr-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 2rem;
    font-weight: 600;
    color: #ffffff;
    letter-spacing: -0.5px;
    margin-bottom: 0;
}
.tr-subtitle {
    font-size: 0.82rem;
    color: #555;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 4px;
    margin-bottom: 2.5rem;
}
.tr-divider {
    border: none;
    border-top: 1px solid #222;
    margin: 1.8rem 0;
}

/* ── Cards ── */
.tr-card {
    background: #141414;
    border: 1px solid #252525;
    border-radius: 8px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
}
.tr-card-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    color: #4a4a4a;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    margin-bottom: 0.7rem;
}

/* ── Intent badge ── */
.tr-intent-badge {
    display: inline-block;
    background: #1e1e1e;
    border: 1px solid #333;
    border-radius: 4px;
    padding: 4px 12px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    color: #c8c8c8;
    margin-right: 8px;
    margin-bottom: 6px;
}
.tr-intent-badge.primary {
    border-color: #888;
    color: #fff;
    background: #1f1f1f;
}

/* ── Reply box ── */
.tr-reply-box {
    background: #111;
    border: 1px solid #2a2a2a;
    border-left: 3px solid #e0e0e0;
    border-radius: 6px;
    padding: 1.2rem 1.4rem;
    font-size: 0.92rem;
    line-height: 1.75;
    color: #ddd;
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── Follow-up tips ── */
.tr-tip {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 8px 0;
    border-bottom: 1px solid #1c1c1c;
    font-size: 0.88rem;
    color: #bbb;
}
.tr-tip:last-child { border-bottom: none; }
.tr-tip-num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: #555;
    min-width: 20px;
    padding-top: 2px;
}

/* ── History card ── */
.tr-hist-item {
    background: #111;
    border: 1px solid #1e1e1e;
    border-radius: 6px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.6rem;
    font-size: 0.82rem;
}
.tr-hist-q {
    color: #666;
    margin-bottom: 4px;
    font-size: 0.78rem;
}
.tr-hist-intent {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    color: #444;
}

/* ── Textarea override ── */
textarea {
    background: #111 !important;
    color: #ddd !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 6px !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-size: 0.9rem !important;
}
textarea:focus {
    border-color: #555 !important;
    box-shadow: none !important;
}

/* ── Button override ── */
.stButton > button {
    background: #e8e8e8 !important;
    color: #0d0d0d !important;
    border: none !important;
    border-radius: 5px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    padding: 0.55rem 1.6rem !important;
    transition: background 0.15s !important;
}
.stButton > button:hover {
    background: #ffffff !important;
}

/* ── Copy button ── */
.copy-btn-wrap {
    margin-top: 0.8rem;
    text-align: right;
}

/* ── Spinner color ── */
.stSpinner > div { border-top-color: #888 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #0d0d0d; }
::-webkit-scrollbar-thumb { background: #2a2a2a; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 1. 意图识别引擎
# ════════════════════════════════════════════════════════════
def detect_intent(text: str) -> str:
    """
    简单关键词规则引擎。
    [API HOOK] 将此函数整体替换为 LLM 分类调用即可。
    例：
        response = anthropic.messages.create(
            model="claude-sonnet-4-20250514",
            messages=[{"role":"user","content": f"Classify intent: {text}"}],
            system="Return one of: pricing / complaint / product_inquiry / delivery / customization / follow_up / aftersale / general"
        )
        return response.content[0].text.strip()
    """
    t = text.lower()

    price_kw    = ["price", "prices", "pricing", "cost", "quote", "quotation",
                   "how much", "rate", "费用", "价格", "报价", "多少钱"]
    complaint_kw = ["not happy", "disappointed", "bad quality", "poor", "issue",
                    "problem", "wrong", "defect", "不满意", "差", "有问题",
                    "不喜欢", "不好", "质量差", "退货", "投诉"]
    delivery_kw  = ["delivery", "lead time", "ship", "when", "how long", "eta",
                    "交期", "发货", "多久", "几天", "运输", "到货"]
    custom_kw    = ["custom", "customize", "logo", "oem", "odm", "brand",
                    "定制", "打标", "logo", "私模", "贴牌"]
    followup_kw  = ["follow up", "any update", "status", "heard back", "waiting",
                    "跟进", "有消息吗", "怎么样了", "最新情况"]
    aftersale_kw = ["warranty", "repair", "broken", "return", "refund",
                    "售后", "维修", "保修", "退款", "坏了"]
    product_kw   = ["product", "catalog", "catalogue", "specification", "spec",
                    "what do you", "tell me about", "产品", "目录", "参数", "介绍"]

    if any(k in t for k in complaint_kw):   return "complaint"
    if any(k in t for k in aftersale_kw):   return "aftersale"
    if any(k in t for k in price_kw):       return "pricing"
    if any(k in t for k in delivery_kw):    return "delivery"
    if any(k in t for k in custom_kw):      return "customization"
    if any(k in t for k in followup_kw):    return "follow_up"
    if any(k in t for k in product_kw):     return "product_inquiry"
    return "general"


# ════════════════════════════════════════════════════════════
# 2. 回复生成引擎（规则版）
# ════════════════════════════════════════════════════════════
REPLIES = {
    "pricing": {
        "reply": (
            "Hi! Thanks so much for reaching out — great to hear from you!\n\n"
            "We'd love to get you a competitive quote as quickly as possible. "
            "To make sure we send the most accurate pricing, could you help us with a few quick details?\n\n"
            "  1. Which product(s) are you interested in?\n"
            "  2. What quantity are you looking at? (Our pricing gets much better at higher volumes.)\n"
            "  3. Any specific requirements — material, size, packaging, or certifications?\n\n"
            "Once we have those, we can usually turn around a full quotation within 24 hours. "
            "We work with buyers across Europe, North America, and Southeast Asia, so we know how to keep things fast and straightforward.\n\n"
            "Looking forward to your reply!"
        ),
        "intent_label": "💰 询价 / Pricing Inquiry",
        "tips": [
            "追问目标数量（MOQ 及批量价格区间）",
            "询问交货目的地（影响运费和 Incoterms）",
            "了解是否有样品需求，推进寄样流程",
            "确认预计下单时间，制造紧迫感",
        ],
    },
    "complaint": {
        "reply": (
            "Hi, thank you for taking the time to share your feedback — we genuinely appreciate it.\n\n"
            "I'm sorry to hear the product didn't meet your expectations. "
            "We take quality issues very seriously and I'd like to make this right for you.\n\n"
            "Could you help me understand what specifically fell short?\n\n"
            "  • Was it the material or build quality?\n"
            "  • Did the product not match the specifications you ordered?\n"
            "  • Was there any damage during shipping?\n\n"
            "Once I understand the exact issue, I can offer you the best solution — "
            "whether that's a replacement, credit, or a recommendation for a product that's a better fit for your needs.\n\n"
            "We value your business and want to make sure you leave satisfied."
        ),
        "intent_label": "⚠️ 抱怨 / Complaint",
        "tips": [
            "请客户提供问题照片或视频（便于核实）",
            "询问订单号和收货日期，锁定问题批次",
            "主动提出解决方案（补发 / 退款 / 折扣），掌握主动权",
            "引导客户尝试其他产品型号，保留关系",
        ],
    },
    "delivery": {
        "reply": (
            "Hi! Great question — delivery time is one of the things we're really proud of.\n\n"
            "For standard in-stock items, we typically ship within 3–5 business days. "
            "For custom or bulk orders, production lead time is usually 15–25 days depending on quantity.\n\n"
            "To give you a more precise timeline, could you let us know:\n\n"
            "  1. What product and quantity are you ordering?\n"
            "  2. Which country / port is the destination?\n"
            "  3. Do you have a target delivery date we should work toward?\n\n"
            "We work with reliable freight partners worldwide and can arrange air, sea, or express shipment. "
            "Just let us know your priority — speed or cost — and we'll find the best option for you."
        ),
        "intent_label": "🚚 交期咨询 / Delivery Inquiry",
        "tips": [
            "明确数量后可给更精准的生产 + 运输周期",
            "询问目的地港口，准备运费报价",
            "如客户有截止日期，强调我们的准时交货记录",
            "可推荐走空运加急，提升订单价值",
        ],
    },
    "customization": {
        "reply": (
            "Hi! Absolutely — customization is one of our core strengths, and we do it all the time.\n\n"
            "We support OEM/ODM orders including custom logo, packaging, size, material, and color. "
            "No need to worry about complexity — our team handles the whole process end to end.\n\n"
            "To get things moving, it would help to know:\n\n"
            "  1. What product are you looking to customize?\n"
            "  2. Do you have a logo or brand files ready? (AI / PDF / SVG preferred)\n"
            "  3. Any specific size, material, or color requirements?\n"
            "  4. What quantity are you considering? (Custom orders typically start from MOQ.)\n\n"
            "We can also arrange a sample first so you can approve the design before full production. "
            "Let me know and we'll get a project brief started for you right away!"
        ),
        "intent_label": "🎨 定制需求 / Customization",
        "tips": [
            "索取品牌 Logo 文件（AI/PDF），推进设计稿",
            "确认 MOQ 和预算范围",
            "推荐先下样品单，降低客户决策风险",
            "询问是否需要独立包装设计，扩大订单价值",
        ],
    },
    "follow_up": {
        "reply": (
            "Hi! Thanks for following up — I appreciate your patience.\n\n"
            "I want to make sure we're on the same page. "
            "Could you let me know which inquiry or order you're referring to? "
            "(A reference number or the product name would be super helpful.)\n\n"
            "In the meantime, I'm checking on our end and will get back to you with a full update as soon as possible — "
            "usually within a few hours during business hours.\n\n"
            "We're committed to keeping things moving efficiently for you. Thanks again for your patience!"
        ),
        "intent_label": "🔄 跟进 / Follow-up",
        "tips": [
            "确认具体跟进的订单号或询盘记录",
            "如报价已发，询问客户是否有疑问 → 催促下单",
            "如样品已寄，询问收到情况和反馈",
            "给出明确的下一步时间节点，增强信任感",
        ],
    },
    "aftersale": {
        "reply": (
            "Hi, I'm sorry to hear you're experiencing an issue — let's get this sorted out for you quickly.\n\n"
            "Our after-sales support is here to help. To find the best solution:\n\n"
            "  1. Could you share your order number or invoice reference?\n"
            "  2. What's the issue you're facing — damage, malfunction, missing parts?\n"
            "  3. If possible, a photo or short video would help us assess the situation faster.\n\n"
            "Once we confirm the details, we'll propose a solution — repair, replacement, or refund — "
            "depending on the situation. Our goal is to resolve this with as little hassle for you as possible.\n\n"
            "Thank you for giving us the chance to make it right."
        ),
        "intent_label": "🔧 售后服务 / After-Sales",
        "tips": [
            "要求客户提供照片 / 视频证据，走售后流程",
            "核查保修期和责任归属",
            "主动提出解决方案，避免客户升级投诉",
            "售后完成后，适时推荐复购 / 新品",
        ],
    },
    "product_inquiry": {
        "reply": (
            "Hi! Thanks for your interest — happy to walk you through what we offer.\n\n"
            "We carry a wide range of products and can also accommodate custom requirements. "
            "To point you in the right direction quickly:\n\n"
            "  1. What type of product are you looking for?\n"
            "  2. What's the intended application or use case?\n"
            "  3. Do you have any preferred specifications — material, size, certifications?\n\n"
            "We can share our latest catalog, product datasheets, and pricing once I know more about your needs. "
            "Most of our clients find exactly what they need within the first exchange — let's make this easy for you!"
        ),
        "intent_label": "📦 产品咨询 / Product Inquiry",
        "tips": [
            "发送产品目录 PDF 或样品图，直观展示",
            "询问用途和市场，推荐最适合的型号",
            "提到认证（CE / RoHS / ISO），建立信任感",
            "引导到询价环节，推进漏斗",
        ],
    },
    "general": {
        "reply": (
            "Hi there! Thanks for reaching out — we're glad you got in touch.\n\n"
            "We specialize in high-quality industrial and customized products, "
            "serving buyers across Europe, North America, Southeast Asia, and beyond.\n\n"
            "To make sure I can help you in the most useful way, could you tell me a bit more:\n\n"
            "  • What product or category are you exploring?\n"
            "  • Are you looking to source a specific item, or comparing suppliers?\n"
            "  • What's the timeline for your project?\n\n"
            "We offer competitive pricing, fast lead times, and full customization support. "
            "Let's figure out exactly what you need — I'm here to help!"
        ),
        "intent_label": "💬 一般咨询 / General Inquiry",
        "tips": [
            "引导客户说出具体需求（产品 / 数量 / 用途）",
            "发送公司简介或产品目录，建立初步信任",
            "询问其当前供应商情况，寻找切入点",
            "了解采购决策流程和关键联系人",
        ],
    },
}


def generate_reply(customer_msg: str) -> dict:
    """
    主生成函数。
    [API HOOK] 将下方整块替换为真实 API 调用：

    ── Anthropic Claude 示例 ──
    import anthropic
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=SYSTEM_PROMPT,   # 见下方 SYSTEM_PROMPT 常量
        messages=[{"role": "user", "content": customer_msg}]
    )
    raw = response.content[0].text
    # 解析 raw 中的 JSON 字段 → reply / intent_label / tips

    ── OpenAI 示例 ──
    from openai import OpenAI
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": customer_msg}
        ]
    )
    raw = response.choices[0].message.content
    """
    intent = detect_intent(customer_msg)
    data   = REPLIES.get(intent, REPLIES["general"])
    return {
        "intent":       intent,
        "intent_label": data["intent_label"],
        "reply":        data["reply"],
        "tips":         data["tips"],
    }

# [API HOOK] 接真实 API 时的 System Prompt 参考
SYSTEM_PROMPT = """
You are a professional B2B foreign trade sales representative.
Reply ONLY in English. Be natural, concise, and sales-driven.
Detect the customer's intent and respond with:
1. A professional reply that pushes toward a deal
2. Intent classification
3. 3-4 recommended follow-up actions in Chinese

Return JSON:
{
  "intent_label": "...",
  "reply": "...",
  "tips": ["...", "..."]
}
"""


# ════════════════════════════════════════════════════════════
# 3. Session State 初始化
# ════════════════════════════════════════════════════════════
if "history" not in st.session_state:
    st.session_state.history = []   # 最近 5 条
if "result"  not in st.session_state:
    st.session_state.result  = None
if "copied"  not in st.session_state:
    st.session_state.copied  = False


# ════════════════════════════════════════════════════════════
# 4. 页面布局
# ════════════════════════════════════════════════════════════

# ── 标题 ──────────────────────────────────────────────────
st.markdown('<div class="tr-title">TradeReply AI</div>', unsafe_allow_html=True)
st.markdown('<div class="tr-subtitle">外贸客服 · 智能回复 · 推进成交</div>', unsafe_allow_html=True)

# ── 双栏布局 ──────────────────────────────────────────────
col_left, col_right = st.columns([1.1, 1], gap="large")

with col_left:
    # ── 输入区 ────────────────────────────────────────────
    st.markdown('<div class="tr-card-label">📥 客户原话</div>', unsafe_allow_html=True)
    customer_input = st.text_area(
        label="customer_msg",
        label_visibility="collapsed",
        placeholder="粘贴客户发来的消息（中英文均可）...",
        height=150,
        key="customer_input_box",
    )

    btn_col, clear_col = st.columns([2, 1])
    with btn_col:
        generate_btn = st.button("⚡ 生成专业回复", use_container_width=True)
    with clear_col:
        clear_btn = st.button("清空", use_container_width=True)

    if clear_btn:
        st.session_state.result = None
        st.session_state.copied = False
        st.rerun()

    # ── 生成逻辑 ──────────────────────────────────────────
    if generate_btn:
        if not customer_input.strip():
            st.warning("请先输入客户消息。")
        else:
            with st.spinner("正在分析并生成回复…"):
                time.sleep(0.5)   # 模拟延迟；接真实 API 时删除
                result = generate_reply(customer_input.strip())
                st.session_state.result = result
                st.session_state.copied = False

                # 保存到历史记录（最多 5 条）
                record = {
                    "time":         datetime.now().strftime("%H:%M"),
                    "customer_msg": customer_input.strip()[:80],
                    "intent_label": result["intent_label"],
                }
                st.session_state.history.insert(0, record)
                st.session_state.history = st.session_state.history[:5]

    # ── 历史记录 ──────────────────────────────────────────
    if st.session_state.history:
        st.markdown('<hr class="tr-divider">', unsafe_allow_html=True)
        st.markdown('<div class="tr-card-label">🕘 最近记录</div>', unsafe_allow_html=True)
        for rec in st.session_state.history:
            st.markdown(f"""
            <div class="tr-hist-item">
                <div class="tr-hist-q">"{rec['customer_msg']}{'…' if len(rec['customer_msg'])>=80 else ''}"</div>
                <div class="tr-hist-intent">{rec['time']} · {rec['intent_label']}</div>
            </div>
            """, unsafe_allow_html=True)


with col_right:
    result = st.session_state.result

    if result is None:
        st.markdown("""
        <div style="color:#333; font-size:0.85rem; padding:3rem 1rem; text-align:center; line-height:2;">
            在左侧输入客户消息<br>点击「生成专业回复」<br>结果将显示在这里
        </div>
        """, unsafe_allow_html=True)
    else:
        # ── 客户意图 ──────────────────────────────────────
        st.markdown('<div class="tr-card-label">🎯 客户意图识别</div>', unsafe_allow_html=True)
        st.markdown(f'<span class="tr-intent-badge primary">{result["intent_label"]}</span>',
                    unsafe_allow_html=True)

        st.markdown('<hr class="tr-divider">', unsafe_allow_html=True)

        # ── 英文回复 ──────────────────────────────────────
        st.markdown('<div class="tr-card-label">✉️ 专业英文回复</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="tr-reply-box">{result["reply"]}</div>', unsafe_allow_html=True)

        # 一键复制（Streamlit 原生方案）
        copy_col, _ = st.columns([1, 2])
        with copy_col:
            if st.button("📋 复制回复内容", key="copy_btn", use_container_width=True):
                st.session_state.copied = True
        if st.session_state.copied:
            # 利用 JS 写入剪贴板
            reply_escaped = result["reply"].replace("`", "\\`").replace("\\n", "\\n")
            st.markdown(f"""
            <script>
            (function() {{
                const txt = `{result["reply"].replace(chr(10), "\\n").replace("`","\\`")}`;
                navigator.clipboard.writeText(txt).catch(()=>{{
                    const el=document.createElement('textarea');
                    el.value=txt; document.body.appendChild(el);
                    el.select(); document.execCommand('copy');
                    document.body.removeChild(el);
                }});
            }})();
            </script>
            <div style="font-size:0.75rem;color:#555;margin-top:4px;">✓ 已复制</div>
            """, unsafe_allow_html=True)

        st.markdown('<hr class="tr-divider">', unsafe_allow_html=True)

        # ── 跟进建议 ──────────────────────────────────────
        st.markdown('<div class="tr-card-label">📌 推荐跟进动作</div>', unsafe_allow_html=True)
        for i, tip in enumerate(result["tips"], 1):
            st.markdown(f"""
            <div class="tr-tip">
                <span class="tr-tip-num">0{i}</span>
                <span>{tip}</span>
            </div>
            """, unsafe_allow_html=True)
