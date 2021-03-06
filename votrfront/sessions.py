
import contextlib
import fcntl
import gzip
import os
import pickle
from aisikl.exceptions import LoggedOutError


def get_session_cookie(request):
    return request.cookies.get(request.app.session_name)


def set_session_cookie(request, response, sessid):
    if sessid:
        response.set_cookie(request.app.session_name, sessid)
    else:
        response.delete_cookie(request.app.session_name)
    return response


def get_filename(request, sessid, *, logs=False):
    for ch in sessid:
        if ch not in '0123456789abcdef_':
            raise ValueError('Invalid sessid')

    return request.app.var_path('logs' if logs else 'sessions', sessid)


def open_log_file(request, sessid):
    filename = get_filename(request, sessid, logs=True) + '.gz'
    return gzip.open(filename, 'at', encoding='utf8')


def create(request, sessid, session):
    with open(get_filename(request, sessid), 'xb') as f:
        pickle.dump(session, f, pickle.HIGHEST_PROTOCOL)

    return sessid


def delete(request, sessid=None):
    if not sessid: sessid = get_session_cookie(request)
    if not sessid: return
    try:
        os.unlink(get_filename(request, sessid))
        return True
    except FileNotFoundError:
        return False


@contextlib.contextmanager
def transaction(request, sessid=None):
    if not sessid: sessid = get_session_cookie(request)
    if not sessid: raise LoggedOutError('Session cookie not found')

    try:
        f = open(get_filename(request, sessid), 'r+b')
    except FileNotFoundError as e:
        raise LoggedOutError('Votr session does not exist') from e

    with f:
        # Use flock instead of fcntl or lockf. flock has sane semantics on
        # close(2), and we don't need fcntl's byte range locks.
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)

        session = pickle.load(f)

        if not session:
            # If the session is empty, there was probably a race between this
            # request and a logout. The logout arrived first, emptied the
            # session, saved it and unlinked the file. But this request already
            # managed to open the file and was waiting for flock while that was
            # happening. We can react as if the session file didn't exist.
            raise LoggedOutError('Votr session is currently logging out')

        yield session

        # Use pickle.dumps instead of pickle.dump, so that if it fails, the
        # session file is not truncated.
        new_content = pickle.dumps(session, pickle.HIGHEST_PROTOCOL)

        f.seek(0)
        f.truncate(0)
        f.write(new_content)


@contextlib.contextmanager
def logged_transaction(request, sessid=None):
    if not sessid: sessid = get_session_cookie(request)

    with transaction(request, sessid) as session:
        with open_log_file(request, sessid) as log_file:
            client = session.get('client')
            if client: client.context.logger.log_file = log_file
            yield session
