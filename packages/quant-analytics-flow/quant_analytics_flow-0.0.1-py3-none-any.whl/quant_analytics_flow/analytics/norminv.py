import tensorflow as tf

SQRT_2 = tf.sqrt(tf.constant(2.,dtype=tf.float64))

def norminv(x):
    return SQRT_2*tf.math.erfinv(2*(x-0.5))