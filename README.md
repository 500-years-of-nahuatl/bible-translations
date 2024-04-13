# Biblical texts in Nahuatl Variants

## Content

The repository contains biblical text translations in 13 Nahuatl variants. These are listed in `metadata/`.

## Why?

The repo is intended as a data source for research or whatever, prodiding a simple consistent format in `json/`.

### Format

Under `json/`, subdirectories are named using variant codes. Each file is a single biblical book in simple json format:

```.json
{
	"000": "<Book title and subtitle>",
	"001": { /* numbered chapter */
		"head_1": "<unnumbered subheadings>",
		"001": "<numbered verses>"
	}
}
```

## Sources

Data was scraped from the web (`html/`) or downloaded and extracted from epub files (`epubs/extract/`).

## Scripts

Converting from html/epub to json was done with python scripts in the `scripts/` directory.

## Licence

Source material was released under creative commons licence --- full info found in the sources --- and thus under the terms the files here are too.