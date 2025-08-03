#!/usr/bin/env python3

import sys
sys.path.append('glyphd/src')

from glyphd.core.dependencies.gpu_models import get_gpu_models

try:
    models = get_gpu_models()
    print(f'Successfully loaded {len(models)} GPU models')
    if models:
        print('First model:')
        first_model = models[0]
        print(f'  Model: {first_model.model}')
        print(f'  Listing Count: {first_model.listing_count}')
        print(f'  Min Price: {first_model.min_price}')
        print(f'  Avg Price: {first_model.avg_price}')
        print('\nAll models loaded:')
        for model in models:
            print(f'  - {model.model}: {model.listing_count} listings, avg ${model.avg_price:.2f}')
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()