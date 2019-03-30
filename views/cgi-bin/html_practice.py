import cgi, cgitb

form = cgi.FieldStorage()

name = form.getvalue('name')
comment = form.getvalue('textcontent')

print ("Content-type:text/html; charset=utf-8\n\n")
print ("<html>")
print ("<head>")
print ("<title>Text Area - Fifth CGI Program</title>")
print ("</head>")
print ("<body>")
print ("<h2> Entered Text Content is %s</h2>" % comment)
print ("</body>")