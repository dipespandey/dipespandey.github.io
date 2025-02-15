---
layout: post
title: Things to consider when scaling a software product
date: 2024-09-05 11:59:00-0400
description: 
categories: software scaling infrastructure backend
---

I have been working as a backend software engineer for quite a while now. And in the past few years, I have got the chance to work on a few products that have scaled to a few hundred thousand users. As a backend engineer, it becomes quite important to understand how to approach scaling when it comes to 10x or 100x the number of users.

In this post, I will try to list out some of the important things that I have learned over the years that have helped with scaling.

1. **Monolith vs Microservices**


2. **Database Choice**
Unless you have a very good reason to go for NoSQL, stick to traditional relational databases like PostgreSQL or MySQL. It is the most mature and battle-tested database out there. And these days, there are a lot of json-based adapters in PostgreSQL that provides the similar functionality as NoSQL databases.
Still, NoSQL databases can be useful when:
- Your application requires super-low latency.
- Your data is highly unstructured, or you do not have achieve a lot by converting it to relational data.
- You only need to serialize and deserialize data (JSON, XML, YAML, etc.) or perform simple transformations on it.
- You need to store a massive amount of data.

In most of the projects I have worked on, we started with NoSQL databases in the beginning, but later switched to PostgreSQL as the data model became more complex.

3. **Stateless web tier**


4. **Redundancy**
- Vertical scaling or horizontal scaling?


5. **Logging and Metrics**


