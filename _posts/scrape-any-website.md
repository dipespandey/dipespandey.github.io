---
layout: post
title: Building the Spotify Recommender System from scratch
date: 2025-05-05 11:59:00-0400
description: 
categories: recommendation machine-learning 
---

In the [previous post](/2018-01-04-svd-for-recommendation), I wrote about the process of building a basic movie recommendation system using Singular Value Decomposition (SVD). While the system was able to produce pretty good results, it had one problem: it depended on previous ratings to make recommendations to a user. 

In this post, I will write about how Spotify uses it's own smart algorithm to recommend songs to more than half a billion users over the world.

### The Spotify Recommender System
[Annoy or Approximate Nearest Neighbors Oh Yeah](https://github.com/spotify/annoy) is the nearest neighbor algorithm used by Spotify to recommend songs to users. It is a tree-based algorithm that is able to find the nearest neighbors to a given point in a high-dimensional space.

