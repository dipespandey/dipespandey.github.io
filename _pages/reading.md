---
layout: page
title: Reading
permalink: /reading/
description: A list of books I have read/been reading and the ones I plan to read.

nav: true
nav_order: 5
horizontal: false
display_categories: [text, image, video]
---

If you are interested in my collection of online resources to learn about computer science, physics, philosophy, and life, you can check out my [best online resources](/blog/2024/best-online-resources) post.

<!-- Search bar -->
<style>
html[data-theme='dark'] #searchInput {
    background-color: var(--global-card-bg-color);
    color: var(--global-text-color);
    border-color: var(--global-divider-color);
}
.reading {
    color: #dfa63a;
}
.readlist {
    color: #7777d9;
}
.read {
    color: #3e843e;
}
.notes {
    font-size: 12px;
}
</style>

<input type="text" id="searchInput" onkeyup="searchTable()" placeholder="Search for books, authors, genres..." style="width: 100%; padding: 12px 20px; margin: 8px 0; box-sizing: border-box; border: 2px solid #ccc; border-radius: 4px;">

<table class="table table-striped" style="font-size: 12px;" id="bookTable">
<thead>
<tr>
    <th>Book</th>
    <th>Author</th>
    <th>Genre</th>
    <th>Status</th>
    <th>Notes</th>
</tr>
</thead>
<tbody>
<tr>
    <td><a href="https://doc.rust-lang.org/book/" target="_blank">The Rust Programming Language</a></td>
    <td>Steve Klabnik, Carol Nichols</td>
    <td>Programming</td>
    <td class="reading">Reading</td>
    <td class="notes">A book on the Rust programming language.</td>
</tr>
<tr>
    <td><a href="https://www.amazon.com/Database-Internals-Deep-Distributed-Systems/dp/1492040347" target="_blank">Database Internals: A deep-dive into how distributed data systems work</a></td>
    <td>Alex Petrov</td>
    <td>Databases</td>
    <td class="reading">Reading</td>
    <td class="notes">A book on how the internals of a distributed database work.</td>
</tr>
<tr>
    <td><a href="https://www.amazon.com/Beginning-Infinity-Explanations-Transform-World/dp/0143121359" target="_blank">The Beginning of Infinity</a></td>
    <td>David Deutsch</td>
    <td>Philosophy</td>
    <td class="reading">Reading</td>
    <td class="notes">Talks about how contrary to the popular belief, human beings are not just a tiny speck of dust in the universe, our creativity and intelligence is what makes us unique.</td>
</tr>
<tr>
    <td><a href="https://www.amazon.com/Our-Mathematical-Universe-Ultimate-Reality/dp/0307744256" target="_blank">Our Mathematical Universe</a></td>
    <td>Max Tegmark</td>
    <td>Science</td>
    <td class="readlist">Read list</td>
    <td class="notes">A book on the nature of the universe and how mathematics is the language of the universe.</td>
</tr>
<tr>
    <td><a href="https://www.amazon.com/Science-Interstellar-Kip-Thorne/dp/0393351378" target="_blank">The Science of Interstellar</a></td>
    <td>Kip S. Thorne</td>
    <td>Science</td>
    <td class="readlist">Read list</td>
    <td class="notes">A book on the science of the movie Interstellar.</td>
</tr>
<tr>
    <td><a href="https://www.amazon.com/G%C3%B6del-Escher-Bach-Eternal-Golden/dp/0465026567" target="_blank">Gödel, Escher, Bach</a></td>
    <td>Douglas Hofstadter</td>
    <td>Philosophy</td>
    <td class="readlist">Read list</td>
    <td class="notes">A book on the nature of intelligence and creativity.</td>
</tr>
<tr>
    <td><a href="https://www.amazon.com/Dopamine-Nation-Finding-Balance-Indulgence/dp/152474672X" target="_blank">Dopamine Nation</a></td>
    <td>Anna Lembke</td>
    <td>Science</td>
    <td class="readlist">Read list</td>
    <td class="notes">A book on the science of dopamine and how it affects our behavior.</td>
</tr>
<tr>
    <td><a href="https://www.amazon.com/Poor-Charlies-Almanack-Essential-Wisdom/dp/1953953247" target="_blank">Poor Charlie's Almanack - The Essential Wit and Wisdom of Charles T. Munger</a></td>
    <td>Peter D. Kaufman</td>
    <td>Biography, Humor</td>
    <td class="readlist">Read list</td>
    <td class="notes">A collection of Charlie Munger's thoughts on life, business, and investing.</td>
