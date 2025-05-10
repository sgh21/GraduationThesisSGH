ENTRY
{
  author
  author.aux
  editor
  title
  title.aux
%++ main title
  booktitle
  journal
  newspaper
%--
  edition
  address
%++ publisher
  publisher
  organization
%--
  year
  volume
  number
  year.end
  vol.end
  num.end
  date
  date.pub
  pages
  url
  doi
  language
}{
  is.cn
  max
  num
  idx
}{
  tmpstr
  mark
  mtitle
  presser
}

FUNCTION {define.lang}
{
  language empty$ {
    #0 'is.cn :=
  }{
    language "cn" = {
      #1 'is.cn :=
    }{
      #0 'is.cn :=
    } if$
  } if$
}

FUNCTION {define.mtitle}
{
  booktitle empty$ {
    journal empty$ {
      newspaper empty$ 'skip$ {
        newspaper 'mtitle :=
      } if$
    }{
      journal 'mtitle :=
    } if$
  }{
    booktitle 'mtitle :=
  } if$
}

FUNCTION {define.press}
{
  publisher empty$ {
    organization empty$ 'skip$ {
      organization 'presser :=
    } if$
  }{
    publisher 'presser :=
  } if$
}


FUNCTION {output.title}
{
  'tmpstr :=
  tmpstr empty$ {
    is.cn {
      "未知题名" write$
    }{
      "unknown title" write$
    } if$
  }
  { tmpstr write$ } if$
}

FUNCTION {output.names}
{
  'tmpstr :=
  tmpstr num.names$ 'num :=
  num #3 < {
    num 'max :=
  }{
    #3 'max :=
  } if$
  #0 'idx :=
  {idx max <} {
    idx #1 + 'idx :=
    idx #1 > {
      ", " write$
    } 'skip$ if$
    is.cn {
      tmpstr idx "{ll}{ff}" format.name$ write$
    }{
      tmpstr idx "{vv~}{ll}{ j}{ f}" format.name$ write$
    } if$
  } while$
  num #3 > {
    is.cn {
      ", 等" write$
    }{
      ", et al" write$
    } if$
  } 'skip$ if$
}

FUNCTION {output.addrpuber}
{
  url empty$ {
    address empty$ {
      is.cn {
        "出版地不详: " write$
      }{
        "S.l.: " write$
      } if$
    }{
      address ": " * write$
    } if$
    presser empty$ {
      is.cn {
        "出版者不详" write$
      }{
        "S.n." write$
      } if$
    }{
      presser write$
    } if$
    ", " write$
  }{
    address empty$ 'skip$ {
      address write$
      presser empty$ 'skip$ {
        ": " write$
      } if$
    } if$
    presser empty$ {
      address empty$ 'skip$ {
        ", " write$
      } if$
    }{
      presser ", " * write$
    } if$
  } if$
}

FUNCTION {output.year}
{
  'tmpstr :=
  tmpstr empty$ {
    is.cn {
      "某年" write$
    }{
      "the year" write$
    } if$
  }{
    tmpstr write$
  } if$
}

FUNCTION {monograph} % author,title,title.aux,mark,author.aux,edition,address,presser,year,pages,date,url,doi
{
  define.lang
  define.press
  "\bibitem{" cite$ * "} " * write$
  author empty$ 'skip$ {
    author output.names
    ". " write$
  } if$
  title output.title
  title.aux empty$ 'skip$ {
    ": " title.aux * write$
  } if$
  url empty$ {
    "[" mark * "]. " * write$
  }{
    "[" mark * "/OL]. " * write$
  } if$
  author.aux empty$ 'skip$ {
    author.aux output.names
    ". " write$
  } if$
  edition empty$ 'skip$ {
    edition ". " * write$
  } if$
  output.addrpuber
  year output.year
  pages empty$ 'skip$ {
    ": " pages * write$
  } if$
  date empty$ 'skip$ {
    "[" date * "]" * write$
  } if$
  "." write$
  url empty$ 'skip$ {
    " " url * "." * write$
  } if$
  doi empty$ 'skip$ {
    " " doi * "." * write$
  } if$
  newline$
}

FUNCTION {inmonograph} % author,title,mark,author.aux,editor,mtitle,title.aux,edition,address,presser,year,pages,date,url,doi
{
  define.lang
  define.mtitle
  define.press
  "\bibitem{" cite$ * "} " * write$
  author empty$ 'skip$ {
    author output.names
    ". " write$
  } if$
  title output.title
  url empty$ {
    "[" mark * "]" * write$
  }{
    "[" mark * "/OL]" * write$
  } if$
  author.aux empty$ 'skip$ {
    ". " write$
    author.aux output.names
  } if$
  "// " write$
  editor empty$ 'skip$ {
    editor output.names
    ". " write$
  } if$
  mtitle output.title
  title.aux empty$ 'skip$ {
    ": " title.aux * write$
  } if$
  ". " write$
  edition empty$ 'skip$ {
    edition ". " * write$
  } if$
  output.addrpuber
  year output.year
  pages empty$ 'skip$ {
    ": " pages * write$
  } if$
  date empty$ 'skip$ {
    "[" date * "]" * write$
  } if$
  "." write$
  url empty$ 'skip$ {
    " " url * "." * write$
  } if$
  doi empty$ 'skip$ {
    " " doi * "." * write$
  } if$
  newline$
}

