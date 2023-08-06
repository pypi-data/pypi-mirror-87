import dateutil.parser
from parser import ParserError

def dj_to_plotly(filepath) -> list:
    """Get plotly ready data from the file of type `dJ`"""

    if not filepath:
        raise AttributeError('File is invalid')

    with open(filepath, 'r') as f:
        lines = f.readlines()

    if not filepath.endswith('dJ'):
        raise AttributeError('File is invalid')

    header = {}
    for line in lines:
        if line.find('=') > -1:
            header[line.split('=')[0]] = line.split('=')[1].strip()
        elif line.strip() == '$DATA':
            break

    data = {}
    for line in lines:
        if len(line.split(',')) >= 2:
            ts = line.split(',')[0]
            values = line.split(',')[1:]
            try:
                dt = dateutil.parser.parse(ts)
            except ParserError:
                # Invalid datetime string
                continue
            for i, val in enumerate(values):
                try:
                    val = val.strip()
                    val = eval(val)
                except (NameError, SyntaxError):
                    # Invalid val
                    continue
                if f'CHAN_NAME{i}' not in data:
                    data[f'CHAN_NAME{i}'] = []
                data[f'CHAN_NAME{i}'].append((str(dt), val))

    # Order data by timestamp in ascending order
    for key, val in data.items():
        data[key] = sorted(val, key=lambda t: t[0])

    # Prepare data for plotly
    traces = []
    for key, val in data.items():
        x, y = zip(*val)
        traces.append({
            'x': x,
            'y': y,
            'name': header[key],
            'type': 'scatter',
            'mode': 'lines+points',
        })
    return traces
