class VariantMatcher:

    def is_match(self, expressions: str, device: str) -> bool:
        return any(self._is_expression_match(expression, device)
                   for expression in expressions.split(','))

    def _is_expression_match(self, expression: str, device: str) -> bool:
        expression_parts = expression.split('-')
        device_parts = device.split('-')
        for i in range(min(len(expression_parts), len(device_parts))):
            if not self._is_submatch(expression_parts[i], device_parts[i]):
                return False
        return True

    def _is_submatch(self, expression_part: str, device_part: str) -> bool:
        return expression_part == '*' or expression_part == device_part
