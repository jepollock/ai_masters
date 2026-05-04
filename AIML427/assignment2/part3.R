# install.packages("recipes")
# install.packages("Metrics")
# install.packages("glmnet")
library(Metrics)
library(recipes)
library(glmnet)

calculate_errors <- function(ActualY, PredictedY) {
  # Get the test error
  mse = mse(TestY, PredictedY)
  rmse = rmse(TestY, PredictedY)
  rss = sum((TestY - PredictedY)^2)
  
  return(list(mse=mse, rmse=rmse, rss=rss))
}

print_errors <- function(Title, Error) {
  sprintf("%s Error: {mse=%.4f, rmse=%.4f, rss=%.4f}", Title, Error$mse, Error$rmse, Error$rss)
}

# https://xkcd.com/221/ - 4 is overused
random_seed = 221
set.seed(random_seed)

Credit <- read.csv("ass2_data_2026/part3/Credit.csv")

PrunedCredit = Credit
# Split Credit into X and Y, Y = balance
Y = PrunedCredit$Balance

# Drop Index
PrunedCredit$X = NULL
PrunedCredit$Balance = NULL

# Obtain the indices of the training sample, 50% train, 50% test.

train = sample(nrow(PrunedCredit), nrow(PrunedCredit)/2)
# Negative indices indicate "everything _except_ the ones listed"
test = -train

TrainCredit = PrunedCredit[train,]
TrainY = Y[train]
TestCredit = PrunedCredit[test,]
TestY = Y[test]

# Encode the nominal fields
# model.matrix  encoding is biased. It converts Gender/M/F into 
# GenderFemale(T|F). This is instantly wrong. There is no situation
# where this is correct (other than homework). It assumes the test
# data has the same set of values, that production has the same set of 
# values and that the values won't change over time.
# NZ Passports have 3 genders, so it's instantly broken.
# Same applies to Ethnicity.
# It should be:
# Student -> binary
# Gender -> one-hot - NOT BINARY
# Married -> binary
# Ethnicity -> one hot - NOT A FIXED SET

# Create the recipe, keep the test data from infecting the model.
# Select everything, balance was pruned earlier.
linear.transform <- recipe(~., data=TrainCredit) %>%
  # One Hot encode it to properly deal with unseen data
  step_dummy(one_hot=TRUE, all_nominal_predictors()) %>%
  prep()

X.linear.train <- bake(linear.transform, new_data=TrainCredit)
X.linear.test <- bake(linear.transform, new_data=TestCredit)

# Linear Regression
linear.model = lm(TrainY~as.matrix(X.linear.train))
linear.predictions = predict(linear.model, newdata=X.linear.test)

# Begin nonlinear regressions.

# Select everything, balance was pruned earlier.
nonlinear.transform <- recipe(~., data=TrainCredit) %>%
  # OneHot encode it to properly deal with unseen data
  step_dummy(one_hot=TRUE, all_nominal_predictors()) %>%
  # Make predictor pairs
  step_interact(terms=~all_predictors():all_predictors())  %>%
  prep()

X.nonlinear.train <- bake(nonlinear.transform, new_data=TrainCredit)
p = ncol(X.nonlinear.train)
X.nonlinear.test <- bake(nonlinear.transform, new_data=TestCredit)

# Ridge Regression
alpha=0
thresh=1e-12
grid=10^seq(3,-2,length=100)
nfolds=10
ridge.model = cv.glmnet(
  as.matrix(X.nonlinear.train), 
  TrainY, 
  alpha=alpha, 
  nfolds=nfolds, 
  lambda=grid, 
  thresh=thresh)

# Select Tuning parameter using cross-validation
ridge.best_lambda = ridge.model$lambda.min
# Get the predictions
ridge.predictions = predict(ridge.model, s=ridge.best_lambda, newx=as.matrix(X.nonlinear.test))

# Lasso Regression
alpha=1
thresh=1e-12
grid=10^seq(3,-2,length=100)
nfolds=10
lasso.model = cv.glmnet(
  as.matrix(X.nonlinear.train), 
  TrainY, 
  alpha=alpha, 
  nfolds=nfolds, 
  lambda=grid, 
  thresh=thresh)

# Select Tuning parameter using cross-validation
lasso.best_lambda = lasso.model$lambda.min
# Get the predictions
lasso.predictions = predict(lasso.model, s=lasso.best_lambda, newx=as.matrix(X.nonlinear.test))
lasso.best_df = lasso.model$glmnet.fit$df[lasso.model$lambda == lasso.model$lambda.min]
lasso.num_selected = p - lasso.best_df

# Report

pdf("ridge_model_lambda.pdf")
plot(ridge.model, sign.lambda=1, main="Ridge Regression Lambda")
dev.off()
pdf("lasso_model_lambda.pdf")
plot(lasso.model, sign.lambda=1, main="Lasso Regression Lambda")
dev.off()

pdf("linear_regression.pdf")
plot(x=linear.predictions, y=TestY, main="Linear Regression", xlab="Predictions", ylab="Tests")
dev.off()
pdf("ridge_regression.pdf")
plot(x=ridge.predictions, y=TestY, main="Ridge Regression", xlab="Predictions", ylab="Tests")
dev.off()
pdf("lasso_regression.pdf")
plot(x=lasso.predictions, y=TestY, main="Lasso Regression", xlab="Predictions", ylab="Tests")
dev.off()

pdf("all_on_one.pdf")
plot(x=linear.predictions, y=TestY, col="black", main="Prediction Comparisons", xlab="Predictions", ylab="True")
points(x=ridge.predictions, y=TestY, col="red")
points(x=lasso.predictions, y=TestY, col="blue")
legend("topleft", legend=c("Linear", "Ridge", "Lasso"), col=c("black", "red", "blue"), lty=1)
dev.off()

sink("part3.txt")
print_errors("Linear Regression", calculate_errors(TestY, linear.predictions))

sprintf("Nonlinear value of p = %d", p)

sprintf("Ridge Regression: Best Lambda = %f", ridge.best_lambda)
print_errors("Ridge Regression", calculate_errors(TestY, ridge.predictions))

sprintf("Lasso Regression: Best Lambda = %f", lasso.best_lambda)
sprintf("Lasso Regression: Degrees of Freedom = %d", lasso.best_df)
sprintf("Lasso Regression: Selected Feature Count = %d", lasso.num_selected)
print_errors("Lasso Regression", calculate_errors(TestY, lasso.predictions))

print("Ridge Coefficients")
ridge.coeff = coef(ridge.model, s="lambda.min")
ridge.coeff.sorted = ridge.coeff[order(ridge.coeff[,1]),]
print(ridge.coeff.sorted)

print("Lasso Coefficients")
lasso.coeff = coef(lasso.model, s="lambda.min")
# the sort doesn't work here for some reason
print(lasso.coeff)
print("sorted coefficients")
print(lasso.coeff[order(unlist(lasso.coeff))])
sink()
