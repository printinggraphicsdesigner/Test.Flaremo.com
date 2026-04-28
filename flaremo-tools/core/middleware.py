
class ToolMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from core.models import Tool

        request.tool = None

        # 👉 URL থেকে slug detect করবে
        path = request.path.strip('/')

        # example: /translator/ → translator
        if path:
            slug = path.split('/')[0]
            tool = Tool.objects.filter(slug=slug).first()

            if tool:
                request.tool = tool

        response = self.get_response(request)
        return response
