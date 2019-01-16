import tensorflow as tf

a=[1.0,2.0,3.0,4.0,5.0,6.0]

d = tf.data.Dataset.from_tensor_slices(a)
d = d.repeat().batch(1)
ite = d.make_one_shot_iterator()
data = ite.get_next()
data.set_shape([1])

var = tf.get_variable(name='hhh',shape=[1])
op = tf.assign(var, data)
opp = tf.identity(var)
print('###################')
print(var)
print(opp)
print('###################')
var=var+1.0
op = op + 1.0
#var = tf.get_variable(name='hhh',initializer=data)

with tf.Session() as sess:
  tf.global_variables_initializer().run()
  for i in range(10):
    oo = sess.run(op)
    print(oo)
    bb, dd = sess.run([var,opp])
    print(bb)
    print(dd)
    print('\n')
  
