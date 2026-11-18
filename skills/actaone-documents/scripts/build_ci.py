"""Render structured report content with the existing actaOne concept layout.

Derived from outputs/hardware-konzept/build.py (page structure and Chromium PDF).
Report content is supplied as JSON, never copied from the original report.
"""
import argparse
import html
import json
import shutil
from pathlib import Path


SKILL = Path(__file__).resolve().parents[1]


def esc(value):
    return html.escape(str(value), quote=True)


def block(item):
    kind = item['type']
    if kind in ('paragraph', 'heading', 'note'):
        tag, cls = {'paragraph': ('p', ''), 'heading': ('h3', ''),
                    'note': ('p', 'note')}[kind]
        return f'<{tag} class="{cls}">{esc(item["text"])}</{tag}>'
    if kind == 'list':
        return '<ul class="keys">' + ''.join(f'<li>{esc(x)}</li>' for x in item['items']) + '</ul>'
    if kind == 'table':
        headers = item['headers']
        if not headers or any(len(row) != len(headers) for row in item['rows']):
            raise ValueError('Table rows must match the nonempty header list')
        head = ''.join(f'<th>{esc(x)}</th>' for x in headers)
        rows = ''.join('<tr>' + ''.join(f'<td>{esc(x)}</td>' for x in row) + '</tr>' for row in item['rows'])
        return f'<table class="t"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table>'
    if kind == 'tiles':
        if not 1 <= len(item['items']) <= 4:
            raise ValueError('Use one to four tiles per block')
        return '<div class="tiles">' + ''.join(
            f'<div class="tile"><div class="tl">{esc(x["label"])}</div>'
            f'<div class="tv">{esc(x["value"])}</div><div class="tn">{esc(x.get("note", ""))}</div></div>'
            for x in item['items']) + '</div>'
    raise ValueError(f'Unknown block type: {kind}')


def document(data):
    title, subtitle = esc(data['title']), esc(data.get('subtitle', ''))
    date, label = esc(data.get('date', '')), esc(data.get('label', 'entwurf'))
    sections = data['sections']
    if not isinstance(sections, list) or not sections:
        raise ValueError('Provide at least one section')
    pages = [f'''<section class="page cover"><div class="band"></div>
      <div class="content"><div class="cover-top"><img src="assets/actaone-logo-sm.png" class="logo" alt="actaOne"></div>
      <div class="cover-main"><div class="kicker">{label}</div><div class="ctitle">{title}</div>
      <div class="csub">{subtitle}</div><div class="cmeta">{date}</div></div></div>
      <div class="cover-foot">actaOne · {label}</div></section>''']
    for n, section in enumerate(sections, 2):
        body = ''.join(block(item) for item in section['blocks'])
        pages.append(f'''<section class="page"><div class="band"></div><div class="content">
          <div class="eyebrow">{esc(section.get('eyebrow', ''))}</div><h1>{esc(section['title'])}</h1>{body}</div>
          <div class="foot"><span>actaOne · {label}</span><span>{date} · Seite {n} von {len(sections)+1}</span></div></section>''')
    return f'''<!doctype html><html lang="de"><head><meta charset="utf-8">
      <title>{title}</title><link rel="stylesheet" href="style.css">
      <style>.content {{ display: flow-root; overflow-wrap: anywhere; }}
      .t {{ table-layout: fixed; }} .foot {{ gap: 4mm; }}</style></head><body>{''.join(pages)}</body></html>'''


def render(folder, browser_path=None):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=browser_path)
        try:
            page = browser.new_page()
            # This template is self-contained: do not fetch external assets or fonts.
            page.route('http://**/*', lambda route: route.abort())
            page.route('https://**/*', lambda route: route.abort())
            page.emulate_media(media='print')
            page.goto((folder / 'index.html').as_uri(), wait_until='load')
            page.evaluate("Promise.all([400, 600, 700].map(w => document.fonts.load(`${w} 12px Inter`)))")
            page.evaluate('document.fonts.ready')
            if not page.evaluate("Array.from(document.fonts).every(f => f.status === 'loaded')"):
                raise RuntimeError('A bundled font failed to load')
            if not page.evaluate('Array.from(document.images).every(i => i.complete && i.naturalWidth > 0)'):
                raise RuntimeError('A bundled image failed to load')
            overflow = page.evaluate('''() => Array.from(document.querySelectorAll('.page')).flatMap((p, i) => {
                const c = p.querySelector('.content');
                const f = p.querySelector('.foot, .cover-foot');
                const r = c.getBoundingClientRect();
                const limit = f.getBoundingClientRect().top - 12;
                return r.bottom > limit || c.scrollWidth > c.clientWidth + 1 || f.scrollWidth > f.clientWidth + 1
                    ? [i + 1] : [];
            })''')
            if overflow:
                raise RuntimeError(f'Content exceeds page area on pages {overflow}; split sections before exporting')
            page.pdf(path=str(folder / 'document.pdf'), prefer_css_page_size=True,
                     print_background=True, display_header_footer=False)
        finally:
            browser.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path, help='JSON content; see examples/report.json')
    parser.add_argument('--output', type=Path, required=True, help='New output directory (must not exist)')
    parser.add_argument('--browser', help='Path to installed Chrome/Edge; otherwise Playwright Chromium')
    parser.add_argument('--html-only', action='store_true', help='Generate source without PDF/layout checks')
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding='utf-8-sig'))
    markup = document(data)
    folder = args.output.resolve()
    folder.mkdir(parents=True, exist_ok=False)
    shutil.copytree(SKILL / 'assets' / 'ci', folder, dirs_exist_ok=True)
    (folder / 'index.html').write_text(markup, encoding='utf-8')
    (folder / 'content.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    if not args.html_only:
        render(folder, args.browser)
    print(folder / ('index.html' if args.html_only else 'document.pdf'))


if __name__ == '__main__':
    main()
