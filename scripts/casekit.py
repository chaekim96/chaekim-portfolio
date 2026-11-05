"""Small HTML helpers for the case-study copy in scripts/projects/<slug>.py."""
import html


def confirm_tag(msg):  # visible confirm tag
    return f'<span class="confirm">[CONFIRM: {html.escape(msg)}]</span>'

def paras(*texts):
    return "\n".join(f"        <p>{x}</p>" for x in texts)

def bullets(*items):
    return "        <ul>\n" + "\n".join(f"          <li>{x}</li>" for x in items) + "\n        </ul>"

def stat_grid(*pairs):
    cells = "".join(f'<div><b>{b}</b><span>{s}</span></div>' for b, s in pairs)
    return f'        <div class="results">{cells}</div>'

def artifact_grid(*items):
    """items: (src, caption) for real images, or ('', caption) for a placeholder."""
    out = []
    for src, cap in items:
        if src:
            out.append(f'<figure><img src="{src}" alt="{html.escape(cap)}" loading="lazy"><figcaption>{cap}</figcaption></figure>')
        else:
            out.append(f'<div class="ph">{confirm_tag(cap)}</div>')
    return '        <div class="artifacts">' + "".join(out) + "</div>"

def links(*pairs):
    return "        <p>" + " · ".join(f'<a href="{u}" target="_blank" rel="noopener">{t} ↗</a>' for t, u in pairs) + "</p>"

def cover(src, alt, w=960, h=600):
    return f'<img src="{src}" alt="{html.escape(alt)}" width="{w}" height="{h}">'
