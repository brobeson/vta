"""Mock up some random filters."""

import torch
import PIL.Image

mask = torch.rand((3, 3), dtype=float)

image = PIL.Image.new(mode="F", size=(3, 3))
image = PIL.Image.fromarray(mask.tolist())
