from argparse import ArgumentParser
from contextlib import closing
from itertools import starmap
from logging import warning
from os import sched_getaffinity, sysconf
from re import compile
from typing import Any, Callable, Iterator, List, Mapping, Optional, Tuple

from pylxd import Client
from pylxd.models import Container
from tabulate import tabulate

__all__ = [
    'print_resources',
    'run_print_resources_script',
]


_DEFAULT_CPU_COUNT = len(sched_getaffinity(0))
_DEFAULT_MEMORY_GB = sysconf('SC_PAGE_SIZE') * sysconf('SC_PHYS_PAGES') * 2**-30

_PRINT_HEADERS = ('Container', 'CPU', 'Memory', 'HDD', 'Network', 'Profiles')

_MEMORY_UNIT_MULTIPLICATION_MAP = {
    'b': 2**-30,
    'kb': 2**-20,
    'mb': 2**-10,
    'gb': 1,
    'tb': 2**10,
}

_MEMORY_PATTERN = compile(
    r'^\s*(\d+(?:\.\d+)?)\s*(?i:({}))?\s*$'.format(
        '|'.join(_MEMORY_UNIT_MULTIPLICATION_MAP)
    )
)


def _format_size(size_gb: Optional[float]) -> str:
    """Format memory size in GB to string."""
    return size_gb and '{:.2f} GB'.format(size_gb) or 'UNKNOWN'


def _parse_size_to_gb(
    memory_size: str,
    warning_callback: Callable[[str], None]
) -> Optional[float]:
    """Memory size string parsing to GB units."""
    try:
        memory_size, memory_unit = _MEMORY_PATTERN.match(memory_size).groups()

    except (ValueError, AttributeError):
        warning_callback(memory_size)
        return

    try:
        memory_factor = _MEMORY_UNIT_MULTIPLICATION_MAP[memory_unit.lower()]

    except KeyError:
        warning_callback(memory_size)
        return

    try:
        return memory_factor * float(memory_size)

    except (ValueError, TypeError):
        warning_callback(memory_size)


def _iter_disk_devices(
    container_name: str,
    devices: Mapping[str, Mapping[str, Any]],
) -> Iterator[Tuple[str, Optional[float]]]:
    for device in devices.values():
        if device['type'] != 'disk':
            continue

        yield device['path'], _parse_size_to_gb(
            device.get('size', ''),
            lambda memory: warning(
                'Unknown disk units {!r} for {!r}.'.format(
                    memory,
                    container_name,
                ),
            ),
        )


def _iter_resources(containers: List[Container]) -> Iterator[Tuple[str, ...]]:
    """Iterate over containers to fetch resources data."""
    total_memory_gb = 0.0
    total_disk_gb = 0.0

    def format_disk(path: str, disk_size_gb: Optional[float]):
        nonlocal total_disk_gb
        total_disk_gb += disk_size_gb or 0.0
        return '{!r}: {}'.format(path, _format_size(disk_size_gb))

    for container in containers:
        config = container.expanded_config
        devices = container.expanded_devices

        container_name = container.name
        container_status = container.status

        memory_size_gb = _parse_size_to_gb(
            config.get('limits.memory', '{}GB'.format(_DEFAULT_MEMORY_GB)),
            lambda memory: warning(
                'Unknown memory units {!r} for {!r}.'.format(
                    memory,
                    container_name,
                ),
            ),
        )
        if container_status.lower() == 'running':
            total_memory_gb += memory_size_gb or 0.0

        yield (
            '{} ({})'.format(container_name, container_status),
            '{} (allowance: {})'.format(
                config.get('limits.cpu', _DEFAULT_CPU_COUNT),
                config.get('limits.cpu.allowance', '100%'),
            ),
            _format_size(memory_size_gb),
            '\n'.join(
                starmap(
                    format_disk,
                    _iter_disk_devices(container_name, devices),
                )
            ),
            '\n'.join(
                (
                    '{}: {}'.format(
                        device['nictype'],
                        device['parent'],
                    )
                    for device in devices.values()
                    if device['type'] == 'nic'
                )
            ),
            '\n'.join(container.profiles),
        )

    yield (
        '=== SUMMARY ===',
        '',
        '{:.2f} GB ({:.2%})'.format(
            total_memory_gb,
            total_memory_gb / _DEFAULT_MEMORY_GB,
        ),
        '{:.2f} GB'.format(total_disk_gb),
        '',
        '',
    )


def print_resources(client: Client):
    print(tabulate(
        tuple(_iter_resources(client.containers.all())),
        _PRINT_HEADERS,
        tablefmt='grid',
    ))


def run_print_resources_script():
    parser = ArgumentParser(description='Tool for displaying  LXD containers '
                                        'actual resources.')
    parser.add_argument('-e',
                        '--endpoint',
                        help='LXD endpoint to connect to.',
                        required=False,
                        default=None)
    parser.add_argument('-c',
                        '--cert-filepath',
                        help='LXD certificate file path to connect over '
                             'endpoint.',
                        required=False,
                        default=None)
    parser.add_argument('-k',
                        '--key-filepath',
                        help='LXD private key file path to connect over '
                             'endpoint.',
                        required=False,
                        default=None)

    args = parser.parse_args()

    client = Client(
        endpoint=args.endpoint,
        cert=None if (
            args.cert_filepath is None or args.key_filepath is None
        ) else (args.cert_filepath, args.key_filepath),
    )

    with closing(client.api.session):
        print_resources(client)
