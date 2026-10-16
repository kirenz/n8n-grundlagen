"""Nachgezeichnete n8n-Ansichten (Canvas und Knoten-Panel) als SVG.

Keine Screenshots: Die Bilder werden aus den Workflow-Dateien und kurzen
Panel-Beschreibungen erzeugt und tragen den Hinweis „Darstellung, kein Screenshot“.
"""

import json
from html import escape

F = 'font-family="Inter, Helvetica, Arial, sans-serif"'
INK, MUTED, RULE, BG = "#18181b", "#6b7280", "#d1d5db", "#f6f6f7"
EXPR_BG, EXPR_FG = "#eef6ec", "#2f7a26"
NOTE = "Darstellung nach n8n, kein Screenshot"

TYPE = {
    "n8n-nodes-base.formTrigger": ("form", "#ee6b3a", True),
    "n8n-nodes-base.manualTrigger": ("manual", "#6b7280", True),
    "n8n-nodes-base.scheduleTrigger": ("clock", "#d97706", True),
    "n8n-nodes-base.if": ("if", "#2f7a26", False),
    "n8n-nodes-base.set": ("set", "#4f46e5", False),
    "n8n-nodes-base.wait": ("wait", "#be185d", False),
    "n8n-nodes-base.dataTable": ("table", "#ea580c", False),
    "n8n-nodes-base.summarize": ("sum", "#0d9488", False),
    "n8n-nodes-base.emailSend": ("mail", "#6b7280", False),
    "@n8n/n8n-nodes-langchain.chainLlm": ("chain", "#7c3aed", False),
    "@n8n/n8n-nodes-langchain.lmChatGoogleGemini": ("gemini", "#2563eb", False),
}


def t(x, y, s, size=13, weight=400, fill=INK, anchor="start", mono=False):
    fam = 'font-family="ui-monospace, Menlo, monospace"' if mono else F
    return f'<text x="{x}" y="{y}" {fam} font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{escape(str(s))}</text>'


def icon(kind, cx, cy, col):
    s = f'stroke="{col}" stroke-width="2.5" fill="none" stroke-linecap="round"'
    if kind == "form":
        return f'<rect x="{cx-12}" y="{cy-15}" width="24" height="30" rx="3" {s}/>' + "".join(f'<line x1="{cx-7}" y1="{cy-7+i*7}" x2="{cx+7}" y2="{cy-7+i*7}" {s}/>' for i in range(3))
    if kind == "manual":
        return f'<path d="M{cx-8},{cy-12} L{cx-8},{cy+10} L{cx-2},{cy+4} L{cx+4},{cy+14} L{cx+8},{cy+12} L{cx+2},{cy+2} L{cx+10},{cy+2} Z" {s}/>'
    if kind == "clock":
        return f'<circle cx="{cx}" cy="{cy}" r="14" {s}/><path d="M{cx},{cy-8} L{cx},{cy} L{cx+7},{cy+4}" {s}/>'
    if kind == "if":
        return f'<path d="M{cx-14},{cy} L{cx-2},{cy} M{cx-2},{cy} L{cx+12},{cy-10} M{cx-2},{cy} L{cx+12},{cy+10}" {s}/>'
    if kind == "set":
        return f'<path d="M{cx-12},{cy+12} L{cx-10},{cy+4} L{cx+6},{cy-12} L{cx+12},{cy-6} L{cx-4},{cy+10} Z" {s}/>'
    if kind == "wait":
        return f'<line x1="{cx-5}" y1="{cy-12}" x2="{cx-5}" y2="{cy+12}" {s}/><line x1="{cx+5}" y1="{cy-12}" x2="{cx+5}" y2="{cy+12}" {s}/>'
    if kind == "table":
        return f'<rect x="{cx-14}" y="{cy-12}" width="28" height="24" rx="2" {s}/><line x1="{cx-14}" y1="{cy-4}" x2="{cx+14}" y2="{cy-4}" {s}/><line x1="{cx}" y1="{cy-12}" x2="{cx}" y2="{cy+12}" {s}/>'
    if kind == "sum":
        return t(cx, cy + 10, "Σ", 28, 700, col, "middle")
    if kind == "mail":
        return f'<rect x="{cx-14}" y="{cy-10}" width="28" height="20" rx="2" {s}/><path d="M{cx-14},{cy-10} L{cx},{cy+2} L{cx+14},{cy-10}" {s}/>'
    if kind == "chain":
        return t(cx, cy + 7, "KI", 20, 800, col, "middle")
    if kind == "gemini":
        return f'<path d="M{cx},{cy-14} C{cx+2},{cy-2} {cx+2},{cy-2} {cx+14},{cy} C{cx+2},{cy+2} {cx+2},{cy+2} {cx},{cy+14} C{cx-2},{cy+2} {cx-2},{cy+2} {cx-14},{cy} C{cx-2},{cy-2} {cx-2},{cy-2} {cx},{cy-14} Z" fill="{col}"/>'
    return ""


