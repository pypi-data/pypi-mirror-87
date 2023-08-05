from typing import Dict, Tuple, Union
from collections import Iterable
from .exceptions import ValidationError
from .fields import Field


class Validation:
    _error_formats = {
        "required": "Field{} '{}' {} required but not provided.",
        "invalid_format": "Field{} '{}' {} in an invalid format.",
        "unknowns": "Field{} '{}' {} in unknown validation rule.",
    }

    @classmethod
    def _validate(cls, payload: Dict, validation_rule: Union[Dict, Field, callable], base=None) -> Tuple[Dict, Dict]:
        """
        :returns
        """

        errors_dict = {k: [] for k in cls._error_formats}
        new_payload = {}
        if isinstance(validation_rule, Dict) or isinstance(validation_rule, Dict):
            for key in validation_rule:
                str_field = key if base is None else '{}.{}'.format(base, key)

                if key not in payload:
                    # if key is not present, check if it was required or in case any default value.

                    if validation_rule[key].get('required', False) and 'default' not in validation_rule[key]:
                        errors_dict['required'].append(str_field)
                    else:
                        # only set default value if it exists
                        if 'default' in validation_rule[key]:
                            new_payload[key] = validation_rule[key]['default']

                else:
                    pattern = validation_rule[key].get('pattern')
                    if validation_rule[key].get("sub_pattern"):
                        if issubclass(pattern, Iterable):
                            new_payload[key] = []
                            pattern = validation_rule[key].get('sub_pattern')
                            if isinstance(payload.get(key), Iterable):
                                for i, _ in enumerate(payload.get(key)):
                                    _payload, _error_dict = cls._validate(_, pattern, str_field+".{}".format(i))
                                    if not cls._is_error(_error_dict):
                                        new_payload[key].append(_payload)
                                    else:
                                        errors_dict['required'] += _error_dict["required"]
                                        errors_dict['invalid_format'] += _error_dict["invalid_format"]

                            else:
                                errors_dict['required'] += str_field
                                errors_dict['invalid_format'] += str_field
                        else:
                            errors_dict['invalid_format'].append(str_field)

                    # if value is None & null is True
                    elif validation_rule[key].get('null', False) and payload[key] is None:
                        new_payload[key] = None

                    # no checks
                    elif pattern is None:
                        new_payload[key] = payload.get(key)

                    # check if pattern is again a dict, recursive check
                    elif isinstance(pattern, Field) or isinstance(pattern, Dict):
                        if isinstance(payload.get(key), dict):
                            _payload, _error_dict = cls._validate(payload.get(key), pattern, str_field)
                            if not cls._is_error(_error_dict):
                                new_payload[key] = _payload
                            else:
                                errors_dict['required'] += _error_dict["required"]
                                errors_dict['invalid_format'] += _error_dict["invalid_format"]
                        else:
                            errors_dict['invalid_format'].append(str_field)
                    # check if pattern is re.compile("regex")
                    elif hasattr(pattern, 'match') and callable(pattern.match):  # pattern is a regex
                        if pattern.match(str(payload.get(key))):
                            new_payload[key] = payload.get(key)
                        else:
                            errors_dict['invalid_format'].append(str_field)
                    # check if pattern is any callback type
                    elif callable(pattern):  # pattern is a callable type, or a lambda function for preprocessing
                        try:
                            new_payload[key] = pattern(payload.get(key))
                        except Exception as e:
                            errors_dict['invalid_format'].append(str_field)

                    # do not parse, unknown error
                    else:
                        errors_dict['unknowns'].append(str_field)

        elif callable(validation_rule):
            # pattern is a callable type, or a lambda function for preprocessing
            try:
                new_payload = validation_rule(payload)
            except Exception as e:
                errors_dict['invalid_format'].append(str(base))
                
        return new_payload, errors_dict

    @classmethod
    def _is_error(cls, error_dict):
        for k, v in error_dict.items():
            if v:
                return True

        return False

    @classmethod
    def _return(cls, payload, error, raise_exception):
        if raise_exception and error:
            raise ValidationError(payload)

        return payload, error

    @classmethod
    def validate(cls, payload, validate_dict: Union[Dict, Field, callable], base=None, raise_exception=False):
        """
        :param payload: input payload
        :param validate_dict: validation rules
        :param raise_exception:
        if raise_exception is True:
            if error:
             ValidationError will be raised
        else:
            if error:
                returns error_message, True
            else:
                returns new_payload, False
        :return:
        """
        payload, error_dict = cls._validate(payload, validate_dict, base)

        if not cls._is_error(error_dict):
            return cls._return(payload, False, raise_exception)

        else:
            messages = []
            for k, v in cls._error_formats.items():
                if len(error_dict[k]):
                    messages.append(v.format(
                        's' if len(error_dict[k]) > 1 else '',
                        "', '".join(sorted(error_dict[k])),
                        'are' if len(error_dict[k]) > 1 else 'is', ))

            return cls._return("\n".join(messages), True, raise_exception)


if __name__ == "__main__":
    pass
