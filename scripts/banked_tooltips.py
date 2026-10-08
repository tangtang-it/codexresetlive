# -*- coding: utf-8 -*-
import html

BANKED_TOOLTIPS = {
    "zh-hans": "这是一张重置卡：要在 Codex 的「设置 → 用量」里手动使用才会生效。",
    "zh-hant": "這是一張重置卡：要在 Codex 的「設定 → 用量」裡手動使用才會生效。",
    "en": 'This is a Banked Reset: You must manually redeem it under Codex "Settings → Usage" to apply.',
    "ja": "これはバンク枠（リセットカード）です：Codexの「設定 → 利用状況」から手動で適用する必要があります。",
    "ko": "뱅크 리셋 카드입니다: Codex의 '설정 → 사용량'에서 직접 활성화해야 적용됩니다.",
    "es": 'Es un Banked Reset: Debes canjearlo manualmente en "Ajustes → Uso" de Codex.',
    "de": 'Dies ist ein Banked Reset: Muss unter Codex "Einstellungen → Nutzung" manuell eingelöst werden.',
    "fr": 'Il s\'agit d\'un Banked Reset: À activer manuellement dans "Paramètres → Utilisation" de Codex.',
    "pt-br": 'Este é um Banked Reset: Deve ser resgatado manualmente em "Configurações → Uso" do Codex.',
    "ru": "Это накопительный сброс (Banked Reset): его нужно вручную активировать в «Настройки → Использование» в Codex."
}

def render_banked_badge(code, badge_text="BANKED"):
    tip = BANKED_TOOLTIPS.get(code, BANKED_TOOLTIPS["en"])
    tip_esc = html.escape(tip, quote=True)
    return (
        '<span class="banked-wrap" tabindex="0" onclick="this.classList.toggle(\'active\')">'
        f'<span class="badge banked">{badge_text}</span>'
        '<span class="banked-info-icon" title="查看使用说明">?</span>'
        f'<span class="banked-tooltip">{tip_esc}</span>'
        '</span>'
    )

def render_stream_items(recs, code, esc_func):
    items = []
    for r in recs[-10:][::-1]:
        t = r["type"]
        if t == "banked":
            b_html = render_banked_badge(code, "BANKED")
        else:
            b_html = f'<span class="badge {t}">{t.upper()}</span>'
        
        quote = esc_func(r["text"])
        ts_utc = r["at"][:16].replace("T", " ") + " UTC"
        url = r["url"]
        
        item_html = (
            '<div class="post-mini">\n'
            '  <div class="pm-head">\n'
            '    <span class="pm-author">Tibo <span style="font-weight:400;color:var(--muted)">@thsottiaux</span></span>\n'
            f'    {b_html}\n'
            '  </div>\n'
            f'  <div class="pm-quote">{quote}</div>\n'
            '  <div class="pm-foot">\n'
            f'    <span data-utc="{r["at"]}">{ts_utc}</span>\n'
            f'    <a href="{url}" target="_blank" rel="noopener nofollow" style="color:var(--primary)">View on X &#x2197;</a>\n'
            '  </div>\n'
            '</div>'
        )
        items.append(item_html)
    return "".join(items)
