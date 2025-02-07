from cosalib.cmdlib import runcmd


def create_local_container_manifest(repo, tag, images):
    '''
    Create local manifest list
    @param images list of image specifications (including transport)
    @param repo str registry repository
    @param tag str manifest tag
    '''
    cmd = ["podman", "manifest", "create", f"{repo}:{tag}"]
    runcmd(cmd)
    for image in images:
        cmd = ["podman", "manifest", "add", f"{repo}:{tag}", image]
        runcmd(cmd)


def delete_local_container_manifest(repo, tag):
    '''
    Delete local manifest list
    @param repo str registry repository
    @param tag str manifest tag
    '''
    cmd = ["podman", "manifest", "rm", f"{repo}:{tag}"]
    runcmd(cmd)


def push_container_manifest(repo, tag, v2s2=False):
    '''
    Push manifest to registry
    @param repo str registry repository
    @param tag str manifest tag
    @param v2s2 boolean use to force v2s2 format
    '''
    cmd = ["podman", "manifest", "push",
           "--all", f"{repo}:{tag}", f"{repo}:{tag}"]
    if v2s2:
        # `--remove-signatures -f v2s2` is a workaround for when you try
        # to create a manifest with 2 different mediaType. It seems to be
        # a Quay issue.
        cmd.extend(["--remove-signatures", "-f", "v2s2"])
    runcmd(cmd)


def create_and_push_container_manifest(repo, tag, images, v2s2):
    '''
    Do it all! Create, Push, Cleanup
    @param repo str registry repository
    @param tag str manifest tag
    @param images list of image specifications (including transport)
    @param v2s2 boolean use to force v2s2 format
    '''
    create_local_container_manifest(repo, tag, images)
    push_container_manifest(repo, tag, v2s2)
    delete_local_container_manifest(repo, tag)
