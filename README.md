# Promptly

[![Build Status](https://travis-ci.org/aventurella/promptly.png?branch=master)](https://travis-ci.org/aventurella/promptly)

A little python utility to help you build command line prompts that can
be styled using CSS.

## Lets Make a Promptly Form

```python
    from promptly import Form
    from promptly import StringInput
    from promptly import IntegerInput
    from promptly import ChoiceInput
    from promptly import BooleanInput

    form = Form()

    # add questions in the sequence you would like them to appear

    form.add('name',
        StringInput('What is your name?',
        default='Aubrey'))

    form.add('age',
        IntegerInput('What is your age?',
        default=1))

    form.add('color',
        ChoiceInput('What is your favorite color',
            zip(range(1,4), ('red', 'green', 'blue')),
        default=1))

    form.add('yaks', BooleanInput('Do you like yaks?', default=True))

    # Our form is created, lets prompt the user for the answers:

    # promptly comes with a default set of styles or you can
    # provide your own.

    with open('/path/to/my/styles.css') as css:
        form.run(prefix='[promptly] ', stylesheet=css.read())

    # control has returned back to our script, lets see what the user said:

    print(form.name.value)
    print(form.age.value)
    print(form.color.value)  # this will be a (key, value) tuple
    print(form.yaks.value)

    # Or we can just convert the whole form into a dictionary:
    d = dict(form)
    print(d)

```

## CSS Styling
Promptly prompts are styles with a very limited subset of CSS.
Only the following properties apply:

- color
- background-color
- font-weight

The avialable colors are limited to the color names provided by colorama:

```
    Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
    Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
    Style: DIM, NORMAL, BRIGHT, RESET_ALL
```

In other words:
```css
    .prefix {
        color: white;
        background-color: blue;
    }
```

The font-weight property maps to colorama Style values in the following way:

```
    font-weight: normal;   -> Style.NORMAL
    font-weight: bold;     -> Style.BRIGHT
    font-weight: lighter;  -> Style.DIM
```

### Heads Up

The CSS parser in promptly is **VERY VERY** primitive. It's just enough to parse
what is below and that's all. It is by no means a full implementation of the
CSS spec.


## Default Prompty Stylesheet

Below is the default stylesheet included with promptly. This stylesheet
presents the exhaustive set of selectors that can be used to style
your prompts. If it's not below, promptly doesn't support it.

Remember each selector can support:

```css
    color: <value>
    background-color: <value>
    font-weight: </value>
```

The default stylesheet below does not use every available option
for obvious reasons. But you should feel free too if you so desire.

```body``` will set the default color and font-weight and background color.
The additional styles effectively cascade on top of body.


```css
    body{
        color:white;
        font-weight:normal;
    }

    .prefix{
        color:blue;
        font-weight:lighter;
    }

    .string .label{
        color:magenta;
    }

    .string .default-wrapper{
        color:white;
    }

    .string .default-value{
        color:yellow;
    }

    .integer .label{
        color:magenta;
    }

    .integer .default-wrapper{
        color:white;
    }

    .integer .default-value{
        color:yellow;
    }

    .boolean .label{
        color:magenta;
    }

    .boolean .default-wrapper{
        color:white;
    }

    .boolean .default-value{
        color:yellow;
    }

    .boolean .other-value{
        color:yellow;
    }

    .boolean .seperator{
        color:white;
    }

    .choices .label{
        color:magenta;
    }

    .choices .default-wrapper{
        color:white;
    }

    .choices .default-value{
        color:yellow;
    }

    .choices .option-key{
        color:yellow;
    }

    .choices .seperator{
        color:yellow;
        font-weight:lighter;
    }

    .choices .option-value{
        color:white;
    }

    .choices .action{
        color:magenta;

    }
```
