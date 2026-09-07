Résumé lives here in three formats, all published:

  index.html  → the web version at /resumes/  (fonts are inlined, so it
                renders identically offline and exports cleanly to PDF)
  *.pdf       → generated from index.html via headless Chrome
  *.docx      → ATS-friendly Word version, plain single-column

To regenerate the PDF after editing index.html:

  chrome --headless --disable-gpu --no-pdf-header-footer \
    --print-to-pdf="resumes/Thayagapriyan-Dravidamani-Resume.pdf" \
    "file:///<abs-path>/resumes/index.html"

The .docx is maintained separately — edit it in Word directly.
Keep both filenames stable; the site links to them by name.
