class Variable:
    def __init__(self, name, kind, aggregation_tsx,
                 filter_tsx, interpolation):
        self.name = name
        self.kind = kind
        self.aggregation_tsx = aggregation_tsx
        self.filter_tsx = filter_tsx
        self.interpolation = interpolation

    def as_dict(self):
        """
        Represent the current Variable as a dict

        The returned dict should be valid for serialization and
        passing back to TSI or for creating new variables.

        Returns
        -------
        dict
            Variable stored as a python dict
        """
        var_description = {'kind': self.kind}
        if self.filter_tsx is not None:
            var_description['filter'] = {'tsx': self.filter_tsx}
        if self.aggregation_tsx is not None:
            var_description['aggregation'] = {'tsx': self.aggregation_tsx}
        if self.interpolation is not None:
            var_description['interpolation'] = self.interpolation

        return {self.name: var_description}

    def copy(self):
        """
        Create a copy of the Variable

        Returns
        -------
        Variable
                Copied object
        """
        return Variable(name=self.name,
                        kind=self.kind,
                        aggregation_tsx=self.aggregation_tsx,
                        filter_tsx=self.filter_tsx,
                        interpolation=self.interpolation)

    def __repr__(self):
        return f'<{self.kind} variable {self.name}>'


class NumericVariable(Variable):
    def __init__(self, name, kind, aggregation_tsx,
                 filter_tsx, interpolation, var_value_tsx):
        super(NumericVariable, self).__init__(name=name,
                                              kind=kind,
                                              aggregation_tsx=aggregation_tsx,
                                              filter_tsx=filter_tsx,
                                              interpolation=interpolation)
        self.var_value_tsx = var_value_tsx

    def copy(self):
        """
        Create a copy of the Variable

        Returns
        -------
        Variable
                Copied object
        """
        return NumericVariable(name=self.name,
                               kind=self.kind,
                               var_value_tsx=self.var_value_tsx,
                               aggregation_tsx=self.aggregation_tsx,
                               filter_tsx=self.filter_tsx,
                               interpolation=self.interpolation)

    def as_dict(self):
        """
        Represent the current Variable as a dict

        The returned dict should be valid for serialization and
        passing back to TSI or for creating new variables.

        Returns
        -------
        dict
            Variable stored as a python dict
        """
        var_description = super(NumericVariable, self).as_dict()[self.name]
        var_description['value'] = {'tsx': self.var_value_tsx}

        return {self.name: var_description}


class CategoricalVariable(Variable):
    def __init__(self, name, kind, aggregation_tsx,
                 filter_tsx, interpolation, var_value_tsx,
                 categories, default_category):
        super(CategoricalVariable, self).__init__(name=name,
                                                  kind=kind,
                                                  aggregation_tsx=aggregation_tsx,
                                                  filter_tsx=filter_tsx,
                                                  interpolation=interpolation)
        self.var_value_tsx = var_value_tsx
        self.categories = [Category(label=c['label'],
                                    values=c['values'],
                                    annotations=c['annotations'])
                           for c in categories]
        self.default_category = DefaultCategory(label=default_category['label'],
                                                annotations=default_category['annotations'])

    def copy(self):
        """
        Create a copy of the Variable

        Returns
        -------
        Variable
                Copied object
        """
        return CategoricalVariable(name=self.name,
                                   kind=self.kind,
                                   var_value_tsx=self.var_value_tsx,
                                   aggregation_tsx=self.aggregation_tsx,
                                   filter_tsx=self.filter_tsx,
                                   interpolation=self.interpolation,
                                   categories=self.categories,
                                   default_category=self.default_category)

    def as_dict(self):
        """
        Represent the current Variable as a dict

        The returned dict should be valid for serialization and
        passing back to TSI or for creating new variables.

        Returns
        -------
        dict
            Variable stored as a python dict
        """
        var_description = super(CategoricalVariable, self).as_dict()[self.name]
        var_description['value'] = {'tsx': self.var_value_tsx}
        var_description['categories'] = [{'label': c.label,
                                          'values': c.values,
                                          'annotations': c.annotations} for c in self.categories]
        var_description['defaultCategory'] = {'label': self.default_category.label,
                                              'annotations': self.default_category.annotations}

        return {self.name: var_description}


class Category:
    def __init__(self, label, values, annotations):
        self.label = label
        self.values = values
        self.annotations = annotations

    def __repr__(self):
        return f'<Category {self.label} for values {self.values}>'


class DefaultCategory:
    def __init__(self, label, annotations):
        self.label = label
        self.annotations = annotations

    def __repr__(self):
        return f'<Default Category {self.label}>'


def variable_helper(var_name, var_info):
    """
    Helper function which returns the appropriate Variable object given
    a TSI server response.
    """
    var_kind = var_info['kind']
    var_value = var_info.get('value')
    var_value_tsx = var_value['tsx'] if var_value is not None else None
    var_filter = var_info.get('filter')
    var_filter_tsx = var_filter['tsx'] if var_filter is not None else None
    var_aggregation = var_info.get('aggregation')
    var_aggregation_tsx = var_aggregation['tsx'] if var_aggregation is not None else None
    var_interpolation = var_info.get('interpolation')
    var_categories = var_info.get('categories')
    var_default_category = var_info.get('defaultCategory')

    # Create the appropriate Variable types
    if var_kind == 'aggregate':
        return Variable(name=var_name,
                        kind=var_kind,
                        aggregation_tsx=var_aggregation_tsx,
                        filter_tsx=var_filter_tsx,
                        interpolation=var_interpolation)
    elif var_kind == 'numeric':
        return NumericVariable(name=var_name,
                               kind=var_kind,
                               aggregation_tsx=var_aggregation_tsx,
                               filter_tsx=var_filter_tsx,
                               interpolation=var_interpolation,
                               var_value_tsx=var_value_tsx)
    elif var_kind == 'categorical':
        return CategoricalVariable(name=var_name,
                                   kind=var_kind,
                                   aggregation_tsx=var_aggregation_tsx,
                                   filter_tsx=var_filter_tsx,
                                   interpolation=var_interpolation,
                                   var_value_tsx=var_value_tsx,
                                   categories=var_categories,
                                   default_category=var_default_category)
    else:
        # Notably we do not yet support Categorical vars
        raise RuntimeError(f'Variable type {var_kind} not yet supported')
