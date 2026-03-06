# standard library imports
import abc
from collections.abc import Hashable, Sequence
from typing import Any

# 3rd party imports
import numpy as np
from smqtk_image_io.bbox import AxisAlignedBoundingBox
from typing_extensions import override


class ScoreDetections:
    """Interface abstracting the behavior of taking detections and computing the corresponding metric scores.

    Interface abstracting the behavior of taking the actual and predicted detections and
    computing the corresponding metric scores.

    Implementations should verify the validity of the input data.

    Note that current implementations are not required to verify nor correct dimension
    (in)consistency, which may impact scoring.
    """

    @abc.abstractmethod
    def score(
        self,
        actual: Sequence[Sequence[tuple[AxisAlignedBoundingBox, dict[Hashable, Any]]]],
        predicted: Sequence[Sequence[tuple[AxisAlignedBoundingBox, dict[Hashable, float]]]],
    ) -> Sequence[float]:
        """Generate a sequence of scores corresponding to a specific metric.

        :param actual:
            Ground truth bbox and class label pairs.
        :param predicted:
            Output detections from a detector with bbox and
            class-wise confidence scores.

        Returns:
            Metric score values as a float-type sequence with the length matching
            the number of samples in the ground truth input.
        """

    def __call__(
        self,
        actual: Sequence[Sequence[tuple[AxisAlignedBoundingBox, dict[Hashable, Any]]]],
        predicted: Sequence[Sequence[tuple[AxisAlignedBoundingBox, dict[Hashable, float]]]],
    ) -> Sequence[float]:
        """Alias for :meth:`.ScoreDetection.score`."""
        return self.score(actual, predicted)


class ClassAgnosticPixelwiseIoUScorer(ScoreDetections):
    """Implementation of `ScoreDetection` interface that computes the Pixelwise IoU scores in a Class-Agnostic manner.

    The call to the scorer method returns a sequence of float values containing the Pixelwise IoU
    scores for the specified ground truth and predictions inputs.
    """

    @override
    def score(  # noqa: C901
        self,
        actual: Sequence[Sequence[tuple[AxisAlignedBoundingBox, dict[Hashable, Any]]]],
        predicted: Sequence[Sequence[tuple[AxisAlignedBoundingBox, dict[Hashable, float]]]],
    ) -> Sequence[float]:
        """Computes pixelwise IoU scores and returns sequence of float values equal to the length of the input data."""
        if len(actual) != len(predicted):
            raise ValueError("Size mismatch between actual and predicted data")
        for actual_det in actual:
            if len(actual_det) < 1:
                raise ValueError("Actual bounding boxes must have detections and can't be empty.")

        ious = list()

        for act, pred in zip(actual, predicted, strict=False):
            width, height = 1, 1
            for act_bbox, _ in act:
                width = max(width, act_bbox.max_vertex[0])
                height = max(width, act_bbox.max_vertex[1])

            for pred_bbox, _ in pred:
                width = max(width, pred_bbox.max_vertex[0])
                height = max(width, pred_bbox.max_vertex[1])

            width = int(width) + 1
            height = int(height) + 1

            actual_mask = np.zeros((height, width), dtype=bool)
            predicted_mask = np.zeros((height, width), dtype=bool)

            for act_bbox, _ in act:
                x_1, y_1 = act_bbox.min_vertex
                x_2, y_2 = act_bbox.max_vertex
                # Black formatting keeps moving the noqa comment down a line, which causes flake8 error
                # fmt: off
                actual_mask[int(y_1): int(y_2), int(x_1): int(x_2)] = 1
                # fmt: on

            for pred_bbox, _ in pred:
                x_1, y_1 = pred_bbox.min_vertex
                x_2, y_2 = pred_bbox.max_vertex
                # Black formatting keeps moving the noqa comment down a line, which causes flake8 error
                # fmt: off
                predicted_mask[int(y_1):int(y_2), int(x_1):int(x_2)] = (
                    1
                )
                # fmt: on

            intersection = np.logical_and(actual_mask, predicted_mask)
            union = np.logical_or(actual_mask, predicted_mask)

            ious.append(np.sum(intersection) / np.sum(union))

        return ious
