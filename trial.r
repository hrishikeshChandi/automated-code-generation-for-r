options(repos = c(CRAN = 'https://cloud.r-project.org'))

if(!require(ggplot2)){install.packages('ggplot2'); library(ggplot2)}

# Load the mtcars dataset
 data(mtcars)

# Summary statistics
 summary(mtcars)

# Correlation matrix
cor(mtcars)

# Scatter plot of mpg vs. hp
ggplot(mtcars, aes(x = hp, y = mpg)) + geom_point()
