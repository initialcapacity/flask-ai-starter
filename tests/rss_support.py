rss_feed = """<?xml version="1.0" encoding="UTF-8" ?>
    <rss version="2.0">
    
    <channel>
      <title>Test Feed</title>
      <link>https://rss.example.com</link>
      <description>Example RSS</description>
      <item>
        <title>Feed 1</title>
        <link>https://rss.example.com/1</link>
      </item>
      <item>
        <title>Feed 2</title>
        <link>https://rss.example.com/2</link>
      </item>
    </channel>
    </rss>"""

html_page = """
    <html lang="en">
    <head>
    <title>Page title</title>
    </head>
    <body>
    <script>
    const a = 12
    console.log(a)
    </script>
    
    <h1>A heading</h1>
    
    <p>Some text</p>
    <p>in two paragraphs</p>
    
    <style>
    h1 {
        color: red;
    }
    </style>
    </body>
    </html>
    """