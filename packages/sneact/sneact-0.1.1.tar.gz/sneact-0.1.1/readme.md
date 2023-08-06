# Sneact

Sneact is a python library for building user interfaces.

__That's so draft.__


## Hot new features!

### Conditions!

```python
from sneact import Sneact, s, _
from sneact.cond import when, when_not, then
from sneact.html import div, p

scope = {
    "ok_text": "Hello!",
    "not_text": "Hello not!",
    "show_text": True
}
page = (+Sneact(scope)
    <<div>>_
        @when(s.show_text, +then
            <<p>> s.ok_text <<-p>>_
        )
        @when_not(s.show_text, +then
            <<p>> s.not_text <<-p>>_
        )
    <<-div>>_
)
```

##### Result:

```html
<div>
<p>Hello!</p>
</div>
```

### Loops!

```python
from sneact import Sneact, s, _
from sneact.html import div, img
from sneact.loop import for_each, do, item

scope = {
    "images": ["cat.png", "dog.png", "frog.png"]
}
page = (+Sneact(scope)
    <<div>>_
        @for_each(s.images, +do
            <<img(src=item)>>_
        )
    <<-div>>_
)
```

##### Result:

```html
<div>
<img src=cat.png>
<img src=dog.png>
<img src=frog.png>
</div>
```

## Example 1

### Python code

```python
from sneact import Sneact, s, _
from sneact.html import div, p, img

scope = {
    "title": "Tiger",
    "subtitle": "About tigers",
    "image": '"tiger.png"',
}
home_page = (+Sneact(scope)
    <<div>>_
        <<p>> s.title <<-p>>_
        <<p>> s.subtitle <<-p>>_
        <<div>>_
            <<p>> s.text <<-p>>_
            <<img(src=s.image)>>_
        <<-div>>_
    <<-div>>_
)
scope["text"] = "Hello tigers. We love Tigers."
result = home_page.as_html()
```

### Resulting html

```html
<div>
<p>Tiger</p>
<p>About tigers</p>
<div>
<p>Hello tigers. We love Tigers.</p>
<img src="tiger.png">
</div>
</div>
```

[Pytest code link](https://github.com/machineandme/sneact/blob/df9c3c47a6da3d219724240ca298d2240274ac0c/tests/test_sneact.py#L11)

## Example 2


### Python code

```python
from sneact import Sneact, s, _
from sneact.html import p, h1, header, footer

scope = {}
page = (+Sneact(scope)
    <<header>>_
    	**s.header
    <<-header>>_
    <<p>> "Lorem you know" <<-p>>_
    <<footer>>_
    	**s.footer
    <<-footer>>_
)
scope["header"] = (+Sneact(scope)
    <<h1>> "Page" <<-h1>>_
)
scope["footer"] = (+Sneact(scope)
    <<p>> "Copyright Kiselev Nikolay 2020" <<-p>>_
)
result = page.as_html()
```

### Resulting html

```html
<header>
<h1>Page</h1>
</header>
<p>Lorem you know</p>
<footer>
<p>Copyright Kiselev Nikolay 2020</p>
</footer>
```

[Pytest code link](https://github.com/machineandme/sneact/blob/df9c3c47a6da3d219724240ca298d2240274ac0c/tests/test_sneact.py#L49)
