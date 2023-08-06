"""TPURunner class."""
from typing import Dict
import numpy as np

from iva_tpu import TPUDevice, TPUProgram
from .runner import Runner


class TPURunner(Runner):
    """Runner for IVA TPU."""

    def __init__(self, program_path: str):
        """
        Program initialization.

        Parameters
        ----------
        program_path
            path to TPU program
        """
        self.program = TPUProgram(program_path)
        input_nodes = self.get_input_nodes()
        output_nodes = self.get_output_nodes()
        super().__init__(program_path, input_nodes, output_nodes)

        self.device = TPUDevice()
        self.device.load(self.program)

    def __call__(self, tensors: Dict[str, np.ndarray], dtype=np.float32) -> Dict[str, np.ndarray]:
        """
        Run inference using IVA TPU.

        Parameters
        ----------
        tensors
            Input tensors for inference
        dtype
            The desired data-type for the returned data (np.float32 or np.int8)
            If not given, then the type will be determined as np.float32.

        Returns: Result after TPU
        -------

        """
        tpu_out_tensors = self.device.run(tensors, dtype)
        return tpu_out_tensors

    def get_input_nodes(self) -> list:
        """
        Get a list of names of the graph input nodes.

        Returns
        -------
        A list of names of input nodes
        """
        input_nodes = [d['layer_name'] for d in self.program.inputs]
        return input_nodes

    def get_output_nodes(self) -> list:
        """
        Get a list of names of the graph output nodes.

        Returns
        -------
        A list of names of output nodes
        """
        output_nodes = [d['layer_name'] for d in self.program.outputs]
        return output_nodes
