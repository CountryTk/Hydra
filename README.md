# PyPad
A simple cross-platform python editing notepad written in python.

This editor is fully customizable, just edit the config.yaml file. All color codes  **MUST** be hex color codes!

Required modules: PyQt5

Full Credit for this idea goes to [Fuchsiaff](https://github.com/Fuchsiaff)

Basic config.yaml:

```yaml
colorscheme:
  search_dir: "./colorschemes"
  active_scheme: "basic"

```

# Colorscheme Customization

Font options are "bold", "italic" and "underline". Each "block" must consist of a font key, a css_class key, a color key (as well as an optional background key).

Example: (background only applies to editor background in general, not individual elements)

```yaml
Keyword.Constant:
  color: "#F5C747"
  font:
    - bold

  css_class: pre .kc
```

Full token reference for color customizing is below.

| Token Type                    | CSS/YAML Class |
| ----------------------------- | -------------- |
| `Text.Whitespace`             | w              |
| `Escape`                      | esc            |
| `Error`                       | err            |
| `Other`                       | x              |
| `Keyword`                     | k              |
| `Keyword.Constant`            | kc             |
| `Keyword.Declaration`         | kd             |
| `Keyword.Namespace`           | kn             |
| `Keyword.Pseudo`              | kp             |
| `Keyword.Reserved`            | kr             |
| `Keyword.Type`                | kt             |
| `Name`                        | n              |
| `Name.Attribute`              | na             |
| `Name.Builtin`                | nb             |
| `Name.Builtin.Pseudo`         | bp             |
| `Name.Class`                  | nc             |
| `Name.Constant`               | no             |
| `Name.Decorator`              | nd             |
| `Name.Entity`                 | ni             |
| `Name.Exception`              | ne             |
| `Name.Function`               | nf             |
| `Name.Function.Magic`         | fm             |
| `Name.Property`               | py             |
| `Name.Label`                  | nl             |
| `Name.Namespace`              | nn             |
| `Name.Other`                  | nx             |
| `Name.Tag`                    | nt             |
| `Name.Variable`               | nv             |
| `Name.Variable.Class`         | vc             |
| `Name.Variable.Global`        | vg             |
| `Name.Variable.Instance`      | vi             |
| `Name.Variable.Magic`         | vm             |
| `Literal`                     | l              |
| `Literal.Date`                | ld             |
| `Literal.String`              | s              |
| `Literal.String.Affix`        | sa             |
| `Literal.String.Backtick`     | sb             |
| `Literal.String.Char`         | sc             |
| `Literal.String.Delimiter`    | dl             |
| `Literal.String.Doc`          | sd             |
| `Literal.String.Double`       | s2             |
| `Literal.String.Escape`       | se             |
| `Literal.String.Heredoc`      | sh             |
| `Literal.String.Interpol`     | si             |
| `Literal.String.Other`        | sx             |
| `Literal.String.Regex`        | sr             |
| `Literal.String.Single`       | s1             |
| `Literal.String.Symbol`       | ss             |
| `Literal.Number`              | m              |
| `Literal.Number.Bin`          | mb             |
| `Literal.Number.Float`        | mf             |
| `Literal.Number.Hex`          | mh             |
| `Literal.Number.Integer`      | mi             |
| `Literal.Number.Integer.Long` | il             |
| `Literal.Number.Oct`          | mo             |
| `Operator`                    | o              |
| `Operator.Word`               | ow             |
| `Punctuation`                 | p              |
| `Comment`                     | c              |
| `Comment.Hashbang`            | ch             |
| `Comment.Multiline`           | cm             |
| `Comment.Preproc`             | cp             |
| `Comment.PreprocFile`         | cpf            |
| `Comment.Single`              | c1             |
| `Comment.Special`             | cs             |
| `Generic`                     |  g             |
| `Generic.Deleted`             | gd             |
| `Generic.Emph`                | ge             |
| `Generic.Error`               | gr             |
| `Generic.Heading`             | gh             |
| `Generic.Inserted`            | gi             |
| `Generic.Output`              | go             |
| `Generic.Prompt`              | gp             |
| `Generic.Strong`              | gs             |
| `Generic.Subheading`          | gu             |
| `Generic.Traceback`           | gt             |
 ------------------------------- ----------------
