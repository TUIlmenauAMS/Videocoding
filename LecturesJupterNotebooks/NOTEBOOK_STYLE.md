# Notebook Style

The lecture notebooks are read in Colab, on GitHub, in JupyterLab and in VS Code. Plain Markdown looks right in all of them, follows light and dark mode, and is easy to edit in Colab. These conventions keep all lectures consistent.

## Title cell

The first cell of every lecture:

```markdown
<a target="_blank" href="https://colab.research.google.com/github/TUIlmenauAMS/Videocoding/blob/main/LecturesJupterNotebooks/LectureN/LectureN.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

# <font color="#B85C38">Lecture N: Title</font>

*Video Coding · Prof. Gerald Schuller*

First paragraph of the lecture ...
```

## Headings

- `#` only once, for the lecture title.
- `##` for every section, including `## Python Example: ...`.
- `###` for a subsection inside a section, if needed.
- Headings are left-aligned and in Title Case. Use them only for headings, not for whole sentences or questions.
- Title and section headings use the brown heading colour `#B85C38`, which is readable in light and dark mode:

  ```markdown
  ## <font color="#B85C38">Motion Estimation and Prediction</font>
  ```

  Keep the `##` in front of the `<font>`, so the line stays a real heading for Colab's table of contents and collapsible sections. Use `<font color>` rather than `<span style>`, because Colab removes `style` attributes in text cells.

## Text

- Separate paragraphs with a blank line instead of `<br>`.
- Do not wrap text in `<font>`, `<p style=...>` or `<center>` blocks. Markdown inside them is not rendered in JupyterLab or on GitHub, so `**bold**` shows up with its asterisks. (The only `<font>` is the colour inside a heading line, see above.)
- Use **bold** for key terms, and `- ` for lists.
- Highlight observations and conclusions as a quote block: `> **Observe:** ...`
- Write links as `[text](https://...)`.

## Figures

Use absolute URLs, so the figures also load in Colab, and describe the figure in the alt text:

```markdown
![Block diagram of a video encoder with motion estimation](https://github.com/TUIlmenauAMS/Videocoding/blob/main/LecturesJupterNotebooks/LectureN/Img-LectureN/LectureN-1.PNG?raw=1)

*Fig. 2: Caption (source: Author: “Book”)*
```

If a figure is too large, use `<img src="..." alt="..." width="600">` instead.

## Math

- Inline math: `$x_n$`.
- Display math: `$$ ... $$` on its own lines, with a blank line before and after.

## Code cells

- Put a short Markdown cell before each code cell that says what it shows.
- Import modules by name (`import numpy as np`), not with `import *`.
- Before committing: in Colab *Runtime → Restart session and run all* (in Jupyter *Kernel → Restart Kernel and Run All Cells*), and make sure no cell ends with an error. Delete empty cells.

## Presenting in the lecture

Use the browser zoom (Ctrl/Cmd and +, 150–200 %). It enlarges text, code and figures together, in every environment.
