from django.views.generic.list import ListView

class SplitListView(ListView):
    model = None
    queryset_filter_kwargs = None
    queryset_exclude_kwargs = None
    queryset_only_fields = None
    queryset_order_by_fields = None

    def get_model(self):
        return self.model

    def get_queryset_base(self):
        return self.get_model().objects.all()

    def get_queryset_filter_kwargs(self):
        return self.queryset_filter_kwargs

    def get_queryset_exclude_kwargs(self):
        return self.queryset_exclude_kwargs

    def get_queryset_order_by_fields(self):
        if self.queryset_order_by_fields:
            return self.queryset_order_by_fields

    def get_queryset_only_fields(self):
        return self.queryset_only_fields

    def get_queryset(self,**kwargs):
        qs = self.get_queryset_base()
        filter_kwargs = self.get_queryset_filter_kwargs()
        if filter_kwargs:
            qs = qs.filter(**filter_kwargs)
        exclude_kwargs = self.get_queryset_exclude_kwargs()
        if exclude_kwargs:
            qs = qs.exclude(**exclude_kwargs)
        only_fields = self.get_queryset_only_fields()
        if only_fields:
            qs = qs.only(*only_fields)
        order_by_fields = self.get_queryset_order_by_fields()
        if order_by_fields:
            qs = qs.order_by(*order_by_fields)
        return qs
