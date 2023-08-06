from typing import List, Union

from europy.lifecycle.reporting import put_test
from europy.lifecycle.result import TestLabel
from europy.lifecycle.result_promise import TestPromise


def decorator_factory(labels: List[Union[str, TestLabel]],
                      name: str = "",
                      description: str = ""):
    def inner_wrapper(func):
        put_test(TestPromise(name, labels, func, description))

        return func

    return inner_wrapper