def canvas(workflow_file, title, highlight=None, width=900):
    """Canvas-Ansicht eines Workflows. highlight: Name eines Knotens, der markiert wird."""
    w = json.load(open(workflow_file, encoding="utf-8"))
    nodes = {n["name"]: n for n in w["nodes"]}
    xs = [n["position"][0] for n in w["nodes"]]
    ys = [n["position"][1] for n in w["nodes"]]
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    span = max(maxx - minx, 1)
    scale = min(1.0, (width - 220) / span)
    ox, oy = 90 - minx * scale, 90 - miny * scale
    H = int((maxy - miny) * scale + 230)

    def pos(n):
        return n["position"][0] * scale + ox, n["position"][1] * scale + oy

    sz = 80
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {H}" width="{width}" height="{H}">',
           '<defs><pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="#d4d4d8"/></pattern>'
           f'<marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#9ca3af"/></marker></defs>',
           f'<rect width="{width}" height="{H}" fill="{BG}"/><rect width="{width}" height="{H}" fill="url(#dots)"/>',
           t(20, 28, title, 15, 700)]
    for src, c in w["connections"].items():
        for ctype, outs in c.items():
            for oi, targets in enumerate(outs):
                for tg in targets:
                    a, b = nodes[src], nodes[tg["node"]]
                    (x1, y1), (x2, y2) = pos(a), pos(b)
                    if ctype == "ai_languageModel":
                        out.append(f'<path d="M{x1+sz/2},{y1} L{x2+sz/2},{y2+sz+26}" stroke="#9ca3af" stroke-width="2" stroke-dasharray="5 4" fill="none"/>')
                        out.append(t(x2 + sz / 2 + 8, (y1 + y2 + sz) / 2 + 16, "Model", 11, 600, MUTED))
                        continue
                    sx, sy = x1 + sz, y1 + sz / 2
                    if a["type"].endswith(".if"):
                        sy = y1 + (sz * 0.3 if oi == 0 else sz * 0.7)
                    ex, ey = x2, y2 + sz / 2
                    mx = (sx + ex) / 2
                    out.append(f'<path d="M{sx},{sy} C{mx},{sy} {mx},{ey} {ex-4},{ey}" stroke="#9ca3af" stroke-width="2" fill="none" marker-end="url(#ar)"/>')
                    if a["type"].endswith(".if"):
                        out.append(t(sx + 8, sy - 6, "true" if oi == 0 else "false", 11, 600, "#2f7a26" if oi == 0 else "#b91c1c"))
    for n in w["nodes"]:
        x, y = pos(n)
        kind, col, trig = TYPE.get(n["type"], ("set", MUTED, False))
        sub = n["type"].endswith("lmChatGoogleGemini")
        hl = highlight == n["name"]
        stroke = "#ff6d5a" if hl else "#c7c7cc"
        if sub:
            out.append(f'<circle cx="{x+sz/2}" cy="{y+sz/2}" r="{sz/2-4}" fill="#ffffff" stroke="{stroke}" stroke-width="{3 if hl else 1.5}"/>')
        else:
            rx = f'<path d="M{x+sz*0.45},{y} L{x+sz-10},{y} Q{x+sz},{y} {x+sz},{y+10} L{x+sz},{y+sz-10} Q{x+sz},{y+sz} {x+sz-10},{y+sz} L{x+sz*0.45},{y+sz} Q{x},{y+sz} {x},{y+sz/2} Q{x},{y} {x+sz*0.45},{y} Z" fill="#ffffff" stroke="{stroke}" stroke-width="{3 if hl else 1.5}"/>' if trig else f'<rect x="{x}" y="{y}" width="{sz}" height="{sz}" rx="10" fill="#ffffff" stroke="{stroke}" stroke-width="{3 if hl else 1.5}"/>'
            out.append(rx)
            if trig:
                out.append(f'<path d="M{x-16},{y+sz/2-8} L{x-22},{y+sz/2+1} L{x-17},{y+sz/2+1} L{x-20},{y+sz/2+9} L{x-12},{y+sz/2-2} L{x-17},{y+sz/2-2} Z" fill="#ff6d5a"/>')
        out.append(icon(kind, x + sz / 2, y + sz / 2, col))
        label = n["name"]
        out.append(t(x + sz / 2, y + sz + 18, label, 12, 600, INK, "middle"))
    out.append(t(width - 16, H - 12, NOTE, 11, 400, MUTED, "end"))
    out.append("</svg>")
    return "".join(out)


