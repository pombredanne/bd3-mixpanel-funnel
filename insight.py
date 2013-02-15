from bitdeli.insight import insight, segment, segment_label
from bitdeli.widgets import Text, Bar, Table, Widget
from discodb.query import Q, Literal, Clause

class TokenInput(Widget):
    pass

class Funnel(Widget):
    pass

def unique(events):
    seen = set()
    for event in events:
        if event not in seen:
            yield event
            seen.add(event)

def query(model, seq):
    return model.query(Q([Clause([Literal(event)]) for event in seq]))
            
@insight
def view(model, params):
    chosen = list(unique(params['events']['value'] if 'events' in params else []))
    def steps(events):
        for i in range(len(events)):
            yield events[i], len(query(model, events[:i + 1]))
            
    widgets = [TokenInput(id='events',
                          size=(12, 1),
                          label='Event Sequence',
                          value=chosen,
                          data=list(model))]
    if chosen:
        widgets += [Funnel(id='funnel',
                           size=(12, 6),
                           data=list(steps(chosen)))]
    return widgets

def segment_sequence(params):
    events = params['params']['events']['value']
    return events[:events.index(params['value'][0]) + 1]

@segment
def segment(model, params):
    print 'pa', params
    print 'sa', segment_sequence(params)
    return query(model, segment_sequence(params))
    
@segment_label
def label(segment, params):
    return 'Funnel: Users who have gone through %s' %\
            ','.join(segment_sequence(params))
