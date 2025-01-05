import Filters.OfferFilters
import Filters.TrainFilters

import sys, inspect

def format_markdown_param(param):
    formatted = '>**{}**: {}'.format(param._name, param._annotation.__name__)

    if param._default is not param.empty:
        formatted = '{} *= {}*'.format(formatted, str(param._default))

    formatted += '  '

    return formatted

def format_markdown_filter_classes(module_name: str):
    res = ""

    for name, obj in inspect.getmembers(sys.modules[module_name]):
        if inspect.isclass(obj):
            name = obj.__name__
            sign = inspect.signature(obj)
            doc = obj.__doc__

            res += "### {}\n".format(name)
            res += "\t{}\n".format(doc)
            
            if len(sign.parameters.values()) > 0:
                res += "#### Параметры:  \n"

            for param in sign.parameters.values():
                res += "{}\n".format(format_markdown_param(param))
                
            res += "---\n"
    
    return res

def main():
    res = "# Фильтры\n\n"
    res += "## Фильтры для билетов\n\n"
    res += format_markdown_filter_classes('Filters.OfferFilters')
    res += "## Фильтры для поездов\n\n"
    res += format_markdown_filter_classes('Filters.TrainFilters')

    print("Filters/FILTERS.md")
    # print(res)

    with open("Filters/FILTERS.md", "w") as f:
        f.write(res)


main()