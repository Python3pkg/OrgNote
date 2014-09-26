#!/usr/bin/env python
#-*- coding: utf-8 -*-

# OrgNote  ---- A simple org-mode blog, powered by python
# 
# orgnote.py ---- write blog by org-mode note
# 
# author: Leslie Zhu
# email: pythonisland@gmail.com
#
# Write note by Emacs with org-mode, and convert .org file itno .html file
# thus use orgnote.py convert into new html with speciall css
# 

import re,time


# #########################################################
# Setting of Blog(You shoud update it!)
# #########################################################

# the blog list which list the html path and display title
# it must be a list()
__dirs__ = ["./public/index.org"]
__title__ = "My Blog"
__author__ = "My Name"
__description__ = "My information"
__blog_keywords__ = "My Blog keywords"


# ####################
# init
# ####################
__site_name__ = __title__
__notes__ = list()
__localnotes__ = list()
__archives__ = list()

__menus__ = [
    ["/public/minyi.html","归档","fa fa-sitemap","MinYi"],
    ["/public/archive.html","归档","fa fa-archive","归档"],
    ["/public/about.html","关于","fa fa-user","关于"],
]

__menus_map__ = {
    "MinYi":"minyi",
    "归档": "archive",
    "关于": "about"
    }

__minyi__ = [
    ["/public/tags/nopublic.html","fa fa-link","暂不公开"]
]

__keywords__ = list()
__tags__ = dict()
__page_tags__ = dict()





# ##############
# Parse html
# ##############

def gen_notes(dirs=list()):
    """
    gen each note from blog list
    """
    import os
    global __notes__,__localnotes__
    for notedir in dirs:
        dirname = os.path.dirname(notedir)
        for line in open(notedir):
            public = False
            local  = False
            if "- [[" in line: public = True
            if "+ [[" in line: local  = True
            
            if public or local:
                line = line.replace("]","")
                line = line.split('[')[2:]

                if line[0][0] == ".":
                    link = dirname + "/" + line[0]
                else:
                    link = line[0]

                name = line[1]
            
                if public:
                    __notes__ += [[link,name]]
                if local:
                    __localnotes__ += [[link,name]]


def header_prefix(deep=1,title=__title__):
    """
    gen the header of each html
    """
    
    if deep == 1:
        path = "."
    elif deep == 2:
        path = ".."

    return """
    <!DOCTYPE HTML>
    <html>
    <head>
    <meta charset="utf-8">

    <title>%s</title>
    <meta name="author" content="%s">
    <meta name="description" content="%s">
    <meta property="og:site_name" content="%s"/>
    <meta name="Keywords" content="%s">

    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
    <meta property="og:image" content="undefined"/>
    <link href="/favicon.ico" rel="icon">

    
    <link rel="stylesheet" href="/css/bootstrap.min.css" media="screen" type="text/css">
    <link rel="stylesheet" href="/css/font-awesome.css" media="screen" type="text/css">
    <link rel="stylesheet" href="/css/style.css" media="screen" type="text/css">
    <link rel="stylesheet" href="/css/highlight.css" media="screen" type="text/css">
    </head>
    """ % (title, __author__, __description__, __site_name__,__blog_keywords__)

def body_prefix():
    return """
    <body>  
    <nav id="main-nav" class="navbar navbar-inverse navbar-fixed-top" role="navigation">

    <div class="container">

    <button type="button" class="navbar-header navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
    <span class="sr-only">Toggle navigation</span>
    <span class="icon-bar"></span>
    <span class="icon-bar"></span>
    <span class="icon-bar"></span>
    </button>

    <a class="navbar-brand" href="/index.html">%s</a>
    """ % __title__

def gen_href(line=list()):
    if len(line) == 4:          # menu
        if "rss" in line[0]:
            return "<li><a href=\"%s\" title=\"%s\" target=\"_blank\"><i class=\"%s\"></i>%s</a></li>" % (line[0],line[1],line[2],line[3])
        else:
            return "<li><a href=\"%s\" title=\"%s\"><i class=\"%s\"></i>%s</a></li>" % (line[0],line[1],line[2],line[3])
    elif len(line) == 3:        # archive
        return "<li><a href=\"%s\" target=\"_blank\"><i class=\"%s\"></i>%s</a></li>" % (line[0],line[1],line[2])
    else:
        return ""

