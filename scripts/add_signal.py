# -*- coding: utf-8 -*-
"""
Single-command signal entry & full-site compiler pipeline.
Usage:
  python scripts/add_signal.py --id <tweet_id> --text "..." --type release --time 2026-10-09T20:38:12.000Z
"""
import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "tibo_reset_history.json"

def main():
    parser = argparse.ArgumentParser(description='Add a verified signal and rebuild radar site.')
    parser.add_argument('--id', required=True, help='Tweet or signal ID')
    parser.add_argument('--text', required=True, help='Signal text')
    parser.add_argument('--time', default=None, help='ISO8601 UTC timestamp, defaults to now')
    parser.add_argument('--type', default='release', choices=['release', 'announcement', 'regular', 'banked'], help='Signal type')
    parser.add_argument('--status', default='confirmed', help='Signal status')
    args = parser.parse_args()

    tid = str(args.id).strip()
    if not re.fullmatch(r'[0-9]{18,20}', tid):
        print(f'[ERROR] Invalid Tweet ID format: {tid}')
        sys.exit(1)

    at = args.time or datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z')

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    records = data.get('records', [])
    rec_map = {r['id']: r for r in records}

    new_record = {
        'id': tid,
        'at': at,
        'type': args.type,
        'status': args.status,
        'text': args.text.strip(),
        'url': f'https://x.com/thsottiaux/status/{tid}'
    }

    rec_map[tid] = new_record
    sorted_recs = sorted(rec_map.values(), key=lambda x: x['at'])
    data['records'] = sorted_recs
    data['total'] = len(sorted_recs)

    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f'[SUCCESS] Recorded signal {tid} in {DATA_FILE}. Total count: {len(sorted_recs)}')

    # Run compute_stats.py
    print('[PIPELINE] Running compute_stats.py...')
    subprocess.check_call([sys.executable, str(ROOT / 'scripts' / 'compute_stats.py')])

    # Run build_studio.py
    print('[PIPELINE] Running build_studio.py...')
    subprocess.check_call([sys.executable, str(ROOT / 'scripts' / 'build_studio.py')])

    # Run verify_site.py
    print('[PIPELINE] Running verify_site.py...')
    subprocess.check_call([sys.executable, str(ROOT / 'scripts' / 'verify_site.py')])
    print('[DONE] Pipeline finished successfully!')

if __name__ == '__main__':
    main()