# README

## Background
There's an interesting paper by Casey Mullin: [A Canon Within a Canon: The Influence of the 30 berühmte Quartette on the Contemporary Reception of Haydn's String Quartets](httpe://cedar.wwu.edu/cgi/viewcontent.cgi?article=2108&context=wwuet) that has some interesting data tables in it.

I decided it would be great to pry them out of the pdf. And also that code would be easier than a lot of cut and paste.

I surveyed the python options:
* Tabula (relies on java install)
* Camelot (doesn't)

## List of Tables:
1. Earliest Editions of Haydn’s String Quartets (Single Opus Groups)
2. Complete Editions of Haydn’s String Quartets (consisting of or including parts), 1801-2014 
3. Incomplete Editions of Haydn’s String Quartets, 1808-1918: Publication Details 
4. Incomplete Editions of Haydn’s String Quartets, 1808-1918: Contents
    * this is where TCQ is enumerated
5. Sequence and numbering of works in the TCQ
    * volume breakdown - I: (14q), II: (16q)
6. Total Frequency of Haydn String Quartet Recordings
    * Good summary stats
7. Average Frequency of Haydn String Quartet Recordings
    * Summary Stats, not that useful
8. Frequency of Haydn String Quartet Recordings, by Time Period
9. Average Frequency of Haydn String Quartet Recordings, by Time Period
    * Summary Stats, not that useful
10. Frequency of Haydn String Quartet Recordings, by Time Period (incomplete
opus samplings only)
11. Average Frequency of Haydn String Quartet Recordings, by Time Period
(incomplete opus samplings only)
    * Summary Stats, not that useful
    * SKIPPED BY `camelot`!
12. Appendix. Discography of Haydn String Quartets (on Tangible Media)
    * Written as the 11th table by `camelot`

## Installing Dependencies
*use [Camelot](https://camelot-py.readthedocs.io/en/master/)*

```bash
pip install camelot-py
pip install opencv-python
brew install ghostscript tcl-tk
pip install ghostscript
```
 
## Code

`wget "https://cedar.wwu.edu/cgi/viewcontent.cgi?article=2108&context=wwuet" -O canon.pdf -nc`

See `parse.py`, which opens `canon.pdf` and produces 3 files in the directory `./extracted`:
1. `table6.csv`: the contents of table 6 (Total Freq)
1. `table8.csv`: the contents of table 8 (Total Freq by time period)
1. `recordings.csv`: the appendix

Then run `clean.py` which merges Peters volume information with the data in recordings.csv, and does some other cleanup, before producing `./site/recordings.csv`, which should be suitable for visualization. Note: several (5) records in recordings.csv don't have valid / easily parsable Dates. They are skipped.

## Visualization 
A [crossfilter](https://github.com/crossfilter/crossfilter)-powered exploration of './site/recordings.csv'
    * [docs for dc.js](https://github.com/dc-js/dc.js/blob/develop/docs/api-latest.md) are helpful.

Currently just using a single file since it's small and self-contained. TODO: think about pulling in dependencies.

## Deploying:
Deploy to github pages:
1. On Local Machine
```
git init -b main
git add .gitignore
# git add other selected files or just `git add .`
gh repo create
```

2. On Github, [configure custom action](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site#publishing-with-a-custom-github-actions-workflow)
    * use static
    * modify the script to point to ./site