def gen_tag_href(name=""):    
    if name not in ["MinYi","归档","关于"]:
        return "<a href=\"/public/tags/%s.html\"><i class=\"%s\"></i>%s</a>" % (name,name,name)
    else:
        return "<a href=\"/%s.html\"><i class=\"%s\"></i>%s</a>" % (__menus_map__[name],name,name)

def body_menu(menus=list()):
    """
    each menu's layout: link,title,fa-name,name
    """

    output = ""

    output += """
    <div class="collapse navbar-collapse nav-menu">

    <ul class="nav navbar-nav">
    """
    
    for menu in menus:
        output += gen_href(menu)

    output +="""
    </ul>

    </div> <!-- navbar -->
    </div> <!-- container -->
    </nav>
    """

    return output

def contain_prefix(tags=[],name=""):
    output =  """
    <div class="clearfix"></div>
    <div class="container">
    <div class="content">

    <div class="page-header">
    <h1>My Blot Title</h1>
    </div>

    <div class="row page">
    <div class="col-md-9">
    <div class="mypage">

    <div class="slogan">
    <i class="fa fa-heart"></i>
    """

    if not tags:
        output += "主页君: " + __author__
    elif len(tags) == 1:
        output += name
        output += gen_tag_href(tags[0])
    else:
        output += name
        for tag in tags:
            output += gen_tag_href(tag)
            if tag != tags[-1]: output += " , "

            
    output += """
    </div>  
    """

    return output

def gen_date(link=""):
    """ Filter Publish data from HTML metadata>"""

    for line in open(link).readlines():
        if "<meta name=\"generated\"" in line:
            line = line.strip()
            pattern="([0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9]|[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9])"
            pubdate=re.search(pattern,line).groups(1)[0]
            break
    if "/" in pubdate:
        pubdate=time.strptime(pubdate, "%m/%d/%Y")
    elif "-" in pubdate:
        pubdate=time.strptime(pubdate, "%Y-%m-%d")
    else:
        pubdate=re.search("([0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9])",link).groups(1)[0]
        pubdate=time.strptime(pubdate, "%Y-%m-%d")

    pubdate=time.strftime("%Y-%m-%d %a",pubdate)
    return pubdate

def gen_title(link=""):
    """ Filter Title from HTML metadata """


    for line in open(link).readlines():
        if "<title>" in line:
            line = line.strip()
            title=re.match("<title>(.*)</title>",line).groups(1)[0]
            break
    return title

def gen_category(link=""):
    """ Filter Keywords from HTML metadata """
    
    keywords = ""
    for line in open(link).readlines():
        if "<meta name=\"keywords\"" in line:
            line = line.strip()
            keywords=re.search("content=\"(.*)\"",line).groups(1)[0].strip()
            break

    if len(keywords) > 0:
        return [i.strip() for i in keywords.split(",")]
    else:
        return ["札记"]

def contain_notes(data=list()):
    # each note

    output = ""

    for item in data:
        output += """
        <h3 class="title">
        <a href="%s">%s</a>
        <span class="date">%s </span>
        </h3>
        """ % (gen_public_link(item[0],"/public/"),item[1],gen_date(item[0]))

        
        output += """
        <div class="entry">
        <div class="row">
        <div class="col-md-12">
        """

        
        output += contain_note(item[0])

        sub_title = sub_title = "<h1 class=\"title\">%s</h1>" % gen_title(item[0])
        output = output.replace(sub_title,"")
        
        output += """
        </div> <!-- entry -->
        """
        

    output += """
    </div> <!-- mypage -->
    </div> <!-- col-md-9 -->
    """ 

    return output

def gen_prev(num=0):
    if num == 0:
        return ""
    else:
        return gen_public_link(__notes__[num-1][0],"/public/")

def gen_next(num=0):
    if num == len(__notes__) - 1:
        return ""
    else:
        return gen_public_link(__notes__[num+1][0],"/public/")

def gen_tag_list(public=True):
    if not public: return
    for num,link in enumerate(__notes__):
        keywords = gen_category(link[0])

        __page_tags__[link[0]] = keywords

        for key in keywords:
            if key not in __keywords__:
                __keywords__.append(key)
            if not __tags__.has_key(key):
                __tags__[key] = list()
            else: pass

            __tags__[key].append([link[0], link[1].strip()])

