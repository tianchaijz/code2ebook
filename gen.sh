#!/bin/sh

title=$1
pdf_file=$2

gen_ebook() {
    title=$1
    src2html.pl --tab-width 4 --color --cross-reference \
        --navigator --line-numbers . $title
}

ebook2pdf() {
    html=$1
    pdf=$2
    ebook-convert $html $pdf \
        --override-profile-size \
        --paper-size a3 \
        --pdf-default-font-size 12 \
        --pdf-mono-font-size 12 \
        --margin-left 10 --margin-right 10 \
        --margin-top 10 --margin-bottom 10 \
        --page-breaks-before='/' \
        --authors='tianchaijz'
}


gen_ebook $title

ebook2pdf html_out/index.html $pdf_file

cp $pdf_file ~/tmp/ebook/
