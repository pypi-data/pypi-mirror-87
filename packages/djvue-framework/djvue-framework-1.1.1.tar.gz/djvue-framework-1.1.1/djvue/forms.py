class PropsComponent:
    props = {}

    def __init__(self, **kwargs):
        self.props = dict(kwargs)

    def to_dict(self):
        return self.props


class LayoutComponent:
    props = PropsComponent()


class ComponentList:
    fields = []

    def __init__(self, *children, **kwargs):
        self.fields = list(children)

    @staticmethod
    def mapfun(x):
        if isinstance(x, str):
            return x
        else:
            return x.to_dict()

    def to_dict(self):
        return list(map(self.mapfun, self.fields))


class Div(LayoutComponent):
    css_class = ''
    tag = 'div'

    def __init__(self, *children, **kwargs):
        self.fields = ComponentList(*children)
        if hasattr(self, "css_class") and "css_class" in kwargs:
            self.css_class += " %s" % kwargs.pop("css_class")

        self.props = PropsComponent(**kwargs)

    def to_dict(self):
        return {
            'children': self.fields.to_dict(),
            'tag': self.tag,
            'props': self.props.to_dict()
        }


class Row(Div):
    tag = 'BRow'

    def __init__(self, *children, **kwargs):
        super(Row, self).__init__(*children, **kwargs)


class Col(Div):
    tag = 'BCol'

    def __init__(self, *fields, **kwargs):
        super(Col, self).__init__(*fields, **kwargs)


class DVFormLayout:
    def get_form_layout(self):
        if self.Meta.fields == '__all__':
            return Div(*(list(self.fields.keys()))).to_dict()
        else:
            filtered = list(filter(lambda x: x in set(self.Meta.fields), list(self.fields.keys())))
            return Div(*filtered).to_dict()