def contain_page(link="",num=0, public=True):
    global __archives__

    output = ""
    
    data = open(link).read()
    data = re.search("(<div id=\"content\">.*</div.).*</body>",data.replace('\n','TMD')) 
    data = data.groups()[0].replace('TMD','\n')

    if public:
        __archives__.append([gen_public_link(__notes__[num][0],"/public/"),"fa fa-file-o",__notes__[num][1].strip()])
            
        if num == 0:
            prev_page = '<li class="prev disabled"><a><i class="fa fa-arrow-circle-o-left"></i>上一页</a></li>'
        else:
            prev_page = '<li class="prev"><a href="%s" class=alignright prev"><i class="fa fa-arrow-circle-o-left"></i>上一页</a></li>' % gen_prev(num)

        if num == len(__notes__) - 1:
            next_page = '<li class="next disabled"><a><i class="fa fa-arrow-circle-o-right"></i>下一页</a></li>' 
        else:
            next_page = '<li class="next"><a href="%s" class="alignright next">下一页<i class="fa fa-arrow-circle-o-right"></i></a></li>' % gen_next(num)

        page_order = """
    <div>
    <center>
    <div class="pagination">
    <ul class="pagination">
    %s
    <li><a href="/public/archive.html" target="_blank"><i class="fa fa-archive"></i>Archive</a></li>
    %s
    </ul>
    </div>
    </center>
    </div>
    """ % (prev_page,next_page)
    else:
        page_order = ""

    
    if "<div class=\"ds-thread\">" in data:
        index = data.find("<div class=\"ds-thread\">")
        data = data[:index] + page_order + data[index:]
    elif "<div id=\"postamble\">" in data:
        index = data.find("<div id=\"postamble\">")
        data = data[:index] + page_order + duosuo() + data[index:]
    else:
        print "ignore prev"


    output += data
    output += "</div> <!-- col-md-12 -->"
    output += "</div> <!-- row -->"

    return output
    
def contain_note(link=""):
    import re
    
    output = ""
    
    alldata = open(link).read()
       
    data=re.search("(<div id=\"content\">.*<div id=\"outline-container-1\" class=\"outline-2\">).*</body>",alldata.replace('\n','TMD'))
    data2=re.search("(<div id=\"content\">.*<div class=\"ds-thread\"></div>).*</body>",alldata.replace('\n','TMD'))
    data3=re.search("(<div id=\"content\">.*<div id=\"postamble\">).*</body>",alldata.replace('\n','TMD'))
    
    if data:
        data = data.groups()[0].replace('TMD','\n')
        data = data.replace("<div id=\"outline-container-1\" class=\"outline-2\">","</div>")
        data = data.replace("#sec",gen_public_link(link,"/public/") + "#sec")
        output += data
    else:
        if data2:
            data = data2
        elif data3:
            data = data3

        data = data.groups()[0].replace('TMD','\n')
        data = data.replace('TMD','\n')
        data = data.split('</p>')[:5]
        output += '</p>'.join(data)
        output += "</div>"

        

    output +=  """
    <footer>
    <div class="alignleft">
    <a href="%s#more" class="more-link">阅读全文</a>
    </div>
    <div class="clearfix"></div>
    </footer>
    """ % gen_public_link(link,"/public/")

    output += "</div> <!-- col-md-12 -->"
    
    output += "</div> <!-- row -->"

    return output

def contain_archive(data=list()):
    
    output = ""


    output += """
    <!-- display as entry -->
    <div class="entry">
     <div class="row">
      <div class="col-md-12">
    """

    for archive in data:
        if len(archive) == 2:
            newarchive = ["/public/"+archive[0].split('/')[-1],'fa fa-file-o',archive[1]]
            output += gen_href(newarchive)
        else:
            output += gen_href(archive)

    output += """
    </div>
    </div>
    </div>
    """

    output += """
    </div> <!-- mypage -->
    </div> <!-- col-md-9 -->
    """

    return output
    
