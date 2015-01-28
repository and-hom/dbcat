from frontend.util import filter_types


def menu(request):
    return {
        'filter_types': filter_types()
    }