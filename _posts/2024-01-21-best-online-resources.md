---
layout: post
title: My go-to learning resources on the internet
date: 2024-01-21 11:59:00-0400
categories: cs book project learning
gisqus_comments: true
---

In the list below, I have tried to include some resources online that I find myself coming back to again and again. So, it serves like a bookmark for me.
They include topics from computer science, physics, philosophy, and life.

<style>
html[data-theme='dark'] #searchInput {
    background-color: var(--global-card-bg-color);
    color: var(--global-text-color);
    border-color: var(--global-divider-color);
}
</style>

<!-- <input type="text" id="searchInput" onkeyup="searchTable()" placeholder="Search for resources, descriptions, categories..." style="width: 100%; padding: 12px 20px; margin: 8px 0; box-sizing: border-box; border: 2px solid #ccc; border-radius: 4px;"> -->

<script>
function searchTable() {
    var input, filter, table, tr, td, i, j, txtValue;
    input = document.getElementById("searchInput");
    filter = input.value.toLowerCase();
    table = document.querySelector("table");
    tr = table.getElementsByTagName("tr");

    for (i = 1; i < tr.length; i++) {
        tr[i].style.display = "none";
        td = tr[i].getElementsByTagName("td");
        for (j = 0; j < td.length; j++) {
            if (td[j]) {
                txtValue = td[j].textContent || td[j].innerText;
                if (txtValue.toLowerCase().indexOf(filter) > -1) {
                    tr[i].style.display = "";
                    break;
                }
            }
        }
    }
}
</script>


<table class="table table-striped">
    <thead>
        <tr>
            <th>Resource</th>
            <th>Description</th>
            <th>Category</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>
                <a href="https://github.com/remzi-arpacidusseau/ostep-projects/">Projects for an Operating Systems Class</a>
            </td>
            <td>
                Based on courses taught at the University of Wisconsin-Madison, 
                this repository contains a collection of projects that cover a wide range of topics in operating systems.
            </td>
            <td>
                Operating Systems
            </td>
        </tr>
        <tr>
            <td>
                <a href="https://aosabook.org/en/500L/introduction.html">500 lines or less</a>
            </td>
            <td>
                Focuses on the design decisions that programmers make in the small when they are building something new from scratch. 
            </td>
            <td>
                Programming
            </td>
        </tr>
        <tr>
            <td>
                <a href="https://karpathy.github.io/">Andrej Karpathy's Blog</a>
            </td>
            <td>
                A great resource for learning about machine learning and deep learning. His videos on <a href="https://www.youtube.com/@AndrejKarpathy/videos">youtube</a> are also great resources to help you build everything from scratch.
            </td>
            <td>
                Machine Learning
            </td>
        </tr>
        <tr>
            <td>
                <a href="https://news.ycombinator.com/">Hacker News</a>
            </td>
            <td>
                News and discussions about technology and startups.
            </td>
            <td>
                Technology
            </td>
        </tr>
        <tr>
            <td>
                <a href="https://paulgraham.com/articles.html">Paul Graham's Essays</a>
            </td>
            <td>
                Essays on technology, startups, life, and programming.
            </td>
            <td>
                Technology, Philosophy, Life
            </td>
        </tr>
        <tr>
            <td>
                <a href="https://writingexamples.com/">Writing Examples</a>
            </td>
            <td>
                Learn From the Best Writing of All Time
            </td>
            <td>
                Writing
            </td>
        </tr>
    </tbody>
</table>

