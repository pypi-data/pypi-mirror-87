import typing

from momotor.bundles.elements.steps import Step
from momotor.bundles.exception import CircularDependencies

__all__ = ['get_complete_step_dependencies']


def get_complete_step_dependencies(steps: typing.Mapping[str, Step]) \
        -> typing.Tuple[typing.Dict[str, typing.Set[str]], typing.Dict[str, typing.Set[str]]]:

    dependencies = {
        step_id: set(depends.step for depends in step.depends)
        for step_id, step in steps.items()
    }

    full_deps = {}

    def _get_full_deps(step_id, previous):
        if step_id in full_deps:
            return full_deps[step_id]

        previous = previous | {step_id}  # Do not use |=, it needs to be a new set
        step_deps = set(dependencies[step_id])
        for full_dep_id in dependencies[step_id]:
            if full_dep_id in previous:
                raise CircularDependencies("Recipe contains circular reference in step dependencies")

            step_deps |= _get_full_deps(full_dep_id, previous)

        full_deps[step_id] = step_deps
        return step_deps

    reverse_deps = {
        step_id: set() for step_id in steps.keys()
    }

    for step_id in dependencies.keys():
        for dep_id in _get_full_deps(step_id, set()):
            reverse_deps[dep_id].add(step_id)

    return full_deps, reverse_deps
