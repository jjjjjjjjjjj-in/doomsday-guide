"""返答が英語になっていないかを、返答を終える前に自動で確かめる（Stop フック）。

運営者は日本語で話す。英語の返答が混じっていたら、終わらせずに「日本語で書き直して」と Claude に戻す。
運営者の許可を得て入れた（2026-11-06）。
"""
import json
import re
import sys

JA = re.compile(r"[぀-ヿ㐀-鿿ｦ-ﾟ]")  # ひらがな・カタカナ・漢字
EN = re.compile(r"[A-Za-z]")


def strip_code(text):
    """コード・URL・ファイル名など、英語でしか書けない部分は数えない"""
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`]*`", " ", text)
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"[\w./-]+\.(?:py|js|css|html|md|json|csv|png|pdf|yml|txt)\b", " ", text)
    return text


def mostly_english(text):
    t = strip_code(text)
    ja, en = len(JA.findall(t)), len(EN.findall(t))
    return en >= 40 and ja < en * 0.3


def turn_texts(path):
    """最後に運営者が話したあとの、Claude の文章をすべて集める"""
    texts = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                o = json.loads(line)
            except ValueError:
                continue
            m = o.get("message") or {}
            if o.get("type") == "user" and isinstance(m.get("content"), str):
                texts = []  # 運営者の新しい発言
            elif o.get("type") == "assistant" and isinstance(m.get("content"), list):
                texts += [c.get("text", "") for c in m["content"] if c.get("type") == "text"]
    return texts


def main():
    data = json.load(sys.stdin)
    if data.get("stop_hook_active"):  # 書き直しのあとは、もう一度止めない（くり返し防止）
        return
    path = data.get("transcript_path")
    if not path:
        return
    try:
        bad = [t for t in turn_texts(path) if mostly_english(t)]
    except OSError:
        return
    if bad:
        print(json.dumps({
            "decision": "block",
            "reason": "【日本語ルール違反】この返答に英語の文章が入っています（CLAUDE.md の最重要ルール）。"
                      "運営者は英語を読みません。英語で書いた部分の内容を、すべて日本語で書き直して、もう一度返答してください。"
                      "最初の英語の部分: " + bad[0][:120].replace("\n", " "),
        }, ensure_ascii=False))


if __name__ == "__main__":
    main()
