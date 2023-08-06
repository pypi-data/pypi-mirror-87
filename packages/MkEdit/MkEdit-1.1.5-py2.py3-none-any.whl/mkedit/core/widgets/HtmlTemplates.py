#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


class HtmlTemplates:
    def __init__(self, baseDir):
        self.TEMPLATES_DIR = baseDir

    def _read_template(self, template_path):
        with open(os.path.join(self.TEMPLATES_DIR, template_path)) as template:
            result = template.read()
            return result

    def render(self, data):
        str = '''<!DOCTYPE html>
<html lang="zh-cn">
<head>
    <meta charset="UTF-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <meta content="IE=edge, chrome=1" http-equiv="X-UA-Compatible"/>
    <meta content="text/html;charset=utf-8" http-equiv="content-type"/>
    <link href="https://www.catbro.cn/css/matery.css" rel="stylesheet">
    <!--    <link href="https://cdn.bootcss.com/github-markdown-css/3.0.1/github-markdown.min.css" rel="stylesheet">-->
    <link rel="stylesheet"
          href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@9.16.2/build/styles/default.min.css">
    <script type="text/javascript"
            src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@9.16.2/build/highlight.min.js"></script>
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mermaid/8.4.4/mermaid.min.js"></script>
    <script type="text/javascript"
            src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML"></script>
    <script type="text/javascript">
        MathJax.Hub.Config({
            tex2jax: {
                inlineMath: [
                    ['$$$', '$$$'],
                    ['((', '))']
                ]
            }
        });
    </script>
    <style>

        /*

Original highlight.js style (c) Ivan Sagalaev <maniac@softwaremaniacs.org>

*/

        .hljs {
            display: block;
            overflow-x: auto;
            padding: 0.5em;
            background: #000000;
        }


        /* Base color: saturation 0; */

        .hljs,
        .hljs-subst {
            color: #444;
        }

        .hljs-comment {
            color: #888888;
        }

        .hljs-keyword,
        .hljs-attribute,
        .hljs-selector-tag,
        .hljs-meta-keyword,
        .hljs-doctag,
        .hljs-name {
            font-weight: bold;
        }


        /* User color: hue: 0 */

        .hljs-type,
        .hljs-string,
        .hljs-number,
        .hljs-selector-id,
        .hljs-selector-class,
        .hljs-quote,
        .hljs-template-tag,
        .hljs-deletion {
            color: #880000;
        }

        .hljs-title,
        .hljs-section {
            color: #880000;
            font-weight: bold;
        }

        .hljs-regexp,
        .hljs-symbol,
        .hljs-variable,
        .hljs-template-variable,
        .hljs-link,
        .hljs-selector-attr,
        .hljs-selector-pseudo {
            color: #BC6060;
        }


        /* Language color: hue: 90; */

        .hljs-literal {
            color: #78A960;
        }

        .hljs-built_in,
        .hljs-bullet,
        .hljs-code,
        .hljs-addition {
            color: #397300;
        }


        /* Meta color: hue: 200 */

        .hljs-meta {
            color: #1f7199;
        }

        .hljs-meta-string {
            color: #4d99bf;
        }


        /* Misc effects */

        .hljs-emphasis {
            font-style: italic;
        }

        .hljs-strong {
            font-weight: bold;
        }


        img {
            max-width: 100%;
        }

        body {
            font-family: Helvetica, arial, sans-serif;
            /*font-size: 14px !important;*/
            /*line-height: 1.6 !important;*/
            /*padding-top: 10px !important;*/
            /*padding-bottom: 10px !important;*/
            background-color: white !important;
            padding: 30px !important;
        }

        body > *:first-child {
            margin-top: 0 !important;
        }

        body > *:last-child {
            margin-bottom: 0 !important;
        }

        a {
            color: #4183C4;
        }

        a.absent {
            color: #cc0000;
        }

        a.anchor {
            display: block;
            padding-left: 30px;
            margin-left: -30px;
            cursor: pointer;
            position: absolute;
            top: 0;
            left: 0;
            bottom: 0;
        }

        h1, h2, h3, h4, h5, h6 {
            margin: 20px 0 10px;
            line-height: 1.9 !important;
            padding: 0;
            font-weight: bold;
            -webkit-font-smoothing: antialiased;
            cursor: text;
            position: relative;
        }

        h1:hover a.anchor, h2:hover a.anchor, h3:hover a.anchor, h4:hover a.anchor, h5:hover a.anchor, h6:hover a.anchor {
            background: url("../../images/modules/styleguide/para.png") no-repeat 10px center;
            text-decoration: none;
        }

        h1 tt, h1 code {
            font-size: inherit;
        }

        h2 tt, h2 code {
            font-size: inherit;
        }

        h3 tt, h3 code {
            font-size: inherit;
        }

        h4 tt, h4 code {
            font-size: inherit;
        }

        h5 tt, h5 code {
            font-size: inherit;
        }

        h6 tt, h6 code {
            font-size: inherit;
        }

        h1 {
            font-size: 28px !important;
            color: black;
        }

        h2 {
            font-size: 24px !important;
            border-bottom: 1px solid #cccccc;
            color: black;
        }

        h3 {
            font-size: 18px;
        }

        h4 {
            font-size: 16px;
        }

        h5 {
            font-size: 14px;
        }

        h6 {
            color: #777777;
            font-size: 14px;
        }

        p, blockquote, ul, ol, dl, li, table, pre {
            margin: 15px 0 !important;
        }

        hr {
            color: #cccccc;
            height: 4px;
            padding: 0;
        }

        body > h2:first-child {
            margin-top: 0;
            padding-top: 0;
        }

        body > h1:first-child {
            margin-top: 0;
            padding-top: 0;
        }

        body > h1:first-child + h2 {
            margin-top: 0;
            padding-top: 0;
        }

        body > h3:first-child, body > h4:first-child, body > h5:first-child, body > h6:first-child {
            margin-top: 0;
            padding-top: 0;
        }

        a:first-child h1, a:first-child h2, a:first-child h3, a:first-child h4, a:first-child h5, a:first-child h6 {
            margin-top: 0;
            padding-top: 0;
        }

        h1 p, h2 p, h3 p, h4 p, h5 p, h6 p {
            margin-top: 0;
        }

        li p.first {
            display: inline-block;
        }

        ul, ol {
            padding-left: 30px;
        }

        ul :first-child, ol :first-child {
            margin-top: 0;
        }

        ul :last-child, ol :last-child {
            margin-bottom: 0;
        }

        dl {
            padding: 0;
        }

        dl dt {
            font-size: 14px;
            font-weight: bold;
            font-style: italic;
            padding: 0;
            margin: 15px 0 5px;
        }

        dl dt:first-child {
            padding: 0;
        }

        dl dt > :first-child {
            margin-top: 0;
        }

        dl dt > :last-child {
            margin-bottom: 0;
        }

        dl dd {
            margin: 0 0 15px;
            padding: 0 15px;
        }

        dl dd > :first-child {
            margin-top: 0;
        }

        dl dd > :last-child {
            margin-bottom: 0;
        }

        blockquote {
            border-left: 4px solid #dddddd;
            padding: 0 15px;
            color: #777777;
        }

        blockquote > :first-child {
            margin-top: 0;
        }

        blockquote > :last-child {
            margin-bottom: 0;
        }

        table {
            padding: 0;
        }

        table tr {
            border-top: 1px solid #cccccc;
            background-color: white;
            margin: 0;
            padding: 0;
        }

        table tr:nth-child(2n) {
            background-color: #f8f8f8;
        }

        table tr th {
            font-weight: bold;
            border: 1px solid #cccccc;
            text-align: left;
            margin: 0;
            padding: 6px 13px;
        }

        table tr td {
            border: 1px solid #cccccc;
            text-align: left;
            margin: 0;
            padding: 6px 13px;
        }

        table tr th :first-child, table tr td :first-child {
            margin-top: 0;
        }

        table tr th :last-child, table tr td :last-child {
            margin-bottom: 0;
        }

        img {
            max-width: 100%;
        }

        span.frame {
            display: block;
            overflow: hidden;
        }

        span.frame > span {
            border: 1px solid #dddddd;
            display: block;
            float: left;
            overflow: hidden;
            margin: 13px 0 0;
            padding: 7px;
            width: auto;
        }

        span.frame span img {
            display: block;
            float: left;
        }

        span.frame span span {
            clear: both;
            color: #333333;
            display: block;
            padding: 5px 0 0;
        }

        span.align-center {
            display: block;
            overflow: hidden;
            clear: both;
        }

        span.align-center > span {
            display: block;
            overflow: hidden;
            margin: 13px auto 0;
            text-align: center;
        }

        span.align-center span img {
            margin: 0 auto;
            text-align: center;
        }

        span.align-right {
            display: block;
            overflow: hidden;
            clear: both;
        }

        span.align-right > span {
            display: block;
            overflow: hidden;
            margin: 13px 0 0;
            text-align: right;
        }

        span.align-right span img {
            margin: 0;
            text-align: right;
        }

        span.float-left {
            display: block;
            margin-right: 13px;
            overflow: hidden;
            float: left;
        }

        span.float-left span {
            margin: 13px 0 0;
        }

        span.float-right {
            display: block;
            margin-left: 13px;
            overflow: hidden;
            float: right;
        }

        span.float-right > span {
            display: block;
            overflow: hidden;
            margin: 13px auto 0;
            text-align: right;
        }

        code, tt {
            margin: 0 2px;
            padding: 0 5px;
            white-space: nowrap;
            border: 1px solid #eaeaea;
            background-color: #000000;
            border-radius: 3px;
        }

        pre code {
            margin: 0;
            padding: 0;
            white-space: pre;
            border: none;
            background: transparent;
        }

        .highlight pre {
            background-color: #f8f8f8;
            border: 1px solid #cccccc;
            font-size: 13px;
            line-height: 19px !important;
            overflow: auto;
            padding: 6px 10px;
            border-radius: 3px;
        }

        pre {
            background-color: #000000;
            border: 1px solid #cccccc;
            font-size: 13px;
            line-height: 19px !important;
            overflow: auto;
            padding: 6px 10px;
            border-radius: 3px;
        }

        pre code, pre tt {
            background-color: transparent;
            border: none;
        }
    </style>
</head>
<body id="preArea">
<div id="preMkContent">
'''+data+'''
</div>
<script>
    var config = {
        theme: 'default',
        logLevel: 'fatal',
        securityLevel: 'strict',
        startOnLoad: true,
        arrowMarkerAbsolute: false,

        flowchart: {
            htmlLabels: true,
            curve: 'linear',
        },
        sequence: {
            diagramMarginX: 50,
            diagramMarginY: 10,
            actorMargin: 50,
            width: 150,
            height: 65,
            boxMargin: 10,
            boxTextMargin: 5,
            noteMargin: 10,
            messageMargin: 35,
            mirrorActors: true,
            bottomMarginAdj: 1,
            useMaxWidth: true,
            rightAngles: false,
            showSequenceNumbers: false,
        },
        gantt: {
            titleTopMargin: 25,
            barHeight: 20,
            barGap: 4,
            topPadding: 50,
            leftPadding: 75,
            gridLineStartPadding: 35,
            fontSize: 11,
            fontFamily: '"Open-Sans", "sans-serif"',
            numberSectionStyles: 4,
            axisFormat: '%Y-%m-%d',
        }
    };
    mermaid.initialize(config);
    window.reloadMermaid = function reloadMermaid() {
        mermaid.init({
            noteMargin: 10
        }, ".mermaid");

    }

    // window.highlightBlock = function highlightBlock() {
    //      document.querySelectorAll('pre code').forEach((block) => {
    //         window.hljs.highlightBlock(block);
    //     });
    // }
    //
    // document.addEventListener('DOMContentLoaded', (event) => {
    //     window.highlightBlock()
// });
</script>
<!--<script>hljs.initHighlightingOnLoad();</script>-->


</body>
</html>
'''
        return str