</tr>
<tr>
    <td><a href="https://www.amazon.com/Invent-Wander-Collected-Writings-Bezos/dp/1647820715" target="_blank">Amazon Letters to Shareholders 1997 - 2020</a></td>
    <td>Jeff Bezos</td>
    <td>Business</td>
    <td class="readlist">Read list</td>
    <td class="notes">A collection of letters from Jeff Bezos to Amazon shareholders.</td>
</tr>
<tr>
    <td><a href="https://www.amazon.com/Antifragile-Things-That-Disorder-Incerto/dp/0812979680" target="_blank">Antifragile</a></td>
    <td>Nassim Nicholas Taleb</td>
    <td>Philosophy, Economics</td>
    <td class="read">Read</td>
    <td class="notes">A book on how to be antifragile.</td>
</tr>
<tr>
    <td><a href="https://www.amazon.com/Atomic-Habits-Proven-Build-Break/dp/0735211299" target="_blank">Atomic Habits</a></td>
    <td>James Clear</td>
    <td>Self-help</td>
    <td class="read">Read</td>
    <td class="notes">A very practical book on how habits are formed and how to break them.</td>
</tr>
<tr>
    <td><a href="https://www.amazon.com/Hard-Thing-About-Things-Building/dp/0062273205" target="_blank">The Hard Thing about Hard Things</a></td>
    <td>Ben Horowitz</td>
    <td>Business</td>
    <td class="read">Read</td>
    <td class="notes">A book on how to build and run a startup with stories from his experience at Netscape and Loudcloud.</td>
</tr>
<tr>
    <td><a href="https://www.amazon.com/Metamorphosis-Franz-Kafka/dp/1557427666" target="_blank">Metamorphosis</a></td>
    <td>Franz Kafka</td>
    <td>Fiction</td>
    <td class="read">Read</td>
    <td class="notes">Interesting story on how human life is not always what we expect it to be.</td>
</tr>
<tr>
    <td><a href="https://www.amazon.com/Chaos-Monkeys-Obscene-Fortune-Failure/dp/0062458191" target="_blank">Chaos Monkeys</a></td>
    <td>Antonio Garcia Martinez</td>
    <td>Business</td>
    <td class="read">Read</td>
    <td class="notes">A story about how companies are built and how they fail. Has stories from Google, Facebook, Twitter, etc. during their early days.</td>
</tr>
<tr>
    <td><a href="https://www.amazon.com/American-Prometheus-Triumph-Tragedy-Oppenheimer/dp/0375726268" target="_blank">American Prometheus</a></td>
    <td>Kai Bird, Martin J. Sherwin</td>
    <td>History</td>
    <td class="read">Read</td>
    <td class="notes">A story about the development of the atomic bomb and the people involved, especially J. Robert Oppenheimer.</td>
</tr>
<tr>
    <td><a href="https://www.amazon.com/Sapiens-Humankind-Yuval-Noah-Harari/dp/0062316117" target="_blank">Sapiens</a></td>
    <td>Yuval Noah Harari</td>
    <td>History</td>
    <td class="read">Read</td>
    <td class="notes">An excellent starter book on history and human evolution.</td>
</tr>
<tr>
    <td><a href="https://www.amazon.com/Meditations-Marcus-Aurelius/dp/9354407269" target="_blank">Meditations</a></td>
    <td>Marcus Aurelius</td>
    <td>Philosophy</td>
    <td class="read">Read</td>
    <td class="notes">A collection of Marcus Aurelius's thoughts on life and how to live it.</td>
</tr>
</tbody>
</table>

<script>
function searchTable() {
    var input = document.getElementById("searchInput");
    var filter = input.value.toLowerCase();
    var table = document.getElementById("bookTable");
    var tr = table.getElementsByTagName("tr");

    for (var i = 1; i < tr.length; i++) {
        var td = tr[i].getElementsByTagName("td");
        var found = false;
        
        for (var j = 0; j < td.length; j++) {
            var cell = td[j];
            if (cell) {
                var text = cell.textContent || cell.innerText;
                if (text.toLowerCase().indexOf(filter) > -1) {
                    found = true;
                    break;
                }
            }
        }
        
        tr[i].style.display = found ? "" : "none";
    }
}
</script>