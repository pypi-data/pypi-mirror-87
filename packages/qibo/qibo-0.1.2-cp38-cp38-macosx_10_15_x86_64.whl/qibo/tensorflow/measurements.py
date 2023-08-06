# -*- coding: utf-8 -*-
# @authors: S. Efthymiou
import numpy as np
import tensorflow as tf
from qibo.base import measurements as base_measurements
from qibo.config import DTYPES
from typing import Dict, Optional, Tuple


class GateResult(base_measurements.GateResult):

    @staticmethod
    def _convert_to_binary(x: tf.Tensor, n: int) -> tf.Tensor:
        _range = tf.range(n - 1, -1, -1, dtype=x.dtype)
        return tf.math.mod(tf.bitwise.right_shift(x[:, tf.newaxis], _range), 2)

    @staticmethod
    def _convert_to_decimal(x: tf.Tensor, n: int) -> tf.Tensor:
        _range = tf.range(n - 1, -1, -1, dtype=x.dtype)
        _range = tf.math.pow(2, _range)[:, tf.newaxis]
        return tf.matmul(x, _range)[:, 0]

    @staticmethod
    def _calculate_counts(decimal_samples: tf.Tensor) -> Tuple[np.ndarray]:
        return np.unique(decimal_samples.numpy(), return_counts=True)

    @staticmethod
    def _apply_bitflips(noiseless_samples: tf.Tensor, probs: Tuple[float]
                        ) -> tf.Tensor:
        dtype = DTYPES.get('DTYPE')
        fprobs = tf.cast(probs, dtype=dtype)
        sprobs = tf.random.uniform(noiseless_samples.shape, dtype=dtype)
        flip0 = tf.cast(sprobs < fprobs[0], dtype=noiseless_samples.dtype)
        flip1 = tf.cast(sprobs < fprobs[1], dtype=noiseless_samples.dtype)
        noisy_samples = noiseless_samples + (1 - noiseless_samples) * flip0
        noisy_samples = noisy_samples - noiseless_samples * flip1
        return noisy_samples


class CircuitResult(base_measurements.CircuitResult):

    @staticmethod
    def _calculate_register_results(register_qubits: Dict[str, Tuple[int]],
                                    gate_result: GateResult
                                    ) -> Dict[str, GateResult]:
        results = {}
        for name, qubit_tuple in register_qubits.items():
            slicer = tuple(gate_result.qubit_map[q] for q in qubit_tuple)
            samples = tf.gather(gate_result.samples(True), slicer, axis=-1)
            results[name] = GateResult(qubit_tuple, binary_samples=samples)
        return results
