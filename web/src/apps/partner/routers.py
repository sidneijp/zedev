from rest_framework.routers import DefaultRouter, Route


class DynamicCustomRouter(DefaultRouter):
    def add_action(
            self, action_name, url_path=None, methods=[], detail=False,
            lookup_value=None
    ):
        name = '{basename}'
        initkwargs = {'suffix': 'List'}
        if detail:
            assert lookup_value is not None
            name = f'{name}-detail'
            initkwargs = {'suffix': 'Instance'}

        url_path = url_path or rf'{lookup_value}/{action_name}'
        url = r'^{prefix}/' + url_path + '{trailing_slash}$'

        mapping = {}
        for method in methods:
            mapping[method.lower()] = action_name

        print (url, mapping, name, detail, initkwargs)
        self.routes.append(
            Route(
                url=url,
                mapping=mapping,
                name=name,
                detail=detail,
                initkwargs=initkwargs
            ),
        )
