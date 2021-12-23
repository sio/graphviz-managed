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


def test_samples_readme():
    '''Check that all code samples are included into README'''
    with open('README.md') as f:
        readme = f.read()
    samples_count = 0
    for child in SAMPLES_DIRECTORY.iterdir():
        if child.suffix != '.py':
            continue
        sample = get_sample(child)
        assert sample in readme
        samples_count += 1
    assert samples_count == SAMPLES_COUNT


def get_sample(path):
    '''Retrieve code sample from a path object'''
    start = r'# ---8<--- START SAMPLE ---8<---'
    end   = r'# ---8<--- END SAMPLE ---8<---'
    sample_lines = []
    collect = False
    with open(path) as f:
        for line in f:
            if line.strip() == end:
                break
            if collect:
                sample_lines.append(line)
            if line.strip() == start:
                collect = True
        else:
            raise ValueError(f'sample markers not found in {path}')
    return ''.join(sample_lines).strip()
