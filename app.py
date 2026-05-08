import streamlit as st
import re

# ページ設定
st.set_page_config(page_title="AI作詞チェッカー・プロ", page_icon="🎼", layout="centered")

# デザイン調整
st.markdown("""
    <style>
    .main { background-color: #fcfbf7; }
    .stAlert { border-radius: 10px; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3.5em; background-color: #1a365d; color: white; font-weight: bold; }
    h1, h2 { color: #1a365d; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎼 AI作詞チェッカー")
st.subheader("〜グローブ・エンターブレインズ流・プロの採用方程式〜")
st.info("※このチェッカーは、資料にある「脱ありきたり」「死語の排除」「臨界点をエグる」基準で、忖度なしの審査を行います。")

# --- 1. 詳細な死語・NGフレーズ辞書 ---
DEATH_WORDS = {
    "夢のかけら": "「夢」と「かけら」の組み合わせ。昭和・平成初期のベタなフレーズです。現代では通用しません。",
    "愛のかけら": "「かけら」系は全滅です。古い当て字やフレーズは音楽シーンでは雑音になります。",
    "未来": "「明日・希望・未来・夢」を並べるのは思考停止の証。具体的でない「未来」は死語です。",
    "瞳": "「瞳に映る」などは使い古された表現。もっと独自の視覚情報を入れてください。",
    "空に描く": "「空、星、月、花」などの自然現象に逃げないでください。情景描写が安易です。",
    "星に誓う": "「星に願いを/誓う」系は完全に予定調和。聴き手の心に引っかかりません。",
    "両手を広げ": "「両手を広げて（翼を広げて）」はNGポーズ。描写がアマチュアの典型です。",
    "君は一人じゃない": "根拠のない「大丈夫」「一人じゃない」は、聴き手をエグる力がありません。",
    "奇跡を掴む": "「奇蹟/軌跡」という言葉の乱用。もはや誰も感動しない言葉の壁です。",
    "扉": "「心の扉を開く」といった比喩は、もはや古典を通り越して古臭いです。"
}

# --- 2. 入力フォーム ---
lyric_input = st.text_area("審査対象の歌詞をこちらに貼り付けてください", height=350, placeholder="プロの現場では1行目が勝負です。")

# --- 3. 診断実行 ---
if st.button("プロの視点で「ガチ審査」を開始する"):
    if not lyric_input:
        st.warning("歌詞が入力されていません。審査を開始できません。")
    else:
        score = 100
        critical_feedbacks = []
        
        # A. 死語・NG表現チェック（NotebookLMのような厳しい言い回しに）
        found_death = [w for w in DEATH_WORDS.keys() if w in lyric_input]
        for w in found_death:
            score -= 15
            critical_feedbacks.append(f"❌ **【死語認定】「{w}」**: {DEATH_WORDS[w]}")

        # B. 描写の具体性チェック（フックとなる言葉があるか）
        concrete_hooks = ["時", "分", "駅", "道", "嘘", "毒", "秒", "左手", "ポケット", "腕時計", "温度", "体温"]
        if not any(hook in lyric_input for hook in concrete_hooks):
            score -= 30
            critical_feedbacks.append("⚠️ **【情景描写の欠如】**: 映像が浮かびません。時間、場所、二人の物理的な距離感が不明瞭です。誰にでも当てはまる歌詞は、誰の心にも残りません。")

        # C. 形容詞への依存チェック
        adjectives = ["悲しい", "嬉しい", "寂しい", "切ない", "眩しい"]
        found_adj = [a for a in adjectives if a in lyric_input]
        if found_adj:
            score -= 10
            critical_feedbacks.append(f"⚠️ **【心理描写の逃げ】**: 「{', '.join(found_adj)}」といった形容詞をそのまま使わないでください。その感情を「仕草」や「風景」でエグり出すのがプロの仕事です。")

        # --- 結果表示（NotebookLM風の総評） ---
        st.divider()
        final_score = max(5, score) # 最低点を5点に設定
        
        if final_score >= 85:
            st.success(f"### 【総合スコア：{final_score}点 / 100点】")
            st.markdown("#### **判定：プロ級（コンペ提出推奨）**")
            st.write("素晴らしい。独自の毒と、エグるようなリアリティが同居しています。言葉選びに「覚悟」が感じられます。")
        elif final_score >= 50:
            st.warning(f"### 【総合スコア：{final_score}点 / 100点】")
            st.markdown("#### **判定：アマチュア級（要全面修正）**")
            st.write("基礎はできていますが、言葉がまだ「優等生」です。もっと臨界点を攻めてください。優れるな、異なれ。")
        else:
            st.error(f"### 【総合スコア：{final_score}点 / 100点】")
            st.markdown("#### **判定：プロ提出不可レベル（ザ・アマチュア）**")
            st.write("率直に申し上げて、典型的なアマチュア歌詞です。ありきたりな言葉のオンパレードで、リアリティが欠片もありません。")

        st.subheader("📋 具体的なダメ出しと改善案")
        if not critical_feedbacks:
            st.write("特になし。このまま個性を伸ばしてください。")
        else:
            for fb in critical_feedbacks:
                st.markdown(fb)

        # アドバイスの補足（資料の言葉を引用）
        st.divider()
        st.markdown("### 💡 プロへの第一歩")
        st.write("「花鳥風月」や「未来・夢・奇跡」を封印してください。**『いつ、どこで、誰が、どんな仕草をして、どう心が壊れたか』**。その映像を1ミリ単位で描写することから再スタートしてください。")

# サイドバー
st.sidebar.title("グローブ・エンターブレインズ流 勝ち技")
st.sidebar.markdown("""
- **臨界点をエグる:** ギリギリのリアリティを。
- **脱ありきたり:** 「空・風・太陽」は死語。
- **逆算思考:** ヒットから逆算して言葉を選ぶ。
- **お買い得な作家:** 修正は即対応、短納期こそ武器。
""")
