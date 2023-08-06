from rest_framework.routers import SimpleRouter, Route


class DjvueSimpleRouter(SimpleRouter):

    def get_routes(self, viewset):
        routes = []

        if hasattr(viewset, 'list_select_key'):
            routes.append(Route(
                url=r'^{prefix}/djvue/list_keys{trailing_slash}$',
                mapping={
                    'get': 'list_keys',
                },
                name='{basename}-list_keys',
                detail=False,
                initkwargs={}
            ), )

        if hasattr(viewset, 'get_footer'):
            routes.append(Route(
                url=r'^{prefix}/djvue/footer{trailing_slash}$',
                mapping={
                    'get': 'get_footer_config',
                },
                name='{basename}-get_footer',
                detail=False,
                initkwargs={}
            ), )

        if hasattr(viewset, 'get_autocomplete'):
            routes.append(Route(
                url=r'^{prefix}/autocomplete{trailing_slash}$',
                mapping={
                    'get': 'get_autocomplete',
                },
                name='{basename}-autocomplete',
                detail=False,
                initkwargs={}
            ), )

        if hasattr(viewset, 'get_autocomplete'):
            routes.append(Route(
                url=r'^{prefix}/{lookup}{trailing_slash}autocomplete{trailing_slash}$',
                mapping={
                    'get': 'get_autocomplete',
                },
                name='{basename}-autocomplete',
                detail=False,
                initkwargs={}
            ), )

        routes += super().get_routes(viewset)

        return routes
