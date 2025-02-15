<!-- ---
layout: post
title: Visualizing a LLM
date: 2025-01-02 11:59:00-0400
categories: llm
gisqus_comments: true
---

In this post, I will try to visualize how the layers of a Large Language Model (LLM) work.
Usually for me, if I want to understand a machine learning concept and want it to stick, visualizing
helps a lot along with the math.

So, let's take a simple LLM that can be trained with minimal resources locally and see what happens to the 
input text as it passes through the layers.

I will be using the gemma-2 [LLM](https://github.com/karpathy/llm) model by microsoft because it is small
but has been trained on a large corpus of text. So, we should be able to see some sensible outputs with it's 
finetuned model.



References:
- https://www.youtube.com/watch?v=UGO_Ehywuxc
- https://transformer-circuits.pub/2024/july-update/index.html#dark-matter -->