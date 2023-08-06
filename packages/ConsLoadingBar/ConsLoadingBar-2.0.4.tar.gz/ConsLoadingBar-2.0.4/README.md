# Progress Indicators for Python

![pypi](https://shields.io/pypi/v/consloadingbar.svg)

## ![demo](./progressbar.gif)

### GitHub Page: [flamechain/ConsLoadingBar](https://github.com/flamechain/ConsLoadingBar)

### Full Docs: [flamechain/ConsLoadingBar/Documentation.md](https://github.com/flamechain/ConsLoadingBar/blob/main/Documentation.md)

Backwards Compatible Since 2.0.0

## Import

Imported simply:

```python
import consloadingbar, time # time import is not required, but will be used for eta calculation later
```

## Built-In Demo

You can use [demo.py](https://github.com/flamechain/ConsLoadingBar/blob/main/demo.py), or call SimulateTasks() to see another bult-in demo class. You can read more about how this class works in the full docs [here](https://github.com/flamechain/ConsLoadingBar/blob/main/Documentation.md).

```python
clb = consloadingbar.SimulateTasks()
```

## ProgressBar()

### Bar() Params for ProgressBar

| Name | Description | Type | Default |
|-|-|:-:|-|
| barLength | Length of bar in characters | int | 20 |
| useETACalculation | Stall bar depending on current eta | boolean | False |
| taskCount | Total amount of tasks displayed | int | None |
| mainBarChar | Character of the filled-in bar | string | '█' |
| progressPointBarChar | Last character of the filled-in bar | string | None |
| endPointChars | Suffix and prefix of the bar | list | ['&#124;', '&#124;'] |
| title | Title to show when the bar is running | string | 'Running...' |
| emptyBarChar | Character for the non-filled-in bar | string | ' ' |

### Params

| Name | Description | Type | Default |
|-|-|:-:|-|
| current | Current percentage complete | int | |
| time_ | Current time passed since start, used for eta calculations | float | None |
| tasksDone | How many tasks done to display | int | 0 |
| lazyLoad | If used, only updates when needed, no tasks or eta displayed | int-bool | None |
| returnString | Return a string value of the bar instead of printing to the console | boolean | False |

You can use the params from Bar() to customize the look of the bar (see demo) and the params from the method for iter-specific things like current percentage.

```python
clb = consloadingbar.Bar(useColor=True, taskCount=10)

start = time.time()

for i in range(101):
    currentTime = time.time() - start
    # Do something. For demo purposes you can sleep the program for about 0.01 seconds.
    clb.progressBar(i, time_=currentTime, tasksDone=i//10)
```

This will display tasks and eta. You can also call the start() method for multiline titles:

```python
clb.start()
```

```txt
Running...
        |                    |   0%  [tasks=0/10]
```

Or you can use the end() method to show a full bar. This example has useColor enabled.

```python
clb.end()
```

<pre>
<span style="color:green">Finished</span>
        |████████████████████| <span style="color:green">100%  [tasks=10/10]</span>
</pre>

## ProgressCircle()

### Bar() Params for ProgressCircle()

| Name | Description | Type | Default |
|-|-|:-:|-|
| phases | The phases for the spinner | list | ['&#124;', '/', '-', '\\'] |

### Params

| Name | Description | Type | Default |
|-|-|:-:|-|
| stop() | Call on main thread to end method | func-bool | False |
| time_ | Call instead to make it stop itself after given seconds | float | None |
| title | Title to show while running | string | 'Loading'
| status | Call instead to print once showing the phases index of status | int | None |
| char | Call instead to print a custom char not in phases | string | None |
| returnString | Return a string value of the bar instead of printing to the console | boolean | False |

This is used to show a spinner go round in a circle pattern. See demo above. To call just tell it when to stop using time, or stop() param.

```python
clb.progressCircle(time_=2) # Will run for 2 seconds
```

You can also use phases to change what to show each iteration. See Demo also.

```python
clb = consloadingbar.Bar(phases=['|', '-'])

clb.progressCircle(time_=2)
```

This now only has 2 phases, '|' and '-'.

You can also use the char param to manually put in what to display.

```python
clb = consloadingbar.Bar()

for i in range(101):
    # Do something. For demo purposes you can sleep the program for about 0.01 seconds.
    clb.progressCircle(char=i)
```

This will count up to 100.

___

## Installation

Install via pip using `pip install ConsLoadingBar`.

```bash
pip install ConsLoadingBar
```

To make sure you have the current version you can use this command instead:

```bash
pip install --upgrade ConsLoadingBar
```

You can also directly call the module from python:

```bash
python3 -m pip install ConsLoadingBar
```

___

## License

ConsLoadingBar is licensed under the MIT License
