project = 'viewdom'
html_title = 'viewdom'
copyright = '2020, Paul Everitt <pauleveritt@me.com>'
release = '0.4.1'
extensions = [
    'sphinx.ext.autodoc',
    'myst_parser',
]
templates_path = ['_templates']
html_theme = 'sphinx_book_theme'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
html_static_path = ['_static']
html_theme_options = dict(
    extra_footer='Theme by the <a href="https://ebp.jupyterbook.org">'
    + 'Executable Book Project</a>.',
    repository_url='https://github.com/pauleveritt/viewdom',
    use_repository_button=True,
)
html_css_files = [
    'custom.css',
]
html_sidebars = {
    "**": [
        'subtitle.html',
        'sidebar-search-bs.html',
        'sbt-sidebar-nav.html',
    ]
}
