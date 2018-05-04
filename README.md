# TruthChecker

Playing around with machine learning, one usually needs some kind of ground truth. 
For vision tasks, this ground truth often has the shape of bounding boxes in an image associated with a label.

There are many tools to create such ground truths. 

This script helps in the validation process of a new ground truth. 
It finds all labels in a data set. 
For each label, it shows all images in sequence where only the bounding box for that label is drawn. 

Checking the correctness for one label in a sequence of images is easier than checking a sequence of images where all labels are shown at the same time.

