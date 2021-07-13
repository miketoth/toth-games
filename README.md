# toth-games

## Developing

* Use `hugo server` to run locally
* Run `hugo` before checking in to generate files (we don't have CI right now)

## Using Disqus

To prevent split threads across posts, we need to add some additional data to each post. For example:

``` my-first-post.md
---
title: "Testing!"
date: 2020-07-24T15:39:23-07:00
draft: false
disqus_identifier: 'a unique identifier for each page where Disqus is present'
disqus_title: 'a unique title for each page where Disqus is present'
disqus_url: 'unique URL for each page where Disqus is present'
---

![Legends Logo](/toth-games/legends_logo_v1.png)

Look at this cool new game we made

There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.

```
