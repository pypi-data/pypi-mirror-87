# MkDocs Boring Theme

This is the MkDocs Boring Theme.
It is based on the CSS framework [Min](http://mincss.com) which claims to be one of the slimmest but also one of the most compatible CSS frameworks.

Check out the demo page to get a feeling of this theme.


## Goal

The goal is to provide a lightweight theme which still does not look too awkward.
*Min* promotes itself as being only 995 bytes, which is hard to challenge.

It's ultimately small size requires a few overwriting features which can be found in `css/boring.css`.

## Install & Usage

The boring theme is packaged and available on PyPI:

```
pip install mkdocs-boring-theme
```

If you want to use the theme in your MkDocs project simply include it in the `mkdocs.yml`:

```
theme:
  name: boring

```

## Configuration

The theme allows the usage of two new configuration parameters:

```
provider_name: Example
provider_url: https://example.com
```

The provider will be shown in the top-left corner which can link to the providers home page.



## Todo List

This theme is a work in progress. It lacks a few features, which I try to list here

* Nested menus with dropdown effects
* Minimizing `css/boring.css`



# License


MIT License

Copyright 2020 Max Resing

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
