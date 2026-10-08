import pathlib

head_path = pathlib.Path('_tpl_head_v2.html')
head_txt = head_path.read_text('utf-8')
target_head = '.col-t{font-size:13px;font-weight:700;color:var(--on-dark);text-transform:uppercase;letter-spacing:.4px}'
replace_head = '.col-t{font-size:13px;font-weight:700;color:var(--on-dark);text-transform:uppercase;letter-spacing:.4px;display:inline-flex;align-items:center;gap:8px}\n.col-t-avatar{width:22px;height:22px;border-radius:50%;object-fit:cover;border:1px solid rgba(255,255,255,0.18);box-shadow:0 1px 3px rgba(0,0,0,0.35);flex-shrink:0}'

if target_head in head_txt:
    head_txt = head_txt.replace(target_head, replace_head, 1)
    head_path.write_text(head_txt, 'utf-8')
    print('Head updated successfully.')
else:
    print('Target not found in head!')

body_path = pathlib.Path('_tpl_body_v2.html')
body_txt = body_path.read_text('utf-8')
target_body = '<span class="col-t">Tibo Sottiaux (@thsottiaux)</span>'
replace_body = '<span class="col-t"><img class="col-t-avatar" src="/assets/avatars/tibo.jpg" alt="Tibo Sottiaux" width="22" height="22" loading="lazy">Tibo Sottiaux (@thsottiaux)</span>'

if target_body in body_txt:
    body_txt = body_txt.replace(target_body, replace_body, 1)
    body_path.write_text(body_txt, 'utf-8')
    print('Body updated successfully.')
else:
    print('Target not found in body!')
