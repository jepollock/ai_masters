# AIML420 Assignment 3

* author: Jason Pollock
* email: jason@pollock.ca
* email: pollocjaso@myvuw.ac.nz

## How to run

### Part 1

```
make part1
..or..
make all
```

Sample output:

```
jupyter nbconvert report.ipynb \
	--TagRemovePreprocessor.remove_cell_tags='{"remove_cell"}' \
	--TagRemovePreprocessor.remove_all_outputs_tags='{"remove_output"}' \
	--TagRemovePreprocessor.remove_input_tags='{"remove_input"}' \
	--ExecutePreprocessor.kernel_name=python3 \
	--Exporter.preprocessors='["nbconvert.preprocessors.TagRemovePreprocessor"]' \
	--to pdf
[NbConvertApp] Converting notebook report.ipynb to pdf
[NbConvertApp] ERROR | Notebook JSON is invalid: Additional properties are not allowed ('jetTransient' was unexpected)

Failed validating 'additionalProperties' in display_data:

On instance['cells'][4]['outputs'][0]:
{'data': {'text/markdown': 'Operation Start Times:',
          'text/plain': '<IPython.core.display.Markdown object>'},
 'jetTransient': {'display_id': None},
 'metadata': {},
 'output_type': 'display_data'}
[NbConvertApp] Writing 47713 bytes to notebook.tex
[NbConvertApp] Building PDF
[NbConvertApp] Running xelatex 3 times: ['xelatex', 'notebook.tex', '-quiet']
[NbConvertApp] Running bibtex 1 time: ['bibtex', 'notebook']
[NbConvertApp] WARNING | bibtex had problems, most likely because there were no citations
[NbConvertApp] PDF successfully created
[NbConvertApp] Writing 60970 bytes to report.pdf
```

See report.pdf for the generated report.


### Part 2

#### Task A

```
make part2_taska
...or...
./perceptron
```

Sample Output:

```
./perceptron
Loading datasets...
Perceptron, Linearly Separable
| Model | Epoch | Accuracy |
| --- | --- | --- |
| Separable | 1 | 0.525 |
| Separable | 5 | 0.625 |
| Separable | 10 | 0.8 |
| Separable | 15 | 0.825 |
| Separable | 20 | 0.75 |
| Separable | 50 | 0.8 |
| Separable | 60 | 0.65 |
| Separable | 80 | 0.675 |
| Separable | 100 | 0.75 |
| Separable | 120 | 0.775 |
| Separable | 150 | 0.575 |
| Separable | 200 | 0.625 |
```



#### Task B

```
make part2_taskb
...or...
./perceptron_b.py
```

Sample Output:

```
./perceptron_b.py
Loading datasets...
Perceptron, Non-Linearly Separable
| Model | Epoch | Accuracy |
| --- | --- | --- |
| Non-Separable | 1 | 0.4633333333333333 |
| Non-Separable | 5 | 0.5233333333333333 |
| Non-Separable | 10 | 0.6566666666666666 |
| Non-Separable | 15 | 0.7766666666666666 |
| Non-Separable | 20 | 0.7366666666666667 |
| Non-Separable | 50 | 0.6566666666666666 |
| Non-Separable | 60 | 0.6566666666666666 |
| Non-Separable | 80 | 0.6566666666666666 |
| Non-Separable | 100 | 0.6933333333333334 |
| Non-Separable | 120 | 0.6566666666666666 |
| Non-Separable | 150 | 0.6566666666666666 |
| Non-Separable | 200 | 0.6566666666666666 |
```

#### Task C

```
make part2_taskc
...or...
./multi_layer_perceptron.py --max_epoch=300
```

Sample Output:

```
./multi_layer_perceptron.py --max_epoch=300
Loading datasets...
/opt/anaconda3/lib/python3.13/site-packages/sklearn/neural_network/_multilayer_perceptron.py:781: ConvergenceWarning: Stochastic Optimizer: Maximum iterations (300) reached and the optimization hasn't converged yet.

[....]

 warnings.warn(
/opt/anaconda3/lib/python3.13/site-packages/sklearn/neural_network/_multilayer_perceptron.py:781: ConvergenceWarning: Stochastic Optimizer: Maximum iterations (300) reached and the optimization hasn't converged yet.
  warnings.warn(
| Activation Function | Epoch | Sizes | Accuracy |
| --- | --- | --- | --- |
| identity | 300 | (100,) | 0.763 |
| logistic | 300 | (100,) | 0.757 |
| tanh | 300 | (100,) | 0.950 |
| relu | 300 | (100,) | 0.950 |

[....]

```

#### Task D

```
make part2_taskd
...or...
./multi_layer_perceptron.py
```

Sample Output:

```
./multi_layer_perceptron.py
Loading datasets...
| Activation Function | Epoch | Sizes | Accuracy |
| --- | --- | --- | --- |
| identity | 800 | (100,) | 0.763 |
| logistic | 800 | (100,) | 0.757 |
| tanh | 800 | (100,) | 0.940 |
| relu | 800 | (100,) | 0.950 |
| identity | 800 | (5, 2) | 0.757 |
| logistic | 800 | (5, 2) | 0.750 |
| tanh | 800 | (5, 2) | 0.940 |
| relu | 800 | (5, 2) | 0.943 |
| identity | 800 | (10, 5) | 0.760 |
| logistic | 800 | (10, 5) | 0.937 |
| tanh | 800 | (10, 5) | 0.930 |
| relu | 800 | (10, 5) | 0.947 |
| identity | 800 | (16, 8) | 0.763 |
| logistic | 800 | (16, 8) | 0.923 |
| tanh | 800 | (16, 8) | 0.937 |
| relu | 800 | (16, 8) | 0.957 |
| identity | 800 | (20, 10) | 0.783 |
| logistic | 800 | (20, 10) | 0.933 |
| tanh | 800 | (20, 10) | 0.930 |
| relu | 800 | (20, 10) | 0.953 |
| identity | 800 | (20, 10, 5) | 0.767 |
| logistic | 800 | (20, 10, 5) | 0.937 |
| tanh | 800 | (20, 10, 5) | 0.957 |
| relu | 800 | (20, 10, 5) | 0.960 |
| identity | 800 | (5, 10) | 0.763 |
| logistic | 800 | (5, 10) | 0.760 |
| tanh | 800 | (5, 10) | 0.940 |
| relu | 800 | (5, 10) | 0.940 |
```

