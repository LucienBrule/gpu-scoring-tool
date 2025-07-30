#!/usr/bin/env python3
"""
Test script to verify WamatekShopifyLoader works with real data.
"""

import json
import tempfile
from pathlib import Path

from glyphsieve.core.ingest.shopify.wamatek_loader import WamatekShopifyLoader


def main():
    loader = WamatekShopifyLoader()
    print('Testing WamatekShopifyLoader with real data...')

    # Load only first JSON object to test (lines 1-3515 based on earlier analysis)
    data_file = Path('recon/wamatek/wamatek_cards.jsonl')
    if not data_file.exists():
        print(f'Data file not found: {data_file}')
        return

    # Read first complete JSON object (lines 1-3515)
    with open(data_file, 'r') as f:
        lines = []
        for i, line in enumerate(f, 1):
            lines.append(line)
            if i >= 3515:  # First JSON object ends around line 3515
                break

        json_text = ''.join(lines)
        data = json.loads(json_text)

    print(f'Found {len(data["products"])} products in first JSON object')

    # Test with a small subset (first 3 products only)
    subset_data = {'products': data['products'][:3]}

    # Write subset to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as temp_f:
        json.dump(subset_data, temp_f)
        temp_path = temp_f.name

    try:
        listings = loader.load(temp_path)
        print(f'Successfully loaded {len(listings)} listings')

        if listings:
            print('\nSample listing:')
            for key, value in listings[0].items():
                print(f'  {key}: {value}')

        # Test CSV output
        output_path = Path('tmp/test_wamatek_output.csv')
        output_path.parent.mkdir(exist_ok=True)
        loader.to_input_csv(listings, output_path)
        print(f'\nCSV output written to {output_path}')

        # Show first few lines of CSV
        if output_path.exists():
            print('\nFirst few lines of CSV:')
            with open(output_path, 'r') as f:
                for i, line in enumerate(f):
                    if i < 3:  # Show header + first 2 data rows
                        print(f'  {line.strip()}')

    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    main()
