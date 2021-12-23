'''
Check that all samples are up to date
'''

import pytest
from pathlib import Path

SAMPLES_DIRECTORY = Path('samples')
SAMPLES_COUNT = 4
SAMPLES_DEFAULT_RENDER = 'svg'
SAMPLES_CUSTOM_RENDER = {
    'diag': 'png',
}

def test_samples_rendered():
    '''Check that all code samples have been rendered'''
    if not SAMPLES_DIRECTORY.exists():
        raise ValueError(f'directory not found: {SAMPLES_DIRECTORY}')
    samples_count = 0
    for child in SAMPLES_DIRECTORY.iterdir():
        if child.suffix != '.py':
            continue
        samples_count += 1
        suffix = SAMPLES_DEFAULT_RENDER
        if child.stem in SAMPLES_CUSTOM_RENDER:
            suffix = SAMPLES_CUSTOM_RENDER[child.stem]
        assert child.with_suffix(f'.{suffix}').exists()
    assert samples_count == SAMPLES_COUNT
