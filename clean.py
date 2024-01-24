import csv
import json
import os


def read_json(filename):
    with open(filename) as f:
        return json.load(f)


def read_csv(filename):
    with open(filename) as f:
        return list(csv.DictReader(f))


def key(r):
    o = r['Opus'].rjust(3, '0')
    n = r['Number']
    return '_'.join([o, n]) if n else o


def to_str(r):
    return "{Catalog}: {Ensemble} on {Label} [{Date}] -- {Issue} - {Notes}".format(**r)


def merge(peters, recordings):
    for r in recordings:
        k = key(r)
        # e.g. Opus 2 #3 present in data, but not peters, so will have None
        # for some recordings
        r['Catalog'] = k
        r['Peters'] = peters.get(k)

    return recordings


def write(data, directory, filename, fieldnames):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)

    with open(path, 'w') as f:
        w = csv.DictWriter(f, fieldnames, extrasaction='ignore')
        w.writeheader()
        w.writerows(data)


def clean(recordings):
    cleaned = []
    for r in recordings:
        # Fix year to be a 4 digit int-interpretable thing
        # Try first 4 or last 4 chars, declare failure otherwise.
        y = r['Date']
        if y[:4].isnumeric():
            r['Date'] = int(y[:4])
        elif  y[-4:].isnumeric():
            r['Date'] = int(y[-4:])
        else: # unsure how to parse
            print("Couldn't parse '%s', removing %s" % (y, to_str(r)))
            # we lose about 5 old recordings; some spelunking might be possible to find dates for
            # Lener, Poltronieri, Lowenguth quartets
            continue

        # Camelot added an unlabeled column which I'm pretty sure is table row
        # from the original tables (which restarts numbering on each page.
        # this isn't useful; kill it.
        del r['']
        if r['Ensemble'] == 'Aeolian Quartet (London, England)':
            r['Ensemble'] = 'Aeolian Quartet'

        cleaned.append(r)

    return cleaned


def main():
    peters = read_json('./data/haydn_peters.json')
    recordings = read_csv('./extracted/appendix.csv')

    data = merge(peters, recordings)
    data = clean(data)

    # This ignores the "Source" column, which ... I don't know what to do with anyway. :)
    cols = 'Catalog, Opus, Number, Peters, Date, Ensemble, Label, Issue, Notes'.split(', ')
    write(data, './site', 'recordings.csv', cols)

    return data


if __name__ == '__main__':
    main()
