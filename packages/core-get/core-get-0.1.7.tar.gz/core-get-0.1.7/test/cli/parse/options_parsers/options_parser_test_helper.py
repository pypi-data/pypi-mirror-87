from core_get.cli.parse.composite_parser import CompositeParser


def do_test_parse(parser_type, *args: str):
    composite_parser = CompositeParser()
    [options] = composite_parser.parse([parser_type()], list(args))
    return options
