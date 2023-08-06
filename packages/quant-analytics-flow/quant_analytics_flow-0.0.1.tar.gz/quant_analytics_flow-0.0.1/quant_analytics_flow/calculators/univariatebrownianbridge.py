import tensorflow as tf
import numpy as np
import math

class UnivariateBrownianBridge():
    def __init__(self, number_time_steps):
        self.number_time_steps = number_time_steps

        self.left_index = np.zeros(number_time_steps, dtype=int)
        self.right_index = np.zeros(number_time_steps, dtype=int)
        self.bridge_index = np.zeros(number_time_steps, dtype=int)
        self.left_weight = np.zeros(number_time_steps)
        self.right_weight = np.zeros(number_time_steps)
        self.std_dev = np.zeros(number_time_steps)

        self._map = np.zeros(number_time_steps, dtype=int)

        self._map[-1] = 1
        self.bridge_index[0] = number_time_steps - 1
        self.std_dev[0] = math.sqrt(1.0 * number_time_steps)
        self.left_weight[0] = 0
        self.right_weight[0] = 0

        j=0
        for i in range(1,number_time_steps):
            while self._map[j] == True:
                j = j + 1
            k = j
            while self._map[k] == False:
                k = k + 1
            l = j+((k-1-j)>>1)
            self._map[l]=i
            self.bridge_index[i]=l
            self.left_index[i]=j
            self.right_index[i]=k
            self.left_weight[i]=(k-l)/(k+1-j)
            self.right_weight[i]=(1+l-j)/(k+1-j)
            self.std_dev[i]=np.sqrt(((1+l-j)*(k-l))/(k+1-j))
            j=k+1
            if j>=number_time_steps:
                j=0

        self.bridge_index_t = tf.constant(tf.convert_to_tensor(self.bridge_index,dtype=tf.int32))
        self.right_index_t = tf.constant(tf.convert_to_tensor(self.right_index,dtype=tf.int32))
        self.left_index_t = tf.constant(tf.convert_to_tensor(self.left_index,dtype=tf.int32))
        self.std_dev_t = tf.constant(tf.convert_to_tensor(self.std_dev))
        self.right_weight_t = tf.constant(tf.convert_to_tensor(self.right_weight))
        self.left_weight_t = tf.constant(tf.convert_to_tensor(self.left_weight))

    @tf.function(experimental_compile=True, input_signature=(tf.TensorSpec(shape=(None,None,None), dtype=tf.float64),
                                                tf.TensorSpec(shape=(), dtype=tf.bool),
                                                tf.TensorSpec(shape=(), dtype=tf.int32),
                                                tf.TensorSpec(shape=(None), dtype=tf.int32),
                                                tf.TensorSpec(shape=(None), dtype=tf.int32),
                                                tf.TensorSpec(shape=(None), dtype=tf.int32),
                                                tf.TensorSpec(shape=(None), dtype=tf.float64),
                                                tf.TensorSpec(shape=(None), dtype=tf.float64),
                                                tf.TensorSpec(shape=(None), dtype=tf.float64)))
    def buildPath(z, increment, number_time_steps, left_index, right_index, bridge_index, left_weight, right_weight, std_dev):
        path = tf.TensorArray(dtype=tf.float64,size=number_time_steps+1)
        path = path.write(number_time_steps,std_dev[0]*z[0])
        path = path.write(0,0*z[0]);  
        j = 0
        k = 0
        l = 0
        i = 0
        for i in range(1,number_time_steps):
            j = left_index[i]
            k = right_index[i]
            l = bridge_index[i]
            path = path.write(l+1,left_weight[i] * path.read(j) + right_weight[i] * path.read(k+1) + std_dev[i] * z[i])

        if increment:
            for i in range(0,number_time_steps):
                path = path.write(i, path.read(i+1) - path.read(i))

        return path.stack()

    def path(self,z,increment):
        return UnivariateBrownianBridge.buildPath(z, increment, self.number_time_steps, self.left_index_t, self.right_index_t, self.bridge_index_t, self.left_weight_t, self.right_weight_t, self.std_dev_t)