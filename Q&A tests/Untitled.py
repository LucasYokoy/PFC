#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tensorflow as tf


# In[2]:


# Declaring variables (all variables are technicaly tensors)
# the value is defined in the first parameter, the type is defined on the second
string = tf.Variable("String variable", tf.string)
number = tf.Variable(123, tf.int16)
floating = tf.Variable(3.14, tf.float64)


# In[6]:


# the same syntax can declare tensors of higher rank and dimension
# you can gauge the rank of a tensor with tf.rank(tensor)
# the dimension can be gauged with the tensor.shape attribute
rank1_tensor = tf.Variable(["Test"], tf.string)
rank2_tensor = tf.Variable([["test", "ok"], ["test", "yes"], ["test", "another"]], tf.string)
tf.rank(rank2_tensor)


# In[7]:


tf.rank(string)


# In[8]:


rank2_tensor.shape


# In[9]:


# tensors can be reshaped with tf.reshape(tensor, new_shape)
# if the last value in the new shape matrix is -1, tensorflow infers what value it must be
# tf.ones\zeros(shape) creates a tensor with the specified shape, populated only by 1s\0s
tensor1 = tf.ones([1,2,3])
print(tensor1)


# In[12]:


tensor1 = tf.reshape(tensor1, [2,3,1])
print(tensor1)


# In[17]:


# tensors can be declared with tf.Variable/Constant/Placeholder/SparceTensor
# in the context of a tf.Session, the value of a tensor can be evaluated with tensor.eval()
# with tf.Session() as sess:
#     tensor.eval()


# In[ ]:




