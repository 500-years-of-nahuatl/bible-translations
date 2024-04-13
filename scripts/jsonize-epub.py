#!/usr/bin/env python3
import argparse, json, os
from lxml import etree


books = [
    "1CH.xhtml", "2SA.xhtml", "ECC.xhtml", "HEB.xhtml", "LAM.xhtml",
    "PHM.xhtml", "1CO.xhtml", "2TH.xhtml", "EPH.xhtml", "HOS.xhtml",
    "LEV.xhtml", "PHP.xhtml", "1JN.xhtml", "2TI.xhtml", "PRO.xhtml",
    "1KI.xhtml", "3JN.xhtml", "EST.xhtml", "ISA.xhtml", "PSA.xhtml",
    "1PE.xhtml", "ACT.xhtml", "EXO.xhtml", "JAS.xhtml", "LUK.xhtml",
    "REV.xhtml", "1SA.xhtml", "AMO.xhtml", "EZK.xhtml", "JDG.xhtml",
    "MAL.xhtml", "ROM.xhtml", "1TH.xhtml", "COL.xhtml", "EZR.xhtml",
    "JER.xhtml", "MAT.xhtml", "RUT.xhtml", "1TI.xhtml", "GAL.xhtml",
    "JHN.xhtml", "MIC.xhtml", "SNG.xhtml", "2CH.xhtml", "JOB.xhtml",
    "MRK.xhtml", "TIT.xhtml", "2CO.xhtml", "JOL.xhtml", "NAM.xhtml",
    "2JN.xhtml", "GEN.xhtml", "JON.xhtml", "NEH.xhtml", "ZEC.xhtml",
    "2KI.xhtml", "DAN.xhtml", "HAB.xhtml", "JOS.xhtml", "NUM.xhtml",
    "ZEP.xhtml", "2PE.xhtml", "DEU.xhtml", "HAG.xhtml", "JUD.xhtml",
    "OBA.xhtml"
    ]


def parse_book(book, oebps):
    D = {}
    ns = "{http://www.w3.org/1999/xhtml}"
    parser = etree.XMLParser(remove_blank_text=True)
    root = etree.parse(f"{oebps}/{book}", parser).getroot()
    title = root.find(f".//{ns}div[@class='mt']")
    title2 = root.find(f".//{ns}div[@class='mt2']")
    main = root.find(f".//{ns}div[@class='main']")
    print(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~>{oebps}/{book}")
    #print(title.text)
    D["000"] = title.text.strip()
    if title2 is not None:
        D["000"] = ' '.join([D['000'], title2.text.strip()])
    ch_d = {}
    head_counter = 0
    chapter_nr = None
    verse = None
    for elem in main:
        if elem.attrib["class"] == "psalmlabel":
            if chapter_nr:
                D[chapter_nr] = ch_d
            ch_d = {}
            head_counter = 0
            verse = None
            chapter_nr = "{:0>{}}".format(elem.text.strip(), 3)
        elif elem.attrib["class"] == "s":
            head_counter += 1
            ch_d[f"head_{head_counter}"] = elem.text
        elif elem.attrib["class"] == "p" or elem.attrib["class"] == "q":
            print(verse, elem.text, ch_d)
            if elem.text is not None:
                if verse not in ch_d:
                    ch_d[verse] = elem.text.strip()
                else:
                    print(ch_d[verse], elem.text)
                    ch_d[verse] = ' '.join([ch_d[verse], elem.text.strip()])
            for span in elem.findall(f"{ns}span"):
                if "class" in span.attrib and span.attrib['class'] == 'verse':
                    #print("SPAN", verse, span.text, span.tail)
                    verse = "{:0>{}}".format(span.text.strip(), 3)
                    if span.tail is not None:
                        ch_d[verse] = span.tail.strip()
    D[chapter_nr] = ch_d
    return D




def write(D, oebps, book, epub, counter_1):
    if len(D) < 2:
        print(f"{oebps}/{book}")#, f"json/{epub}/{book[:3]}.json")
        counter_1 += 1
    if not os.path.exists(f"json/{epub}"):
        os.mkdir(f"json/{epub}")
    with open(f"json/{epub}/{book[:3]}.json", "w+") as out:
        json.dump(D, out, ensure_ascii=False, indent=4)
    return counter_1




def main(args):
    counter = 0
    counter_1 = 0
    epubdir = "epubs/extract"
    epubs = os.listdir(epubdir)

    if args.file_list:
        with open(args.file_list, 'r') as inf:
            files = inf.readlines()
            files = [_.strip() for _ in files]
        for f in files:
            counter += 1
            book = f.split('/')[-1]
            oebps = '/'.join(f.split('/')[:-1])
            epub = f.split('/')[2]
            counter_1 = write(parse_book(book, oebps), oebps, book, epub, counter_1)

    else:
        for epub in epubs:
            oebps = f"{epubdir}/{epub}/OEBPS"
            BOOKS = os.listdir(oebps)
            for book in BOOKS:
                if book in books:
                    counter += 1
                    #print(book)
                    counter_1 = write(parse_book(book, oebps), oebps, book, epub, counter_1)

    print(counter, counter_1)




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--file-list", type=str, help="pass a file list")
    args = parser.parse_args()
    main(args)
