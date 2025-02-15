---
layout: post
title: How I run everything in a cheap VPS
date: 2024-02-08 11:59:00-0400
description: Using a $5 VPS to run my blog, and other few projects I work on
categories: vps contabo 
giscus_comments: true
---

Apart from this blog which I host on [GitHub Pages](https://pages.github.com/), I also host a few other projects that have to run some server side logic. So, for this purpose, I have been using a $5/month VPS from [Contabo](https://contabo.com/) for about a year now. While Contabo is not the best option out there(I have heard good things about [Hetzner](https://www.hetzner.com/cloud/)), it has been a good enough option for me except for one time it went down for about a day when there was a spike in traffic. But for the price and the amount of traffic I get, it has been a good enough option for me.

This is how I run several projects on this VPS.
1. Django with gunicorn and nginx for all backend logic for all projects
2. Celery for periodic jobs
3. PostgreSQL for database
4. Redis for caching and queuing
5. Nginx for reverse proxy
6. Certbot for SSL certificates
7. Webshare for rotating proxy IP addresses
8. Github Actions for CI/CD
9. PM2 for managing multiple frontend instances
10. Cloudflare for DNS and CDN

Currently, the following projects are running on this VPS:
<table class="table">
  <thead>
    <tr>
      <th>Project</th>
      <th>Type</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><a href="https://nordstartup.com/">Nordstartup</a></td>
      <td>Django</td>
      <td>Remote job board for Nordic countries</td>
    </tr>
    <tr>
      <td><a href="https://childtales.xyz/">Childtales</a></td>
      <td>Nuxt.js</td>
      <td>Fairytale stories generation using AI for children</td>
    </tr>
    <tr>
      <td><a href="https://merostocks.com/">Merostocks</a></td>
      <td>Nuxt.js</td>
      <td>Nepalese stock market portfolio management</td>
    </tr>
    <tr>
      <td><a href="https://api.genalize.com/docs/">Genalize API</a></td>
      <td>Django</td>
      <td>API for Genalize</td>
    </tr>
  </tbody>
</table>
