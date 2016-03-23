# coding: utf-8


class FormErrors(object):

    def get_first_errors(self):
        first_error_item = self.errors.items()[0]

        return u'%s: %s' % (
            self.fields[first_error_item[0]].label,
            first_error_item[1][0],
        )
