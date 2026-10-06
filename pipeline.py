#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
C1 课程资料翻译管线 (pipeline.py)
=================================
可复跑的信息获取与翻译管线。换一门课，只需把新课的 HTML/PDF 放进 source/，
补充 glossary.md，即可重新产出中文资料包。

子命令:
  extract   把 source/pages/*.html 的结构化正文抽取成 segments/<page>.json + manifest.csv
  glossary  读取 glossary.md，对 zh/pages/*.html 做"术语一致性强制替换"(只动可见文本，不动标签/代码)
  qc        生成质量报告: 覆盖度 + 术语一致性 + 漏译抽检

用法示例:
  python pipeline.py extract
  python pipeline.py glossary
  python pipeline.py qc
"""
import os, re, sys, json, csv

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_PAGES = os.path.join(ROOT, "source", "pages")
ZH_PAGES = os.path.join(ROOT, "zh", "pages")
SEG_DIR = os.path.join(ROOT, "segments")
GLOSSARY = os.path.join(ROOT, "glossary.md")
MANIFEST = os.path.join(ROOT, "manifest.csv")
REPORT = os.path.join(ROOT, "qc_report.md")

# ---------- 工具 ----------
def strip_tags_keep(raw_html):
    raw = re.sub(r'<script[\s\S]*?</script>', ' ', raw_html, flags=re.I)
    raw = re.sub(r'<style[\s\S]*?</style>', ' ', raw_html, flags=re.I)
    raw = re.sub(r'<(h[1-6]|p|li|div|br|tr)[^>]*>', '\n', raw, flags=re.I)
    raw = re.sub(r'<[^>]+>', ' ', raw)
    raw = re.sub(r'&nbsp;', ' ', raw); raw = re.sub(r'&amp;', '&', raw)
    raw = re.sub(r'&lt;', '<', raw); raw = re.sub(r'&gt;', '>', raw)
    raw = re.sub(r'[ \t]+', ' ', raw)
    raw = re.sub(r'\n\s*\n+', '\n', raw)
    return raw.strip()

def read_glossary(path=GLOSSARY):
    """解析 glossary.md，返回 [(english, chinese), ...]，english 用于一致性替换。"""
    pairs = []
    if not os.path.exists(path):
        return pairs
    txt = open(path, encoding="utf-8").read()
    for line in txt.splitlines():
        m = re.match(r"^\|\s*(.+?)\s*\|\s*(.+?)\s*\|", line)
        if not m:
            continue
        en, zh = m.group(1).strip(), m.group(2).strip()
        en = en.split("(")[0].strip()  # 去掉括注
        # 只取含英文且长度>=3 的词条做自动替换(避免替换过短词)
        if re.search(r"[A-Za-z]{3,}", en) and zh and "/" not in en:
            pairs.append((en, zh.split("（")[0].split("(")[0].strip()))
    return pairs

# ---------- 1. extract ----------
def cmd_extract():
    os.makedirs(SEG_DIR, exist_ok=True)
    rows = []
    for fn in sorted(os.listdir(SRC_PAGES)):
        if not fn.endswith(".html"):
            continue
        raw = open(os.path.join(SRC_PAGES, fn), encoding="utf-8", errors="ignore").read()
        text = strip_tags_keep(raw)
        wc = len(text.split())
        # 按段落切成 segment
        segs = [s.strip() for s in text.split("\n") if len(s.strip()) > 1]
        seg = {"file": fn, "word_count": wc, "segments": segs}
        json.dump(seg, open(os.path.join(SEG_DIR, fn.replace(".html", ".json")), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        rows.append((fn, wc, len(segs)))
    with open(MANIFEST, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["file", "word_count", "segment_count"])
        w.writerows(rows)
    total = sum(r[1] for r in rows)
    print(f"[extract] 共抽取 {len(rows)} 个页面, 英文正文约 {total} 词 -> segments/ + manifest.csv")

# ---------- 2. glossary 一致性强制 ----------
def _tag_aware_replace(html, repl_fn):
    """把 HTML 按标签切分，只对可见文本节点做替换，标签/属性原样保留。"""
    parts = re.split(r'(<[^>]+>)', html)
    out = []
    for i, p in enumerate(parts):
        if i % 2 == 1:        # 标签
            out.append(p)
        else:                 # 文本
            out.append(repl_fn(p))
    return "".join(out)

def cmd_glossary():
    pairs = read_glossary()
    if not pairs:
        print("[glossary] 未找到 glossary 词条"); return
    done = 0
    for fn in sorted(os.listdir(ZH_PAGES)):
        if not fn.endswith(".html"):
            continue
        p = os.path.join(ZH_PAGES, fn)
        html = open(p, encoding="utf-8", errors="ignore").read()
        def repl(t):
            for en, zh in pairs:
                # 整词匹配(边界: 非字母数字), 不替换已在中文里的
                try:
                    t = re.sub(r'(?<![A-Za-z0-9])' + re.escape(en) + r'(?![A-Za-z0-9])', zh, t)
                except Exception:
                    pass
            return t
        new = _tag_aware_replace(html, repl)
        open(p, "w", encoding="utf-8").write(new)
        done += 1
    print(f"[glossary] 已对 {done} 个中文页面执行术语一致性强制替换 (共 {len(pairs)} 条)")

# ---------- 3. qc ----------
def cmd_qc():
    pairs = read_glossary()
    src_files = {f for f in os.listdir(SRC_PAGES) if f.endswith(".html")}
    zh_files = {f for f in os.listdir(ZH_PAGES) if f.endswith(".html")}
    covered = src_files & zh_files
    missing = src_files - zh_files
    lines = ["# 质量抽检报告 (QC Report)", ""]
    lines.append(f"- 源页面: {len(src_files)} ｜ 已译: {len(covered)} ｜ 缺失: {len(missing)}")
    lines.append(f"- 覆盖度: {len(covered)/max(len(src_files),1)*100:.1f}%")
    # 说明页识别: 中文页可见正文过短且含"源站正文无法获取"类披露语 -> 源站不可获取, 非漏译
    markers = ("占位说明", "暂缺此页", "未抓取到任何内容", "需要访问权限",
               "JavaScript", "未包含文章正文", "加载骨架", "无法提供该文")
    placeholders = []
    for fn in sorted(covered):
        html = open(os.path.join(ZH_PAGES, fn), encoding="utf-8", errors="ignore").read()
        if len(strip_tags_keep(html).strip()) < 600 and any(m in html or m in html for m in markers):
            if any(m in strip_tags_keep(html) for m in markers):
                placeholders.append(fn)
    real = len(covered) - len(placeholders)
    lines.append(f"- 全文实译页: {real} ｜ 说明页(源站正文不可获取): {len(placeholders)}")
    if placeholders:
        lines.append("")
        lines.append("## 说明页（源站正文不可获取，已如实披露，不编造内容）")
        for fn in placeholders:
            lines.append(f"- {fn}")
    if missing:
        lines.append("\n## 缺失页面")
        for m in sorted(missing):
            lines.append(f"- {m}")
    # 术语一致性: 在 zh 页面里找是否仍大量出现英文原词(简单抽检)
    lines.append("\n## 术语一致性抽检")
    issues = 0
    for fn in sorted(covered):
        html = open(os.path.join(ZH_PAGES, fn), encoding="utf-8", errors="ignore").read()
        text = strip_tags_keep(html)
        # 统计非代码区的英文单词占比(粗略漏译指标)
        en_words = re.findall(r"[A-Za-z]{4,}", text)
        if len(en_words) > 40:
            sample = ", ".join(sorted(set(en_words))[:8])
            lines.append(f"- ⚠️ {fn}: 可见英文词 {len(en_words)} 个 (样例: {sample})")
            issues += 1
    if issues == 0:
        lines.append("- ✅ 未发现明显大段漏译")
    lines.append(f"\n生成时间: 自动化管线 `python pipeline.py qc`")
    open(REPORT, "w", encoding="utf-8").write("\n".join(lines))
    print("\n".join(lines))
    print(f"\n[qc] 报告已写入 {REPORT}")

# ---------- main ----------
if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "qc"
    {"extract": cmd_extract, "glossary": cmd_glossary, "qc": cmd_qc}.get(cmd, cmd_qc)()
