import numpy


class MaskPerformance:

    def __init__(self, true_positive: int = 0,
                 true_negative: int = 0,
                 false_positive: int = 0,
                 false_negative: int = 0):

        self.true_positive: int = true_positive
        self.true_negative: int = true_negative
        self.false_positive: int = false_positive
        self.false_negative: int = false_negative

    # region Raw performance metrics
    def compute_raw_performance(self, prediction_mask: numpy.ndarray, ground_truth_mask: numpy.ndarray):
        """
        Computes the contingency matrix items, representing the raw values of the performance.

        Args:
            prediction_mask: A binary two-dimensional array, representing the predicted mask.
            ground_truth_mask: A binary two-dimensional array, representing the ground truth mask.
        """
        self.true_positive = MaskPerformance.__compute_true_positive(prediction_mask, ground_truth_mask)
        self.true_negative = MaskPerformance.__compute_true_negative(prediction_mask, ground_truth_mask)
        self.false_positive = MaskPerformance.__compute_false_positive(prediction_mask, ground_truth_mask)
        self.false_negative = MaskPerformance.__compute_false_negative(prediction_mask, ground_truth_mask)

    @staticmethod
    def __compute_true_positive(prediction_mask: numpy.ndarray, ground_truth_mask: numpy.ndarray) -> int:
        """
        Computes the true positives of the prediction; that is, the number of pixels that currently are positive
        and have been predicted as positive.

        Args:
            prediction_mask: A binary two-dimensional array, representing the predicted mask.
            ground_truth_mask: A binary two-dimensional array, representing the ground truth mask.

        Returns:
            An integer, representing the number of true positives.
        """
        return int(numpy.sum(numpy.logical_and(prediction_mask == 255, ground_truth_mask == 255)))

    @staticmethod
    def __compute_true_negative(prediction_mask: numpy.ndarray, ground_truth_mask: numpy.ndarray) -> int:
        """
        Computes the true negatives of the prediction; that is, the number of pixels that currently are negative
        and have been predicted as negative.

        Args:
            prediction_mask: A binary two-dimensional array, representing the predicted mask.
            ground_truth_mask: A binary two-dimensional array, representing the ground truth mask.

        Returns:
            An integer, representing the number of true negatives.
        """
        return int(numpy.sum(numpy.logical_and(prediction_mask == 0, ground_truth_mask == 0)))

    @staticmethod
    def __compute_false_positive(prediction_mask: numpy.ndarray, ground_truth_mask: numpy.ndarray) -> int:
        """
        Computes the false positives of the prediction; that is, the number of pixels that currently are negative
        and have been predicted as positive.

        Args:
            prediction_mask: A binary two-dimensional array, representing the predicted mask.
            ground_truth_mask: A binary two-dimensional array, representing the ground truth mask.

        Returns:
            An integer, representing the number of false positives.
        """
        return int(numpy.sum(numpy.logical_and(prediction_mask == 255, ground_truth_mask == 0)))

    @staticmethod
    def __compute_false_negative(prediction_mask: numpy.ndarray, ground_truth_mask: numpy.ndarray) -> int:
        """
        Computes the false negatives of the prediction; that is, the number of pixels that currently are positive
        and have been predicted as negative.

        Args:
            prediction_mask: A binary two-dimensional array, representing the predicted mask.
            ground_truth_mask: A binary two-dimensional array, representing the ground truth mask.

        Returns:
            An integer, representing the number of false negatives.
        """
        return int(numpy.sum(numpy.logical_and(prediction_mask == 0, ground_truth_mask == 255)))
    # endregion

    # region Performance metrics
    def matthews_correlation_coefficient(self) -> float:
        """
        Computes the Matthews correlation coefficient.

        References:
            D. Chicco and G. Jurman. The advantages of the Matthews correlation coefficient (MCC) over F1 score and
                accuracy in binary classification evaluation.
            BMC Genomics. 2020; 21: 6.

        Returns:
            A float value, representing the MCC.
        """
        return (self.true_positive * self.true_negative - self.false_positive * self.false_negative) / \
               numpy.sqrt(float((self.true_positive + self.false_positive) * (self.true_positive + self.false_negative) * (self.true_negative + self.false_positive) * (self.true_negative + self.false_negative)))
    # endregion
