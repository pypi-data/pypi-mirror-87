from typing import Optional

import torch
from torch import nn
from torch import Tensor
import numpy as np


class PositionalEncoding(nn.Module):
    def __init__(self, embedding_size: int, num_positions: int):
        super(PositionalEncoding, self).__init__()

        self.register_buffer(
            "pos_table", _get_sinusoid_encoding_table(num_positions, embedding_size)
        )

    def forward(self, x: Tensor, position: Optional[int] = None):
        if position is None:
            return x + self.pos_table[:, : x.size(1)].clone().detach()
        else:
            return x + self.pos_table[:, position : position + x.size(1)].clone().detach()


def _get_sinusoid_encoding_table(n_position, d_hid):
    def get_position_angle_vec(position):
        return [position / np.power(10000, 2 * (hid_j // 2) / d_hid) for hid_j in range(d_hid)]

    sinusoid_table = np.array([get_position_angle_vec(pos_i) for pos_i in range(n_position)])
    sinusoid_table[:, 0::2] = np.sin(sinusoid_table[:, 0::2])
    sinusoid_table[:, 1::2] = np.cos(sinusoid_table[:, 1::2])

    return torch.FloatTensor(sinusoid_table).unsqueeze(0)


# TODO: Not working
# class PositionalEncoding(nn.Module):
#     def __init__(self, embedding_size: int, num_positions: int):
#         super(PositionalEncoding, self).__init__()
#         print("New positional encoding")
#         if embedding_size % 2 != 0:
#             raise ValueError(
#                 f"Expected even number for positional embedding size, but got {embedding_size} instead."
#             )
#         encoding_table = torch.zeros(num_positions, embedding_size)
#         positions = torch.arange(0, num_positions, dtype=torch.float64).unsqueeze(1)
#         dimensions = torch.arange(0, embedding_size, 2, dtype=torch.float64)
#         div_term = torch.pow(10000.0, dimensions / embedding_size)
#         encoding_table[:, 0::2] = torch.sin(positions / div_term)
#         encoding_table[:, 1::2] = torch.cos(positions / div_term)
#         encoding_table = encoding_table.unsqueeze(0).float()
#         self.register_buffer("encoding_table", encoding_table)
#
#     def forward(self, x: Tensor, position: Optional[int] = None):
#         if position is None:
#             return x + self.encoding_table[:, x.size(1)].clone().detach()
#         else:
#             return x + self.encoding_table[:, position : position + x.size(1)].clone().detach()
