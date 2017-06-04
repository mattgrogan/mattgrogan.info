+++
title = "The Mean, MAD, and More: Measuring accuracy and precision"
date = "2017-06-04"
draft = false
tags = ["stats"]
+++

### Background

It is often important in a business setting to measure the accuracy and precision of a value compared to a target. However, it can be difficult to precisely communicate these measurements to non-technical teams. This is one approach.

First, let's define the terms:

* __Accuracy__: The closeness of a value to its target.
* __Precision__: The closeness of a set of measurements to each other, irrespective of closeness to target.

We will look at metrics that can help us describe the degree of accuracy and precision of a dataset and discuss appropriate remediation.

### Example

Imagine we have a jar of currency: coins and bills of various denominations. We ask four groups of thirty students to guess the total value of the currency in the jar. The students are not aware that the jar contains exactly __$500__.

The guesses are shown below:

```{r}
> d.data
   Group_1 Group_2 Group_3 Group_4
1      441     171     259     122
2      441     191     311     175
3      446     204     313     213
4      447     211     324     239
5      462     216     342     256
6      467     216     348     308
7      471     217     358     319
8      476     222     369     346
9      476     229     373     387
10     477     230     433     509
11     488     233     467     519
12     489     235     485     520
13     490     235     495     520
14     497     237     500     523
15     501     243     520     533
16     502     244     533     539
17     516     245     543     582
18     517     246     559     601
19     518     248     563     633
20     518     252     567     640
21     525     263     577     678
22     533     264     600     730
23     533     271     610     741
24     534     272     629     762
25     537     274     644     781
26     542     285     705     883
27     552     285     708     894
28     556     289     710     914
29     566     291     723     934
30     571     297     782     972
```

Our task is to define __numerical measurements__ that properly describe these four groups.

### Visualization

Before we get into calculating numerical measurements, let's take a look at the data.

```{r}
ggplot(d, aes(x=x)) +
  geom_histogram() +
  facet_wrap(~ group_nbr) +
  geom_vline(xintercept=500, color="red", linetype=2) +
  xlim(0, 1000)
```

![Histogram](/images/accuracy_precision_hist.png)

From this visualization, we can make the following observations:

* Groups 1 and 3 are centered around the target value of __500__, with group 1 clustering more closely. They are __accurate__ but vary in their __precision__.
* Group 2 is tightly grouped, but far from the target. The group is __precise__ but not __accurate__.
* Group 4 shows a wide spread and is neither __accurate__ nor __precise__.


### The Mean: How accurate is the group itself?

Taking the mean reveals the central tendency of each group.

```{r}
> d %>%
+   group_by(group_nbr) %>%
+   summarize(mean = round(mean(x)))

  group_nbr  mean
1   Group_1   495
2   Group_2   260
3   Group_3   486
4   Group_4   395
```

The means reasonably close for the two _accurate_ groups: one and three, with group four further off target. Group two has the "worst" performance - judging by the mean.

If we use only the mean to compare the groups, we lose the nuances between groups one and three. We also lose information regarding the precision of group two.

_The mean does not give us enough information to characterize the groups._

### The MAD: How accurate were the members of the group?

The _Mean Absolute Deviation (MAD)_ is one way to numerically discriminate between groups one and three. Recall that both groups are __accurate__ in that they cluster around the target, but they vary in their __precision__.

To take the MAD, follow these steps:

* First, subtract the target value from each individual measurement. For example, if our first measurement is `441`, the deviation will be `441 - 500 = -59`.
* Next, take the absolute value of each measurement (`|-59| = 59`). This prevents positive and negative deviations from offsetting each other.
* Finally, average the absolute deviations. This is the _mean absolute deviation_ from the target.

```{r}
> d %>%
+   group_by(group_nbr) %>%
+   mutate(deviation = x - target,              # The deviation from target
+          abs_deviation = abs(deviation)) %>%  # Absolute value of deviation
+   summarize(mad = round(mean(abs_deviation))) # The mean absolute deviation

  group_nbr   mad
1   Group_1    27
2   Group_2   240
3   Group_3    79
4   Group_4   279
```

We can now say that, _on average_, students in group one were $27 away from the true value of $500. Some people conceptualize this as a percent: _on average, students in group one were 5.4% (`27 / 500 * 100%`)  off target, while students in group three were 15.8% off target._

### The Group-MAD: How precise are members of the group?

Let's take another look at group two.

![Group Two](/images/group_2_only.png)

The Mean and MAD calculations described group two's guesses as being far from the target, which is true. But these measurements do not help us learn that the guesses are clustered together (that is, they are _precise_). The Group-MAD provides us insight into this nuance.