def wrap(s, n):
    words, lines, cur = str(s).split(" "), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > n:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    return lines + [cur] if cur else lines


def panel(node_name, kind_type, rows, width=760, hint=None):
    """Knoten-Panel. rows: (Label, Wert, Modus) mit Modus fixed|expr|select|toggle|section|list."""
    kind, col, _ = TYPE.get(kind_type, ("set", MUTED, False))
    y = 70
    body = []
    for label, value, mode in rows:
        if mode == "section":
            body.append(t(24, y + 18, label, 12, 700, MUTED))
            y += 30
            continue
        body.append(t(24, y + 15, label, 13, 600))
        y += 24
        lines = wrap(value, int((width - 110) / 7.9)) if mode == "expr" else [value]
        h = 34 if mode not in ("list", "expr") else (24 * len(value) + 14 if mode == "list" else 20 * len(lines) + 14)
        if mode == "expr":
            body.append(f'<rect x="24" y="{y}" width="{width-48}" height="{h}" rx="6" fill="{EXPR_BG}" stroke="#b7dcae"/>')
            body.append(f'<rect x="30" y="{y+7}" width="24" height="20" rx="4" fill="#ffffff" stroke="#b7dcae"/>' + t(42, y + 21, "fx", 11, 700, EXPR_FG, "middle"))
            for li, line in enumerate(lines):
                body.append(t(64, y + 22 + li * 20, line, 13, 500, EXPR_FG, mono=True))
        elif mode == "toggle":
            body.append(f'<rect x="24" y="{y+6}" width="40" height="22" rx="11" fill="#ff6d5a"/><circle cx="53" cy="{y+17}" r="8" fill="#ffffff"/>' + t(74, y + 22, value, 13))
        elif mode == "list":
            body.append(f'<rect x="24" y="{y}" width="{width-48}" height="{h}" rx="6" fill="#ffffff" stroke="{RULE}"/>')
            for i, v in enumerate(value):
                body.append(t(40, y + 24 + i * 24, "• " + v, 13))
        else:
            body.append(f'<rect x="24" y="{y}" width="{width-48}" height="{h}" rx="6" fill="#ffffff" stroke="{RULE}"/>')
            body.append(t(36, y + 22, value, 13, 400, INK, mono=(mode == "fixed" and value[:1] in "{=")))
            if mode == "select":
                body.append(f'<path d="M{width-46},{y+14} L{width-40},{y+20} L{width-34},{y+14}" stroke="{MUTED}" stroke-width="2" fill="none"/>')
        y += h + 14
    if hint:
        body.append(f'<rect x="24" y="{y}" width="{width-48}" height="40" rx="6" fill="#fff7ed" stroke="#fed7aa"/>' + t(36, y + 25, hint, 12, 500, "#9a3412"))
        y += 52
    H = y + 30
    head = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {H}" width="{width}" height="{H}">',
            f'<rect width="{width}" height="{H}" rx="10" fill="#ffffff" stroke="{RULE}"/>',
            f'<rect width="{width}" height="52" rx="10" fill="{BG}"/><rect y="40" width="{width}" height="12" fill="{BG}"/>',
            f'<line x1="0" y1="52" x2="{width}" y2="52" stroke="{RULE}"/>', icon(kind, 36, 26, col),
            t(62, 31, node_name, 15, 700), t(width - 20, 31, "Parameters", 12, 600, "#ff6d5a", "end")]
    return "".join(head + body + [t(width - 16, H - 10, NOTE, 11, 400, MUTED, "end"), "</svg>"])
