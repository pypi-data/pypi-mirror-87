from markupsafe import Markup

from viewdom.h import Context, use_context, html, render  # noqa


def functional_component(children, header="Functional components!"):
    message = use_context("message")  # noqa

    return html(
        """
        <h2>{header}</h2>
        <span>{message}</span>
        {children}
    """
    )


def test_single_renderer():
    vdom = html('<div id="d1">div1</div>')
    assert ['div1'] == vdom.children


def test_double_renderer():
    vdom = html('<div id="d1">div1</div><div id="d2">div2</div>')
    assert ['div1'] == vdom[0].children
    assert ['div2'] == vdom[1].children


def test_render_context():
    def App():
        message = use_context("message")  # noqa
        return html("<div>{message}<//><{functional_component}/>")

    vdom = html(
        """
  <{Context} message='c1'>
    <{App} />
  <//>
"""
    )
    result = render(vdom)
    expected = '<div>c1</div><h2>Functional components!</h2><span>c1</span>'
    assert expected == result


def test_render_escaped_value():
    body = '<span>Escape</span>'  # noqa
    vdom = html('<div>{body}</div>')
    result = render(vdom)
    expected = '<div>&lt;span&gt;Escape&lt;/span&gt;</div>'
    assert expected == result


def test_render_safe_value():
    body = Markup('<span>Escape</span>')  # noqa
    vdom = html('<div>{body}</div>')
    result = render(vdom)
    expected = '<div><span>Escape</span></div>'
    assert expected == result


def test_void():
    """Convert <img></img> to <img/>

    See this for discussion of non-void elements which can't be
    self-closed:
    https://stackoverflow.com/questions/31627593/html-validator-self-closing-syntax-and-non-void-errors
    """

    non_void = '<img></img>'
    vdom = html(non_void)
    result = render(vdom)
    assert '<img/>' == result


def test_non_void():
    """Don't convert <i class="icon"></i> to <i class="icon"/>

    See this for discussion of non-void elements which can't be
    self-closed:
    https://stackoverflow.com/questions/31627593/html-validator-self-closing-syntax-and-non-void-errors
    """

    non_void = '<i class="icon"></i>'
    vdom = html(non_void)
    result = render(vdom)
    assert non_void == result
