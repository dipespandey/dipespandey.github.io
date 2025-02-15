---
layout: page
title: ML Models
permalink: /models/
description: Over the past few years, I have trained and fine-tuned a few models for different tasks. In this page, I am trying to document the process involved.

nav: true
nav_order: 1
horizontal: false
display_categories: [text, image, video]
---

<div class="models">
  {%- assign sorted_models = site.models | sort: "published" | reverse %}
    {%- for model in sorted_models -%}
      {% include models.html %}
    {%- endfor %}
</div>
