#!/usr/bin/python
#-*- coding: utf-8 -*-
import web
#name of the cookie used to store the session id
web.config.session_parameters['cookie_name'] = 'Oletter_session_id'
web.config.session_parameters['cookie_domain'] = None
web.config.session_parameters['timeout'] = 86400, #24 * 60 * 60, # 24 hours   in seconds

#if True, the session timeout is ignored
web.config.session_parameters['ignore_expiry'] = True

#if False, the session is only valid
#           when it is accessed from the same ip address that created the session
web.config.session_parameters['ignore_change_ip'] = True

#used in session id hash generation
web.config.session_parameters['secret_key'] = 'fLjUfxqXtfNoIldA0A0J'
web.config.session_parameters['expired_message'] = 'Session expired'

domain_name = "http://localhost"