# Copyright 2020 Software Factory Labs, Inc.
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

from typing import Optional, Callable, Dict, Tuple
from datetime import datetime
import inspect
from .triggers import Trigger
from . import util


class Job:
    def __init__(self,
                 func: Callable,
                 identifier: str,
                 args: Tuple,
                 kwargs: Dict,
                 dynamic_args: Dict[str, Callable],
                 trigger: Trigger,
                 next_run_time: Optional[datetime] = None,
                 description: Optional[str] = None,
                 coalesce: bool = False,
                 max_instances: int = 0):
        self.func = func
        self.id = identifier
        self.args = args
        self.kwargs = kwargs
        self.trigger = trigger
        self.next_run_time = next_run_time
        self.description = description
        self.coalesce = coalesce
        self.max_instances = max_instances

        try:
            self.func_ref = util.obj_to_ref(self.func)
        except ValueError:
            self.func_ref = None

        self.dynamic_args = {}
        for arg_name, arg_func in dynamic_args.items():
            try:
                arg_func_ref = util.obj_to_ref(arg_func)
            except ValueError:
                arg_func_ref = None

            self.dynamic_args[arg_name] = {'func': arg_func, 'func_ref': arg_func_ref}

    def _modify(self, **changes):
        pass

    def _get_run_times(self, latest: datetime):
        run_times = []
        next_run_time = self.next_run_time
        while next_run_time and next_run_time < latest:
            run_times.append(next_run_time)
            next_run_time = self.trigger.get_next_fire_time(next_run_time, latest)
        return run_times

    def __getstate__(self):
        if self.func_ref is None:
            raise Exception(f'Job function ({self.func}) not serializable')

        dynamic_args = {}
        for arg_name, values in self.dynamic_args.items():
            func = values['func']
            func_ref = values['func_ref']
            if func_ref is None:
                raise Exception(f'Job dynamic arg function ({func}) not serializable')
            dynamic_args[arg_name] = func_ref

        if inspect.ismethod(self.func) and not inspect.isclass(self.func.__self__):
            args = (self.func.__self__,) + tuple(self.args)
        else:
            args = self.args

        return {
            'id': self.id,
            'func': self.func_ref,
            'args': args,
            'kwargs': self.kwargs,
            'dynamic_args': dynamic_args,
            'trigger': self.trigger,
            'next_run_time': self.next_run_time,
            'description': self.description,
            'coalesce': self.coalesce,
            'max_instances': self.max_instances
        }

    def __setstate__(self, state):
        self.id = state['id']
        self.func_ref = state['func']
        self.func = util.ref_to_obj(self.func_ref)
        self.args = state['args']
        self.kwargs = state['kwargs']
        self.trigger = state['trigger']
        self.next_run_time = state['next_run_time']
        self.description = state['description']
        self.coalesce = state['coalesce']
        self.max_instances = state['max_instances']

        self.dynamic_args = {}
        for arg_name, func_ref in state['dynamic_args'].items():
            self.dynamic_args[arg_name] = {'func': util.ref_to_obj(func_ref), 'func_ref': func_ref}

    def __eq__(self, other):
        if isinstance(other, Job):
            return self.id == other.id
        return NotImplemented

    def __repr__(self):
        return f'<Job (id={self.id})>'

    def __str__(self):
        status = f'next run at: {self.next_run_time}'
        return f'{self.id} (trigger: {self.trigger}, {status})'
