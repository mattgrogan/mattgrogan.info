+++
title = "Teaching R with a focus on tidy, dplyr, and ggplot2"
date = "2015-07-31"
draft = false
tags = ["stats", "r"]
+++

In order to build more familiarity and comfort with R across GIA, I started teaching a short (3 hour) Introduction to R course. I've found that the huge steps forward by Hadley and others render a lot of the older guides obsolete.

In the spirit of open-source, I cobbled together my own syllabus. I tried to cover many of the common use cases that data scientists encounter in their daily work.

All the instruction is over at https://github.com/mattgrogan/instruction

## Hour 1: Introduction to R

The first hour is an introduction to base R, mostly. It covers some data types, positional and logical indexing, data frames, and tables. The lesson ends with base graphics and a reminder (err, plea!) to follow common coding guidelines.

[Hour 1 on GitHub](https://github.com/mattgrogan/instruction/blob/master/1-intro-to-r/1-intro-base-r.md)

## Hour 2: Data Wrangling

This section is one of my favorites because data scientists often spend a majority of their time acquiring, cleaning, and transforming data. I cannot express how useful it is to have these tools at your disposal.

We used a real-life dataset of grading results on diamonds sent to three different gemological laboratories. We used the `tidy` package to reshape the data in various ways. Afterwards we jumped into `dplyr`'s five verbs and then added `group_by()`.

[Hour 2 on GitHub](https://github.com/mattgrogan/instruction/blob/master/2-data-wrangling/2-data-wrangling.md)

## Hour 3: Plotting with ggplot2

Again, as this course is focused on exploratory data analysis, we use `ggplot2` to visualize the data in ways that will help guide data scientists as they dive into the data.

I designed the exercises to build up from a simple plot to something relatively complex. The trick here is to be clear about the definitions (`geoms`, `aesthetics`, `facets`, etc.)

[Hour 3 on GitHub](https://github.com/mattgrogan/instruction/blob/master/3-ggplot/3-ggplot.md)

## Results

Overall we had a great class and I received positive feedback. It is often said that the best way to learn something is to teach it, and I definitely appreciated the effort it took to gather this information into a compelling format.
