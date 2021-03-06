# -*- coding: utf-8 -*-

from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from utils import get_split, word_seg_for_search, word_seg_for_index

WIKI_INDEX_DIR = "index/wiki_index"

ix = None

def make_index(wiki_path):
	schema = Schema(url=ID(stored=True, unique=True), title=TEXT, title_show=STORED, content=TEXT, content_show=STORED)
	global ix
	global WIKI_INDEX_DIR

	ix = create_in(WIKI_INDEX_DIR, schema)
	writer = ix.writer()

	lines = []
	title = ""
	url = None
	lc = 0
	for line in open(wiki_path):
		if True:
			lc += 1
			if lc % 100 == 0:
				print lc
			line = line.strip()
			if len(line) == 0:
				continue
			if line.startswith("<doc url="):
				lines = []
				pos_l = line.find("\"") + 1
				pos_r = line.find("\"", pos_l)
				url = line[pos_l:pos_r]
			elif line.startswith("</doc>"):
				content = ""
				for l in lines:
					content += ' ' + word_seg_for_index(l)
				content = content.strip()
				content_show = '\n'.join(lines[1:])
				writer.add_document(url=url.decode('UTF-8'), title=word_seg_for_index(title).decode('UTF-8'), title_show=title.decode('UTF-8'), content=content.decode('UTF-8'), content_show=content_show.decode('UTF-8'))
				#break
			else:
				if len(line) == 0:
					continue
				if len(lines) == 0:
					title = line
				lines.append(line)
		#except:
		#	print line
		#	pass

	writer.commit()
	return

def search_index(queryLine, query_field, N):#unicode!!!
	global ix
	global WIKI_INDEX_DIR
	if not ix:
		ix = open_dir(WIKI_INDEX_DIR)
	rt = []
	with ix.searcher() as searcher:
		query = QueryParser(query_field, ix.schema).parse(queryLine)
		#print 21222
		results = searcher.search(query, limit=N)
		#print 233333
		for r in results:
			rt.append([r['url'], r['title_show'], r['content_show']])
			N -= 1
			#print N
			if N == 0:
				break
	return rt



if False:
	make_index('../data/mix_simplified.txt')

