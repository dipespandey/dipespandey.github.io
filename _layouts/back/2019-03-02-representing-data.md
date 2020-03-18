---
layout: post
title: "Represent Your Data"
author: "Dipesh"
---

This blog post contains introductory content on data science, **the Representation of Data**. I will try to cover how important it is to understand how almost all types of data are represented. Representation is the entry point to most of the data science projects, and it is very crucial that we spend a good bit of time thinking around what's the good way of doing it.

Wikipedia says "data is any sequence of one or more symbols given meaning by specific act(s) of interpretation". So, interpretation is something that plays a big role in how we apply science in data. The idea is to be able to bring out as much information from the data as possible. This process is governed by a phenomenon called Entropy, thanks to **Claude Shannon** for his Information Theory. He says "semantic aspects of data are irrelevant, and nature and meaning of data doesn’t matter when it comes to information content". Instead he quantified information in terms of probability distribution and “uncertainty”.  

We will get back to Shannon and his contribution in the upcoming posts. This one is focused on the four mainstream useful data representation formats: **text**, **audio**, **image** and **video**.
  
  
### Text and Image

The fun thing with computers is that we can play awesome games or call someone at the other side of the world in realtime using them but for every task we do, they represent every data in the binary format: 0 and 1 under the hood. We will dissect how computers store data in each of the formats and see how knowing this will help us further our data journey.
  
    
#### Representing Text

The requirement is to represent/store all the alphanumeric characters as well as the symbols that may arise in real world within a computer memory. 
  
The most commonly adopted method is ASCII which uses 8 bits to represent the text data, meaning we have 256 different combinations, but the first bit is always 0 as a control bit, so we get 128 characters to represent. 
Some of the character representations are shown below:
    
So, the word “computers” (all lower-case) would be 01100011 01101111 01101101 01110000 01110101 01110100 01100101 01110010 01110011.
  <img src="{{ "/assets/ascii.png" | relative_url }}">
   
The above table shows a few initial characters represented in ASCII.

  
#### Representing Image

Computers use the basic additive colors red, green and blue(RGB) for representing all the colors on the screen. Each pixel on a screen has 3 tiny colors: one red, one green and one blue. The combination of these makes it possible to obtain every other color we can see in computers.  
  
Each of these three colors are represented in 8 bits, 24 bits in total. So, the 8 bits combinations of these three colors determine which color we're looking at.

<img src="{{ "/assets/rgb.png" | relative_url }}">

In the above image, we can see red having it's value 167, green as 77 and blue as 193. Converting them into 8 bit binary notation we get a, b an c respectively. The common way of representing them is to use 24 bits concatinating the 8 bits starting from red, to green to blue. So, the numbers 167, 77 and 193 would look like abc when in a computer memory. As long as computer finds a way to know this is a color, it will know the first 8 bits are for red, next 8 for green and the remaining 8 bits for the blue.   
  
When we say a 20 megapixel photo, it means it needs 60 million numbers to be recorded in order to represent it accurately. 


### Why representation matters ?

 ![Alt Text](https://computersciencewiki.org/images/c/c0/8-gif.gif)
Let's get back to the example of representing an image. The image above tries to represent a handwritten letter in terms of matrices. Matrices provide a flexible way to represent images in terms of rows and columns. We can represent the image of a handwritten character in terms of the pixel values it contains. If we look at colored images, we need three matrices for red, green and blue intensities of each row and column of the image. 
  
Above example however uses a single matrix to represent the image pixel intensities. The no. of rows and columns or the dimension of the matrix is to be chosen by ourselves based upon the available memory and the complexity of the image itself. 
