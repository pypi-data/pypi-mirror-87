import tensorflow as tf

from quant_analytics_flow.analytics.norminv import norminv
from quant_analytics_flow.analytics.matrixanalytics import square_root_symmetric_matrix
from quant_analytics_flow.calculators.univariatebrownianbridge import UnivariateBrownianBridge


class MultivariateBrownianBridge():
    def __init__(self, forwardCovarianceMatrices):
        self.forwardCovarianceMatrices = forwardCovarianceMatrices
        self.numberTimeSteps = len(forwardCovarianceMatrices)
        self.numberStates = len(forwardCovarianceMatrices[0])
        self.brownian = UnivariateBrownianBridge(self.numberTimeSteps)

        self.sqrtForwardCovarianceMatrices = tf.TensorArray(dtype=tf.float64, size=self.numberTimeSteps, clear_after_read=False)
        for i in range(self.numberTimeSteps):
            self.sqrtForwardCovarianceMatrices = self.sqrtForwardCovarianceMatrices.write(i, square_root_symmetric_matrix(self.forwardCovarianceMatrices[i]))

    def path(self, number):
        x = tf.math.sobol_sample(self.numberTimeSteps*self.numberStates,number,dtype=tf.dtypes.float64)
        x = tf.transpose(x)
        y = tf.reshape(x, shape=(self.numberTimeSteps,self.numberStates,number))
        z = norminv(y)

        w = self.brownian.path(z, True)
        
        path = tf.TensorArray(dtype=tf.float64,size=self.numberTimeSteps,clear_after_read=False)
        for i in range(len(z)):
            path = path.write(i,tf.matmul(self.sqrtForwardCovarianceMatrices.read(i), w[i]))

        return path.stack()