FUNCTION {serial} % author,title,title.aux,mark,year,volume,number,year.end,vol.end,num.end,address,presser,date,url,doi
{
  define.lang
  define.press
  "\bibitem{" cite$ * "} " * write$
  author empty$ 'skip$ {
    author output.names
    ". " write$
  } if$
  title output.title
  title.aux empty$ 'skip$ {
    ": " title.aux * write$
  } if$
  url empty$ {
    "[" mark * "]. " * write$
  }{
    "[" mark * "/OL]. " * write$
  } if$
  year output.year
  volume empty$ 'skip$ {
    ", " volume * write$
  } if$
  number empty$ 'skip$ {
    "(" number * ")" * write$
  } if$
  "-" write$
  vol.end empty$ {
    num.end empty$ {
      year.end empty$ 'skip$ {
        year.end write$
      } if$
    }{
      year.end output.year
      "(" num.end * ")" * write$
    } if$
  }{
    year.end output.year
    ", " vol.end * write$
    num.end empty$ 'skip$ {
      "(" num.end * ")" * write$
    } if$
  } if$
  ". " write$
  output.addrpuber
  year output.year
  "-" write$
  year.end empty$ 'skip$ {
    year.end write$
  } if$
  date empty$ 'skip$ {
    "[" date * "]" * write$
  } if$
  "." write$
  url empty$ 'skip$ {
    " " url * "." * write$
  } if$
  doi empty$ 'skip$ {
    " " doi * "." * write$
  } if$
  newline$
}

FUNCTION {inserial} % author,title,mark,mtitle,title.aux,year,volume,number,pages,date,url,doi
{
  define.lang
  define.mtitle
  "\bibitem{" cite$ * "} " * write$
  author empty$ 'skip$ {
    author output.names
    ". " write$
  } if$
  title output.title
  url empty$ {
    "[" mark * "]. " * write$
  }{
    "[" mark * "/OL]. " * write$
  } if$
  mtitle output.title
  title.aux empty$ 'skip$ {
    ": " title.aux * write$
  } if$
  ", " write$
  year output.year
  volume empty$ 'skip$ {
    ", " volume * write$
  } if$
  number empty$ 'skip$ {
    "(" number * ")" * write$
  } if$
  pages empty$ 'skip$ {
    ": " pages * write$
  } if$
  date empty$ 'skip$ {
    "[" date * "]" * write$
  } if$
  "." write$
  url empty$ 'skip$ {
    " " url * "." * write$
  } if$
  doi empty$ 'skip$ {
    " " doi * "." * write$
  } if$
  newline$
}

FUNCTION {patent} % author,title,number,date.pub,date,url,doi
{
  define.lang
  "\bibitem{" cite$ * "} " * write$
  author empty$ 'skip$ {
    author output.names
    ". " write$
  } if$
  title output.title
  number empty$ {
    is.cn {
      "未知专利号" write$
    }{
      "unknown number" write$
    } if$
  }
  { number write$ } if$
  url empty$ {
    "[P]. " * write$
  }{
    "[P/OL]. " * write$
  } if$
  date.pub empty$ {
    is.cn {
      "某日" write$
    }{
      "the date" write$
    } if$
  }
  { date.pub write$ } if$
  date empty$ 'skip$ {
    "[" date * "]" * write$
  } if$
  "." write$
  url empty$ 'skip$ {
    " " url * "." * write$
  } if$
  doi empty$ 'skip$ {
    " " doi * "." * write$
  } if$
  newline$
}

FUNCTION {book} % author,title,title.aux,author.aux,edition,address,publisher,year,pages,date,url,doi
{
  "M" 'mark :=
  monograph
}

FUNCTION {inbook} % author,title,author.aux,editor,booktitle,title.aux,edition,address,publisher,year,pages,date,url,doi
{
  "M" 'mark :=
  inmonograph
}

FUNCTION {proceedings} % author,title,title.aux,author.aux,edition,address,publisher/organization,year,pages,date,url,doi
{
  "C" 'mark :=
  monograph
}

FUNCTION {inproceedings} % author,title,author.aux,editor,booktitle,title.aux,edition,address,publisher/organization,year,pages,date,url,doi
{
  "C" 'mark :=
  inmonograph
}

FUNCTION {collection} % author,title,title.aux,author.aux,edition,address,publisher/organization,year,pages,date,url,doi
{
  "G" 'mark :=
  monograph
}

FUNCTION {incollection} % author,title,author.aux,editor,booktitle,title.aux,edition,address,publisher/organization,year,pages,date,url,doi
{
  "G" 'mark :=
  inmonograph
}

FUNCTION {report} % author,title,title.aux,author.aux,edition,address,publisher/organization,year,pages,date,url,doi
{
  "R" 'mark :=
  monograph
}

FUNCTION {thesis} % author,title,title.aux,author.aux,address,publisher/organization,year,pages,date,url,doi
{
  "D" 'mark :=
  monograph
}
FUNCTION {mastersthesis} {thesis}
FUNCTION {phdthesis} {thesis}

FUNCTION {standard} % author,title,title.aux,author.aux,edition,address,publisher/organization,year,pages,date,url,doi
{
  "S" 'mark :=
  monograph
}

FUNCTION {periodical} % author,title,title.aux,year,volume,number,year.end,vol.end,num.end,address,publisher/organization,date,url,doi
{
  "J" 'mark :=
  serial
}

FUNCTION {article} % author,title,journal,title.aux,year,volume,number,pages,date,url,doi
{
  "J" 'mark :=
  inserial
}

FUNCTION {news} % author,title,newspaper,title.aux,year,number,pages,date,url,doi
{
  "N" 'mark :=
  inserial
}

FUNCTION {begin.bbl} {
  "\begin{thebibliography}" write$
  newline$}
FUNCTION {end.bbl} {
  "\end{thebibliography}" write$
  newline$}

READ
EXECUTE {begin.bbl}
ITERATE {call.type$}
EXECUTE {end.bbl}
