from IPython.display import HTML


def display_tag(text, tag, color="linear-gradient(315deg,  #2a2a72 0%, #009ffd 74%)", font_color="white"):
    return HTML(f"""
    '<!DOCTYPE html>
    <html lang="en">
        <head>
            <title>displaCy</title>
        </head>
        <body style="font-size: 16px; font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif, \'Apple Color Emoji\', \'Segoe UI Emoji\', \'Segoe UI Symbol\'; padding: 4rem 2rem; direction: ltr">
        <figure style="margin-bottom: 6rem">
            <div class="entities" style="line-height: 1.0; direction: ltr">
            <mark class="entity" style="background: {color}; padding: 0.30em 0.6em; margin: 0 0.50em; line-height: 2; border-radius: 0.35em; font-size: 3em; color: {font_color}">
                {text}
                <span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; text-transform: uppercase; vertical-align: middle; margin-left: 0.5rem">{tag}</span>
            </mark>
            </div>
        </figure>
    </body>
    </html>'
    """)
