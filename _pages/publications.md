---
layout: page
permalink: /publications/
title: Publications
years: [2022, 2021, 2020]
nav: true
nav_order: 4
---
<div class="publications">

{%- for y in page.years %}
  <h2 class="year">{{y}}</h2>
  {% bibliography -f papers -q @*[year={{y}}]* %}
{% endfor %}

</div>
