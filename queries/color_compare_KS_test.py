import sqlite3
from scipy import stats
conn = sqlite3.connect('../color_analysis_merged.db')
c = conn.cursor()


### make end = None if no upper limit
##def count_color_appearance_in_sentence_lengths(res, color_list, start, end):
####    if end == None:
####        query = """SELECT color.name, color.id, color.base, count(*) FROM color, mention, sentence, clause, book WHERE mention.color=color.id AND mention.clause=clause.id AND clause.sentence=sentence.id AND sentence.book=book.id AND book.id and book.year >=""" + str(start) + """ GROUP BY color.name, color.id"""
####    else:
##    query = """SELECT color.name, color.base, count(*) FROM color, mention, sentence, clause, book WHERE mention.color=color.id AND mention.clause=clause.id AND clause.sentence=sentence.id AND sentence.book=book.id AND book.id and book.year >=""" + str(start) + """ AND book.year <""" + str(end) + """ GROUP BY color.name, color.base"""
##
##    c.execute(query)
##
##    for row in c.fetchall():
##        color_name = row[0]
####        color_id = row[1]
##        base = row[1]
##        count = row[2]
##
##        if color_name in color_list:
##            if color_name not in res:
##                res[color_name] = {
##                           '1800_1810':0,
##                           '1810_1820':0,
##                           '1820_1830':0,
##                           '1830_1840':0,
##                           '1850_1860':0,
##                           '1860_1870':0,
##                           '1870_1880':0,
##                           '1880_1890':0,
##                           '1890_1900':0
##                           }
##                        
##            res[color_name][str(start) + '_' + str(end)] = count
##
##            
### get list of valid base colors
##def parse_color_list():
##    res = []
##    with open('../query_results/colors_appearing_at_most10.txt', 'r') as f:
##        for row in f:
##            row = row.strip('\n')
##            res.append(row) 
##
##    f.close()
##    return res
##
##
### build and empty result dictionary
##color_list = parse_color_list();
##
##res = {}
##
### get counts
##count_color_appearance_in_sentence_lengths(res, color_list, 1800, 1810)
##count_color_appearance_in_sentence_lengths(res, color_list, 1810, 1820)
##count_color_appearance_in_sentence_lengths(res, color_list, 1830, 1840)
##count_color_appearance_in_sentence_lengths(res, color_list, 1840, 1850)
##count_color_appearance_in_sentence_lengths(res, color_list, 1850, 1860)
##count_color_appearance_in_sentence_lengths(res, color_list, 1860, 1870)
##count_color_appearance_in_sentence_lengths(res, color_list, 1870, 1880)
##count_color_appearance_in_sentence_lengths(res, color_list, 1880, 1890)
##count_color_appearance_in_sentence_lengths(res, color_list, 1890, 1900)
##
### write to file
##f = open('../query_results/color_count_per_decade.txt', 'w');
##
##for color in res:
##    s = color
##
##    for key, val in res[color].items():
##        s = s + ',' + str(val)
##
##    f.write(s + '\n')
##    
##f.close()    

# perform ks tests

# color distribution over the decades, each row is the dist for a color
color_dist = [];
color_names = [];

ks_results = [];

f = open('../query_results/color_count_per_decade.txt', 'r');
for row in f:
    row = row.strip('\n').split(',')
    color_names.append(row[0])
    a = list(map(int, row[1:]))
    color_dist.append(a)
    
for i in range(len(color_dist)):
    i_res = [];
    for j in range(len(color_names)):
        i_res.append(stats.ks_2samp(color_dist[i], color_dist[j]).pvalue)

    ks_results.append(i_res)
f.close() 

import plotly.tools as tls
tls.set_credentials_file(username='ChristinaChung', api_key='9Qz7ub7MJHtBqdy6N6OX')
import plotly.plotly as py
import plotly.graph_objs as go

data = [
    go.Heatmap(
        z=ks_results,
        x=color_names,
        y=color_names,
    )
]



py.iplot(data, filename='heat')


