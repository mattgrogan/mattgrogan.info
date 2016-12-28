+++
date = "2015-08-20"
title = "Estimating Contribution to Variance in R"
draft = false
categories = ["stats"]
+++

## Background

Oracle's [Crystal Ball](http://www.oracle.com/us/products/applications/crystalball/overview/index.html) is an Excel add-in that makes it easy to create Monte-Carlo simulations and examine the output distributions.

One of Crystal Ball's diagnostic tools is called the __Contribution to Variance__ chart, shown below. Today's task is to recreate this chart in R.

![Oracle Crystal Ball Sensitivity](images/crystal_ball_sensitivity.png)

## The Contribution to Variance Function

The `contribution_to_variance` function performs the calculation by taking a formula, which specifies the dependent and independent variables, and a data frame. It will return a data frame containing one row for each independent variable. Columns in the data frame show the [Spearman correlation coefficient](http://en.wikipedia.org/wiki/Spearman%27s_rank_correlation_coefficient) and the percent of variation contributed.

``` r
contribution_to_variance <- function(formula, data) {

  # Use model.frame to return a data frame with proper variables from formula
  tmp_data <- model.frame(formula, data)

  # Set up an output dataframe
  out_data <- data.frame(var = names(tmp_data)[-1],
                     cor = NA,
                     pct = NA)

  # Find the correlations
  out_data$cor <- sapply(tmp_data[ , -1], cor, y = tmp_data[, 1])

  # Find the contribution to variance
  out_data$pct <- sign(out_data$cor) * out_data$cor ^ 2 / sum(out_data$cor ^ 2)

  # Order the variable column so that it plots nicely
  row_order <- order(out_data$pct)
  out_data$var <- ordered(out_data$var,
                           levels = out_data[row_order, 'var'])

  # Return data to caller
  out_data[row_order, ]

}

```

## Trying the Function

We'll test the function with a simulated dataset consisting of three independent variables and one dependent variable. The model formula weights each variable differently and is identical to that used to create the Crystal Ball chart above.

``` r
# Number of samples
n <- 10000

# Create the independent variables
x1 <- runif(n, 0, 100)
x2 <- runif(n, 0, 100)
x3 <- runif(n, 0, 100)

# Create the dependent variable
y <- (3 * x1 + 2 * x2 - x3) / 3

# Put it all into a data frame
input_data <- data.frame(x1 = x1, x2 = x2, x3 = x3, y = y)

var_data <- contribution_to_variance(y ~ x1 + x2 + x3, data = input_data)

> var_data
  variable        cor         pct
3       x3 -0.2518511 -0.06398669
2       x2  0.5354290  0.28920486
1       x1  0.8007315  0.64680845

```

These values are reasonably close to the output from Crystal Ball so we will conclude that the algorithm matches that used by Oracle.

## Creating the Chart

Next, we'll use `ggplot2` to create the chart.

``` r
library(ggplot2)

ggplot(var_data, aes(x = variable, y = pct, fill = variable)) +
  geom_bar(alpha = 0.50, stat = "identity") +
  geom_text(aes(y = pct / 2, label = paste0(round(pct * 100, 1), "%"))) +
  coord_flip() +
  ggtitle("Contribution to Variance")

```

![Contribution to Variance](images/contribution_to_variance.png)

## A Real(ish) Dataset

Now let's try the function on the [Motor Trend Car Road Test](https://stat.ethz.ch/R-manual/R-devel/library/datasets/html/mtcars.html) (`mtcars`) dataset.

``` r
mtcar_var <- contribution_to_variance(mpg ~ cyl + disp + hp + drat +
                                    wt + qsec + vs + am + gear +
                                    carb, data = mtcars)

ggplot(mtcar_var, aes(x = variable, y = pct, fill = variable)) +
  geom_bar(alpha = 0.50, stat = "identity") +
  geom_text(aes(y = pct / 2, label = paste0(round(pct * 100, 1), "%"))) +
  coord_flip() +
  ggtitle("Contribution to Variance")

```

![mtcars Contribution to Variance](images/mtcars_contribution_to_variance.png)

From this chart it is clear that the weight (`wt`), number of cylinders (`cyl`), and displacement (`disp`) are the largest negative factors affecting miles per gallon (`mpg`).

## Caveats

As Oracle's [Documentation](http://docs.oracle.com/cd/E17236_01/epm.1112/cb_user/frameset.htm?ch07s04s03.html) notes, the Contribution to Variance calculation can be misleading in some instances. This is particularly true when the inputs are correlated or contain [non-monotonic](http://en.wikipedia.org/wiki/Monotonic_function) relationships.

## Conclusion

Despite the drawbacks of this technique, this calculation can be a useful tool to diagnose models and communicate sensitivity information to business users. Let me know what you think in the comments.
