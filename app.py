# ============================================================
# TradeReply AI · 后端 API V2
# 更好的回复质量 + 多语言支持
# ============================================================

from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import json
import sqlite3
import hashlib
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

DEEPSEEK_API_KEY = "sk-f1862ef94c424e178305e274abdfe6ed"

# ── 数据库初始化 ──
def init_db():
    conn = sqlite3.connect('/root/tradereply.db')
    c = conn.cursor()
    # 用户表
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT,
        plan TEXT DEFAULT 'free',
        daily_count INTEGER DEFAULT 0,
        last_reset TEXT,
        created_at TEXT
    )''')
    # 历史记录表
    c.execute('''CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        customer_msg TEXT,
        intent_label TEXT,
        reply TEXT,
        tips TEXT,
        created_at TEXT
    )''')
    conn.commit()
    conn.close()

init_db()

# ── System Prompt（升级版，更像真人销售）──
SYSTEM_PROMPT_EN = """You are an elite B2B foreign trade sales representative with 10+ years of experience closing deals with international buyers from Europe, North America, Southeast Asia, and the Middle East.

Your personality: warm, confident, professional, and always subtly pushing toward a sale without being pushy.

Your goal: Turn every customer message into a step closer to a signed order.

Rules for every reply:
1. Start with genuine warmth — acknowledge their message specifically, never use generic openers
2. Address their concern directly and completely
3. Always ask 1-2 qualifying questions to gather info and advance the sale
4. End with a clear, specific call to action
5. Sound like a real human sales rep, NOT a chatbot or template

Tone guidelines:
- Friendly but professional, like a trusted business partner
- Confident about product quality without being arrogant
- Use natural business English, occasional contractions are fine (we're, you'll, I'd)
- Avoid corporate jargon, buzzwords, or overly formal language

Intent-specific tactics:
- PRICING: Thank them → ask product/quantity/specs → promise fast quote → mention competitive pricing + quality
- COMPLAINT: Empathize genuinely → ask for specifics → offer concrete solution → turn it into retention opportunity
- DELIVERY: Give realistic timeline → ask destination + quantity → offer shipping options → create urgency if possible
- CUSTOMIZATION: Show enthusiasm → ask logo/size/material/MOQ → offer sample → walk them through the process
- FOLLOW-UP: Show you remember them → give specific update → push for next step → don't let the conversation die
- AFTER-SALES: Apologize sincerely → ask for evidence → offer fair solution → protect the relationship
- PRODUCT: Paint a picture of the product's value → ask use case → recommend specific model → move toward quote

Return ONLY this JSON (no markdown, no extra text):
{
  "intent_label": "intent in format: emoji EN · CN (e.g. 💰 Pricing · 询价)",
  "reply": "your professional reply in English",
  "tips": ["actionable follow-up tip 1 in Chinese", "tip 2", "tip 3", "tip 4"]
}"""

SYSTEM_PROMPT_CN = """你是一位拥有10年以上经验的顶级外贸B2B销售客服，专门服务来自欧洲、北美、东南亚、中东的海外买家。

你的风格：热情、自信、专业，每次回复都在悄悄推进成交，但不会让客户感到压力。

你的目标：把每一条客户消息都变成离签单更近一步的机会。

每次回复规则：
1. 用真诚的热情开头，针对客户的具体情况，绝不用套话
2. 直接解决客户的问题或需求
3. 必须问1-2个能推进销售的问题（获取信息+引导成交）
4. 以明确的行动呼吁结尾
5. 听起来像真人销售，不像AI或模板

意图处理策略：
- 询价：感谢→询问产品/数量/规格→承诺快速报价→暗示竞争优势
- 抱怨：真诚共情→询问具体情况→提出具体解决方案→转化为留存机会
- 交期：给出实际时间→询问目的地+数量→提供运输选项→适当制造紧迫感
- 定制：表现热情→询问logo/尺寸/材质/数量→推荐先打样→引导完成流程
- 跟进：表现出记得他们→给出具体进展→推进下一步→不让对话冷掉
- 售后：真诚道歉→索取证据→提出公平解决方案→保护客户关系
- 产品：描绘产品价值→询问用途→推荐具体型号→引向报价

只返回以下JSON格式（不要markdown，不要多余内容）：
{
  "intent_label": "意图标签格式：emoji 英文 · 中文（如：💰 Pricing · 询价）",
  "reply": "专业英文回复内容",
  "tips": ["中文跟进建议1", "建议2", "建议3", "建议4"]
}"""

def get_system_prompt(lang='auto', customer_msg=''):
    """根据语言选择system prompt"""
    if lang == 'cn':
        return SYSTEM_PROMPT_CN
    elif lang == 'en':
        return SYSTEM_PROMPT_EN
    else:
        # 自动检测：如果消息包含中文字符，用中文prompt
        if any('\u4e00' <= c <= '\u9fff' for c in customer_msg):
            return SYSTEM_PROMPT_CN
        return SYSTEM_PROMPT_EN


# ── 主要API：生成回复 ──
@app.route('/api/reply', methods=['POST'])
def generate_reply():
    try:
        data = request.json
        msg = data.get('message', '').strip()
        lang = data.get('lang', 'auto')
        user_id = data.get('user_id', None)

        if not msg:
            return jsonify({'error': '消息不能为空'}), 400

        # 获取合适的system prompt
        system_prompt = get_system_prompt(lang, msg)

        client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Customer message: {msg}"}
            ],
            max_tokens=1200,
            temperature=0.8,
        )

        raw = resp.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        result = json.loads(raw)

        # 保存到历史记录
        if user_id:
            try:
                conn = sqlite3.connect('/root/tradereply.db')
                c = conn.cursor()
                c.execute('''INSERT INTO history 
                    (user_id, customer_msg, intent_label, reply, tips, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)''',
                    (user_id, msg, result.get('intent_label',''),
                     result.get('reply',''),
                     json.dumps(result.get('tips',[])),
                     datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                conn.commit()
                conn.close()
            except:
                pass

        return jsonify(result)

    except json.JSONDecodeError:
        # JSON解析失败，返回原始文本
        return jsonify({
            'intent_label': '💬 General · 咨询',
            'reply': raw if 'raw' in dir() else 'Sorry, please try again.',
            'tips': ['重新尝试', '检查网络连接']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── 用户注册 ──
@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.json
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()

        if not email or not password:
            return jsonify({'error': '邮箱和密码不能为空'}), 400

        hashed = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect('/root/tradereply.db')
        c = conn.cursor()
        try:
            c.execute('''INSERT INTO users (email, password, plan, daily_count, last_reset, created_at)
                VALUES (?, ?, 'free', 0, ?, ?)''',
                (email, hashed,
                 datetime.now().strftime('%Y-%m-%d'),
                 datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()
            user_id = c.lastrowid
            conn.close()
            return jsonify({'success': True, 'user_id': user_id, 'email': email, 'plan': 'free'})
        except sqlite3.IntegrityError:
            conn.close()
            return jsonify({'error': '该邮箱已注册'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── 用户登录 ──
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()

        hashed = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect('/root/tradereply.db')
        c = conn.cursor()
        c.execute('SELECT id, email, plan, daily_count FROM users WHERE email=? AND password=?',
                  (email, hashed))
        user = c.fetchone()
        conn.close()

        if user:
            return jsonify({
                'success': True,
                'user_id': user[0],
                'email': user[1],
                'plan': user[2],
                'daily_count': user[3]
            })
        else:
            return jsonify({'error': '邮箱或密码错误'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── 获取历史记录 ──
@app.route('/api/history/<int:user_id>', methods=['GET'])
def get_history(user_id):
    try:
        conn = sqlite3.connect('/root/tradereply.db')
        c = conn.cursor()
        c.execute('''SELECT id, customer_msg, intent_label, reply, tips, created_at
            FROM history WHERE user_id=?
            ORDER BY created_at DESC LIMIT 20''', (user_id,))
        rows = c.fetchall()
        conn.close()

        history = []
        for row in rows:
            history.append({
                'id': row[0],
                'customer_msg': row[1],
                'intent_label': row[2],
                'reply': row[3],
                'tips': json.loads(row[4]) if row[4] else [],
                'created_at': row[5]
            })
        return jsonify({'history': history})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── 检查使用次数 ──
@app.route('/api/check-limit', methods=['POST'])
def check_limit():
    try:
        data = request.json
        user_id = data.get('user_id')

        if not user_id:
            # 未登录用户：用IP限制（简单版）
            return jsonify({'can_use': True, 'remaining': 5, 'plan': 'guest'})

        conn = sqlite3.connect('/root/tradereply.db')
        c = conn.cursor()
        c.execute('SELECT plan, daily_count, last_reset FROM users WHERE id=?', (user_id,))
        user = c.fetchone()

        if not user:
            conn.close()
            return jsonify({'error': '用户不存在'}), 404

        plan, daily_count, last_reset = user
        today = datetime.now().strftime('%Y-%m-%d')

        # 重置每日计数
        if last_reset != today:
            c.execute('UPDATE users SET daily_count=0, last_reset=? WHERE id=?', (today, user_id))
            conn.commit()
            daily_count = 0

        conn.close()

        # 限制规则
        limits = {'free': 10, 'pro': 99999, 'lifetime': 99999}
        limit = limits.get(plan, 10)
        remaining = max(0, limit - daily_count)

        return jsonify({
            'can_use': remaining > 0,
            'remaining': remaining,
            'plan': plan,
            'daily_count': daily_count
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── 增加使用次数 ──
@app.route('/api/increment', methods=['POST'])
def increment():
    try:
        data = request.json
        user_id = data.get('user_id')
        if user_id:
            conn = sqlite3.connect('/root/tradereply.db')
            c = conn.cursor()
            c.execute('UPDATE users SET daily_count=daily_count+1 WHERE id=?', (user_id,))
            conn.commit()
            conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
