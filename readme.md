# Slidedown - Terminal Markdown Presentations

Slidedown is a powerful presentation engine that lets you create and deliver stylish presentations using Markdown. With live code execution, theme support, and interactive elements, it transforms your terminal into a dynamic presentation tool.

## Features

- 🚀 **Markdown-based presentations** - Simple syntax for slide creation
- 💻 **Live code execution** - Run Python directly in your slides
- 🎨 **Theme support** - Multiple color schemes included
- 🔄 **Interactive elements** - Refresh content during presentation
- 📱 **Responsive layout** - Adapts to any terminal size
- ⚡ **Keyboard navigation** - Intuitive slide controls

## Installation

```bash
git clone https://github.com/lewepit/slidedown.git
cd slidedown
python3 main.py examples/demo.md ```

## Quick Start

1. Create your presentation file (`presentation.md`):

````markdown
# Welcome to Slidedown

```python live
print("Hello Terminal Presentations!")
```
````

---

# Enjoy!

````
2. Run the presentation:
```bash
slidedown presentation.md
```
````

## Presentation Syntax

### Basic Structure

```markdown
# Slide 1 Title

Content for slide 1

---

## Slide 2 Header

- Bullet points
- More content

---

# Final Slide
```

### Code Blocks

````markdown
```python
# Regular code display
print("Syntax highlighted")
```

---

```python live
# Executable code
import datetime
print("Current time:", datetime.datetime.now())
```

---

```python output_only live
# Shows only output
print("Output only visible")
```
````

### Themes

Press `t` during presentation to cycle through themes:

- `default` (cyan headers, green code)
- `dark` (red headers, yellow code)
- `matrix` (green theme)

## Command Line Options

```bash
slidedown presentation.md [-t TIMEOUT]
```

| Option            | Description                                 | Default |
| ----------------- | ------------------------------------------- | ------- |
| `-t`, `--timeout` | Execution timeout for code blocks (seconds) | 10      |

## Keyboard Controls

| Key         | Action                |
| ----------- | --------------------- |
| →, n, Space | Next slide            |
| ←, p        | Previous slide        |
| Home, g     | First slide           |
| End, G      | Last slide            |
| t           | Cycle themes          |
| +           | Increase timeout      |
| -           | Decrease timeout      |
| r           | Refresh current slide |
| q           | Quit presentation     |

## Troubleshooting

### Common Issues

1. **Module not found errors**:

   ```bash
   # Install required packages
   pip install ...
   ```

2. **Code not executing**:

   - Add `live` flag to code block: `python live`
   - Increase timeout: `slidedown presentation.md -t 10`

3. **Presentation formatting issues**:
   - Ensure slides are separated by `---` on empty lines
   - Check for consistent indentation in code blocks

## Examples

Explore these sample presentations in the [examples](https://github.com/lewepit/slidedown/tree/main/examples) directory:

Run any example:

```bash
slidedown examples/presentation.md
```

## Advanced Usage

### Custom Themes

Create your own color scheme by modifying the `themes` dictionary in the code:

```python
self.themes = {
    "custom": {
        "header": curses.COLOR_MAGENTA,
        "code": curses.COLOR_CYAN,
        "border": curses.COLOR_YELLOW,
        "footer": curses.COLOR_BLUE,
        "output": curses.COLOR_WHITE,
        "shortened": curses.COLOR_RED,
        "error": curses.COLOR_RED
    }
}
```

### Output-Only Slides

Hide code and show only execution results:

````markdown
```python output_only live
# Only output will be displayed
import platform
print(f"System: {platform.system()} {platform.release()}")
```
````

## License

Slidedown is released under the MIT License

---

Transform your terminal into a presentation powerhouse with Slidedown! For more examples and advanced features, explore the [examples directory](https://github.com/lewepit/slidedown/tree/main/examples).
