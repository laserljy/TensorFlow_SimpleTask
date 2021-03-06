# TF actual combat chapter3
# Practice using softmax in TF to complete MNIST task 

from tensorflow.examples.tutorials.mnist import input_data

mnist= input_data.read_data_sets("MNIST_data/", one_hot=True)

print(mnist.train.images.shape, mnist.train.labels.shape)
print(mnist.test.images.shape, mnist.test.labels.shape)
print(mnist.validation.images.shape, mnist.validation.labels.shape)

import tensorflow as tf

sess = tf.InteractiveSession()

x = tf.placeholder(tf.float32, [None, 784])

W = tf.Variable(tf.zeros([784, 10]))

b = tf.Variable(tf.zeros([10]))

y = tf.nn.softmax(tf.matmul(x, W)+b)

y_ = tf.placeholder(tf.float32, [None, 10])

cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))

train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

tf.global_variables_initializer().run()

for i in range(1000):
    batch_xs, batch_ys = mnist.train.next_batch(100)
    train_step.run({x: batch_xs, y_: batch_ys})   
    # 因为之前的x, y_ 都只是placeholder，没有实际的数据。现设定palceholder后加载数据是为了在数据加载之前，就有一个设定好的computation graph吧
    # 有了整体的 computation steps 之后，剩下的就是控制 连续的 batch，一次一次feed 进这个 computation graph 的流水线。
    # 这种设计的效率应该是非常高的，属于一种设计上的优化。

correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))

accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

print(accuracy.eval({x:mnist.test.images, y_:mnist.test.labels}))