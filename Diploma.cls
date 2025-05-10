\NeedsTeXFormat{LaTeX2e}
\renewcommand\normalsize{\@setfontsize\normalsize\@xiipt{20pt plus 2pt minus 2pt}}
\pagenumbering{Roman}%
\newcounter {chapter}
\newcounter {section}[chapter]
\newcounter {subsection}[section]
\newcounter {subsubsection}[subsection]
\renewcommand \thechapter {第\the\c@chapter 章}
\renewcommand \thesection {\the\c@chapter.\the\c@section}
\renewcommand \thesubsection {\thesection.\the\c@subsection}
\renewcommand \thesubsubsection {\thesubsection.\the\c@subsubsection}
\newcounter {figure}[chapter]
\newcounter {subfigure}[figure]
\newcounter {table}[chapter]
\renewcommand \thefigure {图\the\c@chapter.\the\c@figure}
\renewcommand \thesubfigure {\thefigure(\alph{subfigure})}
\renewcommand \thetable {表\the\c@chapter.\the\c@table}
\RequirePackage{xeCJK}
\RequirePackage{graphics}
\RequirePackage{longtable}
\RequirePackage[xetex,bookmarksnumbered=true,hidelinks,pdfstartview=]{hyperref}
\graphicspath{{figure/}}
\newif\if@inmain
\newif\if@lof@exist
\newif\if@lot@exist
\newif\if@claimlof\@claimloftrue
\newif\if@claimlot\@claimlottrue
\def\lof@claim{\if@claimlof
  \@claimloffalse
  \if@filesw\immediate\write\@auxout{\string\global\string\@lof@existtrue}\fi
  \fi}
\def\lot@claim{\if@claimlot
  \@claimlotfalse
  \if@filesw\immediate\write\@auxout{\string\global\string\@lot@existtrue}\fi
  \fi}
