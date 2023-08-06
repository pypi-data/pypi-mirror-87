import tensorflow as tf
from quant_analytics_flow.analytics import constants

def phi_smooth(x,y):
    return (x + y + constants.DELTA + (x - y) ** 2 / constants.DELTA / 4.)/2.

def max_if(x,y):
    return tf.where(tf.abs(x-y)>constants.BOUNDARY,tf.maximum(x,y),phi_smooth(x,y))

def hyperbolic(x):
      """ Using the hyperbolic function 
    
      .. _target hyperbolic_function:

      .. math::

        f(x) = \\frac{1}{2} \\left(x + \sqrt{1 + x^2} \\right)

      Args:
          x (tensor(shape=(...))): M-dimensional tensor

      Returns:
          y (tensor(shape=(...))): Hyperbolic function
          
      """
      
      return (x + tf.sqrt(1. + x*x))/2.

def soft_max_hypterbolic(x,eps=constants.EPSILON):
      """ Using the :ref:`hyperbolic function <target hyperbolic_function>` to approximate :math:`\max(x,0)`
    
      .. _target soft_max_hyperbolic:

      .. math::

          g_(x) = f(x/\\epsilon)\cdot \\epsilon

      Args:
          x (tensor(shape=(...))): M-dimensional tensor
          eps (float64): scaling parameter

      Returns:
          y (tensor(shape=(...))): Hyperbolic function
          
      """
      return hyperbolic(x/eps)*eps