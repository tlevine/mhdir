from .inc import inc

def comp():
    raise NotImplementedError('Interactivity is annoying.')

def cli():
    import horetu
    from . import show
    horetu.horetu({
        'prev': show.prev, 'show': show.show, 'next': show.next,
        'inc': inc,
    }, name = 'm')
