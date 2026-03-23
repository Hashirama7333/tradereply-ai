# ============================================================
# TradeReply AI · V3 Premium UI · DeepSeek
# ============================================================

import streamlit as st
import os
import json
from datetime import datetime
from openai import OpenAI

st.set_page_config(
    page_title="TradeReply AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=Inter:wght@300;400;500&display=swap');

* { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #050505; color: #d0d0d0; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── TOP BAR ── */
.tr-topbar {
    background: #050505;
    border-bottom: 1px solid #111;
    padding: 0 4rem;
    height: 52px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 999;
}
.tr-logo {
    font-family: 'Syne', sans-serif;
    font-size: 16px;
    font-weight: 700;
    color: #fff;
    letter-spacing: -0.5px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.tr-logo-dot {
    width: 6px; height: 6px;
    background: #fff;
    border-radius: 50%;
}
.tr-logo-sub {
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    font-weight: 300;
    color: #222;
    letter-spacing: 3px;
    text-transform: uppercase;
}
.tr-status {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
    color: #333;
    font-family: 'Inter', monospace;
    letter-spacing: 1px;
}
.tr-status-dot {
    width: 5px; height: 5px;
    background: #4ade80;
    border-radius: 50%;
    animation: blink 2s infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

/* ── MAIN GRID ── */
.tr-main {
    display: grid;
    grid-template-columns: 480px 1fr;
    min-height: calc(100vh - 52px);
}
.tr-left {
    border-right: 1px solid #0e0e0e;
    padding: 2.5rem 2.5rem;
}
.tr-right {
    background: #030303;
    padding: 2.5rem 3rem;
}

/* ── SECTION LABEL ── */
.tr-label {
    font-size: 9px;
    font-weight: 500;
    color: #1e1e1e;
    letter-spacing: 3.5px;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
    font-family: 'Inter', monospace;
}

/* ── TEXTAREA ── */
textarea {
    background: #080808 !important;
    color: #c8c8c8 !important;
    border: 1px solid #141414 !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    line-height: 1.8 !important;
    padding: 1rem 1.1rem !important;
    transition: border-color 0.2s !important;
    caret-color: #888 !important;
}
textarea:focus {
    border-color: #252525 !important;
    box-shadow: none !important;
}
textarea::placeholder { color: #1e1e1e !important; font-size: 13px !important; }

/* ── BUTTONS ── */
.stButton > button {
    font-family: 'Syne', sans-serif !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    border-radius: 8px !important;
    text-transform: uppercase !important;
    transition: all 0.15s !important;
    height: 42px !important;
    border: none !important;
}
div[data-testid="column"]:first-child .stButton > button {
    background: #f0f0f0 !important;
    color: #050505 !important;
}
div[data-testid="column"]:first-child .stButton > button:hover {
    background: #fff !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(255,255,255,0.08) !important;
}
div[data-testid="column"]:nth-child(2) .stButton > button {
    background: transparent !important;
    color: #1e1e1e !important;
    border: 1px solid #141414 !important;
}
div[data-testid="column"]:nth-child(2) .stButton > button:hover {
    color: #444 !important;
    border-color: #222 !important;
}

/* ── INTENT PILL ── */
.tr-intent {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #0a0a0a;
    border: 1px solid #141414;
    border-radius: 999px;
    padding: 6px 16px 6px 12px;
    font-size: 11px;
    color: #666;
    margin-bottom: 1.5rem;
    font-family: 'Inter', sans-serif;
    letter-spacing: 0.3px;
}
.i-dot { width: 6px; height: 6px; border-radius: 50%; background: #4ade80; }

/* ── REPLY ── */
.tr-reply {
    background: #070707;
    border: 1px solid #111;
    border-left: 2px solid #c8c8c8;
    border-radius: 10px;
    padding: 1.5rem 1.8rem;
    font-size: 14px;
    line-height: 1.9;
    color: #aaa;
    white-space: pre-wrap;
    word-break: break-word;
    margin-bottom: 1.5rem;
    position: relative;
}

/* ── TIPS ── */
.tr-tips {
    background: #070707;
    border: 1px solid #0e0e0e;
    border-radius: 10px;
    overflow: hidden;
}
.tr-tip {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    padding: 12px 16px;
    border-bottom: 1px solid #0a0a0a;
    font-size: 13px;
    color: #555;
    line-height: 1.6;
    transition: background 0.1s;
}
.tr-tip:last-child { border-bottom: none; }
.tr-tip:hover { background: #0a0a0a; }
.tr-tip-n {
    font-size: 9px;
    color: #1e1e1e;
    min-width: 16px;
    padding-top: 3px;
    font-family: 'Inter', monospace;
    letter-spacing: 1px;
}

/* ── HISTORY ── */
.tr-hist {
    background: #080808;
    border: 1px solid #0e0e0e;
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 6px;
    transition: border-color 0.15s;
    cursor: default;
}
.tr-hist:hover { border-color: #161616; }
.tr-hist-q {
    font-size: 12px;
    color: #2e2e2e;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin-bottom: 3px;
}
.tr-hist-meta {
    font-size: 9px;
    color: #1a1a1a;
    letter-spacing: 1px;
    font-family: 'Inter', monospace;
}

/* ── EMPTY STATE ── */
.tr-empty {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 65vh;
    text-align: center;
    gap: 1rem;
}
.tr-empty-icon {
    font-size: 24px;
    color: #111;
}
.tr-empty-text {
    font-size: 10px;
    color: #1a1a1a;
    letter-spacing: 3px;
    line-height: 2.5;
    text-transform: uppercase;
    font-family: 'Inter', monospace;
}

/* ── COPY ── */
.tr-copy-ok {
    font-size: 10px;
    color: #4ade80;
    letter-spacing: 1.5px;
    margin-top: 6px;
    font-family: 'Inter', monospace;
}

/* ── DIVIDER ── */
.tr-div { border: none; border-top: 1px solid #0a0a0a; margin: 1.8rem 0; }

/* ── COPY BTN OVERRIDE ── */
div[data-testid="column"].copy-col .stButton > button {
    background: #111 !important;
    color: #555 !important;
    border: 1px solid #161616 !important;
    font-size: 10px !important;
}
div[data-testid="column"].copy-col .stButton > button:hover {
    background: #161616 !important;
    color: #888 !important;
}

/* ── SPINNER ── */
.stSpinner > div { border-top-color: #2a2a2a !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 2px; }
::-webkit-scrollbar-track { background: #050505; }
::-webkit-scrollbar-thumb { background: #111; border-radius: 2px; }
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# DeepSeek
# ════════════════════════════════════════════════════════════
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")

SYSTEM_PROMPT = """你是一个专业的外贸B2B销售客服，帮助外贸公司回复海外买家。

任务：
1. 分析客户消息意图
2. 用专业自然有销售力的英文回复
3. 回复像真人外贸销售，不像AI
4. 每次回复推进成交

回复规则：
- 问价格 → 感谢+询问产品/数量/规格+承诺快速报价
- 抱怨 → 感谢反馈+询问具体问题+提出解决方案
- 问交期 → 给时间范围+询问数量和目的地
- 问定制 → 支持定制+询问logo/尺寸/材质/数量
- 跟进 → 感谢耐心+询问具体订单
- 其他 → 引导获取更多信息

必须返回JSON格式：
{
  "intent_label": "意图（中英双语，如：💰 询价 · Pricing）",
  "reply": "专业英文回复",
  "tips": ["建议1", "建议2", "建议3", "建议4"]
}

只返回JSON，不要其他内容。"""


def call_deepseek(msg: str) -> dict:
    try:
        client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": f"客户消息：{msg}"}
            ],
            max_tokens=1000,
            temperature=0.7,
        )
        raw = resp.choices[0].message.content.strip()
        raw = raw.replace("```json","").replace("```","").strip()
        data = json.loads(raw)
        return {
            "intent_label": data.get("intent_label","💬 咨询 · General"),
            "reply":        data.get("reply",""),
            "tips":         data.get("tips",[]),
        }
    except Exception as e:
        return {
            "intent_label": "⚠️ 错误",
            "reply": f"API错误：{str(e)}",
            "tips": [],
        }


def generate_reply(msg: str) -> dict:
    if not DEEPSEEK_API_KEY:
        return {"intent_label":"⚠️ 未配置","reply":"请配置 DEEPSEEK_API_KEY","tips":[]}
    return call_deepseek(msg)


# ── Session ──
for k,v in [("history",[]),("result",None),("copied",False)]:
    if k not in st.session_state: st.session_state[k] = v


# ════════════════════════════════════════════════════════════
# UI
# ════════════════════════════════════════════════════════════
st.markdown("""
<div class="tr-topbar">
  <div class="tr-logo">
    <div class="tr-logo-dot"></div>
    TradeReply AI
  </div>
  <div style="display:flex;align-items:center;gap:2rem">
    <div class="tr-logo-sub">外贸客服智能体</div>
    <div class="tr-status"><div class="tr-status-dot"></div>DEEPSEEK · LIVE</div>
  </div>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([1, 1.2], gap="small")

# ── LEFT ──
with left:
    st.markdown('<div style="padding:2.5rem 2rem">', unsafe_allow_html=True)

    st.markdown('<div class="tr-label">客户消息 · Input</div>', unsafe_allow_html=True)
    inp = st.text_area(
        label="i", label_visibility="collapsed",
        placeholder="粘贴客户消息（中英文均可）...",
        height=210, key="inp",
    )

    c1, c2 = st.columns([3,1])
    with c1:
        gen = st.button("✦  生成专业回复", use_container_width=True)
    with c2:
        clr = st.button("清空", use_container_width=True)

    if clr:
        st.session_state.result = None
        st.session_state.copied = False
        st.rerun()

    if gen:
        if not inp.strip():
            st.warning("请输入客户消息")
        else:
            with st.spinner(""):
                r = generate_reply(inp.strip())
                st.session_state.result = r
                st.session_state.copied = False
                st.session_state.history.insert(0,{
                    "time": datetime.now().strftime("%H:%M"),
                    "msg":  inp.strip()[:55],
                    "intent": r["intent_label"],
                })
                st.session_state.history = st.session_state.history[:5]

    if st.session_state.history:
        st.markdown('<hr class="tr-div">', unsafe_allow_html=True)
        st.markdown('<div class="tr-label">最近记录 · History</div>', unsafe_allow_html=True)
        for rec in st.session_state.history:
            st.markdown(f"""
            <div class="tr-hist">
              <div class="tr-hist-q">"{rec['msg']}{'…' if len(rec['msg'])>=55 else ''}"</div>
              <div class="tr-hist-meta">{rec['time']} · {rec['intent']}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ── RIGHT ──
with right:
    st.markdown('<div style="padding:2.5rem 2.5rem;background:#030303;min-height:calc(100vh - 52px)">', unsafe_allow_html=True)
    res = st.session_state.result

    if res is None:
        st.markdown("""
        <div class="tr-empty">
          <div class="tr-empty-icon">✦</div>
          <div class="tr-empty-text">
            输入客户消息<br>
            点击生成按钮<br>
            AI 实时生成回复
          </div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<div class="tr-label">意图识别 · Intent</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="tr-intent">
          <div class="i-dot"></div>
          {res['intent_label']}
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="tr-label">英文回复 · Reply</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="tr-reply">{res["reply"]}</div>', unsafe_allow_html=True)

        cp1, _ = st.columns([1, 2])
        with cp1:
            if st.button("📋  复制回复", key="cp", use_container_width=True):
                st.session_state.copied = True
        if st.session_state.copied:
            safe = res["reply"].replace("`","\\`").replace("\n","\\n")
            st.markdown(f"""
            <script>
            (function(){{
              navigator.clipboard.writeText(`{safe}`).catch(function(){{
                var e=document.createElement('textarea');
                e.value=`{safe}`;
                document.body.appendChild(e);
                e.select();
                document.execCommand('copy');
                document.body.removeChild(e);
              }});
            }})();
            </script>
            <div class="tr-copy-ok">✓ copied</div>""", unsafe_allow_html=True)

        if res.get("tips"):
            st.markdown('<hr class="tr-div">', unsafe_allow_html=True)
            st.markdown('<div class="tr-label">跟进建议 · Next Steps</div>', unsafe_allow_html=True)
            st.markdown('<div class="tr-tips">', unsafe_allow_html=True)
            for i, tip in enumerate(res["tips"], 1):
                st.markdown(f"""
                <div class="tr-tip">
                  <span class="tr-tip-n">0{i}</span>
                  <span>{tip}</span>
                </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
