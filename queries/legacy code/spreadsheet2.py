import sqlite3
from scipy import stats
import json
conn = sqlite3.connect('../color_analysis_merged.db')
c = conn.cursor()

def total_occurence_per_color():
    res = {}
##    query = """SELECT color.name, count(*) FROM color, mention, sentence, clause, book
##    WHERE mention.color=color.id AND mention.clause=clause.id
##    AND clause.sentence=sentence.id AND sentence.book=book.id AND
##    book.id and color.name IN """ + color_list + """ GROUP BY color.name"""

    query = """SELECT color.name, count(*) FROM color, mention
    WHERE mention.color=color.id GROUP BY color.name"""

    c.execute(query)

    for row in c.fetchall():
        color = row[0]
        count = row[1]

        res[color] = count

    return res

def parse_color_list():
    res = []
    with open('../query_results/thresholded.txt', 'r') as f:
        for row in f:
            row = row.strip('\n')
            res.append(row) 

    f.close()
    return res

def stringify_color_list(color_list):
    res = "("
    for color in color_list:
        res = res + "'" + color + "'" + ","

    res = res[0:len(res) - 1] + ")"

    return res

def number_of_sentences_in_corpus():
    query = """SELECT DISTINCT count(*) FROM sentence, mention, clause, color
WHERE mention.clause = clause.id AND
clause.sentence = sentence.id AND mention.type != 'noun'
AND mention.type != 'verb' AND mention.color = color.id AND
color.name IN """ + sql_format
    
    c.execute(query)


    return c.fetchone()[0]

def occurence_color_in_num_clauses(clause_dist):
    res = {}

    for length in clause_dist:        
        start = str(length[0])
        finish = str(length[1])

        query = """SELECT color.name, count(*) FROM sentence, mention, clause, color
WHERE mention.clause = clause.id AND
clause.sentence = sentence.id AND mention.type != 'noun'
AND mention.type != 'verb' AND mention.color = color.id AND
color.name IN """ + sql_format + """ AND (sentence.num_dep >=""" +\
start + ' AND sentence.num_dep < ' + finish + ') AND sentence.num_dep >= 0' +\
' GROUP BY color.name'

        c.execute(query)

        res[length] = {}
        for row in c.fetchall():
            color = row[0]
            count = row[1]
            res[length][color] = count
            
    return res

def percent_occurence_sentences_of_num_clauses(clause_dist, num_sentences):
    res = {}
    
    for length in clause_dist:
        start = str(length[0])
        finish = str(length[1])
        query = """SELECT count(*) FROM sentence, mention, clause, color
WHERE mention.clause = clause.id AND
clause.sentence = sentence.id AND mention.type != 'noun'
AND mention.type != 'verb' AND mention.color = color.id AND
color.name IN """ + sql_format + """ AND (sentence.num_dep >=""" +\
start + ' AND sentence.num_dep < ' + finish + ') AND sentence.num_dep >= 0'
        
        c.execute(query)

        res[length] = c.fetchone()[0] / num_sentences

    return res
       

col = parse_color_list()

sql_format = '('
for i in range(0, len(col) - 1):
    sql_format += "'" + col[i] + "',"
sql_format += "'" + col[len(col) - 1] + "'"
sql_format += ')'

##string_list = stringify_color_list(color_list)
to = total_occurence_per_color()

# considering sentence lengths of 0-5, 6-15, etc. 
clause_dist = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 10), (10, 21), (21, 31), (31, 41), (41, 100)]

# number of sentences in corpus
num_sentences = number_of_sentences_in_corpus()

print(num_sentences)
# get total occurrence of sentences for various lengths
pos = percent_occurence_sentences_of_num_clauses(clause_dist, num_sentences)

oc = occurence_color_in_num_clauses(clause_dist)

res = []
for color in col:
    stat = {'name': color, 'occur': to[color], 'expected': [], 'actual': [], 'ratio': [], 'p': [], 'percent':[]}
    
    for length in clause_dist:
        expected = to[color] * pos[length]

        actual = oc[length][color] if color in oc[length].keys() else 0
        ratio = actual / expected if expected else float('inf')
        
        stat['expected'].append(expected)
        stat['actual'].append(actual)
        stat['ratio'].append(ratio)
        stat['percent'].append(actual / to[color])
        stat['p'].append(abs(actual - expected) / expected if expected else float('inf'))


    res.append(stat)

f = open('../query_results/spreadsheet_clause.txt', 'w')
f.write(json.dumps(res))
f.close();

res2 = []
for color in res:
    stat = {'name': color['name'], 'actual': color['actual']}
    res2.append(stat)

f = open('../query_results/clause_dep.json', 'w')
f.write(json.dumps(res))
f.close();
    
    



    

