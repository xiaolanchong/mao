Generate the static radical table from the repository root:

```sh
python3 -m pip install -r scripts/key_list/requirements.txt
python3 scripts/key_list/create_key_list_html.py
```

The defaults resolve relative to the script, so it also works from another
directory. The generated page is `site/key_list.html`; edit `template.html`
for layout changes and `src/key_list.yaml` for content, then regenerate.
No JavaScript or webpack build is required for this page.

Use `--input`, `--output`, and `--template` to override paths. Relative links
in the template and generated images assume the output is in `site/`.
