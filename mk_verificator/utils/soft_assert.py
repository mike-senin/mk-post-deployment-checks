from __future__ import with_statement
import contextlib
import sys
import traceback


class MultipleException(Exception):
    pass


class MultpleAssertsCollector(object):
    separator = '-' * 40

    def __init__(self):
        self.exceptions = []

    @contextlib.contextmanager
    def soft_assert(self, additional_error_message='',
                    exception=AssertionError):
        try:
            yield
        except exception:
            _, parent_exception, tb = sys.exc_info()
            tb_info = traceback.extract_tb(tb)
            filename, line, func, text = tb_info[-1]
            error_message = \
                'An error occurred on line {0} in statement: \n\t {1} \n ' \
                'Parent exception message: \n\t {2} \n {3}'.format(
                    line, text, parent_exception.message, self.separator
                )

            message = '\n'.join([additional_error_message, error_message])

            self.exceptions.append(message)
        except Exception:
            # TODO behaviour for unexpected exception should be described here
            _, parent_exception, tb = sys.exc_info()
            tb_info = traceback.extract_tb(tb)
            filename, line, func, text = tb_info[-1]
            error_message = \
                'An error occurred on line {0} ' \
                'in statement: \n\t' \
                '{1}\n{2}'.format(line, text, self.separator)

            error_message = error_message + '\n' + \
                'Parent exception message: ' + parent_exception.message

            message = '\n'.join([additional_error_message, error_message])

            self.exceptions.append(message)

    def release_exceptions(self):
        self.exceptions = []

    def raise_exceptions(self):
        if self.exceptions:
            concatenated_exceptions = \
                '\n' + self.separator + '\n' + '\n'.join(self.exceptions)
            raise MultipleException(concatenated_exceptions)