def contain_about():
    """about me page"""

    output = ""

    output += """
    <!-- display as entry -->
    <div class="entry">
     <div class="row">
      <div class="col-md-12">
    
    <p>这是一个建立在<code><a class="i i1 fc01 h" hidefocus="true" href="https://www.github.com/LeslieZhu/OrgNote" target="_blank">www.github.com</a></code>上的博客.</p>
    <p>网页使用 <code>Emacs</code>的<code>org-mode</code>生成HTML文件，然后<code><a class="i i1 fc01 h" hidefocus="true" href="https://github.com/LeslieZhu/OrgNote" target="_blank">OrgNote</a></code>根据<code>Hexo Freemind主题</code>转换成新的HTML文件。</p>
    </div>
    </div>
    </div>             
    """

    output += duosuo()

    output += """
    </div> <!-- mypage -->
    </div> <!-- col-md-9 -->
    """

    return output

def duosuo():
    return """
    """

def contain_sidebar():
    return """
    <div class="col-md-3">
    <div id="sidebar">
    """

def sidebar_tags():
    
    output = ""

    output += """
    <div class="widget">
    <h4>标签云</h4>
    <ul class="tag_box inline list-unstyled">
    """
    
    for key in __keywords__:
        output += "<li><a href=\"/public/tags/%s.html\">%s<span>%s</span></a></li>" % (key,key,len(__tags__[key]))

    output += """
    </ul>
    </div>
    """

    return output

def sidebar_latest(notes=list(), num=6):
    """
    each note layout: link,name
    """
    output = ""

    output += """
    <div class="widget">
    <h4>最新文章</h4>
    <ul class="entry list-unstyled">
    """

    for note in notes[:num]:
        output += "<li><a href=\"%s\"><i class=\"fa fa-file-o\"></i>%s</a></li>" % (gen_public_link(note[0].replace('"',""),"/public/"),note[1])

    output += """
    </ul>   
    </div> 
    """

    return output

def sidebar_weibo():
    return """
    """

def sidebar_link():
    return """
    <div class="widget">
    <h4>快速链接</h4>
    <ul class="entry list-unstyled">
    <li><a href="http://lesliezhu.github.com" title="LeslieZhu's Github" target="_blank"><i class="fa fa-github"></i>Leslie Zhu</a></li>
    </ul>
    </div>
    """

def contain_suffix():
    return """
    </div> <!-- sidebar -->
    </div> <!-- col-md-3 -->
    </div> <!-- row-fluid -->
    </div>
    </div>
    """

def header_suffix():
    return """
    <div class="container-narrow">
      <footer>
        <p>&copy; 2014 Leslie Zhu
        with help from <a href="http://zespia.tw/hexo/" target="_blank">Hexo</a> and <a href="http://getbootstrap.com/" target="_blank">Twitter Bootstrap</a>. Theme by <a href="http://github.com/wzpan/hexo-theme-freemind/">Freemind.</a>  Published with GitHub Pages. 
      </p> </footer>
    </div> <!-- container-narrow -->
    
    <a id="gotop" href="#">   
      <span>▲</span> 
    </a>

    <link rel="stylesheet" href="./fancybox/jquery.fancybox.css" media="screen" type="text/css">

  </body>
</html>
    """

def gen_public_link(link="",prefix="public/"):
    return prefix+link.split('/')[-1]

def gen_archive():
    output = open("./public/archive.html","w")
    print >> output,header_prefix(title="归档")
    print >> output,body_prefix()
    print >> output,body_menu(__menus__)
    print >> output,contain_prefix(["归档"],"")
    print >> output,contain_archive(__archives__)              # auto gen
    print >> output,contain_sidebar()
    print >> output,sidebar_latest(__notes__)            # auto gen
    print >> output,sidebar_tags()
    print >> output,sidebar_weibo()
    print >> output,sidebar_link()
    print >> output,contain_suffix()
    print >> output,header_suffix()
    output.close()
    
def gen_page(note=list(),num=0,public=True):
    output = open(gen_public_link(note[0]),"w")
    print >> output,header_prefix(2,note[1].strip())
    print >> output,body_prefix()
    print >> output,body_menu(__menus__)
    if public:
        print >> output,contain_prefix(__page_tags__[note[0]],"标签: ")
    else:
        print >> output,contain_prefix(['nopublic'],"标签: ")
    print >> output,contain_page(note[0],num,public)              # auto gen
    print >> output,contain_sidebar()
    print >> output,sidebar_latest(__notes__)            # auto gen
    print >> output,sidebar_tags()
    print >> output,sidebar_weibo()
    print >> output,sidebar_link()
    print >> output,contain_suffix()
    print >> output,header_suffix()
    output.close()
    
