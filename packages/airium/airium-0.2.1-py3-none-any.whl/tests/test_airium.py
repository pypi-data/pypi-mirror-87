import pytest

from airium import Airium, Tag


def test_empty_doc():
    a = Airium()
    assert str(a) == ''
    assert repr(a) == "Airium(base_indent='  ', current_level=0)"


def test_text_only_doc():
    a = Airium()
    a("this is my text")
    assert str(a) == 'this is my text'


def test_single_img():
    a = Airium()
    a.img(src='some.png', alt='that alt')
    assert str(a) == '<img src="some.png" alt="that alt" />'


def test_attribute_values_substitution():
    a = Airium()
    a.img(src='some.png', alt='that "alternative text"')
    assert str(a) == '<img src="some.png" alt="that &quot;alternative text&quot;" />'


def test_call_with_text():
    a = Airium()
    a.div(_t='the div content')
    a.br()

    assert str(a) == '''\
<div>the div content</div>
<br />'''


def test_link():
    a = Airium()
    with a.a(href='https://10.23.1.3:5043'):
        a('nice link')
    a.br()

    assert str(a) == '''\
<a href="https://10.23.1.3:5043">
  nice link
</a>
<br />'''


def test_link_inline():
    a = Airium()
    a.a(href='https://10.23.1.3:5043', _t='nice link')
    a.br()

    assert str(a) == '''\
<a href="https://10.23.1.3:5043">nice link</a>
<br />'''


def test_multiple_context_with_text():
    a = Airium()
    with a.div(_t='the div content'), a.p(_t='inline text for p'), a.span():
        a('text')
        a('egg')

    a.br()
    assert str(a) == '''\
<div>the div content
  <p>inline text for p
    <span>
      text
      egg
    </span>
  </p>
</div>
<br />'''


def test_multiple_context_with_text_2():
    a = Airium()
    with a.div(_t='the div content'), a.p(_t='inline text for p'):
        a.span(_t='text')
        a('egg')
    a.br()
    assert str(a) == '''\
<div>the div content
  <p>inline text for p
    <span>text</span>
    egg
  </p>
</div>
<br />'''


def test_context_with_text():
    a = Airium()
    with a.div(_t='the div content'):
        pass

    a.br()
    assert str(a) == '''\
<div>the div content
</div>
<br />'''


def test_tag_repr():
    t = Tag('tag_name', Airium())
    assert repr(t) == "Tag('tag_name')"


def test_context_single_tag_forgiven():
    a = Airium()
    with pytest.raises(AttributeError, match="The tag: 'img' is a single tag, cannot be used with contexts."):
        with a.img():
            pass


def test_context_single_tag_missing_braces():
    a = Airium()
    with pytest.raises(AttributeError, match="__enter__"):
        with a.img:
            pass


def test_context_paired_tag_missing_braces():
    a = Airium()
    with pytest.raises(AttributeError, match="__enter__"):
        with a.div:
            pass


def test_single_div():
    a = Airium()
    a.div(klass='some')
    a.div(klass='other')

    assert str(a) == '''\
<div class="some"></div>
<div class="other"></div>'''


def test_one_level():
    a = Airium(base_indent='    ')
    with a.div():
        a.img(src='source.png', alt='alt text')
        a('the text')

    expected_result = '''\
<div>
    <img src="source.png" alt="alt text" />
    the text
</div>'''
    assert str(a) == expected_result


def test_table():
    a = Airium()

    with a.table(id='table_372'):
        with a.tr(klass='header_row'):
            a.th(_t='no.')
            a.th(_t='Firstname')
            a.th(_t='Lastname')

        with a.tr():
            a.td(_t='1.')
            a.td(id='jbl', _t='Jill')
            a.td(_t='Smith')  # can use _t or text

        with a.tr():
            a.td(_t='2.')
            a.td(_t='Roland', id='rmd')
            a.td(_t='Mendel')

    expected_result = '''\
<table id="table_372">
  <tr class="header_row">
    <th>no.</th>
    <th>Firstname</th>
    <th>Lastname</th>
  </tr>
  <tr>
    <td>1.</td>
    <td id="jbl">Jill</td>
    <td>Smith</td>
  </tr>
  <tr>
    <td>2.</td>
    <td id="rmd">Roland</td>
    <td>Mendel</td>
  </tr>
</table>'''
    assert str(a) == expected_result


