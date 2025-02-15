---
layout: page
title: Wheatears counting in images
description: Counting wheatears from images using deep learning
importance: 4
published: 2020-10-21 00:00:00-0400
category: image
giscus_comments: true
---

You can find more details in the paper and the colab notebook below.  
**- [The paper](/assets/pdf/Wheatears_counting.pdf)**  
**- [Colab URL](https://colab.research.google.com/drive/1BN3WQDGF3OtiWoNfF4Cwy9yGCjNOqTY6)** 

We are supplied with a raw set of images of a wheatfield with a flock of wheatears. We want to count the number of wheatears in each image. This is an 
actual problem that requires a lot of manual work from farmers. Apparently, wheatears count is a great indicator of the health of the wheat field.

To accomplish this, we used two algorithms:
1. [Faster R-CNN](https://arxiv.org/pdf/1506.01497)
2. [EfficientDet](https://arxiv.org/pdf/1911.09070)

While EfficientDet is a better model than Faster R-CNN, we wanted to compare the two models to see how they perform on this task.


**Dataset**: We used the [Global Wheat Dataset](https://www.global-wheat.com/) for training and testing the models.

#### Some results

<div class="text-center">
    {% include figure.html path="assets/img/wheatears/inference.png" title="example image" class="img-fluid z-depth-1" %}
</div>

<div class="row">
    <div class="col-sm mt-6 mt-md-0">
        {% include figure.html path="assets/img/wheatears/adam.png" title="example image" class="img-fluid z-depth-1" %}
    </div>
    <div class="col-sm mt-6 mt-md-0">
        {% include figure.html path="assets/img/wheatears/sgd.png" title="example image" class="img-fluid z-depth-1" %}
    </div>
</div>

<div class="row">
    <div class="col-sm mt-6 mt-md-0">
        {% include figure.html path="assets/img/wheatears/vald5.png" title="example image" class="img-fluid z-depth-1" %}
    </div>
    <div class="col-sm mt-6 mt-md-0">
        {% include figure.html path="assets/img/wheatears/vald7.png" title="example image" class="img-fluid z-depth-1" %}
    </div>
</div>


<div class="row">
    <div class="col-sm mt-6">
        $$
        \begin{array}{ |c|c|c|c|c|c| } 
         \hline
         ImageID & GT & Detected & Precision & Recall & Accuracy \\ 
         \hline
        2fd875eaa & 27 & 24 & 1.0 & 0.89 & 88.9\% \\
        51b3e36ab & 27 & 29 & 0.86 & 0.93 & 80.6\% \\
        51f1be19e & 18 & 18 & 1.0 & 1.0 & 100.0\% \\
        53f253011 & 31 & 29 & 1.0 & 0.94 & 93.5\% \\
        348a992bb & 37 & 36 & 0.97 & 0.95 & 92.1\% \\
        796707dd7 & 31 & 23 & 1.0 & 0.74 & 74.2\% \\
        aac893a91 & 24 & 21 & 0.95 & 0.83 & 80.0\% \\
        cb8d261a3 & 24 & 21 & 1.0 & 0.88 & 87.5\% \\
        cc3532ff6 & 26 & 29 & 0.9 & 1.0 & 89.7\% \\
        f5a1f0358 & 28 & 31 & 0.9 & 1.0 & 90.3\% \\
        \hline
        Total & 273 & 261 & 0.95 & 0.91 & 87.4\% \\
        \hline
        \end{array}
        $$
        <h6 class="text-center">Faster R-CNN with SGD Optimizer on Test Data</h6>
    </div>
    <div class="col-sm mt-6">
        $$
        \begin{array}{ |c|c|c|c|c|c| } 
         \hline
         ImageID & GT & Detected & Precision & Recall & Accuracy \\ 
         \hline
        2fd875eaa & 27 & 24 & 1.0 & 0.89 & 88.9\% \\
        51b3e36ab & 27 & 29 & 0.9 & 0.96 & 86.7\% \\
        51f1be19e & 18 & 18 & 1.0 & 1.0 & 100.0\% \\
        53f253011 & 31 & 29 & 1.0 & 0.94 & 93.5\% \\
        348a992bb & 37 & 36 & 0.97 & 0.95 & 92.1\% \\
        796707dd7 & 31 & 25 & 1.0 & 0.81 & 80.6\% \\
        aac893a91 & 24 & 21 & 0.95 & 0.83 & 80.0\% \\
        cb8d261a3 & 24 & 21 & 1.0 & 0.88 & 87.5\% \\
        cc3532ff6 & 26 & 29 & 0.9 & 1.0 & 89.7\% \\
        f5a1f0358 & 28 & 31 & 0.9 & 1.0 & 90.3\% \\
        \hline
        Total & 273 & 263 & 0.96 & 0.92 & 88.7\% \\
        \hline
        \end{array}
        $$
        <h6 class="text-center">Faster R-CNN with Adam optimizer on Test Data</h6>
    </div>
</div>

<div class="row">
    <div class="col-sm mt-6 mt-md-0">
        $$
        \begin{array}{ |c|c|c|c|c|c| } 
         \hline
         ImageID & GT & Detected & Precision & Recall & Accuracy \\ 
         \hline
        2fd875eaa & 27 & 24 & 0.88 & 0.88 & 88\% \\
        53f253011 & 31 & 30 & 0.96 & 0.96 & 96\% \\
        51b3e36ab & 27 & 25 & 0.92 & 0.92 & 92\% \\
        51f1be19e & 18 & 18 & 1.0 & 1.0 & 100\% \\
        348a992bb & 37 & 35 & 0.94 & 0.94 & 94\% \\
        796707dd7 & 31 & 26 & 0.83 & 0.83 & 83\% \\
        aac893a91 & 24 & 21 & 0.87 & 0.87 & 87\% \\
        cb8d261a3 & 24 & 24 & 1.0 & 1.0 & 100\% \\
        cc3532ff6 & 26 & 25 & 0.96 & 0.96 & 96\% \\
        f5a1f0358 & 28 & 28 & 1.0 & 1.0 & 100\% \\
        \hline
        Total & 273 & 257 & 0.92 & 0.93 & 92.7\% \\
        \hline
        \end{array}
        $$
        <h6 class="text-center">EfficientDet-D5 results on Test Data</h6>
    </div>
    <div class="col-sm mt-6 mt-md-0">
        $$
        \begin{array}{ |c|c|c|c|c|c| } 
         \hline
         ImageID & GT & Detected & Precision & Recall & Accuracy \\ 
         \hline
        2fd875eaa & 27 & 24 & 0.88 & 0.88 & 88\% \\
        53f253011 & 31 & 30 & 0.96 & 0.96 & 96\% \\
        51b3e36ab & 27 & 25 & 0.92 & 0.92 & 92\% \\
        51f1be19e & 18 & 18 & 1.0 & 1.0 & 100\% \\
        348a992bb & 37 & 38 & 0.97 & 1.0 & 97\% \\
        796707dd7 & 31 & 26 & 0.83 & 0.83 & 83\% \\
        aac893a91 & 24 & 19 & 0.79 & 0.79 & 79\% \\
        cb8d261a3 & 24 & 24 & 1.0 & 1.0 & 100\% \\
        cc3532ff6 & 26 & 25 & 0.92 & 0.96 & 92\% \\
        f5a1f0358 & 28 & 28 & 1.0 & 1.0 & 100\% \\
        \hline
        Total & 273 & 257 & 0.92 & 0.93 & 92.7\% \\
        \hline
        \end{array}
        $$
        <h6 class="text-center">EfficientDet-D7 results on Test Data</h6>
    </div>
</div>