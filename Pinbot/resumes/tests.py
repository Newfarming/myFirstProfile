# coding: utf-8

from resumes.views import  send_to_rabbitmq
resume_id = '5472f1ae81af591e1877c6e8'
message = {"resume_id": resume_id, "file_id": None, "path":
                       None, "content_type": 'html', "start_process": True}
send_to_rabbitmq(message)