\ProvidesClass{Diploma}[2025/04/01 by LINZHR.THU]
\setmainfont{times.ttf}[BoldFont=Arial]
\setCJKmainfont{SimSun}[BoldFont=SimHei]
\setCJKmonofont{DengXian}
\setlength\paperwidth{210mm}
\setlength\oddsidemargin{4.6mm}
\setlength\evensidemargin{4.6mm}
\setlength\textwidth{150mm}
\setlength\paperheight{297mm}
\setlength\topmargin{4.6mm}
\setlength\topskip{0mm}
\setlength\textheight{237mm}
\setlength\footskip{15mm}
\setlength\parindent{2em}
\parskip 0pt plus 6pt
\@twosidetrue
\setcounter{tocdepth}{3}
\newlength\iiiptlen
\setlength\iiiptlen{3pt plus 2pt minus 1pt}
\newlength\viptlen
\setlength\viptlen{6pt plus 4pt minus 2pt}
\newlength\xiiptlen
\setlength\xiiptlen{12pt plus 8pt minus 4pt}
\newlength\xviiiptlen
\setlength\xviiiptlen{18pt plus 12pt minus 6pt}
\newlength\xxivptlen
\setlength\xxivptlen{24pt plus 16pt minus 8pt}
\newlength\bef@float
\setlength\bef@float{9pt plus 2pt minus 2pt}
\newlength\aft@float
\setlength\aft@float{4pt}
\setlength\intextsep\z@skip
\setlength\floatsep\z@skip
\setlength\textfloatsep{3pt}
\def\g@title{请设置论文题目}
\DeclareRobustCommand\SetTitle[1]{\def\g@title{#1}}
\def\g@department{请设置系别}
\DeclareRobustCommand\SetDepartment[1]{\def\g@department{#1}}
\def\g@major{请设置专业}
\DeclareRobustCommand\SetMajor[1]{\def\g@major{#1}}
\def\g@author{作者}
\DeclareRobustCommand\SetAuthor[1]{\def\g@author{#1}}
\def\g@instru{指导教师}
\def\g@institle{教授}
\DeclareRobustCommand\SetInstructor[2]{\def\g@instru{#1}\def\g@institle{#2}}
\DeclareRobustCommand\SetJointInstructor[2]{\def\g@instru@{#1}\def\g@institle@{#2}}
\newdimen\g@authorlen
\newdimen\g@instrulen
\newdimen\g@instrulen@
\newdimen\g@suitablelen
\def\@just#1#2{#1\ifx #2\relax\let\@@just\relax\else\hfil\let\@@just\@just\fi\@@just #2}
\DeclareRobustCommand\JustifyLine[1]{\expandafter\@just #1\relax}
\let\Document@Begin\document
\def\document{%
  \Document@Begin
  \bibliographystyle{mybst}%
  \normalsize
  \pagestyle{empty}%
  \leavevmode\vskip 16mm
  \begin{center}\fontsize{36pt}{0}\selectfont
    \includegraphics{tsinghua.pdf}
    \vskip 9mm
    \makebox[110mm][s]{\textbf{\JustifyLine{综合论文训练}}}
  \end{center}\vskip 17mm
  \begingroup
    \parbox[c][47mm][t]{\textwidth}{\centering\fontsize{26pt}{36pt}\selectfont\textbf{\g@title}}\par
    \CJKfontspec{FangSong}\fontsize{16pt}{32pt}\selectfont
    \settowidth\g@authorlen{\g@author}%
    \settowidth\g@instrulen{\g@instru}%
    \ifdim\g@authorlen >\g@instrulen
      \g@suitablelen\g@authorlen
    \else
      \g@suitablelen\g@instrulen
    \fi
    \ifdefined\g@instru@
      \settowidth\g@instrulen@{\g@instru@}%
      \ifdim\g@suitablelen <\g@instrulen@
        \g@suitablelen\g@instrulen@
      \fi
    \fi
    \ifdim 4em <\g@suitablelen
      \g@suitablelen{4em}%
    \fi
    \noindent
    \hspace*{30mm}系\hskip 2em 别：\g@department\\
    \hspace*{30mm}专\hskip 2em 业：\g@major\\
    \hspace*{30mm}作\hskip 2em 者：%
    \ifdim\g@suitablelen >\g@authorlen\makebox[\g@suitablelen][s]{\JustifyLine{\g@author}}\else\g@author\fi\\
    \hspace*{30mm}指导教师：%
    \ifdim\g@suitablelen >\g@instrulen\makebox[\g@suitablelen][s]{\JustifyLine{\g@instru}}\else\g@instru\fi
    \hskip 1em \g@institle
    \ifdefined\g@instru@
      \newline\hspace*{30mm}\hskip -1em 副指导教师：
      \ifdim\g@suitablelen >\g@instrulen@\makebox[\g@suitablelen][s]{\JustifyLine{\g@instru@}}\else\g@instru@\fi
      \hskip 1em \g@institle@
    \else \vskip 32pt \fi
    \vskip 30mm
  \endgroup
  \begin{center}\fontsize{16pt}{0}\selectfont
    \ChineseNumber{\number\year}年\ChineseNumber{\number\month}月
  \end{center}%
  \cleardoublepage
  \vskip 27mm
  \begin{center}\fontsize{22pt}{0}\bfseries
    关于论文使用授权的说明
  \end{center}%
  \vskip 36pt \par
  \begingroup\fontsize\@xivpt{26pt}\selectfont
    \noindent\hskip 2em
    本人完全了解清华大学有关保留、使用综合论文训练论文的规定，即：学校有权保留论文的复印件，允许论文被查阅和借阅；学校可以公布论文的全部或部分内容，可以采用影印、缩印或其他复制手段保存论文。
  \endgroup
  \vskip 21mm
  \hskip 3ex 作者签名：\hskip 41mm 导师签名：\par
  \vskip 4mm \hskip 3ex 日\hskip 2em 期：\hskip 41mm 日\hskip 2em 期：
  \cleardoublepage\pagenumbering{Roman}%
  \def\@oddfoot{\hfil\fontsize\@xpt{0}\selectfont\thepage\hfil}%
  \let\@evenfoot\@oddfoot
}
\DeclareRobustCommand\StartMainText{\@inmaintrue\clearpage\pagenumbering{arabic}}
\DeclareRobustCommand\ChsAbstract{%
  \clearpage
  \pdfbookmark{中文摘要}{CabsPosition}%
  \vskip 8mm
  \begin{center}\fontsize{16pt}{0}\bfseries
    摘\hskip 1em 要
  \end{center}\vskip 6mm\par}
\DeclareRobustCommand\EngAbstract{%
  \clearpage
  \pdfbookmark{英文摘要}{EabsPosition}%
  \vskip 8mm
  \begin{center}\fontsize{16pt}{0}\bfseries
    Abstract
  \end{center}\vskip 6mm\par}
\DeclareRobustCommand\ChsKeywords[1]{%
  \vskip 20pt
  \noindent\textbf{关键词：}\ #1}
\DeclareRobustCommand\EngKeywords[1]{%
  \vskip 20pt
  \noindent\begingroup
    \setmainfont{timesbd.ttf}Keywords:
  \endgroup\ #1}
\DeclareRobustCommand\Acknowledgments{%
  \cleardoublepage
  \refstepcounter{chapter}
  \addcontentsline{toc}{chapter}{\protect\numberline{致\hspace{1em}谢}}%
  \vskip 8mm
  \begin{center}\fontsize{16pt}{0}\bfseries
    致\hskip 1em 谢
  \end{center}\vskip 6mm \par}
\DeclareRobustCommand\Statement{%
  \cleardoublepage
  \refstepcounter{chapter}
  \addcontentsline{toc}{chapter}{\protect\numberline{声\hspace{1em}明}}%
  \vskip 8mm
  \begin{center}\fontsize{16pt}{0}\bfseries
    声\hskip 1em 明
  \end{center}\vskip 6mm \par
  本人郑重声明：所呈交的综合论文训练论文，是本人在导师指导下，独立进行研究工作所取得的成果。尽我所知，除文中已经注明引用的内容外，本论文的研究成果不包含任何他人享有著作权的内容。对本论文所涉及的研究工作做出贡献的其他个人和集体，均已在文中以明确方式标明。
  \vskip 21mm
  \hfill 签\ 名：\underline{\hspace{6em}}\ 日\ 期：\underline{\hspace{6em}}}
\newcounter{achivenum}
\DeclareRobustCommand\Achievements{%
  \cleardoublepage
  \refstepcounter{chapter}
  \addcontentsline{toc}{chapter}{\protect\numberline{在学期间}参加课题的研究成果}%
  \vskip 8mm
  \begin{center}\fontsize{16pt}{0}\bfseries
    在学期间参加课题的研究成果
  \end{center}\vskip 6mm}
\newenvironment{MyPapers}{%
  \begingroup\fontsize\@xivpt{20pt}\bfseries
  \noindent 学术论文：
  \endgroup
  \fontsize\@xpt{16pt}\selectfont
  \parskip\iiiptlen
  \list{[\the\c@achivenum]}{%
    \labelwidth 5.0ex
    \leftmargin 5.5ex
    \@nmbrlisttrue\def\@listctr{achivenum}}
}{\endlist}
\newenvironment{MyPatents}{%
  \begingroup\fontsize\@xivpt{20pt}\bfseries
  \noindent 专利：
  \endgroup
  \fontsize\@xpt{16pt}\selectfont
  \parskip\iiiptlen
  \list{[\the\c@achivenum]}{%
    \labelwidth 5.0ex
    \leftmargin 5.5ex
    \@nmbrlisttrue\def\@listctr{achivenum}}%
}{\endlist}
\DeclareRobustCommand\ListOfContents{%
  \clearpage\vskip 8mm
  \begin{center}\fontsize{16pt}{0}\bfseries
    目\hskip 1em 录\pdfbookmark{目录}{tocPosition}
  \end{center}\vskip 6mm \par
  \@starttoc{toc}%
  \if@lof@exist
    \clearpage\vskip 8mm
    \begin{center}\fontsize{16pt}{0}\bfseries
      插图清单\pdfbookmark{插图清单}{lofPosition}
    \end{center}\vskip 6mm \par
    \@starttoc{lof}%
  \fi
  \if@lot@exist
    \clearpage\vskip 8mm
    \begin{center}\fontsize{16pt}{0}\bfseries
      附表清单\pdfbookmark{附表清单}{lotPosition}
    \end{center}\vskip 6mm \par
    \@starttoc{lot}
  \fi}
\newenvironment{Abbreviations}{%
  \clearpage\vskip 8mm
  \begin{center}\fontsize{16pt}{0}\bfseries
    符号和缩略语说明\pdfbookmark{符号和缩略语}{abbPosition}
  \end{center}\vskip 6mm
  \def\arraystretch{1}%
  \begin{longtable}[l]{p{14ex}p{61ex}}%
}{\end{longtable}}
\newcounter{refnum}
\newenvironment{thebibliography}{%
  \clearpage\vskip 8mm
  \refstepcounter{chapter}%
  \begin{center}\fontsize{16pt}{0}\bfseries
    参考文献\addcontentsline{toc}{chapter}{\protect\numberline{参考文献}}
  \end{center}\vskip 6mm
  \fontsize\@xpt{16pt}\selectfont
  \parskip\iiiptlen
  \list{[\the\c@refnum]}{%
    \labelwidth 5.0ex
    \leftmargin 5.5ex
    \usecounter{refnum}}%
}{\endlist}
\DeclareRobustCommand\cite[1]
{\ifx\TeX\HyTeX\else\if@inmain
  \textsuperscript{[}%
  \@tempswatrue
  \let\@citea\@empty
  \let\@citeb\@empty
  \let\@citeu\@empty
  \@for\@citei:=#1\do
  {%
    \if@filesw\immediate\write\@auxout{\string\citation{\@citei}}\fi
    \@ifundefined{b@\@citei}{%
      \G@refundefinedtrue
      \edef\@citeu{?\@citeu}%
      \@latex@warning{Citation "\@citei" on page \thepage \space undefined}%
     }{%
       \if@tempswa\@tempswafalse
         \edef\@citea{\@nameuse{bti@\@citei}}%
       \else
         \edef\@citeb{\@citeb ,\@nameuse{bti@\@citei}}%
       \fi
     }%
  }%
  \ifx\@citea\@empty
    \textsuperscript{\@citeu}%
  \else\ifx\@citeb\@empty
    \textsuperscript{\@nameuse{itb@\@citea}}%
    \ifx\@citeu\@empty\else
      \textsuperscript{,\@citeu}%
    \fi
  \else
    \let\@cite@str\@empty
    \edef\@citeb{\expandafter\@gobble\@citeb}%
    \@cite@sort
    \edef\@citea{\expandafter\@gobble\@cite@str}%
    \@cite@mark
    \ifx\@citeu\@empty\else
      \textsuperscript{,\@citeu}%
    \fi
  \fi\fi
  \textsuperscript{]}%
\fi\fi}
\def\@cite@sort
{%
  \@tempswatrue
  \let\@citebb\@empty
  \@for\@citei:=\@citeb\do
  {%
    \ifnum \@citea >\@citei\relax
      \if@tempswa\@tempswafalse
        \let\@citeaa\@citea
      \else
        \edef\@citebb{\@citebb ,\@citea}%
      \fi
      \let\@citea\@citei
    \else
      \if@tempswa\@tempswafalse
        \let\@citeaa\@citei
      \else
        \edef\@citebb{\@citebb ,\@citei}%
      \fi
    \fi
  }%
  \ifx\@citebb\@empty
    \edef\@cite@str{\@cite@str ,\@citea ,\@citeaa}%
  \else
    \edef\@cite@str{\@cite@str ,\@citea}%
    \edef\@citea{\@citeaa}%
    \edef\@citeb{\expandafter\@gobble\@citebb}%
    \@cite@sort
  \fi
}
\def\@cite@mark
{%
  \@tempswatrue
  \@for\@citei:=\@citea\do
  {%
    \if@tempswa\@tempswafalse
      \textsuperscript{\@nameuse{itb@\@citei}}%
      \let\@citeb\relax
      \@tempcnta\@citei
      \advance\@tempcnta\@ne
      \@tempcntb\z@
    \else\ifnum\@tempcnta =\@citei
      \advance\@tempcnta\@ne
      \advance\@tempcntb\@ne
      \let\@citeb\@citei
      \ifnum\@tempcntb >\@ne
        \def\@cite@str{-}%
      \else
        \def\@cite@str{,}%
      \fi
    \else
      \ifx\relax\@citeb\else
        \textsuperscript{\@cite@str\@nameuse{itb@\@citeb}}%
        \let\@citeb\relax
      \fi
      \textsuperscript{,\@nameuse{itb@\@citei}}%
      \@tempcnta\@citei
      \advance\@tempcnta\@ne
      \@tempcntb\z@
    \fi\fi
  }%
  \ifx\relax\@citeb\else
    \textsuperscript{\@cite@str\@nameuse{itb@\@citeb}}%
  \fi
}
\let\bibcite@\bibcite
\def\bibcite#1#2{%
    \global\@namedef{bti@#1}{#2}%
    \global\@namedef{itb@#2}{\@nameuse{b@#1}}%
    \bibcite@{#1}{#2}}
\DeclareRobustCommand\chapter[2][]
{%
  \clearpage\vskip\xxivptlen
  \refstepcounter{chapter}%
  \begin{center}\fontsize{16pt}{22pt}\bfseries
    \thechapter\hspace{1ex}#2%
  \end{center}%
  \addcontentsline{toc}{chapter}{\protect\numberline{\thechapter}#2}%
  \IfBlankF{#1}{\label{txt:#1}}%
  \vskip\xviiiptlen\par
}
\DeclareRobustCommand\section[2][]
{%
  \removelastskip\vskip\xxivptlen
  \noindent
  \refstepcounter{section}%
  \begingroup\fontsize\@xivpt{20pt}\bfseries
    \thesection\hspace{1ex}#2\nopagebreak
  \endgroup
  \addcontentsline{toc}{section}{\protect\numberline{\thesection}#2}%
  \IfBlankF{#1}{\label{txt:#1}}%
  \vskip\viptlen\par
}
\DeclareRobustCommand\subsection[2][]
{%
  \removelastskip\vskip\xiiptlen
  \noindent
  \refstepcounter{subsection}%
  \begingroup\fontsize{13pt}{20pt}\bfseries
    \thesubsection\hspace{1ex}#2\nopagebreak
  \endgroup
  \addcontentsline{toc}{subsection}{\protect\numberline{\thesubsection}#2}%
  \IfBlankF{#1}{\label{txt:#1}}%
  \vskip\viptlen\par
}
\DeclareRobustCommand\subsubsection[2][]
{%
  \removelastskip\vskip\xiiptlen
  \noindent
  \refstepcounter{subsubsection}%
  \textbf{\thesubsubsection\hspace{1ex}#2}\nopagebreak
  \IfBlankF{#1}{\label{txt:#1}}%
  \vskip\viptlen\par
}
\newcommand\footnotesize{\@setfontsize\footnotesize\@ixpt{11pt}}
\newcommand\@makefntext[1]{%
  \hangindent 1.5em\noindent
  \hb@xt@1.5em{\hss\@thefnmark\ }#1}
\renewcommand\thefootnote{%
  \begingroup
  \setmainfont{SimSun}%
  \ifcase\number\value{footnote}%
    \or ①\or ②\or ③\or ④\or ⑤\or ⑥\or ⑦\or ⑧\or ⑨\or ⑩\else\relax\fi
  \endgroup}
\newcommand*\l@chapter[2]
{
  \begingroup\bfseries\setlength\@tempdima{4em}\noindent
    #1
    \leaders\hbox{$\m@th\mkern3mu.\mkern3mu$}\hfill
    #2
  \endgroup\par
}
\newcommand*\l@section[2]
{
  \setlength\@tempdima{4ex}\hskip -1.5ex
  #1
  \leaders\hbox{$\m@th\mkern3mu.\mkern3mu$}\hfill
  #2 \par
}
\newcommand*\l@subsection[2]
{
  \setlength\@tempdima{6ex}
  #1
  \leaders\hbox{$\m@th\mkern3mu.\mkern3mu$}\hfill
  #2 \par
}
\newcommand*\l@figure[2]
{
  \setlength\@tempdima{7ex}
  #1
  \leaders\hbox{$\m@th\mkern3mu.\mkern3mu$}\hfill
  #2 \par
}
\let\l@table\l@figure
\def\@ChnNum#1#2{%
  \ifcase #1 〇\or 一\or 二\or 三\or 四\or 五\or 六\or 七\or 八\or 九\fi
  \ifx #2\relax\let\@@ChnNum\relax\else\let\@@ChnNum\@ChnNum\fi
  \@@ChnNum #2}
\DeclareRobustCommand\ChineseNumber[1]{\expandafter\@ChnNum #1\relax}
\newcommand\labelitemi{●}
\newcommand\labelitemii{■}
\newcommand\labelitemiii{◆}
\newcommand\labelenumi{\the\c@enumi}
\newcommand\labelenumii{\@roman\c@enumii}
\newcommand\labelenumiii{\@alph\c@enumiii}
\labelsep 1.5ex
\def\@listi{%
  \labelwidth 2.0ex
  \leftmargin 3.0ex}
\def\@listii{%
  \labelwidth 2.0ex
  \leftmargin 3.0ex}
\def\@listiii{%
  \labelwidth 2.0ex
  \leftmargin 3.0ex}
\def\ftype@figure{1}
\DeclareRobustCommand\InsertFigure[4][]
{%
  \@xfloat{figure}[!htb]\vskip\bef@float
  \begin{center}\fontsize\@xpt{12pt}\selectfont
  \IfBlankTF{#2}{\includegraphics{#4}}{\resizebox{#2}{!}{\includegraphics{#4}}}%
  \vskip\iiiptlen
  \IfBlankTF{#1}{#3}{%
    \refstepcounter{figure}%
    \thefigure\hskip 1ex #3\label{fig:#1}%
    \addcontentsline{lof}{figure}{\protect\numberline{\thefigure}#3}\lof@claim}%
  \end{center}\vskip\iiiptlen\vskip\aft@float
  \end@float
}
\newenvironment{multifigures}{%
  \@xfloat{figure}[!htb]\vskip\bef@float
  \begin{center}\fontsize\@xpt{12pt}\selectfont
}{
  \end{center}\vskip\aft@float
  \end@float}
\DeclareRobustCommand\MultiFigure[5][]
{%
  \begin{minipage}[b]{#3}\centering
    \IfBlankTF{#2}{\includegraphics{#5}}{\resizebox{#2}{!}{\includegraphics{#5}}}%
    \vskip\iiiptlen
    \IfBlankTF{#1}{#4}{%
      \refstepcounter{figure}%
      \thefigure\hskip 1ex #4\label{fig:#1}%
      \addcontentsline{lof}{figure}{\protect\numberline{\thefigure}#4}\lof@claim}\vskip\iiiptlen
  \end{minipage}%
}
\newif\if@subfig
\newenvironment{subfigures}[2][]
{%
  \@xfloat{figure}[!htb]\vskip\bef@float
  \begin{center}\fontsize\@xpt{12pt}\selectfont
  \def\subfig@title{#2}
  \IfBlankTF{#1}{%
    \@subfigfalse
  }{%
    \@subfigtrue
    \refstepcounter{figure}\label{fig:#1}%
    \edef\the@subfig{\thefigure}}%
}{%
  \par
  \if@subfig
    \the@subfig\hskip 1ex\subfig@title
    \addcontentsline{lof}{figure}{\protect\numberline{\the@subfig}\subfig@title}\lof@claim
  \else\subfig@title\fi
  \end{center}\vskip\iiiptlen\vskip\aft@float
  \end@float
}
\DeclareRobustCommand\SubFigure[5][]
{
  \begin{minipage}[b]{#3}\centering
    \IfBlankTF{#2}{\includegraphics{#5}}{\resizebox{#2}{!}{\includegraphics{#5}}}\par
    \vskip\iiiptlen
    \@tempswafalse
    \IfBlankF{#1}{\@tempswatrue(\refstepcounter{subfigure}\alph{subfigure})\label{fig:#1}}%
    \IfBlankF{#4}{\if@tempswa\hskip 1ex\fi #4}%
    \vskip\iiiptlen
  \end{minipage}%
}
\renewcommand\arraystretch{1.5}
\setlength\tabcolsep{6\p@}
\arrayrulewidth=1.0pt
\def\whline{\noalign{\ifnum0=`}\fi\hrule\@height1.5pt\futurelet\reserved@a\@xhline}
\def\ftype@table{2}
\newenvironment{table}[4][]
{%
  \@xfloat{table}[!htb]\begin{center}%
  \fontsize\@xpt{12pt}\selectfont
  \vskip\bef@float\vskip\iiiptlen
  \IfBlankTF{#1}{#2}{%
    \refstepcounter{table}
    \thetable\hskip 1ex #2\label{tab:#1}%
    \addcontentsline{lot}{table}{\protect\numberline{\thetable}#2}\lot@claim}\vskip\iiiptlen
  \parskip\iiiptlen
  \par
  \begin{tabular}{#3}%
  \whline
  #4\\
  \hline
}{
  \whline
  \end{tabular}\end{center}\vskip\aft@float
  \end@float
}
\renewcommand\theequation{\the\c@chapter-\the\c@equation}
\DeclareRobustCommand\eqref[1]{式(\ref{#1})}
\DeclareRobustCommand\StartAppendix{%
  \newcounter{append}%
  \let\chapter@old\chapter
  \def\chapter{\refstepcounter{append}\chapter@old}%
  \renewcommand\thechapter{附录\Alph{append}}%
  \renewcommand\thesection{\Alph{append}.\the\c@section}%
  \renewcommand\theequation{\Alph{append}-\the\c@equation}%
  \renewcommand\thefigure {图\Alph{append}.\the\c@figure}%
  \renewcommand\thetable {表\Alph{append}.\the\c@table}%
}
\newcounter{rflstnum}%
\newenvironment{reflist}{%
  \fontsize\@xpt{16pt}\selectfont
  \parskip\iiiptlen
  \list{[\the\c@rflstnum]}{%
    \labelwidth 5.0ex
    \leftmargin 5.5ex
    \usecounter{rflstnum}}%
}{\endlist}
