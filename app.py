import streamlit as st
from openai import OpenAI

# 1. 初期設定
st.set_page_config(page_title="AI作詞ディレクター", page_icon="🎼")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🎼 AI作詞チェッカー PRO")
st.subheader("〜グローブ・エンターブレインズ流・AIガチ審査〜")

# 2. 入力フォーム
lyric_input = st.text_area("審査対象の歌詞を貼り付けてください", height=400)

if st.button("プロの視点でAI審査を開始する"):
    if not lyric_input:
        st.warning("歌詞が入力されていません。")
    else:
        with st.spinner("AIディレクターが審査中..."):
            try:
                # 3. AIへの命令文（ここが知能の核になります）
                response = client.chat.completions.create(
                    model="gpt-4o", # または gpt-3.5-turbo
                    messages=[
                        {"role": "system", "content": """
あなたは「グローブ・エンターブレインズ」の鬼ディレクターです。
以下の基準で厳格に作詞を審査し、NotebookLMのように鋭くダメ出しをしてください。

【審査基準】
1. 死語の排除：「空・風・太陽・未来・夢・瞳・奇跡」などは死語として厳しく減点。
2. 臨界点をエグる：ありきたりな励ましではなく、ギリギリのリアリティがあるか。
3. 情景描写：具体的か？「いつ、どこで、誰が、どんな仕草をしたか」が浮かぶか。
4. フック：一度聴いたら忘れられない毒やクセがあるか。

【出力構成】
- 総合スコア（100点満点）
- プロの厳しいダメ出し（箇条書き）
- 改善に向けたプロのアドバイス
                        """},
                        {"role": "user", "content": f"以下の歌詞を審査してください：\n\n{lyric_input}"}
                    ]
                )
                
                # 4. 結果表示
                result = response.choices[0].message.content
                st.divider()
                st.markdown(result)
                
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")

st.sidebar.markdown("### AI連携モード稼働中")
st.sidebar.write("このチェッカーはChatGPTの知能を利用して、文脈に基づいた高度な診断を行っています。")
