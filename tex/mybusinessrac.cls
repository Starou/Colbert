\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{sdevrac}[2012/06/01 MyBusiness Monthly Activity Report]

\RequirePackage{fontspec}
%%\RequirePackage[showboxes,absolute]{textpos}
\RequirePackage[absolute]{textpos}

\DeclareOption{twocolumn}{\OptionNotUsed}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax
\LoadClass[a4paper,onecolumn]{article}

%%\RequirePackage[a4paper, showframe]{geometry}

\RequirePackage{calc}
\setlength\textwidth{7in}
\setlength\textheight{10in}
\setlength\oddsidemargin{(\paperwidth-\textwidth)/2 - 1in}
\setlength\topmargin{(\paperheight-\textheight
                      -\headheight-\headsep-\footskip)/2 - 1in}


\renewcommand{\maketitle}{%
    \begin{center}%
        {\LARGE \@title \par}%
    \end{center}%
}

\newcommand{\reffacture}[1]{\def\@reffacture{\texttt{#1}}}
\newcommand{\nbjours}[1]{\def\@nbjours{\texttt{#1}}}
\newcommand{\lieu}[1]{\def\@lieu{\texttt{#1}}}
%%\newcommand{\date}[1]{\def\@date{\texttt{#1}}}

% Initialisation %

\reffacture{}
\nbjours{}

%%

\newcommand{\makerefs}{%
    \vskip 4.5em%
    Référence facture : \@reffacture \\
    Nombre de jours : \@nbjours \\
    \vskip 2.5em%
}

\newcommand{\makesignature}{%
    \begin{textblock*}{10cm}(10cm,26cm)%
        \begin{center}
        \@author
        \end{center}
    \end{textblock*}%
}

%%


\AtBeginDocument{%
    \begin{textblock*}{210mm}(0mm,1.5mm)%
        \begin{center}
            \fontsize{36pt}{30pt}{MyBusiness}%
        \end{center}
    \end{textblock*}%
}
