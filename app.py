# 1. 診断用データの強化（より厳しく）
DEATH_WORDS = {
    "夢のかけら": "「夢」と「かけら」の組み合わせは、グローブ的死語の典型。あまりにも古臭いです。",
    "未来": "「明日・希望・未来」は漠然としすぎていて、リアリティの欠片もありません。",
    "空": "「空・星・花」といった花鳥風月テーマは、逃げの表現です。具体的描写から逃げないでください。",
    "両手を広げ": "「両手（または翼）を広げて」は完全にNGワード。安易なポーズ描写はやめましょう。",
    "君は一人じゃない": "安易な励ましは、今の音楽シーンでは「雑音」とみなされます。",
    "奇跡": "出会えた奇跡、なんて言葉は使い古されすぎていて、もはや誰も感動しません。"
}

# 3. 診断ロジック（パワーアップ版）
if st.button("プロの視点で審査する（グローブ・エンターブレインズ流）"):
    if not lyric_input:
        st.warning("歌詞が入力されていません。審査不能です。")
    else:
        score = 100
        critical_feedbacks = []
        
        # ① 死語・NGフレーズの徹底チェック
        found_death_words = [w for w in DEATH_WORDS.keys() if w in lyric_input]
        for w in found_death_words:
            score -= 15
            critical_feedbacks.append(f"❌ **【死語認定】「{w}」**: {DEATH_WORDS[w]}")

        # ② 描写の具体性チェック（より厳格に）
        concrete_hooks = ["時", "分", "駅", "道", "指", "髪", "嘘", "毒", "秒"]
        if not any(hook in lyric_input for hook in concrete_hooks):
            score -= 25
            critical_feedbacks.append("⚠️ **【描写不足】**: 全体的に言葉が漠然としています。もっと『臨界点をエグる』ような、特定の一人を指す具体的な仕草や時間を書いてください。")

        # ③ タイトルの想定チェック（タイトルが短すぎる、または「未来」などを含む場合）
        if len(lyric_input.split('\n')[0]) < 3 or "未来" in lyric_input.split('\n')[0]:
            score -= 10
            critical_feedbacks.append("📢 **【タイトル案の脆弱性】**: タイトルはキャッチコピーです。予定調和を壊す「引っかかり」のある言葉を選んでください。")

        # 結果表示（NotebookLM風の厳しいトーン）
        st.divider()
        if score > 80:
            st.success(f"【総合スコア：{score}点 / 100点（合格圏内）】")
            st.write("プロの現場でも通用する可能性があります。独自の毒とフックが効いています。")
        elif score > 40:
            st.warning(f"【総合スコア：{score}点 / 100点（アマチュア級）】")
            st.write("「どこかで聴いたことのある歌」の域を出ていません。言葉を捨て、実体験をエグり出してください。")
        else:
            st.error(f"【総合スコア：{score}点 / 100点（プロ提出不可）】")
            st.write("率直に申し上げて、ありきたりのオンパレードです。資料を読み直し、ゼロから書き直してください。")

        st.subheader("具体的ダメ出し")
        for fb in critical_feedbacks:
            st.markdown(fb)