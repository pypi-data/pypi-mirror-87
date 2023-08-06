# CHANGELOG.md

## 0.2.1 (2020-12-07)

#### Issues:

- Issue [#2](https://gitlab.com/kamichal/airium/-/issues/2)

  Extra spaces generated when closing `<pre>` elements
    - Reported by: **Pavol Federl** [@federl](https://gitlab.com/federl)

#### Fix:

- Resolving issue #2
- Fix reverse translation for `<pre>` elements

#### Housekeeping:

- Add `pyproject.toml` configuration file for `poetry`
- Add CI pipeline for poetry environment test

## 0.2.0 (2020-10-29)

#### Contributions:

- **Antti Kaihola** [@akaihola](https://gitlab.com/akaihola)
    - [Tag chaining feature](https://gitlab.com/kamichal/airium/-/merge_requests/4)
    - [Supplement type annotations](https://gitlab.com/kamichal/airium/-/merge_requests/2)
    - [`ClassVar` fix](https://gitlab.com/kamichal/airium/-/merge_requests/1)

#### Features:

- Allow chaining of tags when they have only one child.
- Add enough typing hints so Mypy is happy with the code base.

#### Fix:

- Fix incorrect use of `ClassVar` in `forward.py`

## 0.1.6 (2020-09-20)

#### Features:

- add info for missing dependencies for translation

## before

> git is supposed to know what was released before the CHANGELOG.md is started
