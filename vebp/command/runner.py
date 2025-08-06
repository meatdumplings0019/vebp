from vebp.runner import Runner


def run_command(args, app):
    rn = Runner(app, getattr(args, 'script', None))
    rn.run()