import csv
import datetime as dt
from urllib.request import urlopen

import lxml.html

URL = "https://explorer.ipco.app/daily-stats"

if __name__ == "__main__":
    with urlopen(URL) as r:
        raw = r.read()
    tree = lxml.html.fromstring(raw)
    tables = tree.findall(".//table")
    assert len(tables) == 1
    table = tables[0]

    with open("stats.csv", "wt", encoding="utf-8") as fw:
        cw = csv.writer(fw)
        header = [j.text for j in table.find("thead").find("tr").findall("th")]
        cw.writerow(header)

        for raw_row in table.find("tbody").findall("tr"):
            row = [j.text for j in raw_row.findall("td")]
            tidx = header.index("Timestamp")
            row[tidx] = dt.datetime.utcfromtimestamp(int(row[tidx])).isoformat()

            cw.writerow(row)
