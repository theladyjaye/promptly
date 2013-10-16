# Promptly

[![Build Status](https://travis-ci.org/aventurella/promptly.png?branch=master)](https://travis-ci.org/aventurella/promptly)

A little python utility to help you build command line prompts that can
be styled using CSS.

## WARNING 0.4 is backwards incompatible

**Migration Guide**
-   `my_form.add.choice` should be become `my_form.add.select`
-   `ChoiceInput` should become `SelectInput`
-   SelectInput (formerly ChoiceInput) and MultiSelectInput now take
    an option_format callable. By default this callable is
    `promptly.utils.numeric_options`. This will take a list ['foo', 'bar']
    and return a list: [(1, 'foo'), (2, 'bar')]. So if you only need
    numbers for your choices or multi-select input's you don't
    need to worry about, you get them for free. If you were passing
    your own in something like: `zip(range(1,3), ['foo', 'bar'])` you
    no longer need to do that. In fact that will break things for you
    so you should replace it with just your list of choices



### New Features

#### Branches
Forms can now branch. The branch input item takes a callable that will
be executed and is expected to return another `Form` object. This `Form`
object will be merged into the currently running form at the location
where the branch was added. The callable signature is as follows:

`my_branch_building_action(form, *args, **kwargs):`

Example branch usage:

```python

def handler(form, name):
    branch = Form()

    if form.age.value < 30:
        branch.add.string('name', 'What is your name?')
    else:
        branch.add.string('name', 'What is your pet's name?', default=name)

    return branch


form = Form()
form.add.int('age', 'What is your age?', default=age)
form.add.branch(handler, name='Lucy')

# The branch fields will be added here in terms of
# position in the form once the user reaches the branch

form.add.int('number', 'What is your favorite number?')
form.run()
```

#### MultiSelectInput
A new input type has been added, `MultiSelectInput`, a shortcut for creating
one is also available in the form of:
`my_form.add.multiselect(key, label, choices, done_label='Done')`

Note that done_label is optional.

MultiSelectInput lets the user choose multiple options from a SelectInput
style display. It marks the currently selected items. If the user chooses the
same option that has already been selected it will be deselected.

A final option is added to the list of choices provided to represent
the sentinel choice. The `done_label` kwarg sets the value used here
By default it is set to *Done*. The user must select the sentinel choice
in order to continue on in the form.





## Lets Make a Promptly Form

```python
    from promptly import Form
    from promptly import StringInput
    from promptly import IntegerInput
    from promptly import SelectInput
    from promptly import BooleanInput
    from promptly import Branch


    # Build our form
    form = Form()

    # add questions in the sequence you would like them to appear

    form.add('name',
        StringInput('What is your name?',
        default='Aubrey'))

    form.add('age',
        IntegerInput('What is your age?',
        default=1))

    # no options_format kwarg is provided for ChoiceInput
    # so it will use the default numeric_options
    form.add('color',
        SelectInput('What is your favorite color',
            ('red', 'green', 'blue'),
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

    if form.age.value < 12:
        print(form.food.value)

    # Or we can just convert the whole form into a dictionary:
    d = dict(form)
    print(d)

```

## Making the same form as above, using sortcuts

```python
    from promptly import Form


    # Build our form
    form = Form()

    # add questions in the sequence you would like them to appear

    form.add.string('name',
        'What is your name?',
        default='Aubrey')

    form.add.int('age',
        'What is your age?',
        default=1)

    # no options_format kwarg is provided for ChoiceInput
    # so it will use the default numeric_options
    form.add.select('color',
        'What is your favorite color',
        ('red', 'green', 'blue'),
        default=1)

    form.add.bool('yaks', 'Do you like yaks?', default=True)

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

    if form.age.value < 12:
        print(form.food.value)

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
