# ============================================================
# TradeReply AI · DeepSeek 真实AI版
# ============================================================

import streamlit as st
import time
import os
from datetime import datetime
from openai import OpenAI

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
.tr-tagline { font-size: 11px; color: #252525; letter-spacing: 3px; text-transform: uppercase; }
.tr-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px;
    color: #252525;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}
textarea {
    background: #0c0c0c !important;
    color: #ccc !important;
    border: 1px solid #1c1c1c !important;
    border-radius: 8px !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-size: 14px !important;
    line-height: 1.75 !important;
}
textarea:focus { border-color: #2e2e2e !important; box-shadow: none !important; }
textarea::placeholder { color: #222 !important; }

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
}
div[data-testid="column"]:nth-child(2) .stButton > button {
    background: transparent !important;
    color: #2a2a2a !important;
    border: 1px solid #1c1c1c !important;
}

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
.intent-dot { width: 6px; height: 6px; border-radius: 50%; background: #4ade80; flex-shrink: 0; }

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
.tr-tip-n { font-family: 'IBM Plex Mono', monospace; font-size: 9px; color: #222; min-width: 14px; padding-top: 3px; }

.tr-hist-item {
    background: #0c0c0c;
    border: 1px solid #141414;
    border-radius: 6px;
    padding: 0.7rem 1rem;
    margin-bottom: 0.45rem;
}
.tr-hist-q { font-size: 12px; color: #3a3a3a; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-bottom: 2px; }
.tr-hist-sub { font-family: 'IBM Plex Mono', monospace; font-size: 9px; color: #1e1e1e; letter-spacing: 1px; }

.tr-empty { text-align: center; padding: 4rem 1rem; }
.tr-empty-cross { font-size: 28px; color: #151515; margin-bottom: 1.2rem; }
.tr-empty-hint { font-family: 'IBM Plex Mono', monospace; font-size: 10px; color: #1e1e1e; letter-spacing: 2px; line-height: 2.2; }
.tr-copied-msg { font-family: 'IBM Plex Mono', monospace; font-size: 10px; color: #4ade80; letter-spacing: 1px; margin-top: 6px; }
.tr-div { border: none; border-top: 1px solid #111; margin: 1.5rem 0; }
.stSpinner > div { border-top-color: #333 !important; }
::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: #080808; }
::-webkit-scrollbar-thumb { background: #181818; border-radius: 2px; }
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# DeepSeek AI 调用
# ════════════════════════════════════════════════════════════

# API Key 从环境变量读取（安全）
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")

SYSTEM_PROMPT = """你是一个专业的外贸B2B销售客服，专门帮助外贸公司回复海外买家的询盘消息。

你的任务：
1. 分析客户消息，判断意图
2. 用专业、自然、有销售力的英文回复
3. 回复要像真人外贸销售，不像AI
4. 每次回复都要推进成交

回复规则：
- 如果客户问价格 → 感谢+询问产品/数量/规格+承诺快速报价
- 如果客户抱怨 → 感谢反馈+询问具体问题+提出解决方案
- 如果客户问交期 → 给出大概时间+询问数量和目的地
- 如果客户问定制 → 支持定制+询问logo/尺寸/材质/数量
- 如果客户跟进 → 感谢耐心+询问具体订单+承诺跟进
- 其他情况 → 引导获取更多信息

必须用JSON格式回复，格式如下：
{
  "intent_label": "意图标签（中英双语，例如：💰 询价 · Pricing Inquiry）",
  "reply": "专业英文回复内容",
  "tips": ["跟进建议1", "跟进建议2", "跟进建议3", "跟进建议4"]
}

只返回JSON，不要其他任何内容。"""


def call_deepseek(customer_msg: str) -> dict:
    """调用 DeepSeek API 生成回复"""
    try:
        client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com"
        )
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"客户消息：{customer_msg}"}
            ],
            max_tokens=1000,
            temperature=0.7,
        )
        raw = response.choices[0].message.content.strip()
        # 清理可能的markdown格式
        raw = raw.replace("```json", "").replace("```", "").strip()
        import json
        data = json.loads(raw)
        return {
            "intent_label": data.get("intent_label", "💬 咨询 · General"),
            "reply":        data.get("reply", ""),
            "tips":         data.get("tips", []),
        }
    except Exception as e:
        # 如果API调用失败，返回错误提示
        return {
            "intent_label": "⚠️ 错误 · Error",
            "reply": f"API调用失败，请检查API Key是否正确。错误：{str(e)}",
            "tips": ["检查 DEEPSEEK_API_KEY 环境变量", "确认API余额充足", "检查网络连接"],
        }


def generate_reply(customer_msg: str) -> dict:
    """主生成函数"""
    if not DEEPSEEK_API_KEY:
        return {
            "intent_label": "⚠️ 未配置 · Not Configured",
            "reply": "请先配置 DEEPSEEK_API_KEY 环境变量。",
            "tips": ["运行：export DEEPSEEK_API_KEY=你的key", "然后重启应用"],
        }
    return call_deepseek(customer_msg)


# ── Session State ──
if "history" not in st.session_state: st.session_state.history = []
if "result"  not in st.session_state: st.session_state.result  = None
if "copied"  not in st.session_state: st.session_state.copied  = False


# ════════════════════════════════════════════════════════════
# UI
# ════════════════════════════════════════════════════════════
st.markdown("""
<div class="tr-header">
  <div>
    <div class="tr-logo">TradeReply <em>AI</em></div>
    <div class="tr-tagline" style="margin-top:4px">外贸客服智能回复 · Powered by DeepSeek</div>
  </div>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([1, 1], gap="large")

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
            with st.spinner("AI 分析中，请稍候..."):
                r = generate_reply(customer_input.strip())
                st.session_state.result = r
                st.session_state.copied = False
                st.session_state.history.insert(0, {
                    "time":   datetime.now().strftime("%H:%M"),
                    "msg":    customer_input.strip()[:60],
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


with right:
    res = st.session_state.result

    if res is None:
        st.markdown("""
        <div class="tr-empty">
          <div class="tr-empty-cross">✦</div>
          <div class="tr-empty-hint">
            在左侧输入客户消息<br>
            点击「生成专业回复」<br>
            AI 将生成专业英文回复
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
            safe = res["reply"].replace("`", "\\`").replace("\n", "\\n")
            st.markdown(f"""
            <script>
            (function(){{navigator.clipboard.writeText(`{safe}`).catch(function(){{
                var e=document.createElement('textarea');e.value=`{safe}`;
                document.body.appendChild(e);e.select();document.execCommand('copy');
                document.body.removeChild(e);
            }});}})();
            </script>
            <div class="tr-copied-msg">✓ 已复制</div>""", unsafe_allow_html=True)

        if res["tips"]:
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