To calculate the Group-MAD, use the mean of the group in place of the target value and otherwise follow the MAD formula as described above.

```{r}
> d %>%
+   group_by(group_nbr) %>%
+   mutate(deviation = x - mean(x),              # The deviation from group mean
+          abs_deviation = abs(deviation)) %>%  # Absolute value of deviation
+   summarize(grp_mad = round(mean(abs_deviation))) # The mean absolute deviation for the group

  group_nbr   grp_mad
1   Group_1    28
2   Group_2    28
3   Group_3    78
4   Group_4   256
```

Now we see that group two is as precise as group one, but the group is obviously off target. Therefore, the group is precise, but not accurate. If we were to intervene (for example, training), the focus should be on improving accuracy only.

### The Bias: Do group members trend above or below the target?

Now we want to improve group two, but none of the measurements described above help us determine the direction to move. For this, we need the _bias_.

The procedure for calculating bias is the same as for the MAD, except we won't take the absolute value.

```{r}
> d %>%
+   group_by(group_nbr) %>%
+   mutate(deviation = x - target) %>%     # The deviation from target
+   summarize(bias = round(mean(deviation))) # The bias

  group_nbr   bias
1   Group_1    -5
2   Group_2  -240
3   Group_3   -14
4   Group_4  -105
```

All four groups have a negative bias, with some groups having a larger bias than others.

### Insights and Responses

Since all metrics are now available, let's take a look at them and see what insights we can gather.

```{r}
> d %>%
+   group_by(group_nbr) %>%
+   mutate(deviation_tgt = x - target,                  # The deviation from target
+          abs_deviation_tgt = abs(deviation_tgt),      # Absolute value of deviation
+          grp_deviation = x - mean(x),                 # The deviation from group mean
+          grp_abs_deviation = abs(grp_deviation)       # Absolute value of deviation
+          ) %>%  
+   summarize(mean = round(mean(x)),                    # The mean
+             mad = round(mean(abs_deviation_tgt)),     # The MAD
+             mad_pct = round(mad / 500, 3),            # MAD as a % of target
+             grp_mad = round(mean(grp_abs_deviation)), # The Group-MAD
+             bias = round(mean(deviation_tgt))         # The bias
+             )

  group_nbr  mean   mad mad_pct grp_mad  bias
1   Group_1   495    27   0.054      28    -5
2   Group_2   260   240   0.480      28  -240
3   Group_3   486    79   0.158      78   -14
4   Group_4   395   279   0.558     256  -105
```

__Group 1__'s mean is nearest the target value of 500. The low MAD, Group-MAD, and near-zero Bias tell us that this group is the most accurate and precise of the four.

_Recommended action: None_

__Group 2__ clearly had some challenge hitting the target, but the low Group-MAD and the Bias' consistency with the MAD (`240 vs. -240`) tells us that this group is precise.

_Recommended action: Work to align the group with the target  without affecting their precision._

__Group 3__'s mean and MAD are slightly worse than the first group. The closeness of the MAD and Group-MAD shows that the group's guesses are centered around the target (that is, they are accurate). However, both metrics are higher than group one, which tells us that this group is less precise than the former.

_Recommended action: Work to increase precision._

__Group 4__'s guesses are all over the place and the metrics show it! While the mean is not as off-target as Group two, the MAD is much worse. On average, the guesses of students in group four were 55% off target.

_Recommended action: Anything that helps both precision and accuracy._

### Frequently Asked Questions

_We already have a measure of precision. It's called the standard deviation._

[That's not a question, professor!](https://youtu.be/QLnDBDUJYmQ) :p

These are simply other descriptive statistics that can help us communicate with stakeholders. I have found that saying individuals in a particular group miss a target by 5% can be easier to absorb than a standard deviation (or confidence interval for that matter.) Your mileage may vary.

_Why would you use MAD over RMSE?_

The Root Mean Squared Error (RMSE) is another way of describing variation. Instead of taking absolute values and averaging them, the RMSE squares them prior to averaging. And then take the square root to get to the original units.

This has two consequences: first, a number squared is always positive so there's no need to take an absolute value. Second, the penalty for larger deviations is much higher using the RMSE.

The penalty is a good feature to use if larger errors result in much greater costs.

### Summary

| Accuracy | Precision | Mean | MAD (Target) | MAD (Group) | Bias |
|----------|-----------|------|--------------|-------------|------|
| High     | High      | Near Target | Lower | Lower | Near Zero |
| Low      | High      | Far from Target | Higher | Lower | Far from Zero |
| High     | Low       | Near Target | Lower | Higher | Near Zero |
| Low      | Low       | Any | Higher | Higher | Any |
