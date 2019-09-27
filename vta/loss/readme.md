# JSON data definition

| Symbol | Description |
|:---|:---|
| `#` | Denotes a comment. |
| `[]` | A homogeneous array. The type of the data should be listed once between the brackets. |
| `{}` | An object (a Python dict). |
| `"foo"` | An object key. This is taken literally, and is case sensitive. |

| Type | Description |
|:---|:---|
| str | A character string |
| float | A floating point value. There is no distinction between single and double precision. |
| int | An integer value. There is no distinction between signed and unsigned integers. |
| bool | One of `True` or `False`. Other synonyms are not guaranteed to work. |
| `{}` | A restricted set of values. Commas separate values, and dashes denote an inclusive range. |

```python
# The name of the sequence: Basketball, Bird1, etc.
"sequence": str

# The threshold used by the tracker to consider scores to be considered
# successful tracking.
"score_threshold": float

# An array of data. There should be one entry for each frame in the sequence.
"frames": [
  {
    # The frame number, starting from 0.
    "frame": int

    # A boolean indicating whether the tracker found the target in this frame.
    "success": bool

    # A string describing the type of online model update performed by the
    # tracker at the end of this frame.
    "update": str {none|long|short}

    # The indices of the top N positive (target) scores from the tracker
    # network.
    "top_indices": [ int ]

    # The following items are arrays that fulfill the following requirements:
    # 1) Each array must have one element per target candidate for this frame.

    # The list of positive (target) scores output by the tracker network. These
    # should be raw scores, not converted to a different range as by soft-max
    # for example.
    "positive_scores": [ float ]

    # The list of negative (background) scores output by the tracker network.
    # There should be raw scores, not converted to a different range as by 
    # soft-max for example.
    "negative_scores": [ float ]

    # The candidate bounding box data. Each row represents a candidate bounding
    # box. Each row is [ x, y, width, height ]. The (x, y) coordinate specifies
    # the position of the candidate box's upper left corner.
    "candidates": [ [ float, float, float, float ] ]
  }
]

