---
layout: post
title: "Exploring Data Science"
author: "Dipesh"
---

## The Problem

After some works in text processing and NLP, I had this client who needed to map around 5k resumes to the jobs. Those resumes were related to ship crew jobs, like Captain, Chef, Engineer, etc. So, it was a tough ask to understand the domain,
and create a proper dataset for the problem


## The Solution

crawl data from website periodically: url-  
get related races from several countries, get data from them including schedule, rider attributes, horse attributes  
use the data above to construct a list of keywords  
use the keywords to search tweets containing a set of keywords for a specific race  
use sentiment analysis on the tweet to find the degree of positivity or negativity  
group the sentiments by race, and calculate overall sentiment to reach to a certain point where prediction is possible  

### Sentiment Analysis


## Major Difficulties

> difficult in making the system realtime as I had to crawl the tweets at a certain period of time, because the system I was using was very mediocre in terms of resources  
> requests hitting API limits, both from Twitter and the horse racing aggregation site  
> the keywords obtained made no sense at times, meaning a rider would name his horse anything, also something that is very common in day to day life that would cause confusion in the classification for the model


## Further Improvement

> It was a project I did when I was starting out with machine learning, was about 3-4 years ago. Now that I have learnt several ways the accuracy of sentiment analysis can be brought up to a greater accuracy, I am working on implementing a better model for sentiment analysis.
Also, I have been looking at faster ways to scrape and crawl the website because that's what is also consuming a lot of the overall time.
