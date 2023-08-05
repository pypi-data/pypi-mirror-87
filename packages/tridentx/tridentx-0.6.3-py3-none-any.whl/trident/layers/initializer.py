
class Initializer(object):
  """Initializer base class: all initializers inherit from this class.
  """
  def __call__(self, shape, dtype=None):
    """Returns a tensor object initialized as specified by the initializer.
    Args:
      shape: Shape of the tensor.
      dtype: Optional dtype of the tensor. If not provided will return tensor
       of `tf.float32`.

    """
    raise NotImplementedError

  def get_config(self):
    """Returns the configuration of the initializer as a JSON-serializable dict.
    Returns:
      A JSON-serializable Python dict.
    """
    return {}