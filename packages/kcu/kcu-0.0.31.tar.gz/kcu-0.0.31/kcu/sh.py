def path(path: str) -> str:
    return path.replace(' ', '\\ ').replace('\\\\ ', '\\ ')

def sh(
    cmd: str,
    debug: bool = False
) -> str:
    import subprocess
    
    if debug:
        print(cmd)

    return subprocess.getoutput(cmd)

def pwd() -> str:
    return sh('pwd')

def mkdir(p: str) -> str:
    return sh('mkdir ' + path(p))

def rmrf(p: str) -> str:
    return sh('rm -rf ' + path(p))

def cp(from_path: str, to_path: str) -> str:
    return sh('cp ' + path(from_path) + ' ' + path(to_path))