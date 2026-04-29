def global_tool(request):
    return {
        'tool': getattr(request, 'tool', None)
    }