# Copyright 2017 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import functools


def grpc_call(fx):
    """Decorator which duplicates the gRPC .with_call interface for RPCs.

    The way this work is that ``callable`` is expected to call an underlying
    gRPC method using ``with_call``; this replaces the callable with a
    :class:`ServiceCall` instance, which gets rid of the returned call
    when it is not needed.

    Args:
        fx (Callable): The callable (usually function) being decorated.

    Returns:
        ServiceCall: A service call instance, which can keep or discard
            the call metadata as appropriate.
    """
    return type('ServiceCall', (object,), {
        '__call__': functools.update_wrapper(
            lambda self, *args, **kwargs: fx(self, *args, **kwargs)[0],
            fx,
        ),
        'with_call': functools.update_wrapper(
            lambda self, *args, **kwargs: fx(self, *args, **kwargs),
            fx,
        ),
    })
