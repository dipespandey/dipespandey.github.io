---
layout: page
title: Pod2Reels
description: Podcast to reels using AI 
img: assets/img/podcast.jpg
importance: 4
category: sideproject
---

This is a side project that converts youtube podcasts into smaller chunks of reels. This is how it works:

1. Download the youtube podcast
2. Get the transcript of the podcast
3. Use GPT-4 api to convert the transcript into several categories based on the content discussed in the podcast. This also provides the 
starting and ending timestamps of the content for each category.
4. Use ffmpeg to split the podcast video into several chunks based on the timestamps.
5. Generate subtitles for each chunk using ffmpeg.

### Outputs
For the input video from the Lex Fridman podcast, about 10 reels are generated with subtitles embedded in the mobile sized 
reels. The following shows the input video and the output reels(only 2 shown here).
<div class="row">
    <div class="col-sm mt-3 mt-md-0 d-flex align-items-center">
        Input video:
        <iframe width="720" height="500" style="width: 100%;" src="https://www.youtube.com/embed/Ff4fRgnuFgQ">
        </iframe>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        Output videos/reels:
        <video src="/assets/video/pod1.mp4" controls width="300" height="300"></video>
        <video src="/assets/video/pod2.mp4" controls width="300" height="300"></video>
    </div>
</div>
