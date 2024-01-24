import camelot
import os
import pandas as pd

from itertools import groupby
from time import time as now


def write_table(df, rename, filename):
    # Some entries have newlines in them; we don't need those anymore.
    for c in df.columns:
        df[c] = df[c].apply(lambda s: s.replace("\n", ""))

    # Use the first row as a header
    df.columns = df.iloc[0]
    df = df[1:]

    if rename:
        df = df.rename(columns=rename)

    # Write out a csv that can be used for visualization purposes.
    df.to_csv(filename)


def main(filename, outdir):
    print("Parsing tables from %s, this may take a few minutes..." % filename)
    start = now()
    tables = camelot.read_pdf(filename, pages='all', flavor='lattice')
    print("Parsed %d tables in %2.1fs" % (len(tables), now() - start))

    # Tables that span multiple pages get multiple entries; can merge them
    # based on their header row.
    header = lambda t:  ' | '.join(c.text.strip() for c in t.cells[0])
    grouped = {h: list(tg) for (h, tg) in groupby(tables, header)}

    # Show tables
    print("Got %d Tables:" % len(grouped))
    for i, (k, v) in enumerate(grouped.items(), 1):
        print("%d. Page %d (%d pages)" % (i, v[0].page - 8, len(v)))

    # Merge the multi-page tables into single entities (dataframes)
    merged = []
    for (k, v) in grouped.items():
        m = v[0].df
        if 1 < len(v):
            m = pd.concat([m] + [t.df[1:] for t in v[1:]])
        merged.append(m)

    print("Merged %d Tables:" % len(merged))
    for i, t in enumerate(merged, 1):
        print("%d. %d rows" % (i, len(t)))

    to_write = [
        # index, cols to rename, filename
       (5, None, "table6"),
       (7, None, "table8"),
       (-1, {"Ensemble61": "Ensemble", "Issue number": "Issue"}, "appendix"),
    ]

    os.makedirs(outdir, exist_ok=True)
    for (ix, rename, name) in to_write:
        print("writing table %d to %s/%s.csv ..." % (ix, outdir, name))
        write_table(merged[ix], rename, os.path.join(outdir, name + ".csv"))

    return merged


if __name__ == '__main__':
    main('canon.pdf', './extracted')
