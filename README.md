# Clifford Quantum Cellular Automata Blog

This repository contains a Jekyll-based blog focused on 1-D Clifford Quantum Cellular Automata research. The blog supports LaTeX equations through MathJax.

## Local Setup

### Prerequisites

- Ruby (version 2.5 or higher)
- RubyGems
- Bundler

### Local Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/blog.git
   cd blog
   ```

2. Install dependencies:
   ```bash
   bundle install
   ```

3. Run the Jekyll server locally:
   ```bash
   bundle exec jekyll serve
   ```

4. Open your browser and navigate to `http://localhost:4000/blog/`

## Deploying to GitHub Pages

1. Create a new repository on GitHub named `yourusername.github.io` (replace "yourusername" with your actual GitHub username).

2. Update the `_config.yml` file:
   ```yaml
   baseurl: "" # for user site
   url: "https://yourusername.github.io"
   ```

3. Push your code to the GitHub repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/yourusername.github.io.git
   git push -u origin main
   ```

4. Enable GitHub Pages in your repository settings:
   - Go to your repository on GitHub
   - Click on "Settings"
   - Scroll down to the "GitHub Pages" section
   - Select the "main" branch as the source
   - Click "Save"

5. Wait a few minutes for GitHub Pages to build and deploy your site
   - Your site will be available at `https://yourusername.github.io`

## Writing Posts with LaTeX

All posts should include `mathjax: true` in the front matter to enable LaTeX support. You can then use LaTeX syntax in your posts:

- Inline math: `$E = mc^2$` renders as $E = mc^2$
- Display math: `$$E = mc^2$$` renders as a centered equation

## License

This project is open source and available under the [MIT License](LICENSE). # Test commit
