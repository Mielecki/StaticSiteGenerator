# StaticSiteGenerator

A program that generates static html pages from markdown files.

## How it works:

1. All Markdown files (`.md`) are stored in the `/content` directory. In the root of the project, there is `template.html`, which defines the layout and structure of each HTML page.
2. The static site generator reads the Markdown files and the template file.
3. The generator converts the Markdown files to a final HTML file for each page and writes them to the `/public` directory.
4. The built-in Python HTTP server is used to serve the contents of the `/public` directory on `http://localhost:8888`.
5. Open a browser and navigate to `http://localhost:8888` to view the rendered site.

This project was developed during the boot.dev online course.