from flask import Flask, render_template, url_for, request, redirect
from configparser import ConfigParser
from flask_bootstrap import Bootstrap
import json

app = Flask(__name__, static_url_path='/static')
bootstrap = Bootstrap(app)

glo_dict = []
options = {}  # values of every values (old one) / free of choices without lists
dict_names = {}  # tables values
groups = {}  # List of groups with friendly new name as a key --> then make everything goes with it

# glo_dict 0:key_dict, 1: Lists, 2: Values, 3: Names
# change this if u want


@app.route("/", methods=['GET', 'POST'])
def index():
    keys_dict = {}
    config = ConfigParser()
    config.read('file.ini')
    List_names = []  # saves the name of lists which is also with the type list by default
    ListChosenNames = []
    for section in config.sections():
        if section.startswith(" \\"):  # good
            k = options.popitem()
            List_names.append(k[0])
            dict_names[k[0]] = k[1]
            continue
        options[section] = {}
        for key, value in config.items(section):
            options[section][key] = value

    if request.method == 'POST':
        f = request.form
        for key in f.keys():
            item = key.split('#')
            if len(item) > 1:
                s, x = item[0], item[1]
                if x == "section":
                    continue
                if s in List_names:
                    ListChosenNames.append(s)
                else:
                    if s not in keys_dict:
                        keys_dict[s] = []
                    keys_dict[s].append(x)
        '''
        print(keys_dict)
        {'SYSTEM Params': ['ldapserviceenable', 'ldapauthfilter',
            'syslogserverip'], 'Voice Engine Params': ['sbcdevicerole']}
        '''
        if keys_dict: 
            glo_dict.append(keys_dict)
        else: 
            glo_dict.append([])
        glo_dict.append(ListChosenNames)
        #print(dict_names)

        if request.form.get('action') == 'Submit':
            return redirect(url_for('group'))

    html = render_template('index.html', options=options,
                           List_names=List_names)
    return html

# in this page the admin groups some items to be changed


@app.route('/group', methods=['GET', 'POST'])
def group():
    key_dict = glo_dict[0]
    List_names = glo_dict[1] #list of names 

    ''' {'g2': ['SYSTEM Params/syslogserverip', 'WEB Params/logowidth'],
      'g1': ['SYSTEM Params/ldapauthfilter', 'BSP Params/exitcpuoverloadpercent']}'''
    table_values = {} #Listchoice : {format index: rows, col0: --, col1: -- , --->}
    row_col = {}
    for list_name in List_names:#elchoices
        if list_name in dict_names: #kol options
            table_values[list_name] = dict_names[list_name] 
            
    #print(table_values)
    for k, v in table_values.items():
        if k not in row_col:
            row_col[k] = {}
        row = list(table_values[k]['format index'].strip(';').split(', '))
        col = list(table_values.keys())[1:]
        row_col[k]['row'] = row
        row_col[k]['col'] = col

    #print(row_col)
            
    if request.method == 'POST':
        group_items = request.form.getlist('group')

        for group in group_items:
            name, items = group.split(':')
            groups[name] = items.split(',')
        #print(groups)

        if request.form.get('action') == 'Submit':
            return redirect(url_for('page2'))
    return render_template('group.html', key_dict=key_dict, List_names=List_names, row_col=row_col)


@app.route('/page2', methods=['GET', 'POST'])
def page2():
    key_dict = glo_dict[0]
    List_names = glo_dict[1]
    # print(key_dict)
    value_dict = []
    if key_dict:
        for val in key_dict.values():
            value_dict += val
        value_dict += List_names
    else:
        value_dict = List_names


    names = []
    if request.method == 'POST':
        f = request.form
        for item in f.items():
            if item[0] != 'action':
                names.append([item[0], item[1]])
        glo_dict.append(names)
        glo_dict.append(value_dict)
        if request.form.get('action') == 'Submit':
            return redirect(url_for('choose'))

    # default return statement for GET requests
    return render_template('page2.html', key_dict=key_dict, List_names=List_names)


@app.route('/choose', methods=['GET', 'POST'])
def choose():
    names = glo_dict[2]  # use endswith for names[i][0] to map it with glo_dict

    value_dict = glo_dict[3]

    # It doesn't have action in the post request
    if request.method == 'POST':
        f = request.form
        lookup_names = dict(f)
        lookup_names.popitem()
        for k, v in lookup_names.items():
            if v == '':
                lookup_names[k] = k
        glo_dict.append(lookup_names)

        if f.get('action') == 'Submit':
            return redirect(url_for('end'))

    return render_template('choose.html', value_dict=value_dict, names=names)


@app.route('/end', methods=['GET', 'POST'])
def end():
    selected = glo_dict[0]
    List_names = glo_dict[1]  # Chosen List names
    # [['SYSTEM Params#ldapserviceenable', 'int'], ['SYSTEM Params#ldapauthfilter', 'int']]
    names_types = glo_dict[2]
    # print(names_types)
    # {'ldapserviceenable': 'df', 'ldapauthfilter': 'dfdf'}
    names_new = glo_dict[4]
    # {'SYSTEM Params': {'ldapauthfilter': [], 'syslogserverip': [], 'enablesyslog': []}}
    sections = {'Tablenames': {}}

    for k, vl in selected.items():
        if k not in sections:
            sections[k] = {}
        for v in vl:
            sections[k][v] = []

    for name in List_names:
        sections['Tablenames'][name] = []
    # for sections
    for i in range(len(names_types)-len(List_names)):
        sc, it = names_types[i][0].split('#')
        if sc in sections:
            sections[sc][it].append(names_types[i][1])
            sections[sc][it].append(names_new[it])
            sections[sc][it].append(options[sc][it])

        j = i
    if List_names and selected:
        for i in range(len(List_names)):
            sections['Tablenames'][List_names[i]].append(names_types[j+i+1][1])
            sections['Tablenames'][List_names[i]].append(
                names_new[List_names[i].strip()])
            sections['Tablenames'][List_names[i]].append(
                str(dict_names[List_names[i]]))

    elif List_names:
        for i in range(len(List_names)):
            sections['Tablenames'][List_names[i]].append(names_types[i][1])
            sections['Tablenames'][List_names[i]].append(
                names_new[List_names[i].strip()])
            sections['Tablenames'][List_names[i]].append(
                str(dict_names[List_names[i]]))

# Engineer\new_ini.json: http://127.0.0.1:8000/Engineer/engindex.html
    with open("Engineer//new_ini.json", "w") as outfile:
        json.dump(sections, outfile)

    return render_template('end.html')


if __name__ == "__main__":
    app.run(debug=True, port=5001)
