"""
Inspect the ActiveData schema. For example, to see all available tables in ActiveData, run:

.. code-block:: bash

    adr inspect

To see the attributes in a given table run:

.. code-block:: bash

    adr inspect --table <name>
"""
from __future__ import absolute_import, print_function

from adr.context import override
from adr.query import run_query

RUN_CONTEXTS = [
    override('attribute', default=None),
]


def run(args):

    if not args.table:
        data = run_query('meta', args)['edges'][0]['domain']['partitions']
        data = sorted([(d['name'],) for d in data])
        data.insert(0, ('Table',))
        return data

    if not args.attribute:
        data = run_query('meta_columns', args)['data']
        data = sorted([(d['name'],) for d in data])
        data.insert(0, ('Column',))
        return data

    data = run_query('meta_values', args)['data']
    data.insert(0, (args.attribute, 'count'))
    return data
