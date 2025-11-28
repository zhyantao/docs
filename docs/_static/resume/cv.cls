%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Medium Length Professional CV - RESUME CLASS FILE
%
% This template has been downloaded from:
% http://www.LaTeXTemplates.com
%
% This class file defines the structure and design of the template. 
%
% Original header:
% Copyright (C) 2010 by Trey Hunner
%
% Copying and distribution of this file, with or without modification,
% are permitted in any medium without royalty provided the copyright
% notice and this notice are preserved. This file is offered as-is,
% without any warranty.
%
% Created by Trey Hunner and modified by www.LaTeXTemplates.com
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\ProvidesClass{cv}[2010/07/10 v0.9 Resume class]

\LoadClass[11pt,letterpaper]{article} % Font size and paper type

\usepackage[parfill]{parskip} % Remove paragraph indentation
\usepackage{array} % Required for boldface (\bf and \bfseries) tabular columns
\usepackage{ifthen} % Required for ifthenelse statements
\usepackage[pdfborder={0 0 0}]{hyperref} % Required for hyperlink without borders
\usepackage{xeCJK} % Required for Chinese characters

\pagestyle{empty} % Suppress page numbers

%----------------------------------------------------------------------------------------
%	HEADINGS COMMANDS: Commands for printing name and address
%----------------------------------------------------------------------------------------

\def \name#1{\def\@name{#1}} % Defines the \name command to set name
\def \@name {} % Sets \@name to empty by default

\def \addressSep {$\diamond$} % Set default address separator to a diamond

% One, two, three or four address lines can be specified 
\let \@addressone \relax
\let \@addresstwo \relax
\let \@addressthree \relax
\let \@addressfour \relax  % 新增第四行地址变量

% \address command can be used to set the first, second, third and fourth address (last 3 optional)
\def \address #1{
    \@ifundefined{@addressone}{
        \def \@addressone {#1}
    }{
        \@ifundefined{@addresstwo}{
            \def \@addresstwo {#1}
        }{
            \@ifundefined{@addressthree}{
                \def \@addressthree {#1}
            }{
                \@ifundefined{@addressfour}{
                    \def \@addressfour {#1}  % 设置第四行地址
                }{
                    % 如果已经有四行地址，这里可以处理溢出情况
                    % 目前简单地忽略后续地址
                }
            }
        }
    }
}

% \printaddress is used to style an address line (given as input)
\def \printaddress #1{
\begingroup
\def \\ {\addressSep\ }
\centerline{#1}
\endgroup
\par
\addressskip
}

% \printname is used to print the name as a page header - 优化布局
\def \printname {
    \begingroup
    \begin{minipage}{0.3\textwidth} % 左侧信息区域占30%
        \centering
        \vspace{0.5em}
        {\MakeUppercase{\namesize\bf \@name}}
    \end{minipage}%
    \hfill % 填充空间
    \begin{minipage}{0.6\textwidth} % 右侧信息区域占70%
        % 将地址分成两栏显示
        \begin{minipage}[t]{0.48\textwidth} % 左栏地址
            \raggedright % 左对齐
            \@ifundefined{@addressone}{}{\@addressone\par}
            \@ifundefined{@addresstwo}{}{\@addresstwo\par}
        \end{minipage}%
        % \hfill % 两栏之间的间隔
        \begin{minipage}[t]{0.48\textwidth} % 右栏地址  
            \raggedright % 左对齐
            \@ifundefined{@addressthree}{}{\@addressthree\par}
            \@ifundefined{@addressfour}{}{\@addressfour\par}
        \end{minipage}
    \end{minipage}
    \nameskip\break
    \endgroup
}

%----------------------------------------------------------------------------------------
%	PRINT THE HEADING LINES
%----------------------------------------------------------------------------------------

\let\ori@document=\document
\renewcommand{\document}{
    \ori@document  % Begin document
    \printname % Print the name and addresses in new layout
}

%----------------------------------------------------------------------------------------
%	SECTION FORMATTING
%----------------------------------------------------------------------------------------

% Defines the rSection environment for the large sections within the CV
\newenvironment{rSection}[1]{ % 1 input argument - section name
    \sectionskip
    \MakeUppercase{\bf #1} % Section title
    \sectionlineskip
    \hrule % Horizontal line
    \begin{list}{}{ % List for each individual item in the section
            \setlength{\leftmargin}{1.5em} % Margin within the section
        }
        \item[]
              }{
    \end{list}
}

%----------------------------------------------------------------------------------------
%	WORK EXPERIENCE FORMATTING
%----------------------------------------------------------------------------------------

\newenvironment{rSubsection}[4]{ % 4 input arguments - company name, year(s) employed, job title and location
{\bf #1} \hfill {#2} % Bold company name and date on the right
\ifthenelse{\equal{#3}{}}{}{ % If the third argument is not specified, don't print the job title and location line
\\
{\em #3} \hfill {\em #4} % Italic job title and location
}\smallskip
\begin{list}{$\cdot$}{\leftmargin=0em} % \cdot used for bullets, no indentation
    \itemsep -0.5em \vspace{-0.5em} % Compress items in list together for aesthetics
    }{
\end{list}
\vspace{0.5em} % Some space after the list of bullet points
}

% The below commands define the whitespace after certain things in the document - they can be \smallskip, \medskip or \bigskip
\def\namesize{\huge} % Size of the name at the top of the document
\def\addressskip{\smallskip} % The space between the two address (or phone/email) lines
\def\sectionlineskip{\medskip} % The space above the horizontal line for each section 
\def\nameskip{\bigskip} % The space after your name at the top
\def\sectionskip{\medskip} % The space after the heading section
