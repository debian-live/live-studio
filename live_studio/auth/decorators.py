def login_not_required(fn):
    fn.login_not_required = True
    return fn
