# coding: utf-8


class FormErrors(object):

    def get_first_errors(self):
        first_error_item = self.errors.items()[0]
        label = self.fields[first_error_item[0]].label if self.fields.get(first_error_item[0]) else ''
        error_msg = first_error_item[1][0]

        if label:
            ret = u'%s: %s' % (label, error_msg)
        else:
            ret = u'%s' % error_msg
        return ret
