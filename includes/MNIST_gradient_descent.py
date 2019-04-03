#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
"""

import numpy as np;
import tensorflow as tf;

def MNIST_gradient_descent(	X_train = None,
							y_train = None,
							X_test = None,
							y_test = None,
							learning_rate = 0.05,
							epochs = 50,
							batches = 75,
							seed = 42
							):

	## !!! NEED TO HANDLE GRACEFULLY WHEN NO DATASET IS PASSED TO THE FUNCTION.

	## Optimization varibales
	#~epochs = 1000
	#~learning_rate = 0.01

	## Function's environment variables
	update_interval = int ( epochs / 5 );
	#~total_batches = int( len( mnist.train.labels ) / batch_size );
	batch_size = int( len( mnist.train.labels ) / batches );

	# Extracting the dimensions of the problem' space.
	m, n = X_Train.data.shape;

	## Populating the TensorFlow environment
	## Creating the constants
	X = tf.constant(	X_Train,
						dtype = tf.float32,
						name = "X"
						);
	y = tf.constant(	y_Train,
						dtype = tf.float32,
						name = "y"
						);

	## Creating the variables
	theta = tf.Variable(	tf.random_uniform(	[n, 1],
												-1.0,
												1.0
												),
							name="theta"
							);

	## Creating the optimizer
	## calculated using tfs gradient descent optimizer
	#~optimizer = tf.train.GradientDescentOptimizer(learning_rate = learning_rate);

	## calculated using tfs momentum descent optimizer - faster
	optimizer = tf.train.MomentumOptimizer(	learning_rate = learning_rate,
											momentum = 0.9
											);

	## Creating the operations
	y_pred = tf.matmul(	X,
						theta,
						name="predictions"
						);
	error = y_pred - y;
	mse = tf.reduce_mean(	tf.square(error),
							name="mse"
							);
	training_op = optimizer.minimize(mse);

	## Initializing the TensorFlow environment
	init = tf.global_variables_initializer();

	## Running the operations between the variables using a TensorFlow.Session.
	## Class Session: returns TensorFlow operations
	## A Session object encapsulates the environment in which Operation objects
	## are executed, and Tensor objects are evaluated.
	## Note: using the context manager "with", it is not necessary to release
	## the sessions resources when no longer required (using tf.Session.close).
	with tf.Session() as sess:
		## Completing variables and graph structure initialization.
		sess.run(init);
		## For the requested amount of times (epochs = iterations) train the ANN.
		for epoch in range(epochs):
			avg_cost = 0
			for batch in range(total_batches):
				batch_x, batch_y = mnist.train.next_batch(batch_size = batch_size)
				_, cost = sess.run([optimiser, cross_entropy],
								feed_dict = {x: batch_x, y: batch_y})
				avg_cost += cost / batches
			print("Epoch:", (epoch + 1), "cost =", "{:.3f}".format(avg_cost))

			## At regular interval, including iteration 0, print a status update
			## on the achieved effectiveness of the training (the value of the
			## cost function).
			if epoch % update_interval == 0:
				print(	"Epoch ",
						epoch,
						" MSE = ",
						mse.eval()
						);
				## Compute the output of the graph (run the operations); i.e.
				## train the ANN.
				sess.run(training_op);
		## Compute and print the final value of the wheights (is thatwhat theta
		## is?) obtained at the end of the training session (the epochs).
		best_theta = theta.eval();
		print(best_theta)

		print(sess.run(accuracy, feed_dict={x: mnist.test.images, y: mnist.test.labels}))


if __name__ == "__main__":
	#~main()
