# ============================================================
# TradeReply AI · 升级版 UI V2
# ============================================================

import streamlit as st
import time
from datetime import datetime

st.set_page_config(
    page_title="TradeReply AI · 外贸客服Agent",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }
.stApp { background: #080808; color: #e0e0e0; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem 3rem !important; max-width: 1200px !important; }

/* ── Header ── */
.tr-header {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    margin-bottom: 2.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid #141414;
}
.tr-logo {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 20px;
    font-weight: 600;
    color: #fff;
    letter-spacing: -0.5px;
}
.tr-logo em { color: #252525; font-style: normal; }
.tr-tagline {
    font-size: 11px;
    color: #252525;
    letter-spacing: 3px;
    text-transform: uppercase;
}

/* ── Labels ── */
.tr-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px;
    color: #252525;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}

/* ── Textarea ── */
textarea {
    background: #0c0c0c !important;
    color: #ccc !important;
    border: 1px solid #1c1c1c !important;
    border-radius: 8px !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-size: 14px !important;
    line-height: 1.75 !important;
    transition: border-color 0.2s !important;
}
textarea:focus { border-color: #2e2e2e !important; box-shadow: none !important; }
textarea::placeholder { color: #222 !important; }

/* ── Buttons ── */
.stButton > button {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 10px !important;
    font-weight: 600 !important;
    letter-spacing: 2px !important;
    border-radius: 6px !important;
    text-transform: uppercase !important;
    transition: all 0.15s !important;
    height: 40px !important;
}
div[data-testid="column"]:first-child .stButton > button {
    background: #e0e0e0 !important;
    color: #080808 !important;
    border: none !important;
}
div[data-testid="column"]:first-child .stButton > button:hover {
    background: #fff !important;
    transform: translateY(-1px) !important;
}
div[data-testid="column"]:nth-child(2) .stButton > button {
    background: transparent !important;
    color: #2a2a2a !important;
    border: 1px solid #1c1c1c !important;
}
div[data-testid="column"]:nth-child(2) .stButton > button:hover {
    color: #555 !important;
    border-color: #2a2a2a !important;
}

/* ── Intent pill ── */
.tr-intent-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #0e0e0e;
    border: 1px solid #1c1c1c;
    border-radius: 999px;
    padding: 5px 14px 5px 10px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: #888;
    margin-bottom: 1.2rem;
}
.intent-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #4ade80;
    flex-shrink: 0;
}

/* ── Reply card ── */
.tr-reply-card {
    background: #0a0a0a;
    border: 1px solid #181818;
    border-left: 2px solid #d0d0d0;
    border-radius: 8px;
    padding: 1.3rem 1.5rem;
    font-size: 13.5px;
    line-height: 1.85;
    color: #bbb;
    white-space: pre-wrap;
    word-break: break-word;
    margin-bottom: 1.2rem;
}

/* ── Tips card ── */
.tr-tips-card {
    background: #0a0a0a;
    border: 1px solid #141414;
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 1.2rem;
}
.tr-tip-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 10px 14px;
    border-bottom: 1px solid #0f0f0f;
    font-size: 12.5px;
    color: #666;
    line-height: 1.5;
}
.tr-tip-item:last-child { border-bottom: none; }
.tr-tip-n {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px;
    color: #222;
    min-width: 14px;
    padding-top: 3px;
}

/* ── History ── */
.tr-hist-item {
    background: #0c0c0c;
    border: 1px solid #141414;
    border-radius: 6px;
    padding: 0.7rem 1rem;
    margin-bottom: 0.45rem;
    transition: border-color 0.15s;
}
.tr-hist-item:hover { border-color: #1e1e1e; }
.tr-hist-q {
    font-size: 12px;
    color: #3a3a3a;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin-bottom: 2px;
}
.tr-hist-sub {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px;
    color: #1e1e1e;
    letter-spacing: 1px;
}

/* ── Empty state ── */
.tr-empty {
    text-align: center;
    padding: 4rem 1rem;
}
.tr-empty-cross {
    font-size: 28px;
    color: #151515;
    margin-bottom: 1.2rem;
}
.tr-empty-hint {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    color: #1e1e1e;
    letter-spacing: 2px;
    line-height: 2.2;
}

/* ── Copy feedback ── */
.tr-copied-msg {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    color: #4ade80;
    letter-spacing: 1px;
    margin-top: 6px;
}

/* ── Divider ── */
.tr-div { border: none; border-top: 1px solid #111; margin: 1.5rem 0; }

/* ── Spinner ── */
.stSpinner > div { border-top-color: #333 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: #080808; }
::-webkit-scrollbar-thumb { background: #181818; border-radius: 2px; }
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 逻辑
# ════════════════════════════════════════════════════════════
def detect_intent(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ["price","pricing","cost","quote","quotation","how much","rate","费用","价格","报价","多少钱"]): return "pricing"
    if any(k in t for k in ["not happy","disappointed","bad","poor","issue","problem","wrong","defect","不满意","差","有问题","不喜欢","不好","质量差","退货","投诉"]): return "complaint"
    if any(k in t for k in ["delivery","lead time","ship","when","how long","eta","交期","发货","多久","几天","运输","到货"]): return "delivery"
    if any(k in t for k in ["custom","customize","logo","oem","odm","brand","定制","打标","私模","贴牌"]): return "customization"
    if any(k in t for k in ["follow up","any update","status","heard back","waiting","跟进","有消息吗","怎么样了"]): return "follow_up"
    if any(k in t for k in ["warranty","repair","broken","return","refund","售后","维修","保修","退款","坏了"]): return "aftersale"
    if any(k in t for k in ["product","catalog","specification","spec","what do you","tell me about","产品","目录","参数","介绍"]): return "product_inquiry"
    return "general"

REPLIES = {
    "pricing": {
        "reply": "Hi! Thanks so much for reaching out — great to hear from you!\n\nWe'd love to get you a competitive quote as quickly as possible. To make sure we send the most accurate pricing, could you help us with a few quick details?\n\n  1. Which product(s) are you interested in?\n  2. What quantity are you looking at? (Our pricing gets much better at higher volumes.)\n  3. Any specific requirements — material, size, packaging, or certifications?\n\nOnce we have those, we can usually turn around a full quotation within 24 hours. Looking forward to your reply!",
        "intent_label": "💰 询价 · Pricing Inquiry",
        "tips": ["追问目标数量（MOQ 及批量价格区间）","询问交货目的地（影响运费和 Incoterms）","了解是否有样品需求，推进寄样流程","确认预计下单时间，制造紧迫感"],
    },
    "complaint": {
        "reply": "Hi, thank you for taking the time to share your feedback — we genuinely appreciate it.\n\nI'm sorry to hear the product didn't meet your expectations. We take quality issues very seriously and I'd like to make this right for you.\n\nCould you help me understand what specifically fell short?\n\n  • Was it the material or build quality?\n  • Did the product not match the specifications you ordered?\n  • Was there any damage during shipping?\n\nOnce I understand the exact issue, I can offer the best solution — replacement, credit, or a better-fit recommendation.\n\nWe value your business and want to make sure you leave satisfied.",
        "intent_label": "⚠️ 抱怨 · Complaint",
        "tips": ["请客户提供问题照片或视频（便于核实）","询问订单号和收货日期，锁定问题批次","主动提出解决方案（补发/退款/折扣）","引导客户尝试其他产品型号，保留关系"],
    },
    "delivery": {
        "reply": "Hi! Great question — delivery time is one of the things we're really proud of.\n\nFor standard in-stock items, we typically ship within 3–5 business days. For custom or bulk orders, production lead time is usually 15–25 days depending on quantity.\n\nTo give you a more precise timeline:\n\n  1. What product and quantity are you ordering?\n  2. Which country / port is the destination?\n  3. Do you have a target delivery date we should work toward?\n\nWe work with reliable freight partners worldwide and can arrange air, sea, or express shipment.",
        "intent_label": "🚚 交期 · Delivery Inquiry",
        "tips": ["明确数量后可给更精准的生产+运输周期","询问目的地港口，准备运费报价","如客户有截止日期，强调准时交货记录","可推荐走空运加急，提升订单价值"],
    },
    "customization": {
        "reply": "Hi! Absolutely — customization is one of our core strengths.\n\nWe support OEM/ODM orders including custom logo, packaging, size, material, and color. Our team handles the whole process end to end.\n\nTo get things moving:\n\n  1. What product are you looking to customize?\n  2. Do you have brand files ready? (AI / PDF / SVG preferred)\n  3. Any specific size, material, or color requirements?\n  4. What quantity are you considering?\n\nWe can arrange a sample first so you can approve the design before full production!",
        "intent_label": "🎨 定制 · Customization",
        "tips": ["索取品牌 Logo 文件（AI/PDF），推进设计稿","确认 MOQ 和预算范围","推荐先下样品单，降低客户决策风险","询问是否需要独立包装设计，扩大订单价值"],
    },
    "follow_up": {
        "reply": "Hi! Thanks for following up — I appreciate your patience.\n\nCould you let me know which inquiry or order you're referring to? A reference number or product name would be super helpful.\n\nI'm checking on our end and will get back to you with a full update as soon as possible — usually within a few hours during business hours.\n\nWe're committed to keeping things moving efficiently for you!",
        "intent_label": "🔄 跟进 · Follow-up",
        "tips": ["确认具体跟进的订单号或询盘记录","如报价已发，询问客户是否有疑问→催促下单","如样品已寄，询问收到情况和反馈","给出明确的下一步时间节点，增强信任感"],
    },
    "aftersale": {
        "reply": "Hi, I'm sorry to hear you're experiencing an issue — let's get this sorted out quickly.\n\nTo find the best solution:\n\n  1. Could you share your order number or invoice reference?\n  2. What's the issue — damage, malfunction, missing parts?\n  3. A photo or short video would help us assess faster.\n\nOnce we confirm the details, we'll propose a solution — repair, replacement, or refund. Our goal is to resolve this with as little hassle as possible.",
        "intent_label": "🔧 售后 · After-Sales",
        "tips": ["要求客户提供照片/视频证据，走售后流程","核查保修期和责任归属","主动提出解决方案，避免客户升级投诉","售后完成后，适时推荐复购/新品"],
    },
    "product_inquiry": {
        "reply": "Hi! Thanks for your interest — happy to walk you through what we offer.\n\nTo point you in the right direction quickly:\n\n  1. What type of product are you looking for?\n  2. What's the intended application or use case?\n  3. Any preferred specifications — material, size, certifications?\n\nWe can share our latest catalog, product datasheets, and pricing once I know more about your needs. Most clients find exactly what they need within the first exchange!",
        "intent_label": "📦 产品 · Product Inquiry",
        "tips": ["发送产品目录 PDF 或样品图，直观展示","询问用途和市场，推荐最适合的型号","提到认证（CE/RoHS/ISO），建立信任感","引导到询价环节，推进漏斗"],
    },
    "general": {
        "reply": "Hi there! Thanks for reaching out — glad you got in touch.\n\nWe specialize in high-quality industrial and customized products, serving buyers across Europe, North America, Southeast Asia, and beyond.\n\nTo help you in the most useful way:\n\n  • What product or category are you exploring?\n  • Are you sourcing a specific item, or comparing suppliers?\n  • What's the timeline for your project?\n\nWe offer competitive pricing, fast lead times, and full customization support.",
        "intent_label": "💬 咨询 · General Inquiry",
        "tips": ["引导客户说出具体需求（产品/数量/用途）","发送公司简介或产品目录，建立初步信任","询问其当前供应商情况，寻找切入点","了解采购决策流程和关键联系人"],
    },
}

def generate_reply(msg: str) -> dict:
    # [API HOOK] 替换此函数为真实 API 调用
    intent = detect_intent(msg)
    data = REPLIES.get(intent, REPLIES["general"])
    return {"intent": intent, "intent_label": data["intent_label"], "reply": data["reply"], "tips": data["tips"]}


# ── Session State ──
if "history"  not in st.session_state: st.session_state.history  = []
if "result"   not in st.session_state: st.session_state.result   = None
if "copied"   not in st.session_state: st.session_state.copied   = False


# ════════════════════════════════════════════════════════════
# UI
# ════════════════════════════════════════════════════════════
st.markdown("""
<div class="tr-header">
  <div>
    <div class="tr-logo">TradeReply <em>AI</em></div>
    <div class="tr-tagline" style="margin-top:4px">外贸客服智能回复 · B2B Sales Agent</div>
  </div>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([1, 1], gap="large")

# ── LEFT ──
with left:
    st.markdown('<div class="tr-label">客户消息 · Customer Message</div>', unsafe_allow_html=True)
    customer_input = st.text_area(
        label="msg", label_visibility="collapsed",
        placeholder="粘贴客户发来的消息，支持中文和英文...",
        height=200, key="msg_input",
    )

    c1, c2 = st.columns([3, 1])
    with c1:
        gen_btn = st.button("⚡  生成专业回复", use_container_width=True)
    with c2:
        clr_btn = st.button("清空", use_container_width=True)

    if clr_btn:
        st.session_state.result = None
        st.session_state.copied = False
        st.rerun()

    if gen_btn:
        if not customer_input.strip():
            st.warning("请先输入客户消息")
        else:
            with st.spinner("分析中..."):
                time.sleep(0.35)
                r = generate_reply(customer_input.strip())
                st.session_state.result = r
                st.session_state.copied = False
                st.session_state.history.insert(0, {
                    "time": datetime.now().strftime("%H:%M"),
                    "msg":  customer_input.strip()[:60],
                    "intent": r["intent_label"],
                })
                st.session_state.history = st.session_state.history[:5]

    if st.session_state.history:
        st.markdown('<hr class="tr-div">', unsafe_allow_html=True)
        st.markdown('<div class="tr-label">最近记录 · Recent</div>', unsafe_allow_html=True)
        for rec in st.session_state.history:
            st.markdown(f"""
            <div class="tr-hist-item">
              <div class="tr-hist-q">"{rec['msg']}{'…' if len(rec['msg'])>=60 else ''}"</div>
              <div class="tr-hist-sub">{rec['time']} &nbsp;·&nbsp; {rec['intent']}</div>
            </div>""", unsafe_allow_html=True)


# ── RIGHT ──
with right:
    res = st.session_state.result

    if res is None:
        st.markdown("""
        <div class="tr-empty">
          <div class="tr-empty-cross">✦</div>
          <div class="tr-empty-hint">
            在左侧输入客户消息<br>
            点击「生成专业回复」<br>
            结果将显示在这里
          </div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<div class="tr-label">意图识别 · Intent</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="tr-intent-pill">
          <div class="intent-dot"></div>
          {res['intent_label']}
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="tr-label">英文回复 · Reply</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="tr-reply-card">{res["reply"]}</div>', unsafe_allow_html=True)

        cp1, cp2 = st.columns([1, 2])
        with cp1:
            if st.button("📋  复制", key="cp", use_container_width=True):
                st.session_state.copied = True
        if st.session_state.copied:
            safe = res["reply"].replace("`","\\`").replace("\n","\\n")
            st.markdown(f"""
            <script>
            (function(){{navigator.clipboard.writeText(`{safe}`).catch(function(){{
                var e=document.createElement('textarea');e.value=`{safe}`;
                document.body.appendChild(e);e.select();document.execCommand('copy');
                document.body.removeChild(e);
            }});}})();
            </script>
            <div class="tr-copied-msg">✓ 已复制</div>""", unsafe_allow_html=True)

        st.markdown('<hr class="tr-div">', unsafe_allow_html=True)
        st.markdown('<div class="tr-label">跟进建议 · Follow-up Actions</div>', unsafe_allow_html=True)
        st.markdown('<div class="tr-tips-card">', unsafe_allow_html=True)
        for i, tip in enumerate(res["tips"], 1):
            st.markdown(f"""
            <div class="tr-tip-item">
              <span class="tr-tip-n">0{i}</span>
              <span>{tip}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
