"""Runner to run on TLM."""

import logging
import pickle
from typing import Dict
from typing import TYPE_CHECKING
from typing import Tuple

import numpy as np

from .runner import Runner

if TYPE_CHECKING:
    from tpu_tlm_is import Executable
    from tpu_tlm_is.base import TensorDescription

__all__ = [
    'TLMRunner'
]

LOGGER = logging.getLogger(__name__)


class TLMRunner(Runner):
    """TLM runner."""

    def __init__(self, tlm_program_path: str, use_tqdm: bool = False):
        """
        TLM runner initialization.

        Parameters
        ----------
        tlm_program_path
            path to the debug object pickled by `tcf`
        """
        # pylint: disable=import-outside-toplevel
        from tpu_tlm_is import Executable
        from tpu_tlm_is.base import TensorDescription

        with open(tlm_program_path, 'rb') as file:
            tlm_program: Tuple[Executable, Dict[str, TensorDescription]] = pickle.load(file)

        self._tlm_program = tlm_program

        # NOTE: conversion from keys() to list is possible for Python > 3.6 guarantees dict item order
        super().__init__(source_path=tlm_program_path,
                         input_nodes=list(self._executable.in_data.keys()),
                         output_nodes=list(self._executable.out_data.keys()))

        self._use_tqdm = use_tqdm

    @property
    def _executable(self) -> 'Executable':
        executable, _ = self._tlm_program
        return executable

    @property
    def _tensor_descriptions(self) -> 'Dict[str, TensorDescription]':
        _, tensor_descriptions = self._tlm_program
        return tensor_descriptions

    def _check_input_names(self, input_tensors: Dict[str, np.ndarray]):
        if input_tensors.keys() != self._executable.in_data.keys():
            raise ValueError(
                f'Expected inputs {self._executable.in_data.keys()} differs from the provided {input_tensors.keys()}')

    def _check_input_shapes(self, input_tensors: Dict[str, np.ndarray]):
        for name, tensor in input_tensors.items():
            expected_shape = self._tensor_descriptions[name].user_shape.nhwc
            if tensor.shape != expected_shape:
                raise ValueError(f'Invalid input shape {tensor.shape} for tensor "{name}": expected {expected_shape}')

    def __call__(self, input_tensors: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        """Perform TLM run for a given input."""
        # pylint: disable=import-outside-toplevel
        from tpu_commands.frontend.design.api import tlm
        _, output_tensors = tlm(self._tlm_program, input_tensors)
        return output_tensors
