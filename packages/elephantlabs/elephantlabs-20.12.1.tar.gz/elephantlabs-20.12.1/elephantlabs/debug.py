import torch
import numpy as np
from torch import nn


 # an Embedding module containing 10 tensors of size 3
embedding = nn.Embedding(10, 3)
# a batch of 2 samples of 4 indices each
input = torch.LongTensor([[1,2,4,5],[4,3,2,9]])
embedding(input)



# # loss = torch.nn.CrossEntropyLoss()
# # a = np.arange(0, 100).reshape(10,10)
# # b = a.reshape(-1)
# # print(b)
#
# # logits = torch.tensor([[100, 2, 3, 4]], dtype=float)
# # print(logits.shape)
# # true = torch.tensor([0])
# #
# # c = loss(logits, true)
# # print(c)
#
# import torch
# import torch.nn.functional as F
#
# num_classes = 10
# batch_size = 3
#
# # your model outputs / logits
# output = torch.rand(batch_size, num_classes)
#
# # your targets
# target = torch.randint(num_classes, (batch_size,))
#
# # getting loss using cross entropy
# loss = F.cross_entropy(output, target)
#
# # calculating perplexity
# perplexity = torch.exp(loss)
# print('Loss:', loss, 'PP:', perplexity)
# print(output.shape, target.shape)

