"""Perceptron-like modules."""

from torch import nn

from ..typing import FloatTensor

__all__ = [
    "ConcatMLP",
]


class ConcatMLP(nn.Sequential):
    """A 2-layer MLP with ReLU activation and dropout applied to the flattened token representations.

    This is for conveniently choosing a configuration similar to the paper. For more complex aggregation mechanisms,
    pass an arbitrary callable instead.

    .. seealso::

        https://github.com/migalkin/NodePiece/blob/d731c9990/lp_rp/pykeen105/nodepiece_rotate.py#L57-L65
    """

    def __init__(
        self,
        input_dim: int,
        output_dim: int | None = None,
        dropout: float = 0.1,
        ratio: int | float = 2,
        flatten_dims: int = 2,
    ):
        """Initialize the module.

        :param input_dim: the input dimension
        :param output_dim: the output dimension. defaults to input dim
        :param dropout: the dropout value on the hidden layer
        :param ratio: the ratio of the output dimension to the hidden layer size.
        :param flatten_dims: the number of trailing dimensions to flatten
        """
        output_dim = output_dim or input_dim
        hidden_dim = int(ratio * output_dim)
        super().__init__(
            nn.Linear(input_dim, hidden_dim),
            nn.Dropout(dropout),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim),
        )
        self.flatten_dims = flatten_dims

    def forward(self, xs: FloatTensor, dim: int) -> FloatTensor:
        """Forward the MLP on the given dimension.

        :param xs: The tensor to forward
        :param dim: Only a parameter to match the signature of :func:`torch.mean` / :func:`torch.sum` this class is not
            thought to be usable from outside

        :returns: The tensor after applying this MLP
        """
        assert dim == -2
        return super().forward(xs.view(*xs.shape[: -self.flatten_dims], -1))