def test_nested():
    a = Airium(base_indent='    ')
    a('zero')
    with a.div():
        a('one')
        a.div(this='is_extra')
        with a.p(id='main_p'), a.span(style='font-size: 12px;', _t='inline text for span'):
            pass

        a.div(this='as well')
        a.br()
        with a.div(style='some: on;'):
            a.div(this='is nested')
            a('Hi there')
    expected_result = '''\
zero
<div>
    one
    <div this="is_extra"></div>
    <p id="main_p">
        <span style="font-size: 12px;">inline text for span
        </span>
    </p>
    <div this="as well"></div>
    <br />
    <div style="some: on;">
        <div this="is nested"></div>
        Hi there
    </div>
</div>'''

    assert str(a) == expected_result


def test_chaining():
    a = Airium()
    a.html().body().p(_t="Hi there")
    expected_result = '''\
<html>
  <body>
    <p>Hi there</p>
  </body>
</html>'''

    assert str(a) == expected_result


def test_incorrect_chaining():
    a = Airium()
    with pytest.raises(AttributeError, match="'br' is a single tag, creating its children is forbidden."):
        a.br().p(_t="Hi there")


def test_incorrect_chaining_nested():
    a = Airium()
    with pytest.raises(AttributeError, match="'img' is a single tag, creating its children is forbidden."):
        a.html().body().img(href='').p(_t="Hi there")


def test_pre_at_root_level():
    """from: https://gitlab.com/kamichal/airium/-/issues/2 """
    doc = Airium()
    with doc.pre():
        doc("I don't want extra spaces or new lines :(")
        doc("extra text")

    assert str(doc) == """<pre>I don't want extra spaces or new lines :(extra text</pre>"""


def test_pre_at_root_level_2():
    """from: https://gitlab.com/kamichal/airium/-/issues/2 """
    doc = Airium()
    with doc.pre(_t="I don't want extra spaces or new lines :("):
        doc("extra text")

    assert str(doc) == """<pre>I don't want extra spaces or new lines :(extra text</pre>"""


def test_pre_newlines_handling():
    """from: https://gitlab.com/kamichal/airium/-/issues/2 """

    doc = Airium()
    with doc.div().div().div():
        with doc.div():
            with doc.pre():
                doc("I don't want extra spaces or new lines :(")

    assert str(doc) == """<div>
  <div>
    <div>
      <div>
        <pre>I don't want extra spaces or new lines :(</pre>
      </div>
    </div>
  </div>
</div>"""


def test_pre_newlines_handling_on_multilline():
    """from: https://gitlab.com/kamichal/airium/-/issues/2 """

    doc = Airium()
    with doc.div().div().div():
        with doc.div():
            with doc.pre():
                doc("I don't want\nextra\nspaces\nor\nnew lines :(")

    assert str(doc) == """<div>
  <div>
    <div>
      <div>
        <pre>I don't want
extra
spaces
or
new lines :(</pre>
      </div>
    </div>
  </div>
</div>"""


def test_pre_newlines_handling_on_long_text():
    """from: https://gitlab.com/kamichal/airium/-/issues/2 """

    doc = Airium()
    with doc.div().div().div():
        with doc.div():
            with doc.pre():
                doc("""Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
    eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad
    minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip
    ex ea commodo consequat.""")
        doc.br()

    assert str(doc) == """<div>
  <div>
    <div>
      <div>
        <pre>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
    eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad
    minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip
    ex ea commodo consequat.</pre>
      </div>
      <br />
    </div>
  </div>
</div>"""


def test_chaining_context():
    a = Airium()
    with a.html().body().table():
        with a.tr():
            a.td().strong(_t="Hi there")
            with a.td():
                a("Hi there too")
        with a.tr():
            with a.td():
                a("And here")
            a.td().strong(_t="And here too")
    expected_result = '''\
<html>
  <body>
    <table>
      <tr>
        <td>
          <strong>Hi there</strong>
        </td>
        <td>
          Hi there too
        </td>
      </tr>
      <tr>
        <td>
          And here
        </td>
        <td>
          <strong>And here too</strong>
        </td>
      </tr>
    </table>
  </body>
</html>'''

    assert str(a) == expected_result
