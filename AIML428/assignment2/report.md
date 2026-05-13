# Assignment 2

## Task 1
### Bar Chart

#### How it works
The token probability graph has a really high probability for the first token. The presence of a trailing space on the prompt controls this value. The model is unwilling to generate invalid text - which it would be doing if the space wasn't there.

The code takes the top-10 probabilities and their indices. It then creates a colour list, all black, except for the element representing the selected token.

ref: model.py - plot_probs

#### Temperature

Run and generate 3 different sample graphs for the same prompt.

- temperature = 0 - invalid won't work.
- temperature = 0.8
- temperature = 1.0
- temperature = 2.0

Temperature is used to divide the raw logit values, If the value is < 1, it will work to grow the logit values.

If this is <0, it will increase the exponent on the numerator, benefiting larger values, making the distribution steeper. If this is >0, it will decrease the exponent on the numerator, compressing values closer to zero.

### model.py - probability

To do this, I grab the selected_probability, convert it to log space, then add it to an accumulator. When I return from generate, I return the pair of idx and the accumulated log probability. sample.py then converts it back to normal space using torch.exp and prints it out.

It is important to use log space for these computations because multiplying small numbers makes them really small in a hurry. In floating point math, as the mantissa gets smaller, the standard allows the CPU to become less accurate. Remaining in log space allows sum to be used, keeping the scales similar.

The provided temperature ensures there is only a single token with a non-zero probability. This means the total probability of any string will be 1.

### fixed response

The code encodes forced\_response using the encode method and stores it on device in a tensor. It is then passed to generate. All the normal model code is run. After idx\_next is sampled from from the probabilities, idx\_next is popped off the front of forced\_response\_ids. The rest of the code works unchanged.

If the token in the forced\_response is not in the top-200 tokens, the top\_k will need to be changed. Otherwise the probability will end up as -inf for the logit. This should be 0, and therefore not affecting the total probability - but it seems to take it to zero.

Changing the length of the fixed\_response will lower the probability of the response - 

Prompt: "I live in"
Fixed Response: " a little town called Toronto."
Fixed Response: " a little town called Toronto. It is in Ontario."
Fixed Response: " a little town called Toronto. It is in Ontario. In the country of Canada."
Fixed Response: " a little town called Toronto. It is in Ontario. In the country of Canada. I was born in Manitoba."

### eval.py

* TODO: Refactor the code to have a "eval" function.


The code is a fork of sample.py, adding code to load the json file. Within the for loop, it will take the prompt and the response from the json structure and invok the model with the forced\_response. However, it has the ability to use the prompt without using the response, using the response to set the number of tokens to be fetched.

It reports:
1. the average perplexity of the entire run
2. the percentage of responses with the correct answer
3. the percentage of responses with a calculator tool call "<<...>>"

eval.py takes longer to run than training?!?

### Dataset

Dataset: https://huggingface.co/datasets/openai/gsm8k

I chose the gsm8k dataset. It contains a calculator tool call, and math problems. I pruned the test set to 

The dataset is directly converted to prompt/response pairs using convert.py. It uses Pandas to load the parquet files, extracts the true answer from the answer column and converts the column names. Finally, it outputs a json file with records of the following format:

```
    {
        "prompt":"Some mathematical question?",
        "response":"The generated response\n",
        "expected_value":"64"
    },
```

This allows eval.py to see if it got the correct answer, even if it doesn't format it the same way.

I trimmed the test dataset to 10 rows. The full test dataset was going to take 10 hours for inference on my M5.

### Fine Tuning

-- Run eval before with and without fixed response
-- Run eval after with and without fixed response

What other evaluation methods? I added accuracy and the presence of the tool call.

Other evaluation methods use a judge. The judge is either a human or a LLM. The judge either gives a single score for the response (not very good), or the judge selects between pairs of model responses, selecting the preferred response.

We would generate the evaluation results for the A/B models, and then present them to the judge, asking the judge which model it prefers. 
