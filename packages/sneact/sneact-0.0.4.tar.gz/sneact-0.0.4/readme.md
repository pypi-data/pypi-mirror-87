# Sneact

Sneact is a python library for building user interfaces.

__That's so draft.__

## Example 1

### Python code

```python
from sneact import Sneact, s, _
from sneact.html import div, p, img

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
