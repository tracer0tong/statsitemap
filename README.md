This is a simple library for building a graph (NetworkX DiGraph) for website.

I'd prefer to use NetworkX as graph library just because it's lightweight and simple.

Base functions in simplestatsitemap are defined for building are graph with special nodes and edges. It'll try to reduce graph with some algorithm which can merge similar graph nodes.

Nodes - Referer and URI. Edges weight - average call rate for this path. 
For example if some user moves from external page to your site and then moved internaly to another page of your site:
http://external.com -> http://site.com/page1 -> http://site.com/page2

You can build a tree just with three nodes with such code:

sitemap = SimpleSiteMap("http://site.com")
sitemap.add_node("http://site.com/page1","http://external.com")
sitemap.add_node("http://site.com/page2","http://site.com/page1")