def gen_public():
    for i,note in enumerate(__notes__):
        gen_page(note,i)
    for i,note in enumerate(__localnotes__):
        gen_page(note,i,False)

def gen_index():
    output = open("index.html","w")
    print >> output,header_prefix(title="敏毅")
    print >> output,body_prefix()
    print >> output,body_menu(__menus__)
    print >> output,contain_prefix()
    print >> output,contain_notes(__notes__)              # auto gen
    print >> output,contain_sidebar()
    print >> output,sidebar_latest(__notes__)            # auto gen
    print >> output,sidebar_tags()
    print >> output,sidebar_weibo()
    print >> output,sidebar_link()
    print >> output,contain_suffix()
    print >> output,header_suffix()
    output.close()

def gen_about():
    output = open("./public/about.html","w")
    print >> output,header_prefix(title="关于")
    print >> output,body_prefix()
    print >> output,body_menu(__menus__)
    print >> output,contain_prefix(["关于"],"")
    print >> output,contain_about()
    print >> output,contain_sidebar()
    print >> output,sidebar_latest(__notes__)
    print >> output,sidebar_tags()
    print >> output,sidebar_weibo()
    print >> output,sidebar_link()
    print >> output,contain_suffix()
    print >> output,header_suffix()
    output.close()

def gen_minyi():
    output = open("./public/minyi.html","w")
    print >> output,header_prefix(title="MinYi")
    print >> output,body_prefix()
    print >> output,body_menu(__menus__)
    print >> output,contain_prefix(["MinYi"],"")
    print >> output,contain_archive(__minyi__)
    print >> output,contain_sidebar()
    print >> output,sidebar_latest(__notes__)
    print >> output,sidebar_tags()
    print >> output,sidebar_weibo()
    print >> output,sidebar_link()
    print >> output,contain_suffix()
    print >> output,header_suffix()
    output.close()

def gen_tags():
    for key in __keywords__:
        output = open("./public/tags/" + key + ".html","w")
        print >> output,header_prefix(title=key)
        print >> output,body_prefix()
        print >> output,body_menu(__menus__)
        print >> output,contain_prefix([key],"分类: ")
        #print >> output,contain_notes(__tags__[key])
        print >> output,contain_archive(__tags__[key])              # auto gen
        print >> output,contain_sidebar()
        print >> output,sidebar_latest(__notes__)
        print >> output,sidebar_tags()
        print >> output,sidebar_weibo()
        print >> output,sidebar_link()
        print >> output,contain_suffix()
        print >> output,header_suffix()
        output.close()

def gen_nopublic():
    output = open("./public/tags/nopublic.html","w")
    print >> output,header_prefix(title="nopublic")
    print >> output,body_prefix()
    print >> output,body_menu(__menus__)
    print >> output,contain_prefix(["nopublic"],"分类: ")
    print >> output,contain_archive(__localnotes__)              # auto gen
    print >> output,contain_suffix()
    print >> output,header_suffix()
    output.close()
    
    
def usage():
    import sys
    
    print """
    Usage:
          python orgnote.py               ---- update blog
          python orgnote server [port]    ---- start web server
    """
    sys.exit()
            


if __name__ == "__main__":
    import sys,os
    
    if len(sys.argv) == 1:
        gen_notes(__dirs__)
        gen_tag_list()
        gen_public()
        gen_index()
        gen_about()
        gen_minyi()
        gen_archive()
        gen_tags()
        gen_nopublic()
    elif len(sys.argv) == 2:
        if sys.argv[1] == "server":
            try:
                os.system("python -m SimpleHTTPServer")
            except Exception,ex:
                print str(ex)
                usage()
        else:
            usage()
    elif len(sys.argv) == 3 and sys.argv[1] == "server":
        try:
            os.system("python -m SimpleHTTPServer " + sys.argv[2])
        except Exception,ex:
            print str(ex)
            usage()
    else:
        usage()

        