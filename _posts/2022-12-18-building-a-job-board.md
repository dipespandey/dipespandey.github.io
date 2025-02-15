---
layout: post
title: Building a job board for personal use
date: 2022-12-10 11:59:00-0400
description: an example of a blog post with giscus comments
categories: job-board scraping proxy-ip remote-jobs
giscus_comments: true
---

The purpose of this project is to build a remote job board that serves my needs. I am currently a software engineer at a company where I enjoy working but not long ago, I used to struggle finding remote job opportunities. I used to browse a few job boards in the past, but I found them to be quite limited in terms of the type of jobs they offer, especially how they treat remote jobs based on the location limitations like "only US based jobs" or "only jobs in Europe" or "visa required". So, I am building this job board that makes the process of finding remote jobs easier.

### Sources (as of now)
1. [otta.com](https://app.otta.com/)
2. [80000hours](https://jobs.80000hours.org/)
3. [remote.com](https://remote.com/jobs/)
4. [weworkremotely.com](https://weworkremotely.com/)
8. [workingnomads.co](https://workingnomads.co/)


### Setup
Database: [PostgreSQL](https://www.postgresql.org/)  
Backend: [Python](https://www.python.org/), [Django](https://www.djangoproject.com/)  
API: [Django REST Framework](https://www.django-rest-framework.org/)  
Frontend: [Vue.js](https://vuejs.org/)  
Scraping: [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), [requests](https://docs.python-requests.org/en/latest/), [selenium](https://selenium.dev/)
Proxy IP: [Webshare](https://www.webshare.io/)
Queue: [Redis](https://redis.io/)   
Worker: [Celery](https://docs.celeryq.dev/)  

### Data Collection
Every midnnight, the sources mentioned above are scraped and the data is stored in the database.
To avoid being rate limited, the scraping is done with rotating proxy IP addresses. I have used [Webshare](https://www.webshare.io/) for this purpose. It is a cheap option and I pay only $3/month for 100 rotating proxy IP addresses. It provides me with an API which I can use to rotate the IP addresses on each request.
- Use of database triggers to scrape jobs:


### Periodic Jobs
I have used [Celery](https://docs.celeryq.dev/) to run periodic jobs. I have a few periodic jobs that I run every day.
- Scraping jobs from sources
- Cleaning up the database

