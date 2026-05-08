import streamlit as st

# ページの設定
st.set_page_config(page_title="AI作詞チェッカー", page_icon="🎼", layout="centered")

# カスタムCSSでプロ仕様の見た目に
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #005088; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎼 AI作詞チェッカー")
st.subheader("〜プロの採用基準であなたの歌詞を診断〜")
st.write("グローブ・エンターブレインズ流の「勝ち技」に基づき、歌詞を客観的に評価します。")

# 1. 診断用データの定義（資料に基づく）
CLICHE_WORDS = [
    "空", "風", "太陽", "星空", "瞳", "輝く", "奇跡", "運命", "絆", 
    "大丈夫", "君を信じて", "トキメキ", "導火線", "シルエット", "愛してる"
]

ADJECTIVES = ["悲しい", "嬉しい", "寂しい", "切ない"]

# 2. 入力フォーム
lyric_input = st.text_area("ここに歌詞を入力してください（Aメロ〜サビなど）", height=300, placeholder="例：昨日の雨が嘘みたいに晴れた空...")

# 3. 診断ロジック
if st.button("プロの視点で診断を開始する"):
    if not lyric_input:
        st.warning("歌詞を入力してください。")
    else:
        score = 100
        feedbacks = []
        
        # チェック①：死語・ありきたり表現
        found_cliches = [word for word in CLICHE_WORDS if word in lyric_input]
        if found_cliches:
            score -= len(found_cliches) * 10
            feedbacks.append(f"⚠️ **ありきたりな表現:** 「{', '.join(found_cliches)}」が含まれています。これらは『死語』に近く、聴き手の心に刺さりません。具体的な固有名詞や動作に置き換えましょう。")

        # チェック②：具体性の評価（数字や固有名詞のヒント）
        import re
        if not re.search(r'\d|時|分|曜|場所|駅|道|月', lyric_input):
            score -= 20
            feedbacks.append("⚠️ **情景が不明瞭:** 時間、場所、数字などの具体的なフックがありません。ドラマの舞台設定を明確にしましょう。")

        # チェック③：感情の直接表現
        found_adj = [a for a in ADJECTIVES if a in lyric_input]
        if found_adj:
            score -= 15
            feedbacks.append(f"⚠️ **感情の直接表現:** 「{', '.join(found_adj)}」という言葉を使わずに、その時の『温度』や『風景』で感情をエグり出してください。")

        # 4. 結果表示
        st.divider()
        st.header(f"スコア: {max(0, score)}点")
        
        if score >= 80:
            st.success("【判定：プロ級】 独自性のある表現です。このままブラッシュアップしましょう！")
        elif score >= 50:
            st.warning("【判定：アマチュア級】 基礎は良いですが、言葉が一般的です。もっと「自分だけ」の表現を。")
        else:
            st.error("【判定：やり直し】 どこかで聞いたことのある言葉ばかりです。一度全て捨てて実体験を書きましょう。")
        
        st.subheader("アドバイス")
        for fb in feedbacks:
            st.write(fb)

st.sidebar.title("プロの心得")
st.sidebar.info("""
- **死語を殺せ:** 「空・風・太陽」は禁止。
- **具体的に:** 誰か一人をエグるように。
- **スピード:** 修正依頼には即対応。
""")