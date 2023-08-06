import json
import re
import subprocess


def split_indent(txt, i=0):
    return [
        x.strip('\n') for x in
        re.split(r'\n\s{{{}}}(?!\s|\n)'.format(i), txt.strip('\n')) if x]

def matchmany(out, patterns):
    matches = [
        re.search(pattern, line) for line in out.splitlines()
        for pattern in patterns]
    return {
        k: v for match in matches if match
        for k, v in match.groupdict().items()}


def execmatch(cmd, patterns, error_msgs=None):
    '''Perform re.match against all the patterns after running the bash command.

    Arguments:
        command (str): bash command to execute.
        patterns (list(str)): list of regex patterns to match against

    Returns:
        dict containing the group name (as passed in pattern element)
        and value as the matched value.
    '''
    try:
        cmdargs = cmd.split(' ') if isinstance(cmd, str) else cmd
        out = subprocess.run(cmdargs, check=True, capture_output=True).stdout.decode('utf-8')
        if any(msg.lower() in out.lower() for msg in as_tuple(error_msgs)):
            return {}

        return matchmany(out, patterns)
    except subprocess.CalledProcessError:
        return {}

def as_tuple(x):
    return x if isinstance(x, tuple) else (x,) if x else ()


def maybe_cast(data, type_, *keys):
    return dict(data, **{k: type_(data[k]) for k in keys if k in data})


class attrdict(dict):
    '''Simple attribute dict.'''
    def __getitem__(self, k):
        return self.__convert(super().__getitem__(k))

    def __str__(self):
        return json.dumps(
            self, sort_keys=True, indent=4)

    def __getattr__(self, k):
        if k not in self:
            raise AttributeError(k)
        return self[k]

    def get(self, k, **kw):
        return self.__convert(super().get(k, **kw))

    def __convert(self, v):
        return attrdict(v) if isinstance(v, dict) else v
